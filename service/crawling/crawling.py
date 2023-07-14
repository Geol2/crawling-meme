import string
import math
import time
import datetime

from pymysql import ProgrammingError
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from libs import config
from libs import common
from libs import db
from service.tennis.blog.NTennis import NTennis
from service.tennis.blog.tennisBlog import TennisBlog
from service.tennis.blog.tennisLesson import TennisLesson

from service.tennis.tennisFactory import Tennis


class Crawling:
    init = ''
    driver = None

    wait_time = 10

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
