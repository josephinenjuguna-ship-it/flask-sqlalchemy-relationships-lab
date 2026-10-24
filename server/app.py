
#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)



@app.route('/events')
def get_events():
    events = Event.query.all()

    result = [
        {
            "id": event.id,
            "name": event.name,
            "location": event.location
        }
        for event in events
    ]

    return jsonify(result), 200



@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = Event.query.get(id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    result = [
        {
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat()
            if session.start_time else None
        }
        for session in event.sessions
    ]

    return jsonify(result), 200



@app.route('/speakers')
def get_speakers():
    speakers = Speaker.query.all()

    result = [
        {
            "id": speaker.id,
            "name": speaker.name
        }
        for speaker in speakers
    ]

    return jsonify(result), 200



@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = Speaker.query.get(id)

    if speaker is None:
        return jsonify({"error": "Speaker not found"}), 404

    result = {
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": speaker.bio.bio_text
        if speaker.bio else "No bio available"
    }

    return jsonify(result), 200



@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = Session.query.get(id)

    if session is None:
        return jsonify({"error": "Session not found"}), 404

    result = [
        {
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": speaker.bio.bio_text
            if speaker.bio else "No bio available"
        }
        for speaker in session.speakers
    ]

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)