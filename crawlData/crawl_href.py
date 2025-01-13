import requests
from lxml import etree
import time



def get_gamepage_url(url):

    gameLinks = []

    r=requests.get(url)

    root = etree.HTML(r.text)

    rows = root.xpath('//tr')

    for row in rows:

        game_links = row.xpath('.//td[@class="center num"]/a[@href]')

        for link in game_links:
            _link = link.get('href').strip()
            gameLinks.append(_link)

    return gameLinks


def crawl_round(game_Links):
    rounds = []
    for url in game_Links:
        url =  "https://www.renju.net"  +  url
        #print(url)
        time.sleep(0.3)

        r = requests.get(url)

        root = etree.HTML(r.text)

        row = root.xpath('//tr[@id="moves_row"]')

        if row:
            td_content = row[0].xpath('./td/text()')
            if td_content:
                round = td_content[0].strip()
                #print(round)
                if len(round) >=40 :
                    #print(round)
                    rounds.append(round)
    return rounds



