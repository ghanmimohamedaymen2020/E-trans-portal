from app import create_app, db
from app.models import User, Role

def init_db():
    """Initialiser la base de données avec les rôles par défaut"""
    app = create_app()
    
    with app.app_context():
        # Créer les rôles
        roles_data = [
            {'name': 'Timbrage', 'description': 'Gestion du timbrage'},
            {'name': 'Transit', 'description': 'Gestion du transit'},
            {'name': 'Documentation', 'description': 'Gestion de la documentation'},
            {'name': 'Commercial', 'description': 'Gestion commerciale'},
            {'name': 'Admin', 'description': 'Administrateur'}
        ]
        
        for role_data in roles_data:
            if not Role.query.filter_by(name=role_data['name']).first():
                role = Role(**role_data)
                db.session.add(role)
        
        db.session.commit()
        print("✓ Rôles créés avec succès")

if __name__ == '__main__':
    init_db()
