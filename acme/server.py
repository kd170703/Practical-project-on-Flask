from flask import Flask, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)

# Локальное хранилище данных
events = {}

# Максимальные длины полей
MAX_TITLE_LENGTH = 30
MAX_TEXT_LENGTH = 200

@app.route('/api/v1/calendar/', methods=['POST'])
def add_event():
    try:
        # Получаем данные из запроса
        data = request.get_data(as_text=True)
        print(f"Received data: {data}")
        
        # Разделяем данные по символу '|'
        date_str, title, text = data.split('|')
        
        # Проверяем формат даты
        event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Проверяем длину заголовка и текста
        if len(title) > MAX_TITLE_LENGTH:
            return "Title length exceeds 30 characters", 400
        if len(text) > MAX_TEXT_LENGTH:
            return "Text length exceeds 200 characters", 400
        
        # Проверяем, что на эту дату еще нет события
        for event in events.values():
            if event['date'] == date_str:
                return "Event already exists for this date", 400

        # Добавляем событие в хранилище
        new_id = max(events.keys()) + 1 if events else 1
        events[new_id] = {"date": date_str, "title": title, "text": text}
        
        return f"new id: {new_id}", 201
    except ValueError:
        return "Invalid data format. Use: 'YYYY-MM-DD|title|text'", 400


@app.route('/api/v1/calendar/', methods=['GET'])
def get_events():
    return jsonify([{"id": event_id, "date": event["date"], "title": event["title"], "text": event["text"]} for event_id, event in events.items()])


@app.route('/api/v1/calendar/<int:event_id>/', methods=['GET'])
def get_event(event_id):
    event = events.get(event_id)
    if event is None:
        abort(404)
    return jsonify({"id": event_id, "date": event["date"], "title": event["title"], "text": event["text"]})


@app.route('/api/v1/calendar/<int:event_id>/', methods=['PUT'])
def update_event(event_id):
    event = events.get(event_id)
    if event is None:
        abort(404)
    
    try:
        # Получаем данные из запроса
        data = request.get_data(as_text=True)
        print(f"Received data for update: {data}")
        
        # Разделяем данные по символу '|'
        date_str, title, text = data.split('|')
        
        # Проверяем формат даты
        event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Проверяем длину заголовка и текста
        if len(title) > MAX_TITLE_LENGTH:
            return "Title length exceeds 30 characters", 400
        if len(text) > MAX_TEXT_LENGTH:
            return "Text length exceeds 200 characters", 400
        
        # Обновляем событие в хранилище
        event['date'] = date_str
        event['title'] = title
        event['text'] = text
        
        return "updated", 200
    except ValueError:
        return "Invalid data format. Use: 'YYYY-MM-DD|title|text'", 400


@app.route('/api/v1/calendar/<int:event_id>/', methods=['DELETE'])
def delete_event(event_id):
    if event_id in events:
        del events[event_id]
        return "deleted", 200
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)