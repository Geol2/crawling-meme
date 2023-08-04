from libs import db
from service.tennis import tennisFactory


class TennisBlog(tennisFactory.Tennis):

    def exist_tennis_blog(self, data: []):

        for i in range(len(data['url'])):
            url = data['url'][i]
            title = data['title'][i]
            w_date = data['w_date'][i]

            is_checkout = db.mysql.is_checkout_blog(url)
            if is_checkout == 0:
                # 존재하고 있으면 1로 업데이트
                db.mysql.unset_tennis_info(self.tennis_idx)
                db.mysql.unset_tennis_list(self.tennis_idx)
            elif is_checkout == 1:
                # 한 개의 url에 대해 1을 발견 했을 때, 크롤링이 완료되었다고 판단합니다.
                self.file_logger("이전에 크롤링이 완료되었습니다. 블로그 리뷰 블로그가 이미 존재합니다.")
                # return True
            elif is_checkout is None:
                # 해당 url을 찾을 수 없는 경우입니다. 크롤링하지 않은 데이터로 봅니다.
                self.insert_and_increase_tennis_blog(url, title, w_date)

    def insert_and_increase_tennis_blog(self, url, title, w_date):
        self.insert_tennis_blog(url, title, w_date, 1)
        db.mysql.increase_blog_count(self.tennis_idx)
