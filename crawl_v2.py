from selenium import webdriver
import re
import pandas as pd
import unicodedata
from selenium.webdriver.common.action_chains import ActionChains


class Crawl:
    def __init__(self, executable_path, url="https://covid19.gov.vn/ban-tin-covid-19.htm"):
        self.executable_path = executable_path
        self.url = url

    def init_driver(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notificatizons": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        # Thay executable_path
        driver = webdriver.Chrome(executable_path=self.executable_path, chrome_options=chrome_options)
        driver.get(self.url)
        return driver

    def get_patient_number(self, data, start):
        start_idx = data.find("(", start) + 1
        end_idx = data.find(")", start_idx)
        return data[start_idx:end_idx]

    def get_nhap_canh(self, data):
        data = data.replace(".", '')
        nhap_canh = re.search(r"\d+[\s]{0,2}[c]{1}[a]{1}[\s]{0,1}[n]{1}[h]{1}[ậ]{1}[p]{1}[\s][c][ả][n][h]", data)
        if nhap_canh == None:
            return 0
        else:
            nhap_canh = nhap_canh.span()
        data = data[nhap_canh[0]:nhap_canh[1]]
        idx = re.search(r"\d+", data).span()
        return data[idx[0]:idx[1]]

    def crawl(self):
        driver = self.init_driver()
        btn_dien_bien = driver.find_element_by_xpath('//h2[@class="title-section"]/a')
        ActionChains(driver).click(btn_dien_bien).perform()
        data = driver.find_element_by_xpath("//li[contains(@class,'timeline-item')]").text
        data = unicodedata.normalize('NFKC', data)
        data = data.replace(".", '')
        province = ["Hà Nội", "Hải Dương", "Quảng Ninh", "Hải Phòng", "Bắc Ninh", "Hồ Chí Minh", "Gia Lai",
                    "Hòa Bình", "Bình Dương", "Bắc Giang", "Điện Biên", "Hà Giang", "Hưng Yên", "Ninh Thuận",
                    "Hà Nam", "Vĩnh Phúc", "Đà Nẵng", "Quảng Nam", "Đồng Nai", "Thái Bình", "Quảng Ngãi", "Lạng Sơn",
                    "Long An", "Nam Định", "Thanh Hóa", "Nghệ An", "Phú Thọ", "Huế", "Đắk Lắk", "Đắk Nông", "Quảng Trị",
                    "Tuyên Quang", "Sơn La", "Ninh Bình", "Thái Nguyên", "Bạc Liêu", "Trà Vinh", "Tây Ninh",
                    "Đồng Tháp", "Sóc Trăng", "Cần Thơ", "Bắc Kạn", "Lào Cai", "Kiên Giang", "Tiền Giang", "Hà Tĩnh", "Vĩnh Long",
                    "Phú Yên", "Khánh Hòa", "Bình Thuận", "Bà Rịa - Vũng Tàu", "Bình Định", "An Giang", "Bình Phước",
                    "Lâm Đồng", "Bến Tre", "Cà Mau", "Hậu Giang", "Kon Tum", "Quảng Bình", "Lai Châu", "Yên Bái",
                    "BVNĐTW", "BVK"]
        result = {}
        for prov in province:
            idx = data.find(f"{prov} (")
            pro_idx = idx if idx != -1 else data.find(prov+"(")
            if pro_idx == -1:
                result[prov] = 0
            else:
                result[prov] = self.get_patient_number(data=data, start=pro_idx)
        result["Nhập cảnh"] = self.get_nhap_canh(data=data)
        return result


if __name__ == "__main__":
    crawl = Crawl(executable_path='./chromedriver')
    result = crawl.crawl()
    _list = [int(i) for i in list(result.values())]
    _sum = sum(_list)
    print(_sum)
    df = pd.DataFrame(result, index=[0])
    print(df)
    df.to_excel("/home/huyphuong99/Desktop/socanhiemtinh.xlsx")
