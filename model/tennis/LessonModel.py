from libs.db import cursor


class LessonModel:

    @staticmethod
    def getAll():
        query = "SELECT * FROM tb_lesson_list WHERE run_state = 1 AND tennis_naver_id IS NOT NULL ORDER BY seq"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    # def one(self, lesson_idx: int):

    # def is_checkout(self, lesson_idx: int):

    # def getListTennisIdx(self, tennis_idx: int):
