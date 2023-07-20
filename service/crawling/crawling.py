from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from libs import config


class Crawling:
    init = ''
    driver = None

    wait_time = 3

    def __init__(self):
        self.chrome()

    def chrome(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--blink-settings=imagesEnabled=false')

        service = Service(executable_path=config.executable_path)
        # driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(options, service)
        self.driver.implicitly_wait(self.wait_time)

    def browser_exit(self):
        self.driver.quit()
