import pymysql
from . import config


class MySQL:
    def connect(self):
        try:
            connection = pymysql.connect(
                user=config.user, password=config.password, host=config.host, database=config.database,
                port=config.port, charset=config.charset,
                read_timeout=2, write_timeout=2, connect_timeout=2
            )
            return connection.cursor()
        except Exception as e:
            print("접속 중 예외가 발생했습니다.")
            exit(0)

    def close(self, cursor):
        cursor.close()


mysql = MySQL()
cursor = mysql.connect()
data_length = cursor.execute("SELECT * FROM tb_user_login")
data = cursor.fetchall()
for row in data:
    print(row)

mysql.close(cursor)
