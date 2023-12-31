import string

import pymysql

from service.tennis.tennisFactory import Tennis
from . import config
from libs import common


class MySQL:

    @staticmethod
    def connect():
        try:
            connection = pymysql.connect(
                user=config.user, password=config.password, host=config.host, database=config.database,
                port=config.port, charset=config.charset,
                read_timeout=2, write_timeout=2, connect_timeout=2, autocommit=True,
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = connection.cursor()
            return cursor
        except Exception as e:
            print(e)
            common.logger.info(e)
            exit(0)

    def get_lesson_info(self):
        query = "SELECT * FROM tb_lesson_list WHERE run_state = 1 AND tennis_naver_id IS NOT NULL ORDER BY seq"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def insert_blog(self, cursor, tennis_idx: int, data_dict: dict):
        query = '''INSERT INTO `tb_blog_info` (`app_key`, `blog_type`, `tennis_idx`, `blog_title`, `blog_url`, `blog_wdate`, `run_state`, `create_date`, `is_checkout`)
                    VALUES ('ED010', %s, %s, %s, %s, %s, 1, now(), 1)'''
        data = (data_dict.get("blog_type"), tennis_idx, data_dict.get("title"), data_dict.get("url"), data_dict.get("w_date"))
        result = cursor.execute(query, data)
        print(query)
        common.file_logger(query)

        return result

    def is_exist_blog(self, cursor, url: string):
        query = '''SELECT blog_url FROM `tb_blog_info` WHERE blog_url = %s AND blog_type=1'''
        where = (str(url))
        cursor.execute(query, where)
        data = cursor.fetchall()
        if len(data) > 0:
            return True
        return False

    def is_checkout_blog(self, blog_url: string):
        query = ''' SELECT is_checkout, blog_url FROM tb_blog_info WHERE blog_url = %s AND blog_type = 1 '''
        where = blog_url
        result = cursor.execute(query, where)
        data = cursor.fetchone()
        if data is None:
            is_checkout = None
        else:
            is_checkout = data['is_checkout']

        return is_checkout

    def is_checkout_lesson(self, blog_url: string):
        query = ''' SELECT is_checkout FROM tb_blog_info WHERE blog_url = %s AND blog_type = 2 '''
        where = blog_url
        result = cursor.execute(query, where)
        data = cursor.fetchone()
        print(query)
        if data is None:
            is_checkout = None
        else:
            is_checkout = data['is_checkout']

        return is_checkout
    
    def is_exist_lesson(self, url: string):
        query = '''SELECT blog_url FROM `tb_blog_info` WHERE blog_url = %s AND blog_type=2 '''
        where = url
        cursor.execute(query, where)
        data = cursor.fetchall()
        if len(data) > 0:
            return True
        return False

    def is_crawling_lesson(self, url: string):
        query = '''SELECT blog_url FROM `tb_blog_info` WHERE blog_url = %s AND blog_type=2 '''
        where = url
        cursor.execute(query, where)
        data = cursor.fetchall()
        if len(data) > 0:
            return True
        return False

    def increase_blog_count(self, tennis_idx: int):
        query = '''UPDATE tb_tennis_info SET blog_cnt = blog_cnt + 1 WHERE seq= %s '''
        where = tennis_idx
        result = cursor.execute(query, where)
        print(query)
        return result

    def increase_lesson_count(self, tennis_idx: int):
        query = '''UPDATE tb_lesson_list SET blog_cnt = blog_cnt + 1 WHERE seq= %s '''
        where = tennis_idx
        result = cursor.execute(query, where)
        print(query)
        return result

    def set_blog_end_flag(self):
        query = '''UPDATE tb_blog_info SET end_flag = 1 '''
        result = cursor.execute(query)
        print(query)
        return result

    def get_blog_info(self, tennis: Tennis, blog_type: int):
        query = '''SELECT * FROM tb_blog_info WHERE tennis_idx = %s AND blog_type = %s '''
        where = (tennis.tennis_idx, blog_type)
        result = cursor.execute(query, where)
        print(query)
        return result

    def set_blog_info(self, tennis_idx: int):
        query = '''UPDATE tb_blog_info SET is_checkout = 1 WHERE tennis_idx = %s AND blog_type = 1 '''
        where = tennis_idx
        result = cursor.execute(query, where)
        print(query)
        return result

    def set_blog_list(self, tennis_idx: int):
        query = '''UPDATE tb_blog_info SET is_checkout = 1 WHERE tennis_idx = %s AND blog_type = 1 '''
        where = tennis_idx
        result = cursor.execute(query, where)
        print(query)
        return result

    def unset_blog_list(self, tennis_idx: int):
        query = '''UPDATE tb_blog_info SET is_checkout = 0 WHERE tennis_idx = %s AND blog_type = 1 '''
        where = tennis_idx
        result = cursor.execute(query, where)
        print(query)
        return result

    def set_lesson_info(self, seq: int):
        query = '''UPDATE tb_blog_info SET is_checkout = 1 WHERE tennis_idx = %s AND blog_type = 2 '''
        where = seq
        result = cursor.execute(query, where)
        print(query)
        return result

    def set_lesson_info_by_url(self, url: string):
        query = '''UPDATE tb_blog_info SET is_checkout = 1 WHERE blog_url = %s AND blog_type = 2 '''
        where = url
        result = cursor.execute(query, where)
        print(query)
        common.file_logger(query)

        return result

    def set_lesson_list(self, seq: int):
        query = '''UPDATE tb_lesson_list set is_checkout = 1 WHERE seq = %s '''
        where = seq
        result = cursor.execute(query, where)
        print(query)
        return result

    def unset_lesson_list(self, seq: int):
        query = '''UPDATE tb_lesson_list SET is_checkout = 0 WHERE seq = %s '''
        where = seq
        result = cursor.execute(query, where)
        print(query)
        if result > 0:
            return True
        return False

    def unset_lesson_info(self, seq: int):
        query = '''UPDATE tb_blog_info SET is_checkout = 0 WHERE tennis_idx = %s AND blog_type = 2'''
        where = seq
        result = cursor.execute(query, where)
        print(query)
        if result > 0:
            return True
        return False

    def unset_lesson_info_by_tennis_idx(self, tennis_idx: int):
        query = '''UPDATE tb_blog_info SET is_checkout = 0 WHERE tennis_idx = %s AND blog_type = 2'''
        where = tennis_idx
        result = cursor.execute(query, where)
        print(query)
        if result > 0:
            return True
        return False

    def unset_lesson_list_by_idx(self, idx: int):
        query = '''UPDATE tb_lesson_list SET is_checkout = 0 WHERE idx = %s '''
        where = idx
        result = cursor.execute(query, where)
        print(query)
        if result > 0:
            return True
        return False

    def unset_tennis_info(self, seq: int):
        query = '''UPDATE tb_tennis_info SET is_checkout = 0 WHERE seq = %s '''
        where = seq
        result = cursor.execute(query, seq)
        print(query)
        if result > 0:
            return True
        return False

    def search_lesson_list(self, seq: int):
        query = '''SELECT is_checkout FROM tb_lesson_list WHERE seq = %s AND (is_checkout = 0 or is_checkout IS NULL) '''
        where = seq
        result = cursor.execute(query, seq)
        print(query)
        if result > 0:
            # 계속 진행
            return True

        # 진행하지 않음
        return False

mysql = MySQL()
conn = mysql.connect().connection
cursor = mysql.connect()
