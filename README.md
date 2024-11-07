# Parser Quotes

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/requests-2.x-blue)
![BeautifulSoup4](https://img.shields.io/badge/BeautifulSoup4-4.x-green)

Этот проект представляет собой веб-парсер, который собирает цитаты, авторов и теги с сайта [Quotes to Scrape](https://quotes.toscrape.com/), используя язык программирования Python. Собранные данные сохраняются в формате JSON.

## Что было сделано

**Основной функционал**  

Создан класс QuoteParser, который осуществляет парсинг данных с веб-страниц. Также созданы следующие функции:
* fetch_page - отправляет GET-запрос к указанному URL и возвращает объект для парсинга.
* parse_quotes - извлекает цитату, автора и теги с текущей страницы и добавляет их в список quotes_data.
* get_next_page - осуществляет поиск ссылки на следующую страницу и возвращает её URL.
* save_to_json - сохраняет собранные данные в JSON-файл.
* collect - осуществляет запуск процесса парсинга и перехода между страницами.

**Дополнительный функционал**  

Добавлена обработка ошибок: если структура сайта изменится или возникнут проблемы с соединением, парсер не завершит работу аварийно, а выведет сообщение об ошибке.  
Использовано логгирование для отслеживания процесса парсинга.

## Откуда были получены данные

Данные для парсинга были взяты из следующих HTML-элементов на каждой странице сайта Quotes to Scrape:

* Цитата: Текст цитаты извлекался из элемента 'span' с классом 'text', который находится внутри блока с классом 'quote'.
* Автор: Имя автора цитаты извлекалось из элемента 'small' с классом 'author', который также находится в блоке с классом 'quote'.
* Теги: Теги, связанные с каждой цитатой, извлекались из элементов 'a' с классом 'tag', вложенных в блок с классом 'quote'. Каждый тег представлял собой текст внутри элемента 'a'.

## Как осуществлялся сбор

Сбор данных был выполнен следующим образом:

1. Отправка GET-запросов к каждой странице сайта с использованием библиотеки requests.
2. Парсинг HTML-контента: при помощи библиотеки BeautifulSoup данные из HTML-контента каждой страницы извлекались по классам CSS, определенным для цитат, авторов и тегов.
3. Переход между страницами: после обработки каждой страницы программа находила URL следующей страницы и отправляла запрос к новому URL.
4. Сохранение данных: полученные цитаты были добавлены в список словарей и в конце записаны в JSON-файл.

Пример собранных данных:  
```json
[
    {
        "text": "Цитата",
        "author": "Автор",
        "tags": ["тег1", "тег2"]
    }
]
```

## Почему был выбран тот или иной метод/инструмент, а не другой

**Причины выбора инструментов**

* requests — выбрал для отправки HTTP-запросов. Простая и понятная в использовании библиотека, хорошо подходит для отправки обычных запросов. Также она предоставляет встроенные методы для обработки ошибок.  
Выбрал именно эту библиотеку, потому что раньше уже был опыт работы с ней. Из альтернативных вариантов отмечу httpx и urllib.  
httpx предоставляет поддержку асинхронных запросов, но в контексте текущей задачи, это был бы избыточный функционал.
urllib - стандартный инструмент, но я с ним особо не работал.

* BeautifulSoup — выбрал для парсинга HTML-кода. Популярный и мощный инструмент для извлечения данных из HTML-документов.  
Выбрал именно эту библиотеку, потому что она в топе рекомендаций, по соответствующему поисковому запросу. Оценил её возможности и принял решение, что она подойдет для поставленных задач. Из альтернативных вариантов могу отметить lxml и Scrapy. 

**Выбор методов реализации**

* Решил поделить реализацию на отдельные функции, каждая из которых выполняет свою задачу. Это соответствует принципам ООП, а также позволяет отделить разные части логики, улучшает общую стркутру кода, повышает читаемость и упрощает поддержку. 
* Добавил обработку ошибок с использованием исключений и логирование происходящих действий, для большего удобства работы с программой.  


## Локальный запуск проекта

1. Клонируйте репозиторий и перейдите в него через командную строку:
```bash
git clone git@github.com:Khryashoff/Parser-Quotes.git
```
2. Установите и активируйте виртуальное окружение для проекта:
```bash
python -m venv venv
```
```bash
# для ОС Windows
. venv/Scripts/activate
```
3. Обновите pip и установите зависимости из файла requirements.txt:
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```
4. Запустите код:
```bash
python quote_parser.py
```

## Участники разработки

Sergey Khryashchev [(Khryashoff)](https://github.com/Khryashoff)
