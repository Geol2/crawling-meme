from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from libs import config


class Crawling:
    init = ''
    driver = None

    wait_time = 5

    def __init__(self):
        self.chrome()

    def chrome(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')

        service = Service(executable_path=config.executable_path)
        # driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(option, service)
        self.driver.implicitly_wait(self.wait_time)

    def browser_exit(self):
        self.driver.quit()
