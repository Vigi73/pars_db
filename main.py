import requests
from bs4 import BeautifulSoup as bs
import sqlite3


BASE_URL = 'https://tproger.ru'


def get_html(url):
    return requests.get(url).content


def get_pages(url=BASE_URL):
    soup = bs(get_html(url), 'html.parser')
    return int(soup.find('div', {'class': 'pagination'}).find_all('a')[-1]['href'].split('/')[-2])


def write_db(data):
    con = sqlite3.connect('base.sqlite3')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS list_data(title_data TEXT, img_data TEXT, url_data TEXT)''')
    cur.execute('''INSERT INTO list_data VALUES(?, ?, ?)''', [data['title'], data['img'], data['url']])
    con.commit()
    cur.close()
    con.close()
    print('.', end='')


def get_data():
    pages = get_pages()
    for page in range(1, pages + 1):
        print()
        soup = bs(get_html(f'https://tproger.ru/page/{page}/'), 'html.parser')
        try:
            res = soup.find('div', {'id': 'main_columns'}).find_all('article')
            for i, p in enumerate(res, start=1):
                data = {'title': p.a['title'],
                        'img': p.a.img['data-src'],
                        'url': p.a['href']
                        }
                write_db(data)

        except:
            for i, p in enumerate(res, start=1):
                data = {'title': p.h2.text,
                        'img': 'https://perm.axeum.ru/images/products/no%20foto6wg3y66j.jpg',
                        'url': p.a['href']
                        }
                write_db(data)


get_data()
