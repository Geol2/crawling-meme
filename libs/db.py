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

    def get_tennis_info(self, cursor):
        query = "SELECT * FROM tb_tennis_info WHERE run_state = 1"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def get_lesson_info(self, cursor):
        query = "SELECT * FROM tb_lesson_list WHERE run_state = 1 ORDER BY seq ASC"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def insert_blog(self, cursor, tennis_idx: int, data_dict: dict):
        query = '''INSERT INTO `tb_blog_info` (`app_key`, `blog_type`, `tennis_idx`, `blog_title`, `blog_url`, `blog_wdate`, `run_state`, `create_date`)
                    VALUES ('ED010', %s, %s, %s, %s, %s, 1, now())'''
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

    def is_exist_lesson(self, cursor, url: string):
        query = '''SELECT blog_url FROM `tb_blog_info` WHERE blog_url = %s AND blog_type=2 AND is_checkout = 0 '''
        where = (str(url))
        cursor.execute(query, where)
        data = cursor.fetchall()
        if len(data) > 0:
            return True
        return False

    def increase_blog_count(self, cursor, tennis_idx: int):
        query = '''UPDATE tb_tennis_info SET blog_cnt = blog_cnt + 1 WHERE seq= %s '''
        where = tennis_idx
        result = cursor.execute(query, where)
        print(query)
        return result

    def increase_lesson_count(self, cursor, tennis_idx: int):
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

    def set_blog_info(self, cursor, blog_url: string):
        query = '''UPDATE tb_blog_info SET is_checkout = 1 WHERE blog_url = %s '''
        where = blog_url
        result = cursor.execute(query, where)
        print(query)
        return result

    def set_lesson_info(self, seq: int):
        query = '''UPDATE tb_tennis_info SET is_checkout = 1 WHERE seq = %s '''
        where = seq
        result = cursor.execute(query, where)
        print(query)
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
        if len(result) > 0:
            return True
        return False

    def unset_lesson_info(self, seq, int):
        query = '''UPDATE tb_blog_info SET is_checkout = 0 WHERE tennis_idx = %s WHERE blog_type = 2'''
        where = seq
        result = cursor.execute(query, where)
        print(query)
        if len(result) > 0:
            return True
        return False

    def unset_tennis_info(self, seq: int):
        query = '''UPDATE tb_tennis_info SET is_checkout = 0 WHERE seq = %s '''
        where = seq
        result = cursor.execute(query, seq)
        print(query)
        if len(result) > 0:
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
