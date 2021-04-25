from bs4 import BeautifulSoup
from requests import get
from decorators import ProjectDecorators

@final
class HabrPageParser:
    def __init__(self, url) -> None:
        self.url = url
        self.html = self.get_html(self.url)
        self.soup = BeautifulSoup(self.html, "lxml")
        self.clear_page = self.soup.find("div")

    def get_html(self, url: str) -> str:
        return get(url).text

    @ProjectDecorators.result_processing
    def get_articles_names(self) -> str:
        html_page = self.clear_page.find_all("h2")
        articles = ""
        for article in html_page:
            articles += article.text
        return articles.split("\n")

    def get_stat(self) -> str:
        items = self.clear_page.find_all("span", {"class": "post-info__meta-item"})
        output = []
        for elemnts in items:
            title_count = elemnts.get("title")
            count = elemnts.find("span", {"class": "post-info__meta-counter"}).text
            output.append((title_count, count))
        return output


def main() -> None:
    url = "https://habr.com/ru/"
    print(HabrPageParser(url).get_articles_names())


if __name__ == "__main__":
    main()
