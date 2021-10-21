from crawler import Crawl
from extract import Extract


name_file_drive = ["Hà Nội", "Hải Dương", "Quảng Ninh",	"Hải Phòng", "Bắc Ninh", "TP.HCM", "Gia Lai",
                   "Hòa Bình", "Bình Dương", "Bắc Giang", "Điện Biên", "Hà Giang", "Hưng Yên", "Ninh Thuận",
                   "Hà Nam", "Vĩnh Phúc", "Đà Nẵng", "Quảng Nam", "Đồng Nai", "Thái Bình", "Quảng Ngãi", "Lạng Sơn",
                   "Long An", "Nam Định", "Thanh Hóa", "Nghệ An", "Phú Thọ", "Huế",	"Đắk Lắk", "Đắk Nông", "Quảng Trị",
                   "Tuyên Quang", "Sơn La", "Ninh Bình", "Thái Nguyên", "Bạc Liêu",	"Trà Vinh", "Tây Ninh",	"Đồng Tháp",
                   "Sóc Trăng",	"Cần Thơ", "Bắc Kạn","Lào Cai", "Kiên Giang", "Tiền Giang",	"Hà Tĩnh", "Vĩnh Long",
                   "Phú Yên","Khánh Hòa", "Bình Thuận", "Bà Rịa - Vũng Tàu", "Bình Định", "An Giang", "Bình Phước",
                   "Lâm Đồng", "Bến Tre", "Cà Mau",	"Hậu Giang", "Kon Tum",	"Quảng Bình", "Lai Châu", "Yên Bái",
                   "BVNĐTW", "BVK", "Nhập cảnh"]

if __name__ == "__main__":
    results = Crawl(executable_path='./chromedriver').get_data_crawler()
    test = results[0]
    extract = Extract(test, name_file_drive)
    res = extract.extract_info_province()
    print(res)
