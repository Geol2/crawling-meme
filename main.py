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
        print("[" + str(tennis_idx) + "]" + name + " 네이버 플레이스 id가 존재하지 않습니다.")
        continue

    crawl.open_url(naver_id)

    # 리뷰 수와 실제 블로그 수가 다를 수 있더라..
    all_url_list = crawl.find_blog_url()
    all_title_list = crawl.find_title()
    total_count = len(all_url_list)
    if total_count == 0:
        print("[" + str(tennis_idx) + "]" + name + "(" + str(naver_id) + ")" + " 해당 테니스장 URL정보가 올바르지 않아 가져올 수 없습니다.")
    # clickNumber = crawl.get_click_number(len(all_url_list))
    crawl.click_more_blog()
    if total_count != len(all_title_list):
        print("블로그 제목과 제목의 경로 개수가 다릅니다.")
        exit();
    for j in range(total_count - 1):
        url = all_url_list[j]
        title = all_title_list[j]
        mysql.insert_blog(cursor, tennis_idx, title, url)

print("END CRAWLING")
crawl.driver.quit()

cursor.close()
conn.close()
