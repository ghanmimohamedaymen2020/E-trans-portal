import jwt
from functools import wraps
from flask import request, jsonify, current_app
from app.models import User
from config import Config

def token_required(f):
    """Décorateur pour vérifier le token JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Token manquant'}), 401
        
        if not token:
            return jsonify({'message': 'Token manquant'}), 401
        
        try:
            data = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Utilisateur non trouvé'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expiré'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token invalide'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def role_required(role_names):
    """Décorateur pour vérifier les rôles utilisateur"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask_login import current_user
            
            if not current_user.is_authenticated:
                return jsonify({'message': 'Non authentifié'}), 401
            
            if current_user.role.name not in role_names:
                return jsonify({'message': 'Accès refusé'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator

def send_email(recipient, subject, body, html=None):
    """Envoyer un email"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        sender = current_app.config['MAIL_USERNAME']
        password = current_app.config['MAIL_PASSWORD']
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient
        
        msg.attach(MIMEText(body, 'plain'))
        if html:
            msg.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi d'email: {e}")
        return False
