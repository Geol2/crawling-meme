from libs import common
from libs import db
from libs import crawling

crawl = crawling.Crawling()


mysql = db.MySQL()
conn = mysql.connect().connection
cursor = mysql.connect()

tennis_info = mysql.get_tennis_info(cursor)
tennis_info_length = len(tennis_info)

for i in range(tennis_info_length):
    try:
        tennis_idx = int(tennis_info[i][0])
        name = str(tennis_info[i][9])
        naver_id = int(tennis_info[i][16])
    except Exception as e:
        common.logger.info("[" + str(tennis_idx) + "]" + name + " 네이버 플레이스 id가 존재하지 않습니다.")
        continue

    real_url = crawl.open_url(naver_id)
    is_valid_url = crawl.is_valid_url(naver_id, real_url)
    if is_valid_url is False:
        print("[" + str(tennis_idx) + "]" + name + "(" + str(naver_id) + ")" + " 해당 테니스장 URL 주소를 찾을 수 없다는 판단을 했습니다.")
        continue

    # 리뷰 수와 실제 블로그 수가 다를 수 있어서 리뷰 수로 전체를 판단할 수 없음
    crawl.click_more_blog(tennis_idx, name, naver_id)
    all_url_list = crawl.find_blog_url()
    total_count = len(all_url_list)
    if total_count == 0:
        print("[" + str(tennis_idx) + "]" + name + "(" + str(naver_id) + ")" + " 해당 테니스장 리뷰정보가 존재하지 않습니다.")
        continue

    all_title_list = crawl.find_title()
    all_date_list = crawl.find_write_blog_date()

    if total_count != len(all_title_list):
        print("[" + str(tennis_idx) + "]" + " 블로그 제목과 제목의 경로 개수가 다릅니다. 프로그램 수정이 필요할 수 있습니다.")
        exit(0)
    for j in range(total_count):
        url = all_url_list[j]
        title = all_title_list[j]
        write_date = all_date_list[j]
        is_exist_blog = mysql.exist_blog(cursor, url)
        if not is_exist_blog:
            common.logger.info("[" + str(tennis_idx) + "]" + name + "(" + str(naver_id) + ")" + url + " 등록된 리뷰 블로그가 이미 존재합니다.")
            continue
        insert_blog_result = mysql.insert_blog(cursor, tennis_idx, title, url, write_date)
        mysql.increase_blog_count(cursor, tennis_idx)

common.logger.info("END CRAWLING")
crawl.driver.quit()

cursor.close()
conn.close()
