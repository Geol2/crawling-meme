import time

from libs import common


class ExecTime:
    # 어떤 시간이 느릴까?
    time = {
        "total_time": 0.000,
        "browser_open": 0.000,
        "valid_url": 0.000,
        "set_data": 0.000,
        "read_next": 0.000,
    }

    start = 0

    end = 0

    total_start = 0

    total_end = 0

    def start_time(self):
        self.start = time.time()

    def end_time(self):
        self.end = time.time()

    def total_start_time(self):
        self.total_start = time.time()

    def total_end_time(self):
        self.total_end = time.time()

    def total_diff(self):
        diff = self.total_end - self.total_start
        diff = round(diff, 3)
        self.time['total_time'] = self.time['total_time'] + diff

        return diff

    def diff(self, key):
        diff = self.end - self.start
        diff = round(diff, 3)
        self.time[key] = self.time[key] + diff

        return diff

    def time_print(self):
        message = '''
        --------------- Time Printer --------------
        |  total_time(sec)   :    {} sec
        |  browser_open(sec) :    {} sec
        |  set_data(sec)     :    {} sec
        |  valid_url(sec)     :    {} sec
        |  read_next(sec)    :    {} sec
        -------------------------------------------'''.format(self.time['total_time'],
                                                              self.time['browser_open'],
                                                              self.time['set_data'],
                                                              self.time['valid_url'],
                                                              self.time['read_next'])

        common.file_logger(message)
        common.print_logger(message)
