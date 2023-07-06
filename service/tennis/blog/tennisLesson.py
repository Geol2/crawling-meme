from libs import db
from service.tennis import tennisFactory


class TennisLesson(tennisFactory.Tennis):

    def exist_lesson_blog(self, data: []):
        is_checkout = None

        for i in range(len(data['url'])):
            url = data['url'][i]
            is_checkout = db.mysql.is_checkout_lesson(url)
            if is_checkout == 0:
                # 한 개의 url에 대해 0값을 발견 했을 때, idx의 모든 블로그를 0으로 만듭니다.
                db.mysql.unset_lesson_info(self.tennis_idx)
                db.mysql.unset_lesson_list(self.tennis_idx)
            elif is_checkout == 1:
                # 한 개의 url에 대해 1을 발견 했을 때, 크롤링이 완료되었다고 판단합니다.
                self.file_logger("이전에 크롤링이 완료되었습니다. 레슨 리뷰 블로그가 이미 존재합니다.")
            elif is_checkout is None:
                # 해당 url을 찾을 수 없는 경우입니다. 아마 크롤링하지 않은 데이터로 봅니다.
                self.insert_and_increase_tennis_blog(data, i)

    def insert_and_increase_tennis_blog(self, data, i: int):
        self.insert_tennis_blog(data, i, 2)
        self.increase_lesson_count()





    def exist_lesson_blog_old(self):
        for i in range(len(self.tennis_dict['url'])):
            url = self.tennis_dict['url'][i]
            is_exist_blog = db.mysql.is_exist_lesson(db.cursor, url)
            if is_exist_blog is True:
                self.file_logger("등록된 레슨 리뷰 블로그가 이미 존재합니다.")
            else:
                self.insert_and_increase_tennis_blog_old(i)

    def insert_and_increase_tennis_blog_old(self, dict_seq):
        self.insert_tennis_blog_old(dict_seq, 2)
        self.increase_lesson_count()
