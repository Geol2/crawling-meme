import sys

from libs import common, db
from libs.ExecTime import ExecTime
from service.crawling.NaverBlogCrawling import NaverBlogCrawling
from service.crawling.NaverLessonCrawling import NaverLessonCrawling

def main(argv):
    ctime = ExecTime()
    if argv[1] in ("-blog"):
        NaverBlogCrawling().tennis_blog_service(ctime)
        NaverBlogCrawling().browser_exit()
    elif argv[1] in ("-lesson"):
        NaverLessonCrawling().tennis_lesson_service(ctime)
        NaverLessonCrawling().browser_exit()
    elif argv[1] in ("-url"):
        # 특정 url을 가져와서 크롤링하기
        return 0

    common.logger.info("END CRAWLING")
    db.cursor.close()
    db.conn.close()

    return 0

if __name__ == "__main__":
    main(sys.argv)
