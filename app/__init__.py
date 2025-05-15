from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()  # Initialize here, but don't bind until app is created

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from . import models
    db.init_app(app)
    migrate.init_app(app, db)  # Correct: app exists now

    from .routes import main
    app.register_blueprint(main)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    return app
