import string

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

    def __init__(self):
        self.tennis_idx = -1
        self.name = None
        self.naver_place_id = None
        self.w_date = None

    def __init__(self, tennis_idx: int, name: string, naver_place_id: int):
        self.tennis_idx = tennis_idx
        self.name = name
        self.naver_place_id = naver_place_id

    def set_array(self, url: [], title: [], date: []):
        if len(url) is 0:
            raise Exception("테니스장 정보가 존재할 수 없습니다.")
        if len(url) != len(title) or len(url) != len(date) or len(title) != len(date):
            raise Exception("테니스 정보를 합칠 수 없습니다.")

        for i in range(len(url)):
            self.total_count = len(url)
            self.tennis_dict['url'].append(url[i])
            self.tennis_dict['title'].append(title[i])
            self.tennis_dict['w_date'].append(date[i])

    def exist_blog(self):
        for seq in range(self.total_count):
            url = self.tennis_dict['url'][seq]
            is_exist_blog = db.mysql.is_exist_blog(db.cursor, url)
            if is_exist_blog is True:
                self.print_logger("등록된 리뷰 블로그가 이미 존재합니다.")
                self.file_logger("등록된 리뷰 블로그가 이미 존재합니다.")
            else:
                self.insert_and_increase_tennis_blog(seq)

    def insert_and_increase_tennis_blog(self, seq: int):
        self.insert_tennis_blog(seq)
        self.increase_blog_count()

    def insert_tennis_blog(self, seq: int):
        url = self.tennis_dict['url'][seq];
        title = self.tennis_dict['title'][seq];
        w_date = self.tennis_dict['w_date'][seq]

        data = {
            "url": url,
            "title": title,
            "w_date": w_date
        }
        db.mysql.insert_blog(db.cursor, self.tennis_idx, data)

    def increase_blog_count(self):
        db.mysql.increase_blog_count(db.cursor, self.tennis_idx)

    def file_logger(self, message: string, e=None):
        if self.tennis_idx is -1:
            common.logger.info("테니스장 idx 정보가 잘못되었습니다.")
            return

        if self.name is None:
            common.logger.info("테니스장 이름이 존재하지 않습니다.")
        if self.naver_place_id is -1:
            common.logger.info("네이버 플레이스 id가 존재하지 않습니다.")

        common.logger.info("[" + str(self.tennis_idx) + "] " + str(self.name) + "(" + str(self.naver_place_id) + ")" + message)

    def print_logger(self, message=None):
        if self.tennis_idx is -1:
            print("테니스장 idx 정보가 잘못되었습니다.")
            return

        if self.name is None:
            print("테니스장 이름이 존재하지 않습니다.")
        if self.naver_place_id is -1:
            print("네이버 플레이스 id가 존재하지 않습니다.")

        print("[" + str(self.tennis_idx) + "] " + str(self.name) + "(" + str(self.naver_place_id) + ") : " + message)
