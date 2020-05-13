from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.models.Model import model_db
from app.s3.S3Service import s3_blueprint
from app.skills.SkillsService import skill_blueprint
from app.users.UserService import user_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(skill_blueprint)
app.register_blueprint(s3_blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
root_db = SQLAlchemy()

if __name__ == '__main__':
    root_db.init_app(app)
    model_db.init_app(app)
    with app.app_context():
        root_db.create_all()
        model_db.create_all()
    app.run(debug=False)
