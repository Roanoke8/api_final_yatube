# Проект Yatube_api. 
Сообщество авторов, которые делятся своими рассказами с миром. 
В проекте реализован WEB интерфейс, а так же WEB API, для взаимодействия с внешними приложениями. 
API позволяет получать посты, комментарии к постам, подписки и группы авторов. 


___
### Как установить локально:

1. Склонировать проект и перейти в папку проекта:
```
git clone git@github.com:antonysan/api_final_yatube.git 
cd api_final_yatube 
```

Структура проекта:
```
.api_final_yatube 
├── README.md
├── pytest.ini
├── requirements.txt
├── setup.cfg
├── tests
│   ├── __init__.py
│   ├── __pycache__
│   ├── conftest.py
│   ├── fixtures
│   ├── test_comment.py
│   ├── test_follow.py
│   ├── test_group.py
│   ├── test_jwt.py
│   └── test_post.py
└── yatube_api
    ├── api
    ├── db.sqlite3
    ├── manage.py
    ├── posts
    ├── static
    └── yatube_api

```


2. Установить виртуальное окружение и активировать его:
```
python3 -m venv venv 
source venv/bin/activate
```

3. Установить зависимости из файла requirements.txt:
```
pip3 install -r requirements.txt
```
4. Запустить сервер
```
cd yatube_api
python3 manage.py runserver
```
___
### Примеры запросов

Получить список последних постов: 
- тип запроса: GET
```
http://127.0.0.1:8000/api/v1/posts/
```
```
[
    {
        "id": 24,
        "author": "username",
        "text": "Какой-то пост",
        "pub_date": "2022-03-25T08:55:36.534238Z",
        "image": null,
        "group": id_group
    }
]
```

Создать пост:
- Тип запроса: POST
```
http://127.0.0.1:8000/api/v1/posts/
```
- Тело запроса:
```
{
    "text": "Текст поста.",
    "group": 2
}
```

Получить список групп:
- Тип запроса: GET
```
http://127.0.0.1:8000/api/v1/groups/
```
```
[
    {
        "id": 1,
        "title": "Первая группа",
        "slug": "first-group-slug",
        "description": "first-group-slug description"
    }
]
```


