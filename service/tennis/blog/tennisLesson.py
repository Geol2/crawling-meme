from libs import db
from service.tennis import tennisFactory


class TennisLesson(tennisFactory.Tennis):

    def exist_lesson_blog(self, data):
        for i in range(len(data['url'])):
            url = data['url'][i]
            is_exist_blog = db.mysql.is_exist_lesson(db.cursor, url)
            if is_exist_blog is True:
                self.file_logger("등록된 레슨 리뷰 블로그가 이미 존재합니다.")
            else:
                self.insert_and_increase_tennis_blog(data, i)

    def insert_and_increase_tennis_blog(self, data: [], i: int):
        self.insert_tennis_blog(data, i, 2)
        self.increase_lesson_count()
