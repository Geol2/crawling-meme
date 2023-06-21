from libs import db
from libs import crawling

crawl = crawling.Crawling()

totalCount = crawl.find_total()
clickNumber = crawl.get_click_number(totalCount)
showCount = crawl.show_blog_list(clickNumber)
crawl.find_title()

tennis_info = db.mysql.get_tennis_info()

print("END CRAWLING")

crawl.driver.quit()
