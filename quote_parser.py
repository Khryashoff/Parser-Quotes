import json
import logging
import time
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
    )


class QuoteParser:
    """
    Класс QuoteParser предназначен для парсинга информации.
    Он автоматически переходит по страницам, собирая текст, авторов и теги.
    Собранные данные сохраняются в JSON-файл.

    Атрибуты:
        start_url (str): Стартовый URL для начала парсинга.
        current_url (str): Текущий URL для парсинга, изначально start_url.
        output_file (str): Имя файла, в который сохраняются результаты.
        quotes_data (List[Dict[str, str]]): Список словарей, содержащих
        данные о цитатах.
    """
    def __init__(self, start_url: str, output_file: str = 'quotes.json'):
        self.start_url: str = start_url
        self.current_url: str = start_url
        self.output_file: str = output_file
        self.quotes_data: List[Dict[str, str]] = []

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Отправляет GET-запрос к указанному URL и возвращает
        объект BeautifulSoup для парсинга HTML.

        Параметры:
            url (str): URL страницы, которую нужно загрузить.
        Исключения:
            Если запрос не удался (например, ошибка сети), возвращает
            None и выводит сообщение об ошибке.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f'Ошибка при подключении к {url}: {e}')
            return None

    def parse_quotes(self, soup: BeautifulSoup) -> Optional[Dict[str, str]]:
        """
        Извлекает цитаты, авторов и теги с текущей страницы и
        добавляет их в список quotes_data.

        Параметры:
            soup (BeautifulSoup): Объект BeautifulSoup с
            HTML содержимым страницы.
        Исключения:
            Если струтура блока цитаты изменена, выводит
            сообщение об ошибке.
        """
        for quote_block in soup.find_all('div', class_='quote'):
            try:
                text = quote_block.find('span', class_='text').get_text()
                author = quote_block.find('small', class_='author').get_text()
                tags = [
                    tag.get_text() for tag in quote_block.find_all(
                        'a', class_='tag'
                        )
                    ]
                self.quotes_data.append(
                    {
                        'text': text,
                        'author': author,
                        'tags': tags
                    }
                )
            except AttributeError as e:
                logging.warning(f'Ошибка при разборе блока цитаты: {e}')
                return None

    def get_next_page(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Ищет ссылку на следующую страницу, если она
        существует, и возвращает её URL.

        Параметры:
            soup (BeautifulSoup): Объект BeautifulSoup с
            HTML содержимым страницы.
        Возвращает:
            str: URL следующей страницы, если кнопка 'Next' существует.
            None: Если следующей страницы нет, возвращает None,
            чтобы остановить цикл.
        """
        next_button = soup.find('li', class_='next')
        if next_button:
            try:
                next_url = next_button.find('a')['href']
                return f'https://quotes.toscrape.com{next_url}'
            except (TypeError, KeyError):
                logging.warning(
                    'Ошибка при получении ссылки на следующую страницу.'
                    )
                return None
        return None

    def save_to_json(self) -> None:
        """
        Сохраняет собранные данные о цитатах в JSON-файл, определенный в
        атрибуте output_file.

        Исключения:
            Если происходит ошибка при записи в файл,
            выводит сообщение об ошибке.
        """
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.quotes_data, f, ensure_ascii=False, indent=4)
            logging.info(
                '------------------------------------------------------'
                )
            logging.info(
                f'Данные успешно сохранены в файл: {self.output_file}'
                )
        except IOError as e:
            logging.error(f'Ошибка при записи в файл: {e}')

    def collect(self) -> None:
        """
        Основной метод для запуска процесса парсинга и
        перехода между страницами.

        Описание:
            Циклически отправляет запросы к текущему URL, пока
            существует следующая страница.
            Для каждой страницы:
                1. Загружает HTML и передает его в BeautifulSoup.
                2. Извлекает цитаты с помощью parse_quotes().
                3. Определяет URL следующей страницы через get_next_page().
            Если соединение прервано или произошла ошибка при парсинге,
            процесс завершается.
            В конце вызывает save_to_json() для сохранения всех данных в файл.
            Используется небольшая задержка между запросами,
            чтобы избежать блокировки.
        """
        while self.current_url:
            logging.info(f'Парсинг страницы: {self.current_url}')
            soup = self.fetch_page(self.current_url)
            if soup:
                self.parse_quotes(soup)
                self.current_url = self.get_next_page(soup)
                time.sleep(0.3)
            else:
                logging.error('Парсинг остановлен из-за ошибки соединения.')
                break
        self.save_to_json()


if __name__ == '__main__':
    start = QuoteParser('https://quotes.toscrape.com/')
    start.collect()
