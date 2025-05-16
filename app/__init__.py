from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions (not bound yet)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # App Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'  # Needed for flash, sessions

    # Initialize extensions
    from . import models
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from .routes import main
    app.register_blueprint(main)

    # Custom error handler for 404
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    # Custom error handler for 500
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500

    return app
