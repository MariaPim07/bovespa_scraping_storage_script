import os
from os.path import join, dirname
from dotenv import main
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from bovespa_model import BovespaModel

class BovespaScrapData:
    def __init__(self): 
        dotenv_path = join(dirname(__file__), '.env')
        main.load_dotenv(dotenv_path)

        self.chrome_driver = self.__web_driver()
        self.data: list[BovespaModel] = []

    def find_data(self):
        try:
            self.chrome_driver.get(str(os.environ.get("URL")))
            Select(self.chrome_driver.find_element(By.ID, "segment")).select_by_value("2")

            # while True:
            WebDriverWait(self.chrome_driver, 10).until(
                expected_conditions.presence_of_all_elements_located(
                    (By.XPATH, "//table/tbody"),
                ),
            )
            WebDriverWait(self.chrome_driver, 10).until(
                expected_conditions.presence_of_all_elements_located(
                    (By.CLASS_NAME, "pagination-next"),
                ),
            )

            table = self.chrome_driver.find_element(By.XPATH, "//table/tbody")
            pagination = self.chrome_driver.find_element(
                By.CLASS_NAME,
                "pagination-next",
            )

            rows = table.find_elements(By.TAG_NAME, "tr")
            self.__group_data(rows)

            # if "disabled" in pagination.get_dom_attribute("class"):
            #     break
            #
            # self.chrome_driver.execute_script("arguments[0].click();", pagination)
            return self.data
        except Exception as err:
            print(err)

    def __group_data(self, rows):
        for row in rows:
            data = tuple([a.text for a in row.find_elements(By.TAG_NAME, "td")])

            bovespa_model = BovespaModel(
                sector = str(data[0]),
                code = str(data[1]),
                stock = str(data[2]),
                type = str(data[3]),
                theoritical_amount = int(str(data[4]).replace(".", "")),
                percentage_share = float(str(data[5]).replace(",", ".")),
                percentage_accumulated = float(str(data[6]).replace(",", ".")),
            )

            self.data.append(bovespa_model)

    def __web_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        return webdriver.Chrome(options)