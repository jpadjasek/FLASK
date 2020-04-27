import sqlalchemy
from flask import jsonify, request, Response, Blueprint

from app.models.Model import User, Skill

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users)


@user_blueprint.route('/user', methods=['POST'])
def add_user():
    content = request.get_json()
    user = User(first_name=content['first_name'], last_name=content['last_name'])
    try:
        User.add_user(user)
        return jsonify(user)
    except sqlalchemy.exc.IntegrityError as e:
        return get_error_response(400, message='User already exists')


@user_blueprint.route('/user/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    try:
        user = get_user_by_id(user_id)
    except UserNotFoundException:
        return Response(status=204, mimetype='application/json')
    User.delete_user(user)
    return Response(status=204, mimetype='application/json')


@user_blueprint.route('/user/<user_id>/skill', methods=['POST'])
def add_skill_to_user(user_id):
    try:
        user = get_user_by_id(user_id)

    except UserNotFoundException:
        return get_error_response(400, message='User not found')

    content = request.get_json()
    skill = Skill(name=content['name'], user_id=user.id)
    try:
        Skill.add_skill_to_user(skill)
        return jsonify(skill)
    except sqlalchemy.exc.IntegrityError as e:
        return get_error_response(400, message='User already has this skill!')


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        raise UserNotFoundException
    return user


def get_error_response(status_code, message):
    body = f"{{message: {message}}}"
    return Response(body, status=status_code, mimetype='application/json')


class UserNotFoundException(Exception):
    pass
