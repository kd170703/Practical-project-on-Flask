from flask import Flask, request

app = Flask(__name__)

# Локальное хранилище данных
events = []
event_id = 1  # Идентификатор для нового события


class Event:
    def __init__(self, event_id, date, title, text):
        self.id = event_id
        self.date = date
        self.title = title
        self.text = text

    def serialize(self):
        return f"{self.id}|{self.title}|{self.text}"


@app.route('/api/v1/calendar/', methods=['POST'])
def add_event():
    global event_id
    data = request.data.decode("utf-8").strip().split('|')

    if len(data) != 3:
        return "failed to ADD: invalid input", 400

    date, title, text = data

    if len(title) > 30:
        return "failed to ADD: title length > MAX", 400

    if len(text) > 200:
        return "failed to ADD: text length > MAX", 400

    # Проверка на уникальность события в день
    if any(event.date == date for event in events):
        return "failed to ADD: event already exists on this date", 400

    new_event = Event(event_id, date, title, text)
    events.append(new_event)
    event_id += 1
    return f"new id: {new_event.id}", 201


@app.route('/api/v1/calendar/', methods=['GET'])
def get_events():
    return '\n'.join(event.serialize() for event in events), 200


@app.route('/api/v1/calendar/<int:event_id>/', methods=['GET'])
def get_event(event_id):
    event = next((event for event in events if event.id == event_id), None)
    if event:
        return event.serialize(), 200
    return "event not found", 404


@app.route('/api/v1/calendar/<int:event_id>/', methods=['PUT'])
def update_event(event_id):
    event = next((event for event in events if event.id == event_id), None)
    if not event:
        return "event not found", 404

    data = request.data.decode("utf-8").strip().split('|')

    if len(data) != 2:
        return "failed to UPDATE: invalid input", 400

    title, text = data

    if len(title) > 30:
        return "failed to UPDATE: title length > MAX", 400

    if len(text) > 200:
        return "failed to UPDATE: text length > MAX", 400

    event.title = title
    event.text = text
    return "updated", 200


@app.route('/api/v1/calendar/<int:event_id>/', methods=['DELETE'])
def delete_event(event_id):
    global events
    events = [event for event in events if event.id != event_id]
    return "deleted", 200


if __name__ == '__main__':
    app.run(debug=True)
