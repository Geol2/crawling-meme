from libs import db
from service.tennis import tennisFactory


class TennisBlog(tennisFactory.Tennis):

    def exist_blog(self):
        for seq in range(self.total_count):
            url = self.tennis_dict['url'][seq]
            is_exist_blog = db.mysql.is_exist_blog(db.cursor, url)
            if is_exist_blog is True:
                # 존재하고 있으면 1로 업데이트
                db.mysql.update_checkout_blog(url)
            else:
                # 존재하지 않으면 insert
                self.insert_and_increase_tennis_blog(seq)

    def insert_and_increase_tennis_blog(self, dict_seq: int):
        self.insert_tennis_blog(dict_seq, 1)
        db.mysql.increase_blog_count(db.cursor, self.tennis_idx)

    def set_end_flag(self):
        self.set_blog_end_flag()

