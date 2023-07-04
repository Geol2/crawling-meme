from libs import db
from service.tennis import tennisFactory


class TennisLesson(tennisFactory.Tennis):

    def exist_lesson_blog(self):
        for seq in range(self.total_count):
            url = self.tennis_dict['url'][seq]
            is_exist_blog = db.mysql.is_exist_lesson(db.cursor, url)
            if is_exist_blog is True:
                self.file_logger("등록된 레슨 리뷰 블로그가 이미 존재합니다.")
            else:
                self.insert_and_increase_tennis_blog(seq)

    def insert_and_increase_tennis_blog(self, dict_seq: int):
        self.insert_tennis_blog(dict_seq, 2)
        self.increase_lesson_count()
