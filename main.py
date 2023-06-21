from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import math
import time


blog_review_string = "블로그리뷰"
separator = " "
wait_time = 1
data_list = []

option = webdriver.ChromeOptions()
option.add_argument('--headless')

# driver = webdriver.Chrome()
driver = webdriver.Chrome( ChromeDriverManager().install() )
driver.implicitly_wait(wait_time)
driver.get("https://m.place.naver.com/place/1342356243/review/ugc?entry=pll&zoomLevel=12.000&type=photoView")


def find_total():
    # 블로그 수 전체를 찾는 함수
    total_count = 0
    blue_link = driver.find_elements(By.CLASS_NAME, "place_bluelink")
    for e in blue_link:
        blog_review_index = e.text.find(blog_review_string)
        if blog_review_index == 0:
            find_total_count = e.text.split(separator)
            total_count = find_total_count[1]

    return total_count


def show_blog_list(number):
    i = 0;
    # 더보기 없어질 때 까지 계속하기
    for _ in range(number):
        a_tag = driver.find_element(By.CLASS_NAME, "fvwqf")
        a_tag.click()
        time.sleep(1)
        i += 1

    return i


def get_click_number(total_count):
    # 더보기 클릭을 몇 번 해야하는지 찾는 함수
    # 첫 실행 시, 최대 10개는 노출해주므로 전체에서 1번은 클릭을 해주지 않아도 된다
    return math.ceil(int(total_count) / 10) - 1


totalCount = find_total()
clickNumber = get_click_number(totalCount)
showCount = show_blog_list(clickNumber)

print("OK")

driver.quit()
