import string

import pymysql
from . import config


class MySQL:

    @staticmethod
    def connect():
        try:
            connection = pymysql.connect(
                user=config.user, password=config.password, host=config.host, database=config.database,
                port=config.port, charset=config.charset,
                read_timeout=2, write_timeout=2, connect_timeout=2
            )
            cursor = connection.cursor()
            return cursor
        except Exception as e:
            print("접속 중 예외가 발생했습니다.")
            exit(0)

    def get_tennis_info(self, cursor):
        query = "SELECT * FROM tb_tennis_info"
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            print(row)

        return data

    def insert_blog(self, cursor, tennis_idx: int, title: string, url: string):
        query = """INSERT INTO `tb_blog_info` (`app_key`, `blog_type`, `tennis_idx`, `blog_title`, `blog_url`, `blog_wdate`, `run_state`, `create_date`)
                    VALUES ('ED010', 1, %s, %s, %s, now(), 1, now())"""
        result = cursor.execute(query, (tennis_idx, title, url))
        self.connect().connection.commit()

        print(result)
        return result
