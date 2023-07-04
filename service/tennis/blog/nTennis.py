import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

class nTennis:

    naver_palce_id = 0


    def open(self):
        url = "https://m.place.naver.com/place/" + str(self.naver_palce_id) + \
              "/review/ugc?entry=pll&zoomLevel=12.000&type=photoView"
        self.driver.get(url)

        return url

    def readNext(self):
        try:
            a_tag = self.driver.find_element(By.CLASS_NAME, "fvwqf")
            a_tag.click()
            tennis.file_logger("더보기 버튼이 실행되었습니다.")
            time.sleep(1)
            return False
        except NoSuchElementException as e:
            tennis.file_logger("블로그를 모두 보여주었다고 판단합니다.")
            return True
        except RuntimeError as e:
            tennis.file_logger("crawling.click_more_blog() 에서 알 수 없는 오류가 발생하였습니다.")
            return False

    def getList(self):

    def checked_eof(self):
