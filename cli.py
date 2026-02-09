from app import create_app, db
from app.models import User, Role
import click

@click.group()
def cli():
    """Commandes de gestion de l'application"""
    pass

@cli.command()
def init_roles():
    """Initialiser les rôles par défaut"""
    app = create_app()
    
    with app.app_context():
        roles_data = [
            {'name': 'Timbrage', 'nom': 'Timbrage', 'description': 'Gestion du timbrage'},
            {'name': 'Transit', 'nom': 'Transit', 'description': 'Gestion du transit'},
            {'name': 'Documentation', 'nom': 'Documentation', 'description': 'Gestion de la documentation'},
            {'name': 'Commercial', 'nom': 'Commercial', 'description': 'Gestion commerciale'},
            {'name': 'Admin', 'nom': 'Admin', 'description': 'Administrateur'},
            {'name': 'Management', 'nom': 'Management', 'description': 'Dashboard management'}
        ]
        
        for role_data in roles_data:
            if not Role.query.filter_by(name=role_data['name']).first():
                role = Role(**role_data)
                db.session.add(role)
        
        db.session.commit()
        click.echo('✓ Rôles créés avec succès')

@cli.command()
@click.option('--username', prompt='Nom d\'utilisateur')
@click.option('--email', prompt='Email')
@click.option('--password', prompt='Mot de passe', hide_input=True, confirmation_prompt=True)
@click.option('--role', prompt='Rôle (Timbrage/Transit/Documentation/Commercial/Admin)')
def create_user(username, email, password, role):
    """Créer un nouvel utilisateur"""
    app = create_app()
    
    with app.app_context():
        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(username=username).first():
            click.echo('❌ Cet utilisateur existe déjà')
            return
        
        # Récupérer le rôle
        role_obj = Role.query.filter_by(name=role).first()
        if not role_obj:
            click.echo(f'❌ Le rôle {role} n\'existe pas')
            return
        
        # Créer l'utilisateur
        user = User(username=username, email=email, role_id=role_obj.id)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        click.echo(f'✓ Utilisateur {username} créé avec succès')

if __name__ == '__main__':
    cli()
