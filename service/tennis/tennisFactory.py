import string
import time

from libs import common, db


class Tennis:
    tennis_idx = -1
    name = None
    naver_place_id = -1

    tennis_dict = {
        "url": [],
        "title": [],
        "w_date": []
    }

    total_count = 0

    paging = total_count / 10

    def __init__(self, tennis_idx: int, name: string, naver_place_id: int):
        self.tennis_idx = tennis_idx
        self.name = name
        self.naver_place_id = naver_place_id

    def set_array(self, url: [], title: [], date: []):
        #if len(url) == 0:
        #    raise Exception("테니스장 정보가 존재할 수 없습니다.")
        if len(url) != len(title) or len(url) != len(date) or len(title) != len(date):
            raise Exception("테니스 정보를 합칠 수 없습니다.")
        if len(self.tennis_dict["url"]) > 0:
            self.tennis_dict["url"] = []
            self.tennis_dict["title"] = []
            self.tennis_dict["w_date"] = []

        for i in range(len(url)):
            self.total_count = len(url)
            self.tennis_dict["url"].append(url[i])
            self.tennis_dict["title"].append(title[i])
            self.tennis_dict["w_date"].append(date[i])

    def insert_tennis_blog(self, seq: int, blog_type: int):
        url = self.tennis_dict['url'][seq]
        title = self.tennis_dict['title'][seq]
        w_date = self.tennis_dict['w_date'][seq]

        data = {
            "url": url,
            "title": title,
            "w_date": w_date,
            "blog_type": blog_type
        }
        db.mysql.insert_blog(db.cursor, self.tennis_idx, data)

    def increase_lesson_count(self):
        db.mysql.increase_lesson_count(db.cursor, self.tennis_idx)

    def set_blog_end_flag(self):
        db.mysql.set_blog_end_flag(db.cursor, self.tennis_idx)

    def file_logger(self, message: string, e=None):
        if self.tennis_idx == -1:
            common.logger.info("테니스장 idx 정보가 잘못되었습니다.")
            return

        if self.name is None:
            common.logger.info("테니스장 이름이 존재하지 않습니다.")
        if self.naver_place_id == -1:
            common.logger.info("네이버 플레이스 id가 존재하지 않습니다.")

        common.logger.info(time.strftime('[%Y.%m.%d][%H:%M:%S]') + "[" + str(self.tennis_idx) + "] " + str(self.name) +
                           "(" + str(self.naver_place_id) + ")" +
                           message)

    def print_logger(self, message=None):
        if self.tennis_idx == -1:
            print("테니스장 idx 정보가 잘못되었습니다.")
            return

        if self.name is None:
            print("테니스장 이름이 존재하지 않습니다.")
        if self.naver_place_id == -1:
            print("네이버 플레이스 id가 존재하지 않습니다.")

        print(time.strftime('[%Y.%m.%d][%H:%M:%S]') + "[" + str(self.tennis_idx) + "] " + str(self.name) +
              "(" + str(self.naver_place_id) + ") : " + message)
