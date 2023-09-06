Yatube - соц. сеть для публикации дневников.
REST API для проекта Yatube
Реализована аутентификация по JWT-токену

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com:Alexandrsgit/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/Script/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
