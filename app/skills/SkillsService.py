from flask import Blueprint, jsonify, Response

from app.models.Model import Skill

skill_blueprint = Blueprint('skill_blueprint', __name__)


@skill_blueprint.route('/skill', methods=['GET'])
def get_skills():
    skills = Skill.query.all()
    return jsonify(skills)


@skill_blueprint.route('/skill/<skill_id>', methods=['DELETE'])
def delete_skill_by_id(skill_id):
    try:
        skill = get_skill_by_id(skill_id)
    except SkillNotFoundException:
        return Response(status=204, mimetype='application/json')
    Skill.delete_skill(skill)
    return Response(status=204, mimetype='application/json')


def get_skill_by_id(skill_id):
    user = Skill.query.get(skill_id)
    if not user:
        raise SkillNotFoundException
    return user


class SkillNotFoundException(Exception):
    pass
