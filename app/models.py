from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import jwt
from config import Config

class User(UserMixin, db.Model):
    """Modèle utilisateur"""
    __tablename__ = 'users'
    __bind_key__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    
    def set_password(self, password):
        """Hash et défini le mot de passe"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Vérifie le mot de passe"""
        return check_password_hash(self.password_hash, password)
    
    def generate_reset_token(self, expires_in=3600):
        """Génère un token de réinitialisation de mot de passe"""
        return jwt.encode(
            {'user_id': self.id, 'exp': datetime.utcnow().timestamp() + expires_in},
            Config.SECRET_KEY,
            algorithm=Config.JWT_ALGORITHM
        )
    
    def generate_jwt_token(self):
        """Génère un token JWT"""
        return jwt.encode(
            {'user_id': self.id, 'role': self.role.name},
            Config.JWT_SECRET,
            algorithm=Config.JWT_ALGORITHM
        )
    
    def __repr__(self):
        return f'<User {self.username}>'

class Role(db.Model):
    """Modèle des rôles utilisateur"""
    __tablename__ = 'roles'
    __bind_key__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Role {self.name}>'

class Dossier(db.Model):
    """Modèle pour les dossiers de transport"""
    __tablename__ = 'dossiers'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False, index=True)
    type_conteneur = db.Column(db.String(10))  # FCL ou LCL
    date_arrivee = db.Column(db.DateTime, nullable=False, index=True)
    status = db.Column(db.String(50), default='nouveau')  # nouveau, validé, avis_envoyé
    contient_imo = db.Column(db.Boolean, default=False)  # Pour vérifier si inflammable
    avis_envoye = db.Column(db.Boolean, default=False)
    avis_a_envoyer = db.Column(db.Boolean, default=False)
    version_avis = db.Column(db.Integer, default=1)
    validé_transit = db.Column(db.Boolean, default=False)
    validé_documentation = db.Column(db.Boolean, default=False)
    contient_escale = db.Column(db.Boolean, default=False)
    contient_fret = db.Column(db.Boolean, default=False)
    avis_precedent_id = db.Column(db.Integer, db.ForeignKey('dossiers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    avis_versions = db.relationship('Dossier', remote_side=[id], backref='avis_precedent')
    
    def __repr__(self):
        return f'<Dossier {self.numero}>'

class AvisArrivee(db.Model):
    """Modèle pour les avis d'arrivée"""
    __tablename__ = 'avis_arrivees'
    
    id = db.Column(db.Integer, primary_key=True)
    dossier_id = db.Column(db.Integer, db.ForeignKey('dossiers.id'), nullable=False)
    numero_bl = db.Column(db.String(50), unique=True, nullable=False, index=True)
    contenu = db.Column(db.Text)
    statut = db.Column(db.String(50), default='brouillon')  # brouillon, envoyé
    version = db.Column(db.Integer, default=1)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_envoi = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    dossier = db.relationship('Dossier', backref=db.backref('avis_arrivees', lazy=True))
    
    def __repr__(self):
        return f'<AvisArrivee {self.numero_bl}>'

class PasswordResetToken(db.Model):
    """Modèle pour les tokens de réinitialisation de mot de passe"""
    __tablename__ = 'password_reset_tokens'
    __bind_key__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship('User', backref=db.backref('reset_tokens', lazy=True))
    
    def is_valid(self):
        """Vérifie si le token est valide"""
        return not self.is_used and datetime.utcnow() < self.expires_at
