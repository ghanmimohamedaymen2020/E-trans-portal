from flask import Blueprint

# Créer les blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='')
api_bp = Blueprint('api', __name__)

# Importer les routes et blueprints
from app.routes import auth, api_routes
from app.routes.dashboard import dashboard_bp
