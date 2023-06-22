from datetime import datetime
import logging
import os

logger = logging.getLogger(name='crawling')

logger.setLevel(logging.INFO)  # 경고 수준 설정
logger.propagate = False # 전파 방지

formatter = logging.Formatter('|%(asctime)s||%(name)s||%(levelname)s|\n%(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

# 파일 생성
current_time = datetime.now()
filename = datetime.strftime(current_time, "%Y-%m-%d")
file_handler = logging.FileHandler(os.getcwd() + "/logs/svc_" + filename + ".log", mode='w', encoding='utf8')
logger.addHandler(file_handler)  # 핸들러 등록
