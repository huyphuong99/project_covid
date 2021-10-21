from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from numpy.random import randint
from time import sleep
from extract import Extract
import pandas

class Crawl:
    def __init__(self, executable_path, url="https://ncov.moh.gov.vn/dong-thoi-gian"):
        self.executable_path = executable_path
        self.url = url

    def init_driver(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)
        # Thay executable_path
        driver = webdriver.Chrome(executable_path=self.executable_path, chrome_options=chrome_options)
        driver.get(self.url)
        sleep(randint(3,5))
        return driver

    def get_data_crawler(self):
        driver = self.init_driver()
        time_lines = driver.find_elements_by_class_name("timeline")
        results = []
        for time in time_lines:
            result = {}
            t = time.find_element_by_tag_name("h3").text
            result['Time header'] = [t]
            contents = []
            for content in time.find_elements_by_tag_name("p"):
                c = str(content.text).strip()
                if c.startswith("Trong"):
                    if "\n \n" in c:
                        for cc in c.split("\n"):
                            if str(cc).strip().startswith("Trong"):
                                contents.append(cc)
                                break
                    # if '\n \n' in c:
                    #     for cc in c.split('\n'):
                    #         if str(cc).strip().startswith("-"):
                    #             contents.append(cc)
                    # else:
                    #     contents.append(c)
            result['Content'] = contents
            results.append(result)
        driver.close()
        return results



