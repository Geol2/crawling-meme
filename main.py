from selenium import webdriver
from selenium.webdriver.common.by import By

import math

driver = webdriver.Chrome()
driver.get("https://m.place.naver.com/place/1342356243/review/ugc?entry=pll&zoomLevel=12.000&type=photoView")

driver.implicitly_wait(1)

findBlogReviewString = "블로그리뷰"
findSeparator = " "


def findTotal():
    totalCount = 0
    blueLink = driver.find_elements(By.CLASS_NAME, "place_bluelink")
    for e in blueLink:
        blogReviewIndex = e.text.find(findBlogReviewString)
        if blogReviewIndex == 0:
            findTotalCount = e.text.split(" ")
            totalCount = findTotalCount[1]

    return totalCount


def allShowDisplay(clickNumber):
    # 더보기 없어질 때 까지 계속하기
    for _ in range(clickNumber):
        driver.implicitly_wait(1)
        aTag = driver.find_element(By.CLASS_NAME, "fvwqf")
        aTag.click()


def getClickNumber(totalCount):
    return math.ceil(int(totalCount) / 10)


totalCount = findTotal()
clickNumber = getClickNumber(totalCount)
allShowDisplay(clickNumber)

driver.quit()
