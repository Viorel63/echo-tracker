from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.extensions import db
from app.routes.api import api_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    # Импорт и регистрация блюпринтов
    from app.routes.issues import issues_bp
    from app.routes.users import users_bp
    from app.routes.comments import comments_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(issues_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(comments_bp)

    # Создание таблиц
    with app.app_context():
        db.create_all()

    return app
