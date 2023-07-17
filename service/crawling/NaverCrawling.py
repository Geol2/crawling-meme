import datetime
import math
import string
import time

from pymysql import ProgrammingError
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from libs import db, common
from service.crawling.crawling import Crawling
from service.tennis.blog.NTennis import NTennis
from service.tennis.blog.tennisBlog import TennisBlog
from service.tennis.blog.tennisLesson import TennisLesson
from service.tennis.tennisFactory import Tennis


class NaverCrawling(Crawling):

    def is_valid_url(self, tennis: Tennis, real_url: string):
        # 해당 url 주소가 잘못되었는지 판단하는 함수입니다.
        # 클래스 요소를 이용해서 없거나 있거나를 판단할 수 있지만 잘못된 테니스장 주소가 뜨는 것은 막진 못하고 있습니다.
        try:
            # 페이지를 찾을 수 없는 것보다 있는 것을 찾는 것이 아무래도 빠릅니다.
            self.driver.find_element(By.CLASS_NAME, "Fc1rA")
            return True
        except Exception as e:
            tennis.file_logger("네이버 플레이스 URL 주소가 없습니다.")
            return False

    def find_blog_url(self):
        # 블로그 링크를 찾는 부분
        url_list = []
        blog_link = self.driver.find_elements(By.CLASS_NAME, "xg2_q")
        blog_link_count = len(blog_link)

        for i in range(blog_link_count):
            a_tag = blog_link[i].find_element(By.TAG_NAME, "a")
            real_link = a_tag.get_property("href")
            if "?" in real_link:  # query string 을 만나면 추가하지 않기
                real_link_parts = real_link.split("?")
                real_link = real_link_parts[0]
            url_list.append(real_link)
        return url_list

    def click_more(self, tennis: Tennis):
        try:
            a_tag = self.driver.find_element(By.CLASS_NAME, "fvwqf")
            # a_tag.click()
            a_tag.send_keys(Keys.ENTER)
            tennis.file_logger("더보기 버튼이 실행되었습니다.")
            time.sleep(2)
            return False
        except NoSuchElementException as e:
            tennis.file_logger("블로그를 모두 보여주었다고 판단합니다.")
            return True
        except RuntimeError as e:
            tennis.file_logger("crawling.click_more_blog() 에서 알 수 없는 오류가 발생하였습니다.")
            return False

    def find_title(self):
        title_list = []
        review_list = self.driver.find_elements(By.CLASS_NAME, "s2opK")
        for i in range(len(review_list)):
            title = review_list[i].find_element(By.TAG_NAME, "span").text
            title_list.append(title)

        return title_list

    def find_write_blog_date(self):
        date_list = []
        date_element = self.driver.find_elements(By.CLASS_NAME, "FYQ74")
        for i in range(len(date_element)):
            write_date_element = date_element[i].find_element(By.TAG_NAME, "span")
            write_date_text = write_date_element.text
            write_date_parts = write_date_text.split(".")

            if len(write_date_parts) == 4:
                year = 2000 + int(write_date_parts[0])
                month = int(write_date_parts[1])
                day = int(write_date_parts[2])
                weekday = write_date_parts[3]
            else:
                current_year = datetime.datetime.now().year
                month = int(write_date_parts[0])
                day = int(write_date_parts[1])
                year = current_year
                weekday = write_date_parts[2]
            converted_date_string = "{}-{:02d}-{:02d}".format(year, month, day)
            date_list.append(converted_date_string)
        return date_list