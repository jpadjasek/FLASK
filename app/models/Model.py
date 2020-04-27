from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy

model_db = SQLAlchemy()


@dataclass
class Skill(model_db.Model):
    id: int
    name: str
    user_id: int

    id = model_db.Column(model_db.Integer, primary_key=True)
    name = model_db.Column(model_db.String(50), unique=False, nullable=False)
    user_id = model_db.Column(model_db.Integer, model_db.ForeignKey('user.id'), nullable=False, unique=False)

    __table_args__ = (
        model_db.UniqueConstraint('name', 'user_id', name='unique_skill_user'),
    )

    @staticmethod
    def add_skill_to_user(skill):
        model_db.session.add(skill)
        model_db.session.commit()
        return skill

    @staticmethod
    def delete_skill(skill):
        model_db.session.delete(skill)
        model_db.session.commit()


@dataclass
class User(model_db.Model):
    id: int
    first_name: str
    last_name: str
    cv_url: str
    skills: Skill

    id = model_db.Column(model_db.Integer, primary_key=True)
    first_name = model_db.Column(model_db.String(20), unique=False, nullable=False)
    last_name = model_db.Column(model_db.String(120), unique=False, nullable=False)
    cv_url = model_db.Column(model_db.String(120), unique=True, nullable=True)
    skills = model_db.relationship('Skill', backref='user', cascade='all', lazy=True)

    __table_args__ = (
        model_db.UniqueConstraint('first_name', 'last_name', name='unique_name'),
    )

    @staticmethod
    def add_user(user):
        model_db.session.add(user)
        model_db.session.commit()
        return user

    @staticmethod
    def delete_user(user):
        model_db.session.delete(user)
        model_db.session.commit()
