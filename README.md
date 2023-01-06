# Yamdb:tv::notebook::musical_score:

## Ресурс с отзывами о произведениях кино, книгах и пр.:memo:

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Python 3.7
Django 3.2

### Как запустить проект::electric_plug:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Gatitka/api_yamdb.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### URLS:vertical_traffic_light:
- **"v1/titles":**
"http://127.0.0.1:8000/api/v1/titles/"
Список произведений, к которым пишут отзывы.

- **"v1/categories":**
"http://127.0.0.1:8000/api/v1/categories/",
список категорий (типов) произведений.

- **"v1/genres":**
"http://127.0.0.1:8000/api/v1/genres/",
список жанров

- **"'v1/titles/(<title_id>)/reviews/:**
"http://127.0.0.1:8000/api/v1/titles/(<title_id>)/reviews/"
просмотр, создание, редакция отзывов к произведениям

- **"'v1/titles/(<title_id>)/reviews/(<reviews_id>)/comments/:** "http://127.0.0.1:8000/api/v1/titles/(<title_id>)/reviews/(<review_id>)/comments/"
просмотр, создание, редакция комментов к отзывам


### Plugins:heavy_check_mark:

| Plugin | README |
| ------ | ------ |
| GitHub | [https://github.com/Gatitka/api_yamdb/blob/master/README.md]|


### Авторы:dancers:
Александр Лопата

Наталья Кириллова
