import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from PhoneCrawler import PhoneCrawler


class Crawler:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome("C:/Downloads/chromedriver.exe")

    def run(self):
        self.driver.get(self.url)
        try:
            show_more = self.driver.find_element_by_css_selector(
                "#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > div.block-filter-sort > "
                "div.filter-sort__list-product > div > div.cps-block-content_btn-showmore > a")
            while (show_more):
                # Check if there's any popup showing that block the driver click
                try:
                    close_button = self.driver.find_element_by_class_name("cancel-button-top")
                    if close_button:
                        close_button.click()
                        print("Popup closed.")
                except:
                    print("No Popup showing.")
                show_more = self.driver.find_element_by_css_selector(
                    "#layout-desktop > div.cps-container.cps-body > div:nth-child(2) > div > div.block-filter-sort > "
                    "div.filter-sort__list-product > div > div.cps-block-content_btn-showmore > a")
                show_more.click()
                time.sleep(2)
        except:
            print("Can't show more products.")
        pageContent = BeautifulSoup(self.driver.page_source, features="html.parser")
        products = pageContent.find_all("div", class_="product-info")
        self.driver.close()

        # Append to csv file
        devices = []
        df_devices = pd.DataFrame(devices,
                                  columns=['pName', 'tradePrice', 'actualPrice', 'salePrice', 'brand', 'productLine',
                                           'rating',
                                           'technicalDetail', 'url'])
        df_devices.to_csv("phones.csv", index=True)
        for product in products:
            productLink = product.find("a").get("href")
            device = PhoneCrawler(productLink)
            device_info = device.getInfo()
            with open("phones.csv", "a", newline="", encoding="utf-8") as file:
                pd.DataFrame([device_info]).to_csv(file, header=False, index=True, mode='a')


productLineUrl = "https://cellphones.com.vn/mobile.html"  # Crawling phone. Can be modified to crawl tablets, laptops...
crawl = Crawler(productLineUrl)
crawl.run()
