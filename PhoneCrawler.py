from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import re


class PhoneCrawler():
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome("C:/Downloads/chromedriver.exe")

    def getTechnicalInfo(self):
        # Maximum number of scroll attempts before giving up
        global technicalDetailButton
        max_scroll_attempts = 10

        # Scroll down function
        def scroll_down():
            self.driver.execute_script("window.scrollBy(0, window.innerHeight);")

        # Wait for the element to become visible or present
        wait = WebDriverWait(self.driver, 2)

        scroll_attempts = 0
        while scroll_attempts < max_scroll_attempts:
            try:
                # Check if the element is visible or present
                technicalDetailButton = wait.until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="productDetailV2"]/section/div[4]/div[2]/div/div[1]/button')))
                # If the element is found, break out of the loop
                break
            except:
                # If the element is not found yet, scroll down and try again
                scroll_down()
                scroll_attempts += 1

        # If the loop finishes without finding the element
        # if scroll_attempts == max_scroll_attempts:
        #     print("Element not found after scrolling.")
        # else:
        #     print("Element found. Continuing with further actions.")

        try:
            self.driver.execute_script("arguments[0].click();", technicalDetailButton)
            print("Element found. Continuing with further actions.")
        except:
            # Handle the exception if the click still fails
            print("Failed to click on the element.")

        max_li_attempt = 10
        max_div_attempt = 10
        technicalInfo = []

        # Get technical info details
        for i in range(0, max_li_attempt):
            for j in range(1, max_div_attempt):
                try:
                    element_p = self.driver.find_element_by_xpath(
                        f'//*[@id="productDetailV2"]/section/div[4]/div[2]/div/div[1]/div[2]/div[2]/section/div/ul/li[{i}]/div/div[{j}]/p').text
                    element_div = self.driver.find_element_by_xpath(
                        f'//*[@id="productDetailV2"]/section/div[4]/div[2]/div/div[1]/div[2]/div[2]/section/div/ul/li[{i}]/div/div[{j}]/div').text
                    technicalInfo.append({"title": element_p, "value": element_div})
                except:
                    break
        return technicalInfo

    def getInfo(self):
        self.driver.get(self.url)
        html = self.driver.page_source
        phone = BeautifulSoup(html, features="html.parser")

        # Product name
        try:
            pName = phone.find("div", class_="box-product-name").find("h1").get_text()
        except AttributeError:
            pName = re.search(r"/([^/]+)\.html$", self.url).group(1)

        # Giá "thu cũ đổi mới"
        try:
            tradePrice = phone.find(id="trade-price-tabs").find("p", class_="tpt---sale-price").get_text()
            tradePrice = int(''.join(filter(str.isdigit, tradePrice)))
        except AttributeError:
            tradePrice = None

        # Sale price
        try:
            salePriceElement = phone.find(id="trade-price-tabs").find("div", class_="tpt-box has-text-centered is-flex "
                                                                                    "is-flex-direction-column is-flex-wrap-wrap "
                                                                                    "is-justify-content-center is-align-items-center "
                                                                                    "active").find("p",
                                                                                                   class_="tpt---sale-price")
            if salePriceElement is not None:
                salePrice = int(''.join(filter(str.isdigit, salePriceElement.get_text())))
            else:
                salePrice = None
        except:
            try:
                salePriceElement = phone.find("div", class_="box-info__box-price").find("p",
                                                                                        class_="product__price--sale")
                if salePriceElement is not None:
                    salePrice = int(''.join(filter(str.isdigit, salePriceElement.get_text())))
                else:
                    salePrice = None
            except:
                salePrice = None

        # Price before sale
        try:
            actualPriceElement = phone.find(id="trade-price-tabs").find("div",
                                                                        class_="tpt-box has-text-centered is-flex "
                                                                               "is-flex-direction-column is-flex-wrap-wrap "
                                                                               "is-justify-content-center is-align-items-center "
                                                                               "active").find("p", class_="tpt---price")
            if actualPriceElement is not None:
                actualPrice = int(''.join(filter(str.isdigit, actualPriceElement.get_text())))
            else:
                actualPrice = None
        except:
            try:
                actualPriceElement = phone.find("div", class_="box-info__box-price").find("p",
                                                                                          class_="product__price--through")
                if actualPriceElement is not None:
                    actualPrice = int(''.join(filter(str.isdigit, actualPriceElement.get_text())))
                else:
                    actualPrice = None
            except:
                actualPrice = None

        # Brand
        try:
            brand = phone.find_all("a", class_="button__breadcrumb-item")[1].get_text().strip()
        except: # IndexError or AttributeError may occur here
            brand = None

        # Product Line
        try:
            productLine = phone.find_all("a", class_="button__breadcrumb-item")[2].get_text().strip()
        except:  # IndexError or AttributeError may occur here
            productLine = None

        # Rating
        try:
            rating = phone.find("p", class_="title is-4 m-0 p-0").get_text()
            if rating == "0/5":
                rating = None
        except AttributeError:
            rating = None

        # Technical Info
        technicalDetail = self.getTechnicalInfo()
        self.driver.close()
        print(pName, tradePrice, actualPrice, salePrice, brand, productLine, rating, technicalDetail, self.url)
        return [pName, tradePrice, actualPrice, salePrice, brand, productLine, rating, technicalDetail, self.url]

    # def popupHandler():
    #     try:
    #         popup_close_button = driver.find_element_by_class_name("modal-close is-large")
    #         popup_close_button.click()
    #         print("Popup closed")
    #     except:
    #         print("No popup showing")
    #
    #     try:
    #         popup_close_button = driver.find_element_by_class_name("cancel-button-top")
    #         popup_close_button.click()
    #         print("Popup closed")
    #     except:
    #         print("No popup showing")
