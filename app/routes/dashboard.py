from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/', endpoint='index')
@login_required
def index():
    role = current_user.role.name.lower().strip()
    role_key = role.replace(' ', '_')
    role_map = {
        'management': 'management',
        'manager': 'management',
        'gestion': 'management',
        'direction': 'management',
        'adel': 'management'
    }
    template_key = role_map.get(role_key, role_key)
    return render_template(f'dashboard/{template_key}_dashboard.html')

@dashboard_bp.route('/home')
def home():
    """Page d'accueil publique"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('main/index.html')

# ... autres routes du dashboard ...