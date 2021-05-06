import csv
from tqdm import trange
from main import HabrPageParser

NaN = float("NaN")
LAST_PAGE_NUMBER = int(input('Последняя страница для парсинга '))
NAME_FOR_OUTPUT_FILE = str(input('Название файла для вывода '))


def main() -> None:
    for page_number in trange(1, LAST_PAGE_NUMBER + 1):
        url = f"https://habr.com/ru/all/top100/page{page_number}/"
        parsed_page = HabrPageParser(url).result_post_processing()
        raiting, bookmarks, viewers = NaN, NaN, NaN
        with open(f"{NAME_FOR_OUTPUT_FILE}.csv", "a") as csv_file:
            writer = csv.writer(csv_file)
            for article in parsed_page.keys():
                links_to_constants = [raiting, bookmarks, viewers]
                for index, value in enumerate("Рейтинг", "Закладки", "Количество просмотров"): 
                    if value in parsed_page[article]:
                        links_to_constants[index] = parsed_page[article][value]
                    else: 
                        links_to_constants[index] = NaN
                writer.writerow([article, raiting, bookmarks, viewers])


if __name__ == "__main__":
    main()