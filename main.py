from selenium import webdriver
from selenium.webdriver.common.by import By

import math
import time

findBlogReviewString = "블로그리뷰"
findSeparator = " "
waitTime = 10

driver = webdriver.Chrome()
driver.implicitly_wait(waitTime)
driver.get("https://m.place.naver.com/place/1342356243/review/ugc?entry=pll&zoomLevel=12.000&type=photoView")
driver.implicitly_wait(waitTime)


def findTotal():
    # 블로그 수 전체를 찾는 함수
    totalCount = 0
    blueLink = driver.find_elements(By.CLASS_NAME, "place_bluelink")
    for e in blueLink:
        blogReviewIndex = e.text.find(findBlogReviewString)
        if blogReviewIndex == 0:
            findTotalCount = e.text.split(" ")
            totalCount = findTotalCount[1]

    return totalCount


def allShowDisplay(clickNumber):
    i = 0;
    # 더보기 없어질 때 까지 계속하기
    for _ in range(clickNumber):
        aTag = driver.find_element(By.CLASS_NAME, "fvwqf")
        aTag.click()
        time.sleep(1)
        i += 1

    return i

def getClickNumber(totalCount):
    # 더보기 클릭을 몇 번 해야하는지 찾는 함수
    # 첫 실행 시, 최대 10개는 노출해주므로 전체에서 1번은 클릭을 해주지 않아도 된다
    return math.ceil(int(totalCount) / 10) - 1


totalCount = findTotal()
clickNumber = getClickNumber(totalCount)
showCount = allShowDisplay(clickNumber)

driver.quit()
