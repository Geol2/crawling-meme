import getopt
import sys

from libs import common
from libs import crawling


def main(argv):
    crawl = crawling.NaverCrawling()
    if argv[1] in ("-blog"):
        crawling.NaverCrawling().tennis_blog_service()
    elif argv[1] in ("-lesson"):
        crawling.NaverCrawling().tennis_lesson_blog_service()
        crawl.driver.quit()
    elif argv[1] in ("-url"):
        # 특정 url을 가져와서 크롤링하기
        return 0

    crawl.driver.quit()
    common.logger.info("END CRAWLING")
    return 0

if __name__ == "__main__":
    main(sys.argv)
