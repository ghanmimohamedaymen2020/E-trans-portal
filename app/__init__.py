from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name=None):
    """Factory function pour créer l'application Flask"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialiser les extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    
    # Registrer les blueprints
    from app.routes import auth_bp, dashboard_bp, api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Les tables sont créées par init_db_direct.py
    # Pas besoin de create_all() ici

    # Créer les rôles manquants au démarrage
    try:
        from app.models import Role
        with app.app_context():
            default_roles = [
                {'name': 'Admin', 'description': 'Administration système'},
                {'name': 'Timbrage', 'description': 'Gestion du timbrage'},
                {'name': 'Transit', 'description': 'Gestion du transit'},
                {'name': 'Documentation', 'description': 'Gestion de la documentation'},
                {'name': 'Commercial', 'description': 'Gestion commerciale'},
                {'name': 'Management', 'description': 'Dashboard management'}
            ]
            existing = {r.name for r in Role.query.all()}
            to_add = [
                Role(name=role['name'], nom=role['name'], description=role['description'])
                for role in default_roles
                if role['name'] not in existing
            ]
            if to_add:
                db.session.add_all(to_add)
                db.session.commit()
    except Exception:
        pass
    
    return app
