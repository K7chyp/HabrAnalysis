from typing import final
from bs4 import BeautifulSoup
from requests import get
import csv
from tqdm import trange
from decorators import ProjectDecorators

NaN = float("NaN")
LAST_PAGE_NUMBER = 20


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
            output.append([title_count, count])
        return output

    def stats_processing(self) -> dict:
        post_statistics: list = self.get_stat()
        dict_with_stats_and_title = {}
        position = 0
        for _, list_with_local_stats in enumerate(post_statistics, start=1):
            if list_with_local_stats[0] == "Количество просмотров":
                position += 1
                dict_with_stats_and_title[str(position)] = list_with_local_stats
            else:
                if str(position) in dict_with_stats_and_title.keys():
                    previous_list_with_stats = dict_with_stats_and_title[str(position)]
                    new_list_with_stats = (
                        list_with_local_stats + previous_list_with_stats
                    )
                    dict_with_stats_and_title[str(position)] = new_list_with_stats
        return dict_with_stats_and_title

    def make_dict_output_for_better_reading(self) -> dict:
        articles_names: list = self.get_articles_names()
        post_statistics: dict = self.stats_processing()
        page_with_statistics = {}
        for article, statistics_index in zip(articles_names, post_statistics):
            page_with_statistics[article] = post_statistics[statistics_index]
        return page_with_statistics

    def result_post_processing(self) -> dict:
        page: dict = self.make_dict_output_for_better_reading()
        output_page: dict = {}
        for article in page.keys():
            local_dict = {}
            list_with_values = page[article]
            for position in range(len(list_with_values)):
                if position % 2 == 0:
                    local_dict[list_with_values[position]] = list_with_values[
                        position + 1
                    ]
            output_page[article] = local_dict
        return output_page


def main() -> None:
    for page_number in trange(1, LAST_PAGE_NUMBER):
        url = f"https://habr.com/ru/all/top100/page{page_number}/"
        output_result = HabrPageParser(url).result_post_processing()
        with open("output.csv", "a") as csv_file:
            writer = csv.writer(csv_file)
            for article in output_result.keys():
                if "Рейтинг" in output_result[article]:
                    raiting = output_result[article]["Рейтинг"]
                else:
                    raiting = NaN
                if "Закладки" in output_result[article]:
                    bookmarks = output_result[article]["Закладки"]
                else:
                    bookmarks = NaN
                if "Количество просмотров" in output_result[article]:
                    viewers = output_result[article]["Количество просмотров"]
                else:
                    viewers = NaN
                writer.writerow([article, raiting, bookmarks, viewers])


if __name__ == "__main__":
    main()
