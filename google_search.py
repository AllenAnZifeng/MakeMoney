import random
from functools import reduce

import requests
from bs4 import BeautifulSoup
import re

REGEX_MATCH_TAGS = re.compile('<.*?>')


def choose_user_agent():
    return random.choice([
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ (KHTML, like Gecko) Element Browser 5.0',
        'IBM WebExplorer /v0.94',
        'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko)Version/6.0 Mobile/10A5355d Safari/8536.25',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)'])


def choose_google_domain():
    return random.choice(
        ["google.com.af", "google.al", "google.dz", "google.as", "google.ad",
         "google.it.ao", "google.com.ai", "google.com.ag", "google.com.ar",
         "google.am", "google.ac", "google.com.au", "google.at", "google.az",
         "google.bs", "google.com.bh", "google.com.bd", "google.com.by",
         "google.be", "google.com.bz", "google.bj", "google.bt",
         "google.com.bo", "google.ba", "google.co.bw", "google.com.br",
         "google.vg", "google.com.bn", "google.bg", "google.bf", "google.bi",
         "google.com.kh", "google.cm", "google.ca", "google.cv", "google.cat",
         "google.cf", "google.td", "google.cl", "google.com.co", "google.cd",
         "google.cg", "google.co.ck", "google.ci", "google.hr", "google.com.cu",
         "google.com.cy", "google.cz", "google.dk", "google.dj", "google.dm",
         "google.com.do", "google.com.ec", "google.com.eg", "google.com.sv",
         "google.ee", "google.com.et", "google.com.fj", "google.fi",
         "google.fr", "google.ga", "google.gm", "google.ge", "google.de",
         "google.com.gh", "google.com.gi", "google.gr", "google.gl",
         "google.gp", "google.com.gt", "google.gg", "google.gy", "google.ht",
         "google.hn", "google.com.hk", "google.hu", "google.is", "google.co.in",
         "google.co.id", "google.iq", "google.ie", "google.co.im",
         "google.co.il", "google.it", "google.ci", "google.com.jm",
         "google.co.jp", "google.co.je", "google.jo", "google.kz",
         "google.co.ke", "google.ki", "google.com.kw",
         "google.la", "google.lv", "google.com.lb", "google.co.ls",
         "google.com.ly", "google.li", "google.lt", "google.lu", "google.mk",
         "google.mg", "google.mw", "google.com.my", "google.mv", "google.ml",
         "google.com.mt", "google.mu", "google.com.mx", "google.fm",
         "google.md", "google.mn", "google.me", "google.ms", "google.co.ma",
         "google.co.mz", "google.com.na", "google.nr", "google.com.np",
         "google.nl", "google.co.nz", "google.com.ni", "google.ne",
         "google.com.ng", "google.nu", "google.com.nf", "google.no",
         "google.com.om", "google.com.pk", "google.ps", "google.com.pa",
         "google.com.pg", "google.com.py", "google.com.pe", "google.com.ph",
         "google.pn", "google.pl", "google.pt", "google.com.pr",
         "google.com.qa", "google.ro", "google.ru", "google.rw", "google.sh",
         "google.ws", "google.sm", "google.st", "google.com.sa", "google.sn",
         "google.rs", "google.sc", "google.com.sl", "google.com.sg",
         "google.sk", "google.si", "google.com.sb", "google.so", "google.co.za",
         "google.co.kr", "google.es", "google.lk", "google.com.vc", "google.sr",
         "google.se", "google.ch", "google.com.tw", "google.com.tj",
         "google.co.tz", "google.co.th", "google.tl", "google.tg", "google.tk",
         "google.to", "google.tt", "google.tn", "google.com.tr", "google.tm",
         "google.co.ug", "google.com.ua", "google.ae", "google.co.uk",
         "google.com", "google.com.uy", "google.co.uz", "google.vu",
         "google.co.ve", "google.com.vn", "google.co.vi", "google.co.zm",
         "google.co.zw"])


def get_search_html(keyword: str, number: int = 10, start_from: int = 0):
    headers = {'User-Agent': choose_user_agent()}
    return requests.get('https://' + choose_google_domain() + '/search',
                        headers=headers,
                        params={'q': keyword.replace(' ', '+'),
                                'num': number,
                                'start': start_from}).text


class Search_Result():
    title = ''
    link = ''
    desc = ''

    def __init__(self, title, link, desc):
        self.title = title
        self.link = link
        self.desc = desc


def parse_results(html: str):
    soup = BeautifulSoup(html, "html.parser")
    results_div = soup.find_all('div', 'g')
    results = []
    for r in results_div:
        # Title and link
        h3 = r.find('h3', 'r')
        if h3 is not None:
            a = h3.a
            title = reduce(lambda a, b: str(a) + str(b), a.contents)
            title = re.sub(REGEX_MATCH_TAGS, '', title)
            link = 'https://' + choose_google_domain() + str(a['href'])

            # Description
            span = r.find('span', 'st')
            if span is None:
                desc = ''
            else:
                desc = reduce(lambda a, b: str(a) + str(b), span.contents)
                desc = re.sub(REGEX_MATCH_TAGS, '', desc).replace('\n', '')

            results.append(Search_Result(title, link, desc))
    return results


def search(keyword: str, number: int = 50):
    results = []
    while number > 0:
        r = parse_results(
            get_search_html(keyword, number + 5 if number + 5 <= 100 else 100,
                            len(results)))
        number -= len(r)
        results.extend(r)
    return results


if __name__ == '__main__':
    results = search('apple', 50)
    for r in results:
        print('===============================================================')
        print(r.title, r.link)
        print(r.desc)

    print('\n' + str(len(results)) + ' results returned.')
