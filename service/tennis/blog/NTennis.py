import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from libs import common, db


class NTennis:

    naver_place_id = 0

    tennis_dict = {
        "url": [],
        "title": [],
        "w_date": []
    }

    blog_count = 0

    def __init__(self, naver_place_id: int):
        self.naver_place_id = naver_place_id

    def open(self, driver):
        # url 열기
        url = "https://m.place.naver.com/place/" + str(self.naver_place_id) + \
              "/review/ugc?entry=pll&zoomLevel=12.000&type=photoView"
        driver.get(url)

        return url

    def read_next(self, driver):
        # 더보기 실행
        try:
            a = driver.find_element(By.CLASS_NAME, "fvwqf") # 더보기를 찾았을까?
            a.click()
            time.sleep(2)
        except Exception as e:
            common.file_logger(" 더보기를 실행할 수 없습니다.")
            return
        return

    def set_list_new(self, url: [], title: [], date: [], paging: int):
        if len(url) != len(title) or len(url) != len(date) or len(title) != len(date):
            raise Exception("테니스 정보를 합칠 수 없습니다.")
        if len(self.tennis_dict["url"]) > 0:
            self.tennis_dict["url"] = []
            self.tennis_dict["title"] = []
            self.tennis_dict["w_date"] = []

        index = paging * 10 - 10
        for i in range(len(url)):
            if index == len(url):
                break
            self.tennis_dict["url"].append(url[index])
            self.tennis_dict["title"].append(title[index])
            self.tennis_dict["w_date"].append(date[index])
            index += 1
            self.blog_count += 1

        return self.tennis_dict

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

    def is_eof(self, driver, click_count):
        # 끝임을 판단할 함수
        if click_count > 20:
            common.file_logger("블로그 카운트 최대치를 넘었습니다. 잘못된 실행으로 인해 종료합니다.")
            exit()

        try:
            # 더보기를 찾았을까?
            driver.find_element(By.CLASS_NAME, "fvwqf")
            click_count += 1
            time.sleep(2)
            return False
        except NoSuchElementException as e:
            common.file_logger("블로그를 모두 보여주었다고 판단합니다.")
            return True
        except RuntimeError as e:
            common.file_logger("NTennis.is_eof() 에서 알 수 없는 오류가 발생하였습니다.")
            return False
