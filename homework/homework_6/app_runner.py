from flask import Flask
from flask_migrate import Migrate
from polars.testing.parametric.strategies.data import categories

from core.config import settings
from routers.questions import questions_bp
from core.db import db
from models import *
from routers.category import bp as categories_bp


def init_database(app: Flask):
    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)


def register_routers(app: Flask):
    app.register_blueprint(questions_bp)
    app.register_blueprint(categories_bp)


def create_app(app: Flask):
    app.config.update(settings.get_flask_config())

    init_database(app)

    register_routers(app)