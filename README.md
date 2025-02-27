# БИМС МПИТ BACKEND 

## Запуск контейнера

`docker-compose build`
нужно два раза написать докеркомпос ап (не спрашивайте почему так надо))
`docker-compose up`

`docker-compose up`

## Запуск локально

linux 
`source env/bin/activate`

скачивание зависимостей
`pip install -r requirements.txt`

запуск сервера
`uvicorn app.main:app --reload`