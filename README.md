# Calendar Service

## Описание
Сервис для работы с Календарем, предоставляющий API для добавления, чтения, обновления и удаления событий.

## Запуск приложения

1. Создайте виртуальное окружение, если ещё не создано:
    
python -m venv venv
   
2. Активируйте виртуальное окружение:

.\venv\Scripts\activate

3. Установите зависимости:

pip install -r requirements.txt

4. Запустите приложение:

flask --app ./acme/server.py run

API
Добавление нового события:

Bash
curl http://127.0.0.1:5000/api/v1/calendar/ -X POST -d "2023-10-01|Title|Text"
Получение списка всех событий:

Bash
curl http://127.0.0.1:5000/api/v1/calendar/
Получение события по идентификатору:

Ruby
curl http://127.0.0.1:5000/api/v1/calendar/1/
Обновление события по идентификатору:

Ruby
curl http://127.0.0.1:5000/api/v1/calendar/1/ -X PUT -d "New Title|New Text"
Удаление события по идентификатору:

Ruby
curl http://127.0.0.1:5000/api/v1/calendar/1/ -X DELETE