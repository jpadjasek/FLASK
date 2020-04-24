from dataclasses import dataclass

import sqlalchemy
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


@dataclass
class User(db.Model):
    id: int
    username: str
    email: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


@app.route("/users")
def hello():
    users = User.query.all()
    print(users)
    return jsonify(users)


@app.route("/")
def add():
    user_1 = User(username='Wacek', email='wacek@gmail.com')
    db.session.add(user_1)
    try:
        db.session.commit()
        return jsonify(user_1)
    except sqlalchemy.exc.IntegrityError:
        return "Already exists"


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
