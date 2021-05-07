import csv
from tqdm import trange
from main import HabrPageParser

NaN = float("NaN")
LAST_PAGE_NUMBER = int(input("Последняя страница для парсинга "))
NAME_FOR_OUTPUT_FILE = str(input("Название файла для вывода "))


def main() -> None:
    for page_number in trange(1, LAST_PAGE_NUMBER + 1):
        url = f"https://habr.com/ru/all/top100/page{page_number}/"
        parsed_page = HabrPageParser(url).result_post_processing()
        with open(f"{NAME_FOR_OUTPUT_FILE}.csv", "a") as csv_file:
            writer = csv.writer(csv_file)
            for article in parsed_page.keys():
                raiting, bookmarks, viewers = NaN, NaN, NaN
                for title in parsed_page[article].keys():
                    if title == "Количество просмотров":
                        viewers = parsed_page[article][title]
                    elif title == "Закладки":
                        bookmarks = parsed_page[article][title]
                    elif title == "Рейтинг":
                        raiting = parsed_page[article][title]
                writer.writerow([article, raiting, bookmarks, viewers])


if __name__ == "__main__":
    main()
