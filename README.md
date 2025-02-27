# БИМС МПИТ BACKEND 

## Запуск проекта

# БИМС МПИТ BACKEND 

## Запуск контейнера

`docker-compose build`
`docker-compose up`

## Запуск локально

linux 
`source env/bin/activate`

скачивание зависимостей
`pip install -r requirements.txt`

запуск сервера
`uvicorn app.main:app --reload`