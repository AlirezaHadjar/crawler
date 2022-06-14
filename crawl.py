import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas

base_url = "https://www.bartarinha.ir"
def get_page_url (page):
    return f"{base_url}/بخش-اخبار-سیاسی-24?curp=1&categories=24&dateRange%5Bstart%5D=-604800&order=order_time&page={page}"
def get_data (url):
    article = Article(url)
    article.download()
    article.parse()
    text, title = article.text, article.title

    return {"url": url, "text": text, "title": title}

def crawl ():
    data = []
    page = 0

    while True:
        page = page + 1
        url = get_page_url(page)
        html = requests.get(url).text
        soup = BeautifulSoup(html, features="lxml")
        list = soup.find("ul", {"class": "main_land_list"})

        links = list.find_all("li")
        if len(links) == 0: break

        for link in tqdm(links):
            url = base_url + link.h3.a['href']
            print(url)
            try:
                data.append(get_data(url))
            except:
                print(f"Failed to load {url}")
    
    df = pandas.DataFrame(data)
    df.to_csv(f"crawled.csv")


crawl()