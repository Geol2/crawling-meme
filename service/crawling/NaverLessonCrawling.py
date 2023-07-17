from pymysql import ProgrammingError

from libs import db, common
from service.crawling.NaverCrawling import NaverCrawling
from service.tennis.blog.NTennis import NTennis
from service.tennis.blog.tennisLesson import TennisLesson


class NaverLessonCrawling(NaverCrawling):

    def tennis_lesson_service(self, ctime):
        rows = db.mysql.get_lesson_info(db.cursor)
        tennis = None
        rows_length = len(rows)

        ctime.total_start_time()

        for i in range(0, rows_length, 1):
            tennis = TennisLesson(rows[i]["seq"], rows[i]["tennis_name"], rows[i]["tennis_naver_id"])
            lesson_seq = rows[i]["seq"]
            tennis.file_logger(str(tennis.tennis_idx))
            click_count = 0

            try:
                naver_tennis = NTennis(tennis.naver_place_id)
                ctime.start_time()
                url = naver_tennis.open(self.driver)
                ctime.end_time()
                ctime.diff("browser_open")

                paging = 1

                ctime.start_time()
                is_valid = self.is_valid_url(tennis, url)
                ctime.end_time()
                ctime.diff("valid_url")
                if is_valid is False:
                    common.file_logger("URL을 발견할 수 없습니다.")
                    continue

                while True:
                    ctime.start_time()
                    # 블로그 판별
                    data = naver_tennis.set_list(self.find_blog_url(),
                                                 self.find_title(),
                                                 self.find_write_blog_date(),
                                                 paging)
                    ctime.end_time()
                    ctime.diff("set_data")

                    paging += 1
                    ctime.start_time()
                    is_continue = tennis.exist_lesson_blog(data)
                    ctime.end_time()
                    ctime.diff("exist_blog")
                    if is_continue is True:
                        break

                    ctime.start_time()
                    is_eof = naver_tennis.is_eof(self.driver, click_count)
                    ctime.end_time()
                    ctime.diff("is_eof")
                    if is_eof is True:
                        db.mysql.set_lesson_info(tennis.tennis_idx)
                        db.mysql.set_lesson_list(tennis.tennis_idx)
                        break
                    else:
                        ctime.start_time()
                        naver_tennis.read_next(self.driver)
                        ctime.end_time()
                        ctime.diff("read_next")
            except ProgrammingError as e:
                common.file_logger("개발자가 잘못 짬 ^^.. 문법 오류")
                exit()
            except Exception as e:
                db.mysql.unset_lesson_info(lesson_seq)
                db.mysql.unset_lesson_list(lesson_seq)
                common.file_logger("tennis_blog_service_new() 에서 알 수 없는 에러가 발생하였습니다.")

        ctime.total_end_time()
        ctime.total_diff()
        ctime.time_print()
