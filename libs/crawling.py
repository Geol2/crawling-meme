import string
import math
import time
import datetime

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from libs import config
from libs import common
from libs import db

from dto.TennisObj import Tennis


class Crawling:
    init = ''
    driver = None

    wait_time = 1

    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')

        service = Service(executable_path=config.executable_path)
        # driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(option, service)
        self.driver.implicitly_wait(self.wait_time)


class NaverCrawling(Crawling):
    def open_url(self, tennis: Tennis):
        url = "https://m.place.naver.com/place/" + str(tennis.naver_place_id) +\
              "/review/ugc?entry=pll&zoomLevel=12.000&type=photoView"
        self.driver.get(url)

        is_valid_url = self.is_valid_url(tennis, url)
        if is_valid_url is False:
            tennis.print_logger("해당 테니스장 URL 주소를 찾을 수 없다는 판단을 했습니다.")
            return None
        return url

    def is_valid_url(self, tennis: Tennis, real_url: string):
        # 해당 url 주소가 잘못되었는지 판단하는 함수입니다.
        # 클래스 요소를 이용해서 없거나 있거나를 판단할 수 있지만 잘못된 테니스장 주소가 뜨는 것은 막진 못하고 있습니다.
        try:
            title_element = self.driver.find_element(By.CLASS_NAME, "YouOG")
            return True
        except Exception as e:
            tennis.printLogger(e)
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

    def find_blog_count(self ):
        return

    def click_more_blog(self, tennis: Tennis):
        # 더보기 없어질 때 까지 계속하기
        while 1:
            try:
                a_tag = self.driver.find_element(By.CLASS_NAME, "fvwqf")
                a_tag.click()
                tennis.print_logger("더보기 버튼이 실행되었습니다.")
                time.sleep(1)
            except Exception as e:
                tennis.print_logger("더보기 버튼이 없는 것 같아 블로그를 모두 보여주었다고 판단합니다.")
                return 1

        tennis.print_logger("블로그를 모두 보여주었다고 판단합니다.")
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

    def tennis_blog_service(self):
        tennis_info = db.mysql.get_tennis_info(db.cursor)
        tennis_info_length = len(tennis_info)
        tennis = None

        for i in range(tennis_info_length):
            try:
                tennis = Tennis(tennis_info[i][0], tennis_info[i][9], int(tennis_info[i][16]))
                self.open_url(tennis)
                self.click_more_blog(tennis)
                all_url_list = self.find_blog_url()
                self.find_blog_count(all_url_list)
                total_count = len(all_url_list)
                if total_count == 0:
                    tennis.print_logger("해당 테니스장 리뷰정보가 존재하지 않습니다.")
                    continue
            except Exception as e:
                tennis.file_logger("네이버 플레이스 id가 존재하지 않습니다.", e)
                continue


            all_title_list = self.find_title()
            all_date_list = self.find_write_blog_date()

            if total_count != len(all_title_list):
                tennis.print_logger("블로그 제목과 제목의 경로 개수가 다릅니다. 프로그램 수정이 필요할 수 있습니다.")
                exit(0)
            for j in range(total_count):
                url = all_url_list[j]
                title = all_title_list[j]
                write_date = all_date_list[j]
                is_exist_blog = db.mysql.exist_blog(db.cursor, url)
                if not is_exist_blog:
                    common.logger.info(
                        "[" + str(tennis.tennis_idx) + "]" + tennis.name + "(" + str(tennis.naver_id) + ")" + url + " 등록된 리뷰 블로그가 이미 존재합니다.")
                    continue
                insert_blog_result = db.mysql.insert_blog(db.cursor, tennis.tennis_idx, title, url, write_date)
                db.mysql.increase_blog_count(db.cursor, tennis.tennis_idx)

        db.cursor.close()
        db.conn.close()

    def tennis_blog_service_old(self):
        tennis_info = db.mysql.get_lesson_info(db.cursor)
        tennis_info_length = len(tennis_info)

        for i in range(tennis_info_length):
            try:
                tennis_idx = int(tennis_info[i][0])
                name = str(tennis_info[i][9])
                naver_id = int(tennis_info[i][16])
            except Exception as e:
                common.logger.info("[" + str(tennis_idx) + "]" + name + " 네이버 플레이스 id가 존재하지 않습니다.")
                continue

            real_url = self.open_url(naver_id)
            is_valid_url = self.is_valid_url(naver_id, real_url)
            if is_valid_url is False:
                print("[" + str(tennis_idx) + "]" + name + "(" + str(
                    naver_id) + ")" + " 해당 테니스장 URL 주소를 찾을 수 없다는 판단을 했습니다.")
                continue

            # 리뷰 수와 실제 블로그 수가 다를 수 있어서 리뷰 수로 전체를 판단할 수 없음
            self.click_more_blog(tennis_idx, name, naver_id)
            all_url_list = self.find_blog_url()
            total_count = len(all_url_list)
            if total_count == 0:
                print("[" + str(tennis_idx) + "]" + name + "(" + str(naver_id) + ")" + " 해당 테니스장 리뷰정보가 존재하지 않습니다.")
                continue

            all_title_list = self.find_title()
            all_date_list = self.find_write_blog_date()

            if total_count != len(all_title_list):
                print("[" + str(tennis_idx) + "]" + " 블로그 제목과 제목의 경로 개수가 다릅니다. 프로그램 수정이 필요할 수 있습니다.")
                exit(0)
            for j in range(total_count):
                url = all_url_list[j]
                title = all_title_list[j]
                write_date = all_date_list[j]
                is_exist_lesson_blog = db.mysql.exist_lesson_blog(db.cursor, url)
                if not is_exist_lesson_blog:
                    common.logger.info(
                        "[" + str(tennis_idx) + "]" + name + "(" + str(naver_id) + ")" + url + " 등록된 리뷰 블로그가 이미 존재합니다.")
                    continue
                insert_blog_result = db.mysql.insert_lesson_blog(db.cursor, tennis_idx, title, url, write_date)
                db.mysql.increase_blog_count(db.cursor, tennis_idx)

        db.cursor.close()
        db.conn.close()
