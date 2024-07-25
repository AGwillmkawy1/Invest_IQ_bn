from flask import Flask
from flask_cors import CORS
from mainFunc import main_app
from userSocket import socketio


def create_app():
    flask_app = Flask(__name__)
    CORS(flask_app, resources={r"/*": {"origins": "http://localhost:5173"}})
    flaskapp = main_app(flask_app)
    socketio.init_app(flaskapp)
    return flaskapp


app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)
