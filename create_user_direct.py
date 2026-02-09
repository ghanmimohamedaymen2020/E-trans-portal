"""
Script pour créer un utilisateur directement avec pyodbc
"""
import pyodbc
from werkzeug.security import generate_password_hash
import sys

def create_user():
    # Chaîne de connexion
    conn_str = r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=.\SQLEXPRESS;DATABASE=etrans;UID=sa;PWD=Qdg4d85Q"
    
    print("Création d'un nouvel utilisateur")
    print("="*50)
    
    # Demander les informations
    username = input("Nom d'utilisateur: ").strip()
    email = input("Email: ").strip()
    password = input("Mot de passe: ").strip()
    
    print("\nRôles disponibles:")
    print("  1. Timbrage")
    print("  2. Transit")
    print("  3. Documentation")
    print("  4. Commercial")
    print("  5. Admin")
    
    role_choice = input("\nChoisissez un rôle (1-5): ").strip()
    role_map = {
        '1': 'Timbrage',
        '2': 'Transit',
        '3': 'Documentation',
        '4': 'Commercial',
        '5': 'Admin'
    }
    
    role_nom = role_map.get(role_choice)
    if not role_nom:
        print("❌ Choix invalide!")
        return
    
    try:
        # Connexion
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Récupérer l'ID du rôle
        cursor.execute("SELECT id FROM roles WHERE nom = ?", (role_nom,))
        row = cursor.fetchone()
        if not row:
            print(f"❌ Rôle '{role_nom}' introuvable!")
            return
        
        role_id = row[0]
        
        # Hasher le mot de passe
        password_hash = generate_password_hash(password)
        
        # Insérer l'utilisateur
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role_id, actif)
            VALUES (?, ?, ?, ?, 1)
        """, (username, email, password_hash, role_id))
        
        conn.commit()
        
        print("\n" + "="*50)
        print("✓ Utilisateur créé avec succès!")
        print("="*50)
        print(f"Nom d'utilisateur: {username}")
        print(f"Email: {email}")
        print(f"Rôle: {role_nom}")
        print("\nVous pouvez maintenant vous connecter à l'application.")
        
        cursor.close()
        conn.close()
        
    except pyodbc.IntegrityError as e:
        print(f"\n❌ Erreur: Cet utilisateur ou email existe déjà!")
        print(f"   Détails: {str(e)}")
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    create_user()
