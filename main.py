import sys

from libs import common, db
from service.crawling import NaverCrawling


def main(argv):
    if argv[1] in ("-blog"):
        NaverCrawling.NaverCrawling().tennis_blog_service()
        NaverCrawling.NaverCrawling().browser_exit()
    elif argv[1] in ("-lesson"):
        NaverCrawling.NaverCrawling().tennis_lesson_service()
        NaverCrawling.NaverCrawling().browser_exit()
    elif argv[1] in ("-url"):
        # 특정 url을 가져와서 크롤링하기
        return 0

    common.logger.info("END CRAWLING")
    db.cursor.close()
    db.conn.close()

    return 0

if __name__ == "__main__":
    main(sys.argv)
