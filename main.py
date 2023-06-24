from libs import common
from libs import crawling

crawl = crawling.NaverCrawling()
crawling.NaverCrawling().tennis_blog_service()

common.logger.info("END CRAWLING")
crawl.driver.quit()
