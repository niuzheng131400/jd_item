import pymysql
import requests
from jd_crawler.parser.search import parse_jd_item
from jd_crawler.settings import MYSQL_CONF, HEADERS


def saver(item_array):
    """
    持久化爬取结果
    :param item_array:
    :return:
    """
    cursor = mysql_con.cursor()
    SQL = """INSERT INTO jd_search(sku_id, img, price, title, shop, icons)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.executemany(SQL, item_array)
    mysql_con.commit()
    cursor.close()


def donwloader(task):
    """
    请求目标网址的组件
    :param task:
    :return:
    """
    url = "https://search.jd.com/Search"
    params = {
        "keyword": task
    }
    res = requests.get(url=url, params=params, headers=HEADERS, timeout=5, proxies={
        "http": f"http:120.237.144.57"
    })
    return res


def main(task_array):
    """
    爬虫任务的调度
    :return:
    """
    for task in task_array:
        result = donwloader(task)
        item_array = parse_jd_item(result.text)
        saver(item_array)


if __name__ == "__main__":
    # 用来代替生产者
    mysql_con = pymysql.connect(**MYSQL_CONF)
    task_array = ["鼠标", "键盘", "显卡", "耳机"]
    main(task_array)