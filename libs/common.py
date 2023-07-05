import string
import time
from datetime import datetime
from pathlib import Path

import logging
import os

from libs import config


def get_project_root() -> Path:
    return Path(__file__).parent.parent


logger = logging.getLogger(name='crawling')

logger.setLevel(logging.INFO)  # 경고 수준 설정
logger.propagate = False  # 전파 방지

formatter = logging.Formatter('|%(asctime)s||%(name)s||%(levelname)s|\n%(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

# 파일 생성
current_time = datetime.now()
filename = datetime.strftime(current_time, "%Y%m%d")
ROOT_DIR = os.path.abspath(os.curdir)
if config.env == "auto":
    ROOT_DIR = "/www/crawling-meme"
    file_handler = logging.FileHandler(ROOT_DIR + "/logs/cronlog/cronlog-" + filename + ".log", mode='a+',
                                       encoding='utf8')
else:
    file_handler = logging.FileHandler(ROOT_DIR + "/logs/svclog/svc-" + filename + ".log", mode='a+', encoding='utf8')

logger.addHandler(file_handler)  # 핸들러 등록


def file_logger(self, message: string):
    if self.tennis_idx == -1:
        logger.info("테니스장 idx 정보가 잘못되었습니다.")
        return

    if self.name is None:
        logger.info("테니스장 이름이 존재하지 않습니다.")
    if self.naver_place_id == -1:
        logger.info("네이버 플레이스 id가 존재하지 않습니다.")

    logger.info(time.strftime('[%Y.%m.%d][%H:%M:%S]') + "[" + str(self.tennis_idx) + "] " + str(self.name) + "(" +
                str(self.naver_place_id) + ")" + message)