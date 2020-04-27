from dataclasses import dataclass

import sqlalchemy
from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


@dataclass
class Skill(db.Model):
    id: int
    name: str
    user_id: int

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=False)


@dataclass
class User(db.Model):
    id: int
    first_name: str
    last_name: str
    cv_url: str
    skills: Skill

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=True, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    cv_url = db.Column(db.String(120), unique=True, nullable=True)
    skills = db.relationship('Skill', backref='user', cascade='all', lazy=True)


@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users)


@app.route('/user', methods=['POST'])
def add_user():
    content = request.get_json()
    user = User(first_name=content['first_name'], last_name=content['last_name'])
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify(user)
    except sqlalchemy.exc.IntegrityError as e:
        print(e)
        return get_error_response(400, message='User already exists')


@app.route('/user/<user_id>/skill', methods=['POST'])
def delete_user_by_id(user_id):
    try:
        user = get_user_by_id(user_id)

    except UserNotFoundException:
        return get_error_response(400, message='User not found')

    content = request.get_json()
    skill = Skill(name=content['name'], user_id=user.id)
    db.session.add(skill)

    db.session.commit()
    return jsonify(skill)


@app.route('/user/<user_id>', methods=['DELETE'])
def add_skill_to_user(user_id):
    try:
        user = get_user_by_id(user_id)

    except UserNotFoundException:
        return Response(status=204, mimetype='application/json')
    db.session.delete(user)
    db.session.commit()

    return Response(status=204, mimetype='application/json')


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        raise UserNotFoundException
    return user


def get_error_response(status_code, message):
    body = f"{{nmessage: {message}}}"
    return Response(body, status=status_code, mimetype='application/json')


class UserNotFoundException(Exception):
    pass


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
