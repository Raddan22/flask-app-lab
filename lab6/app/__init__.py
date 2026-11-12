import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Конфігурація
    from app.config import DevelopmentConfig, TestingConfig, ProductionConfig
    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }
    app.config.from_object(configs.get(config_name, DevelopmentConfig))
    
    # Ініціалізація розширень
    db.init_app(app)
    migrate.init_app(app, db)
    
    # ========== РЕЄСТРАЦІЯ БЛЮПРИНТІВ ==========
    
        # Реєстрація блюпринтів
    from app.posts import post_bp
    from app.posts import views
    app.register_blueprint(post_bp)
    
    # Додайте це, якщо папка products існує
    from app.products.views import products_bp
    app.register_blueprint(products_bp)
    
    # І це, якщо папка users існує
    from app.users.views import users_bp
    app.register_blueprint(users_bp)
    
    # ============================================
    
    # Головна сторінка
    @app.route('/')
    def home():
        return render_template('base.html', title="Home")
    
    # Обробник 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
    
    return app