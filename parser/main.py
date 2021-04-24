from bs4 import BeautifulSoup
from requests import get


class HabrParser:
    def __init__(self, url):
        self.url = url
        self.html = self.get_html(self.url)
        self.clear_page = self.get_page(self.html)

    def get_html(self, url: str) -> str:
        return get(url).text

    def get_page(self, html: str) -> str:
        soup = BeautifulSoup(html, 'lxml')
        return soup.find('div')

    def get_articles_names(self) -> list:
        html_page = self.clear_page.find_all('h2')
        articles = ''
        for article in html_page:
            articles += article.text
        return list(set(articles.split('\n')))

    def get_stat(self):
        items = self.clear_page.find_all('span', {'class': 'post-info__meta-item'})
        output = []
        for elemnts in items:
            title = elemnts.get('title')
            count = elemnts.find('span', {'class': 'post-info__meta-counter'}).text
            output.append((title, count))


def main() -> None:
    url = 'https://habr.com/ru/'
    HabrParser(url).get_articles_names()


if __name__ == '__main__':
    main()
