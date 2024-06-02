<h1 align="center">
Life is Game
</h1>
<p align="center">
Бот для дисциплинирования и мотивации
</p>

## Установка и запуск
Сначала создадим виртуальное окружение и установим зависимости
```shell
python3 -m venv env
source env/bin/activate
python -m pip install pipenv
pipenv install
```
После нужно провести миграцию моделей для создания базы данных
```shell
python manage.py migrate
```
Теперь нужно заполнить [example.env](example.env) в корне, после переименовать в .env
<br />

Получить API_TOKEN можно [здесь](https://t.me/BotFather)

Получить OPENAI_TOKEN можно [здесь](https://proxyapi.ru)

После можно запустить бота
```shell
python manage.py start_bot
```