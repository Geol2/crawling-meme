from pymysql import ProgrammingError

from libs import db, common
from service.crawling.NaverCrawling import NaverCrawling
from service.tennis.blog.NTennis import NTennis
from service.tennis.blog.tennisBlog import TennisBlog


class NaverBlogCrawling(NaverCrawling):

    def tennis_blog_service(self, ctime):
        rows = db.mysql.get_tennis_info()
        tennis = None

        ctime.total_start_time()

        for row in rows:
            ctime.add_count("total_count")
            tennis = TennisBlog(row["seq"], row["tennis_name"], row["tennis_naver_id"])
            tennis.file_logger(str(tennis.tennis_idx))
            click_count = 0

            try:
                n_tennis = NTennis(tennis.naver_place_id)

                ctime.start_time()
                url, wait = n_tennis.open(self.driver)
                ctime.end_time()
                ctime.diff("browser_open")

                paging = 1

                ctime.start_time()
                is_valid = self.is_valid_url(tennis)
                ctime.end_time()
                ctime.diff("valid_url")
                if is_valid is False:
                    common.file_logger("URL을 발견할 수 없습니다.")
                    ctime.add_count("failed_count")
                    continue
                ctime.add_count("success_count")

                while True:
                    ctime.start_time()
                    data_list = self.find_review_element()
                    ctime.end_time()
                    ctime.diff("find_review_element")

                    ctime.start_time()
                    # 블로그 판별
                    data = n_tennis.set_list(data_list, paging, ctime)
                    ctime.end_time()
                    ctime.diff("set_data")

                    paging += 1
                    ctime.start_time()
                    is_continue = tennis.exist_blog(data)
                    ctime.end_time()
                    ctime.diff("exist_blog")
                    if is_continue is True:
                        break

                    ctime.start_time()
                    is_eof = n_tennis.is_eof(self.driver, click_count)
                    ctime.end_time()
                    ctime.diff("is_eof")
                    if is_eof is True:
                        db.mysql.set_blog_info(tennis.tennis_idx)
                        db.mysql.set_blog_list(tennis.tennis_idx)
                        break
                    else:
                        ctime.start_time()
                        n_tennis.read_next(self.driver)
                        ctime.add_count("click_page_count")
                        ctime.end_time()
                        ctime.diff("read_next")
            except ProgrammingError as e:
                common.file_logger("개발자가 잘못 짬 ^^.. 문법 오류")
                exit()
            except Exception as e:
                db.mysql.unset_tennis_info(tennis.tennis_idx)
                db.mysql.unset_blog_list(tennis.tennis_idx)
                common.file_logger("알 수 없는 에러 발생")

        ctime.total_end_time()
        ctime.total_diff()
        ctime.etc()
        ctime.time_print()
