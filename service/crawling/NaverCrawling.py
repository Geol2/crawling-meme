import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from service.crawling.crawling import Crawling
from service.tennis.tennisFactory import Tennis


class NaverCrawling(Crawling):

    def is_valid_url(self, tennis: Tennis):
        # 해당 url 주소가 잘못되었는지 판단하는 함수입니다.
        # 클래스 요소를 이용해서 없거나 있거나를 판단할 수 있지만 잘못된 테니스장 주소가 뜨는 것은 막진 못하고 있습니다.
        try:
            # 페이지를 찾을 수 없는 것보다 있는 것을 찾는 것이 아무래도 빠릅니다.
            self.driver.find_elements(By.CLASS_NAME, "tAvTy")
            return True
        except Exception as e:
            tennis.file_logger("네이버 플레이스 URL 주소가 없습니다.")
            return False

    def find_review_element(self):
        list = {
            "url": [],
            "title": [],
            "date": []
        }

        reviews = self.driver.find_elements(By.CLASS_NAME, "xg2_q")
        reviews_count = len(reviews)

        for i in range(reviews_count):
            # url 데이터 넣기
            a_tag = reviews[i].find_element(By.TAG_NAME, "a")
            real_link = a_tag.get_property("href")
            if "?" in real_link:  # query string 을 만나면 추가하지 않기
                real_link_parts = real_link.split("?")
                real_link = real_link_parts[0]
            list["url"].append(real_link)

            # title 데이터 넣기
            contents = reviews[i].find_element(By.CLASS_NAME, "kT8X8")
            list['title'].append(contents.find_element(By.CLASS_NAME, "hPTBw").text)

            # 날짜 찾는 부분
            write_date_element = contents.find_element(By.CLASS_NAME, "ZeWU8")
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
            list["date"].append(converted_date_string)

        return list