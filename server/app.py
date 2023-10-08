from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

class TestApp:
    '''Flask application in app.py'''

    with app.app_context():
        m = Message.query.filter(
            Message.body == "Hello 👋"
            ).filter(Message.username == "Liza")

        for message in m:
            db.session.delete(message)

        db.session.commit()

    def test_has_correct_columns(self):
        '''has columns for message body, username, and creation time.'''
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")

            db.session.add(hello_from_liza)
            db.session.commit()

            assert (hello_from_liza.body == "Hello 👋")
            assert (hello_from_liza.username == "Liza")
            assert (type(hello_from_liza.created_at) == datetime)

            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        '''returns a list of JSON objects for all messages in the database.'''
        with app.app_context():
            response = app.test_client().get('/messages')
            records = Message.query.all()

            for message in response.json:
                assert (message['id'] in [record.id for record in records])
                assert (message['body'] in [record.body for record in records])

if __name__ == '__main__':
    app.run(port=5555)
