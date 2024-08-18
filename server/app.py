from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Thoughts.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import routes after app and db are defined
import routes

with app.app_context():
  db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
