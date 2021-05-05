import csv
from tqdm import trange
from main import HabrPageParser

NaN = float("NaN")
LAST_PAGE_NUMBER = int(input('Последняя страница для парсинга '))
NAME_FOR_OUTPUT_FILE = str(input('Название файла для вывода '))


def main() -> None:
    for page_number in trange(1, LAST_PAGE_NUMBER + 1):
        url = f"https://habr.com/ru/all/top100/page{page_number}/"
        output_result = HabrPageParser(url).result_post_processing()
        with open(f"{NAME_FOR_OUTPUT_FILE}.csv", "a") as csv_file:
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
