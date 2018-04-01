import requests
from bs4 import BeautifulSoup

def perform_search(keyword: str, number: int = 10, start_from: int = 0):
    return requests.get('https://www.google.ca/search',
                        params={'q': keyword.replace(' ', '+'),
                                'num': number,
                                'start': start_from}).text

def parse_results(html:str):
    soup = BeautifulSoup(html, "html.parser")
    for c in soup.contents:
        print(c)

if __name__ == '__main__':
    parse_results(perform_search('apple'))