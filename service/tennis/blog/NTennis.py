import time

from selenium.common import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from libs import common, ExecTime


class NTennis:

    naver_place_id = 0

    tennis_dict = {
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
        #url = "https://m.place.naver.com/place/" + "123123123" + \
        #      "/review/ugc?entry=pll&zoomLevel=12.000&type=photoView"
        driver.get(url)
        wait = WebDriverWait(driver,
                             timeout=3,
                             poll_frequency=1,
                             ignored_exceptions=[ElementNotVisibleException,
                                                 ElementNotSelectableException])

        return url, wait

    def read_next(self, driver):
        # 더보기 실행
        try:
            a = driver.find_element(By.CLASS_NAME, "fvwqf") # 더보기를 찾았을까?
            a.click()
        except Exception as e:
            common.file_logger(" 더보기를 실행할 수 없습니다.")
            return
        return

    def set_list(self, data_list: [], paging: int, ctime: ExecTime):
        if len(data_list['url']) == 0:
            raise Exception("테니스 데이터 리스트를 만들 수 없습니다.")

        if len(self.tennis_dict["url"]) > 0:
            self.tennis_dict["url"] = []
            self.tennis_dict["title"] = []
            self.tennis_dict["w_date"] = []

        index = paging * 10 - 10
        for i in range(len(data_list['url'])):
            if index == len(data_list['url']):
                break
            self.tennis_dict["url"].append(data_list['url'][index])
            self.tennis_dict["title"].append(data_list['title'][index])
            self.tennis_dict["w_date"].append(data_list['date'][index])
            index += 1
            ctime.add_count("blog_count")

        return self.tennis_dict

    def get_dict_list(self):
        # 데이터 가져오기
        return self.tennis_dict

    def is_eof(self, driver, click_count):
        # 끝임을 판단할 함수
        if click_count >= 20:
            common.file_logger("블로그 카운트 최대치를 넘었습니다. 잘못된 실행으로 인해 웹 드라이버를 종료합니다.")
            exit()

        try:
            # 더보기를 찾았을까?
            driver.find_element(By.CLASS_NAME, "fvwqf")
            click_count += 1
            return False
        except NoSuchElementException as e:
            common.file_logger("블로그를 모두 보여주었다고 판단합니다.")
            return True
        except RuntimeError as e:
            common.file_logger("NTennis.is_eof() 에서 알 수 없는 오류가 발생하였습니다.")
            return False
