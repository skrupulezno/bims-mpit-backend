создание env
`python -m venv env`

windows
`.\env\Scripts\activate`

linux 
`source env/bin/activate`

скачивание зависимостей
`pip install -r requirements.txt`

запуск сервера
`uvicorn app.main:app --reload`