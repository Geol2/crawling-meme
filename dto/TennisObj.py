import string

from libs import common


class Tennis:
    tennis_idx = -1
    name = None
    naver_place_id = -1

    def __init__(self):
        self.tennis_idx = -1
        self.name = None
        self.naver_place_id = None

    def __init__(self, tennis_idx: int, name: string, naver_place_id: int):
        self.tennis_idx = tennis_idx
        self.name = name
        self.naver_place_id = naver_place_id

    def file_logger(self, message: string, e=None):
        if self.tennis_idx is -1:
            common.logger.info("테니스장 idx 정보가 잘못되었습니다.")
            return

        if self.name is None:
            common.logger.info("테니스장 이름이 존재하지 않습니다.")
        if self.naver_place_id is -1:
            common.logger.info("네이버 플레이스 id가 존재하지 않습니다.")

        common.logger.info("[" + self.idx + "] " + self.name + "(" + self.naver_place_id + ")" + message)
        if e is not None:
            common.logger.info(e)

    def print_logger(self, message: string):
        if self.tennis_idx is -1:
            print("테니스장 idx 정보가 잘못되었습니다.")
            return

        if self.name is None:
            print("테니스장 이름이 존재하지 않습니다.")
        if self.naver_place_id is -1:
            print("네이버 플레이스 id가 존재하지 않습니다.")

        print("[" + self.idx + "] " + self.name + "(" + self.naver_place_id + ")" + message)