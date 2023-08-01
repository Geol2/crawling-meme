from libs import db
from libs.db import cursor


class BlogModel:

    def getAll(self):
        query = "SELECT * FROM tb_tennis_info WHERE run_state = 1 AND tennis_naver_id IS NOT NULL ORDER BY seq"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    #def one(self, blog_idx: int):


    #def is_checkout(self, blog_idx: int):

    #def getListTennisIdx(self, tennis_idx: int):

