from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass4now@localhost/water-tracker'
db = SQLAlchemy(app)
CORS(app)
cors = CORS(app, resources={r"/api": {"origins": "http://localhost:3000"}})


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, description=None):
        self.description = description


    def __repr__(self):
        return f"Event('{self.description}', '{self.created_at}')"
    

def format_event(event):
    return {
        'id': event.id,
        'description': event.description,
        'created_at': event.created_at
    }

@app.route('/')
def hello_world():
    return 'Hello World!'

# create an event in the database
@app.route('/events', methods = ['POST'])
def create_event():
    description = request.json['description']
    event = Event(description=description)
    db.session.add(event)
    db.session.commit()
    return format_event(event)

# get all events from the database list of formatted events
@app.route('/events', methods = ['GET'])
def get_events():
    events = Event.query.order_by(Event.id.asc()).all() 
    return {'events': [format_event(event) for event in events]}

# get a single event from the database
@app.route('/events/<id>', methods = ['GET'])
def get_event(id):
    event = Event.query.filter_by(id=id).one()
    formatted = format_event(event)
    return {"event": formatted}

# delete an event from the database
@app.route('/events/<id>', methods = ['DELETE'])
def delete_event(id):
    event = Event.query.filter_by(id=id).one()
    db.session.delete(event)
    db.session.commit()
    return {"message": "Event deleted"}

# update an event in the database
@app.route('/events/<id>', methods = ['PUT'])
def update_event(id):
    event = Event.query.filter_by(id=id).one()
    event.description = request.json['description']
    event.created_at = datetime.utcnow()
    db.session.commit()
    return {"message": "Event updated"}

if __name__ == '__main__':
    app.run()
