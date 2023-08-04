from libs import db
from service.tennis import tennisFactory


class TennisLesson(tennisFactory.Tennis):

    def exist_lesson_blog(self, data: []):

        for i in range(len(data['url'])):
            url = data['url'][i]
            title = data['title'][i]
            w_date = data['w_date'][i]

            is_checkout = db.mysql.is_checkout_lesson(url)
            if is_checkout == 0:
                # 한 개의 url에 대해 0값을 발견 했을 때, idx의 모든 블로그를 0으로 만듭니다.
                db.mysql.unset_lesson_info(self.tennis_idx)
                db.mysql.unset_lesson_list(self.tennis_idx)
            elif is_checkout == 1:
                # 한 개의 url에 대해 1을 발견 했을 때, 크롤링이 완료되었다고 판단합니다.
                self.file_logger("이전에 크롤링이 완료되었습니다. 레슨 리뷰 블로그가 이미 존재합니다.")
                # return True
            elif is_checkout is None:
                # 해당 url을 찾을 수 없는 경우입니다. 크롤링하지 않은 데이터로 봅니다.
                self.insert_and_increase_tennis_blog(url, title, w_date)

    def insert_and_increase_tennis_blog(self, url, title, w_date):
        self.insert_tennis_blog(url, title, w_date, 2)
        db.mysql.increase_lesson_count(self.tennis_idx)
