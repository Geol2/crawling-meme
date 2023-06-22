import string
import math
import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from libs import config


class Crawling:
    blog_review_string = "블로그리뷰"
    separator = " "
    wait_time = 1
    data_list = []

    driver = ""

    def open_url(self, naver_id: string):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')

        service = Service(executable_path=config.executable_path)

        # driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(option, service)
        self.driver.implicitly_wait(self.wait_time)
        url = "https://m.place.naver.com/place/" + str(naver_id) + "/review/ugc?entry=pll&zoomLevel=12.000&type=photoView"
        self.driver.get(url)


    def find_total(self):
        # 블로그 수 전체를 찾는 함수
        total_count = 0
        blue_link = self.driver.find_elements(By.CLASS_NAME, "place_bluelink")
        for e in blue_link:
            blog_review_index = e.text.find(self.blog_review_string)
            if blog_review_index == 0:
                find_total_count = e.text.split(self.separator)
                total_count = find_total_count[1]

        return total_count

    def find_blog_url(self):
        # 블로그 링크를 찾는 부분
        url_list = []
        blog_link = self.driver.find_elements(By.CLASS_NAME, "xg2_q")
        blog_link_count = len(blog_link)
        for i in range(blog_link_count):
            a_tag = blog_link[i].find_element(By.TAG_NAME, "a")
            real_link = a_tag.get_property("href")
            if "?" in real_link: # query string 을 만나면 추가하지 않기
                real_link_parts = real_link.split("?")
                real_link = real_link_parts[0]
            url_list.append(real_link)
        return url_list


    def click_more_blog(self, tennis_idx: int, name: string, naver_id: int):
        # 더보기 없어질 때 까지 계속하기
        while 1:
            try:
                a_tag = self.driver.find_element(By.CLASS_NAME, "fvwqf")
                a_tag.click()
                print("[" + str(tennis_idx) + "]" + name + "(" + str(naver_id) + ")" + " 더보기 버튼이 실행되었습니다.")
                time.sleep(1)
            except Exception as e:
                print("[" + str(tennis_idx) + "]" + name + "(" + str(naver_id) + ")" +  " 더보기 버튼이 없는 것 같아 블로그를 모두 보여주었다고 판단합니다.")
                return 1;
        print("[" + str(tennis_idx) + "]" + name + "(" + str(naver_id) + ")" + " 블로그를 모두 보여주었다고 판단합니다.")
        return 0

    def get_click_number(self, total_count):
        # 더보기 클릭을 몇 번 해야하는지 찾는 함수
        # 첫 실행 시, 최대 10개는 노출해주므로 전체에서 1번은 클릭을 해주지 않아도 된다
        return math.ceil(int(total_count) / 10) - 1

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
        input_format = "%y.%m.%d.%a"
        output_format = "%Y-%m-%d"
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