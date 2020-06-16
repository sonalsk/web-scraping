import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

def get_data(pageNo):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    r = requests.get('https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_'+str(pageNo)+'?ie=UTF8&pg='+str(pageNo), headers=headers)
    content = r.content
    code = BeautifulSoup(content, features="lxml")

    all_books = []
    for book in code.findAll('div', attrs={'class':'a-section a-spacing-none aok-relative'}):

        name = book.find('span', attrs={'class':'zg-text-center-align'})
        n = name.find_all('img', alt=True)
        author = book.find('a', attrs={'class':'a-size-small a-link-child'})
        price = book.find('span', attrs={'class':'p13n-sc-price'})

        each_book = add_attribute(name, author, price)
        all_books.append(each_book)

    return all_books

def add_attribute(name, author, price):
    each_book = []
    n = name.find_all('img', alt=True)
    if name is not None:
        each_book.append(n[0]['alt'])
    else:
        each_book.append("unknown")

    if author is not None:
        each_book.append(author.text)
    else:
        each_book.append('unknown')

    if price is not None:
        s = str(price.text)[2:].replace(',', '')
        s = s.split('.')[0]
        each_book.append(int(s))
    else:
        each_book.append(0)

    return each_book

name_auth_price = []
no_pages = 2
for i in range(1, no_pages+1):
    name_auth_price.append(get_data(i))

flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(name_auth_price),columns=['Book Name','Author','Price'])
data = df.sort_values(["Price"], axis=0, ascending=False)

data.to_csv('amazon_products.csv', index=False, encoding='utf-8')
