import time

from libs import common


class ExecTime:
    # 어떤 시간이 느릴까?
    time = {
        "total_time": 0.000,
        "browser_open": 0.000,
        "is_eof": 0.000,
        "valid_url": 0.000,
        "set_data": 0.000,
        "find_blog_url": 0.000,
        "find_title": 0.000,
        "find_write_date": 0.000,
        "exist_blog": 0.000,
        "read_next": 0.000,
        "etc": 0.000
    }

    # 개수를 찾아보자
    count = {
        "total_count": 0,
        "success_count": 0,
        "failed_count": 0,
        "blog_count": 0,
        "click_page_count": 0
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

    def diff(self, time_key):
        diff = self.end - self.start
        self.time[time_key] = self.time[time_key] + diff

        return diff

    def add_count(self, count_key):
        self.count[count_key] = self.count[count_key] + 1

    def etc(self):
        self.time['etc'] = self.time['total_time'] - (
                self.time['browser_open']
                + self.time['is_eof']
                + self.time['set_data']
                + self.time['find_blog_url']
                + self.time['find_title']
                + self.time['find_write_date']
                + self.time['valid_url']
                + self.time['exist_blog']
                + self.time['read_next']
        )

    def time_print(self):
        message = '''
            탐색된 테니스장(레슨) 개수 : {} 개
            ┌───────────────────────────────────────────────────────┐
            ├───────────────── ▶ Time Printer ◀ ────────────────────┤
            ├───────────────────────────────────────────────────────┤
            │  browser_open (sec)         :    {} sec             
            │  is_eof (sec)               :    {} sec             
            │  set_data (sec)             :    {} sec             
            │    ├ find_blog_url (sec)    :    {} sec             
            │    ├ find_title (sec)       :    {} sec             
            │    └ find_write_date(sec)   :    {} sec             
            │  valid_url (sec)            :    {} sec             
            │  exist_blog (sec)           :    {} sec             
            │  read_next (sec)            :    {} sec             
            ├─────────────────── ▶ Result ◀ ────────────────────────
            │  total_time (sec)           :    {} sec
            │  etc (sec)                  :    {} sec
            └───────────────────────────────────────────────────────
            URL 탐색 성공 개수 : {} 개
            URL 탐색 실패 개수 : {} 개
            카운팅된 블로그 수 : {} 개
            블로그 더보기 클릭된 수 : {} 번'''.format(
                round(self.count['total_count'], 3),
                round(self.time['total_time'], 3),
                round(self.time['browser_open'], 3),
                round(self.time['is_eof'], 3),
                round(self.time['set_data'], 3),
                round(self.time['find_blog_url'], 3),
                round(self.time['find_title'], 3),
                round(self.time['find_write_date'], 3),
                round(self.time['valid_url'], 3),
                round(self.time['exist_blog'], 3),
                round(self.time['read_next'], 3),
                round(self.time['etc'], 3),
                round(self.count['success_count'], 3),
                round(self.count['failed_count'], 3),
                round(self.count['blog_count'], 3),
                round(self.count['click_page_count'], 3))

        common.file_logger(message)
        common.print_logger(message)
