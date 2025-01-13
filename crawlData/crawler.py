import os

import requests
from lxml import etree
from crawl_href import *

filename = "./train_data/"

#url = "https://www.renju.net/game/search?year_from=1900&year_to=2025&rule=1"
url_2="https://www.renju.net/game/search?year_from=1900&year_to=2025&rule=1&p=2"
url_3="https://www.renju.net/game/search?year_from=1900&year_to=2025&rule=1&p=3"
url_ori = "https://www.renju.net/game/search?year_from=1900&year_to=2025&rule=1&p="


def risky_operation(index,url_usual,file_name):
    try:
        print("第" + str(index) + "页开始爬取")
        url = url_usual + str(index)
        game_links = get_gamepage_url(url)
        rounds = crawl_round(game_links)
        this_file_name = file_name + str(index) + ".txt"

        with open(this_file_name, "w") as f:
            f.write("\n".join(str(round) for round in rounds))

        print("第" + str(index) + "页爬取完毕")
    except Exception as e:
        print(e)
        return False
    else:
        return True


def crawl(url_usual,file_name):
    for index in range(214,5,-1):
        while not risky_operation(index,url_usual,file_name):
            print("尝试重新执行...")

            time.sleep(5)



crawl(url_ori,filename)


# game_links = get_gamepage_url(url)
# rounds = crawl_round(game_links)
#
#
#
# file_name = file_name + "1.txt"
#
# with open(file_name, "w") as f:
#     for round in rounds:
#         f.write(str(round) + "\n")