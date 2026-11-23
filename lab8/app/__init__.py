import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=convention))
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    from app.config import DevelopmentConfig, TestingConfig, ProductionConfig
    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }
    app.config.from_object(configs.get(config_name, DevelopmentConfig))
    
    app.config["SQLALCHEMY_ECHO"] = True
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.posts import post_bp
    from app.posts import views
    app.register_blueprint(post_bp)
    
    try:
        from app.users.views import users_bp
        app.register_blueprint(users_bp)
    except ImportError:
        app.logger.warning("Blueprint 'users' not found. Skipping.")
    
    @app.route('/')
    def home():
        return render_template('base.html', title="Home")
    
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
    
    return app