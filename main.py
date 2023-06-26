import getopt
import sys

from libs import common
from libs import crawling


def main(argv):
    opts = getopt.getopt(argv[:1])
    crawl = ''

    for opt, arg in opts:
        if opt in ("-blog"):
            crawl = crawling.NaverCrawling()
            crawling.NaverCrawling().tennis_blog_service()
        elif opt in ("-url"):
            # 특정 url을 가져와서 크롤링하기
            crawl = crawling.NaverCrawling()
            return 0

    common.logger.info("END CRAWLING")
    crawl.driver.quit()


if __name__ == "__main__":
    main(sys.argv)
