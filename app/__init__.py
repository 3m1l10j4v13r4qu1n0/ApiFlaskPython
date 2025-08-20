#Inicializa la app y extensiones
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        #from app import routes, models, errors  # Import routes and models
        # Importá los modelos aquí para que Flask-Migrate los detecte
        from . import models
        from .routes.main import main as main_blueprint
        from .routes.auth import auth as auth_blueprint
        app.register_blueprint(main_blueprint)
        app.register_blueprint(auth_blueprint)
        from .routes.crud import crud as crud_blueprint
        app.register_blueprint(crud_blueprint, url_prefix='/api')
        from .api.routes_afiliados import afiliados_bp as afiliados_blueprint
        app.register_blueprint(afiliados_blueprint)

    
    return app
