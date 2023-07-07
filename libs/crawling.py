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


class NaverCrawling(Crawling):

    def open_url(self, tennis: Tennis):
        url = "https://m.place.naver.com/place/" + str(tennis.naver_place_id) + \
              "/review/ugc?entry=pll&zoomLevel=12.000&type=photoView"
        self.driver.get(url)

        self.is_valid_url(tennis, url)
        return url

    def is_valid_url(self, tennis: Tennis, real_url: string):
        # 해당 url 주소가 잘못되었는지 판단하는 함수입니다.
        # 클래스 요소를 이용해서 없거나 있거나를 판단할 수 있지만 잘못된 테니스장 주소가 뜨는 것은 막진 못하고 있습니다.
        try:
            # 페이지를 찾을 수 없다는 곳입니다.
            self.driver.find_element(By.CLASS_NAME, "MQgGs")
            return False
        except Exception as e:
            tennis.file_logger("네이버 플레이스 URL 주소가 있습니다.")
            return True

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

    def click_more_end_blog(self, tennis: Tennis):
        # 더보기 없어질 때 까지 계속하기
        is_all_click = False
        click_count = 0

        while 1:
            if click_count > 20:
                is_all_click = True
                return is_all_click

            if is_all_click is False:
                is_all_click = self.click_more(tennis)
                click_count += 1
            else:
                return is_all_click

    def click_more_blog(self, tennis: Tennis):
        # 더보기 한번만 하기
        self.click_more(tennis)

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

    def compare_display_blog(self, tennis: Tennis):
        # 화면상 전체 개수와 데이터베이스 개수가 같은지 다른지 비교하기
        url_list = self.find_blog_url()
        blog_info = db.mysql.get_blog_info(tennis, 1)
        if len(url_list) == blog_info:
            return True
        return False
        # 하다말기

    def compare_display_lesson(self, tennis: Tennis):
        url_list = self.find_blog_url()
        lesson_info = db.mysql.get_blog_info(tennis, 2)
        if len(url_list) == lesson_info:
            return True
        return False

    def tennis_blog_service(self):
        rows = db.mysql.get_tennis_info(db.cursor)
        tennis = None

        for row in rows:
            tennis = TennisBlog(row["seq"], row["tennis_name"], row["tennis_naver_id"])
            tennis.file_logger(str(tennis.tennis_idx))

            try:
                self.open_url(tennis)
                self.click_more_end_blog(tennis)
                tennis.set_array(self.find_blog_url(), self.find_title(), self.find_write_blog_date())
                tennis.exist_blog()
            except Exception as e:
                tennis.file_logger(e)

    def tennis_lesson_service(self):
        rows = db.mysql.get_lesson_info(db.cursor)
        tennis = None
        rows_length = len(rows)

        for i in range(0, rows_length, 1):
            tennis = TennisLesson(rows[i]["seq"], rows[i]["tennis_name"], rows[i]["tennis_naver_id"])
            lesson_seq = rows[i]["seq"]
            tennis.file_logger(str(tennis.tennis_idx))
            click_count = 0

            try:
                naver_tennis = NTennis(tennis.naver_place_id)
                url = naver_tennis.open(self.driver)
                paging = 1
                is_valid = self.is_valid_url(tennis, url)
                if is_valid is False:
                    raise Exception("URL을 발견할 수 없습니다.")

                while True:
                    # 블로그 판별
                    data = naver_tennis.set_list_new(self.find_blog_url(),
                                                     self.find_title(),
                                                     self.find_write_blog_date(), paging)
                    paging += 1
                    tennis.exist_lesson_blog(data)
                    # tennis.set_lesson_info(naver_tennis.tennis_dict["url"])
                    is_eof = naver_tennis.is_eof(self.driver, 20)
                    if is_eof is True:
                        db.mysql.set_lesson_info(tennis.tennis_idx)
                        db.mysql.set_lesson_list(tennis.tennis_idx)
                        break
                    else:
                        naver_tennis.read_next(self.driver)
            except ProgrammingError as e:
                common.file_logger("개발자가 잘못 짬 ^^.. 문법 오류")
                exit()
            except Exception as e:
                db.mysql.unset_lesson_info(lesson_seq)
                db.mysql.unset_lesson_list(lesson_seq)
                common.file_logger("tennis_blog_service_new() 에서 알 수 없는 에러가 발생하였습니다.")












    # 참고만 합니다
    """
    def tennis_blog_service_new(self):
        rows = db.mysql.get_tennis_info(db.cursor)
        rows_length = len(rows)
        tennis = None

        for i in range(0, rows_length, 1):
            tennis = TennisLesson(rows[i]["seq"], rows[i]["tennis_name"], rows[i]["tennis_naver_id"])
            lesson_seq = rows[i]["seq"]
            tennis.file_logger(str(tennis.tennis_idx))

            try:
                naver_tennis = NTennis(tennis.naver_place_id)
                naver_tennis.open(self.driver)
                paging = 1

                while True:
                    # 블로그 판별
                    data = naver_tennis.set_list_new(self.find_blog_url(), self.find_title(),
                                                     self.find_write_blog_date(), paging)

                    paging += 1
                    tennis.exist_lesson_blog(data)
                    tennis.set_blog_info(naver_tennis.tennis_dict["url"])
                    is_eof = naver_tennis.is_eof(self.driver)
                    if is_eof is True:
                        db.mysql.set_lesson_info(tennis.tennis_idx)
                        db.mysql.set_lesson_list(tennis.tennis_idx)
                        break
                    else:
                        naver_tennis.read_next(self.driver)
            except Exception as e:
                db.mysql.unset_lesson_info(lesson_seq)
                db.mysql.unset_lesson_list(lesson_seq)
                common.file_logger("tennis_blog_service_new() 에서 알 수 없는 에러가 발생하였습니다.")

    def tennis_blog_service_old(self):
        rows = db.mysql.get_lesson_info(db.cursor)
        rows_length = len(rows)
        tennis = None

        for i in range(0, rows_length, 1):
            tennis = TennisLesson(rows[i]["seq"], rows[i]["tennis_name"], rows[i]["tennis_naver_id"])
            tennis.print_logger(str(tennis.tennis_idx))

            try:
                self.open_url(tennis)
                self.click_more_end_blog(tennis)
                tennis.set_array(self.find_blog_url(), self.find_title(), self.find_write_blog_date())
                tennis.exist_lesson_blog()
            except Exception as e:
                tennis.file_logger("알 수 없는 오류 발생")

    def tennis_blog_service_older(self):
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
        db.conn.close()"""
