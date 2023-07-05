import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from libs import common, db


class NTennis:

    naver_place_id = 0

    data_dict = {
        "url": [],
        "title": [],
        "w_date": []
    }

    def __init__(self, naver_place_id: int):
        self.naver_place_id = naver_place_id

    def open(self, driver):
        # url 열기
        url = "https://m.place.naver.com/place/" + str(self.naver_place_id) + \
              "/review/ugc?entry=pll&zoomLevel=12.000&type=photoView"
        driver.get(url)
        return url

    def read_next(self, driver, paging: int = 0):
        # 더보기 실행
        a_tag = driver.find_element(By.CLASS_NAME, "fvwqf")
        a_tag.click()
        time.sleep(2)

    def set_list_new(self, url: [], title: [], date: [], pagind: int):
        #if len(url) == 0:
        #    raise Exception("테니스장 정보가 존재할 수 없습니다.")
        if len(url) != len(title) or len(url) != len(date) or len(title) != len(date):
            raise Exception("테니스 정보를 합칠 수 없습니다.")
        if len(self.tennis_dict["url"]) > 0:
            self.tennis_dict["url"] = []
            self.tennis_dict["title"] = []
            self.tennis_dict["w_date"] = []

        index = pagind * 10 - 10
        for i in range(len(url)):
            if index == len(url):
                break
            self.total_count = len(url)
            self.tennis_dict["url"].append(url[index])
            self.tennis_dict["title"].append(title[index])
            self.tennis_dict["w_date"].append(date[index])
            index += 1

    def set_list(self, url: [], title: [], date: []):
        #if len(url) == 0:
        #    raise Exception("테니스장 정보가 존재할 수 없습니다.")
        if len(url) != len(title) or len(url) != len(date) or len(title) != len(date):
            raise Exception("테니스 정보를 합칠 수 없습니다.")
        if len(self.tennis_dict["url"]) > 0:
            self.tennis_dict["url"] = []
            self.tennis_dict["title"] = []
            self.tennis_dict["w_date"] = []

        for i in range(len(url)):
            self.total_count = len(url)
            self.tennis_dict["url"].append(url[i])
            self.tennis_dict["title"].append(title[i])
            self.tennis_dict["w_date"].append(date[i])

    def get_dict_list(self):
        # 데이터 가져오기
        return self.data_dict

    def is_eof(self, driver):
        # 끝임을 판단할 함수
        click_count = 0
        try:
            a_tag = driver.find_element(By.CLASS_NAME, "fvwqf")
            a_tag.click()
            click_count += 1
            time.sleep(2)
            return False
        except NoSuchElementException as e:
            common.file_logger("블로그를 모두 보여주었다고 판단합니다.")
            return True
        except RuntimeError as e:
            common.file_logger("crawling.click_more_blog() 에서 알 수 없는 오류가 발생하였습니다.")
            return False
