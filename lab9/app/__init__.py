from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    from app.config import DevelopmentConfig, TestingConfig, ProductionConfig
    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }
    app.config.from_object(configs.get(config_name, DevelopmentConfig))
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)       
    login_manager.init_app(app) 
    
    # Налаштування Flask-Login
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    
    # Реєстрація блюпринтів
    from app.posts import post_bp
    from app.posts import views
    app.register_blueprint(post_bp)
    
    from app.users.views import users_bp
    app.register_blueprint(users_bp)
    
    @app.route('/')
    def home():
        return render_template('base.html', title="Home")
    
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
    
    return app