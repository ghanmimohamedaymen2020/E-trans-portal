"""
Script alternatif pour initialiser la base de données directement avec pyodbc
"""
import pyodbc
import sys
from werkzeug.security import generate_password_hash

def init_database():
    """Initialise la base de données avec pyodbc directement"""
    
    # Chaîne de connexion qui fonctionne
    conn_str = r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=.\SQLEXPRESS;DATABASE=etrans;UID=sa;PWD=Qdg4d85Q"
    
    try:
        print("Connexion à SQL Server...")
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print("✓ Connexion réussie!")
        
        # Créer la table roles
        print("\nCréation de la table 'roles'...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'roles')
            CREATE TABLE roles (
                id INT IDENTITY(1,1) PRIMARY KEY,
                nom NVARCHAR(50) UNIQUE NOT NULL,
                description NVARCHAR(255)
            )
        """)
        conn.commit()
        print("✓ Table 'roles' créée")
        
        # Insérer les rôles par défaut
        print("\nInsertion des rôles...")
        roles_data = [
            ('Timbrage', 'Gestion des avis d\'arrivée'),
            ('Transit', 'Validation transit'),
            ('Documentation', 'Validation documentation'),
            ('Commercial', 'Suivi commercial'),
            ('Admin', 'Administration système')
        ]
        
        for nom, desc in roles_data:
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM roles WHERE nom = ?)
                INSERT INTO roles (nom, description) VALUES (?, ?)
            """, (nom, nom, desc))
        conn.commit()
        print(f"✓ {len(roles_data)} rôles insérés")
        
        # Créer la table users
        print("\nCréation de la table 'users'...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
            CREATE TABLE users (
                id INT IDENTITY(1,1) PRIMARY KEY,
                username NVARCHAR(80) UNIQUE NOT NULL,
                email NVARCHAR(120) UNIQUE NOT NULL,
                password_hash NVARCHAR(255) NOT NULL,
                role_id INT NOT NULL,
                actif BIT DEFAULT 1,
                created_at DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (role_id) REFERENCES roles(id)
            )
        """)
        conn.commit()
        print("✓ Table 'users' créée")
        
        # Créer la table dossiers
        print("\nCréation de la table 'dossiers'...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'dossiers')
            CREATE TABLE dossiers (
                id INT IDENTITY(1,1) PRIMARY KEY,
                numero_dossier NVARCHAR(50) UNIQUE NOT NULL,
                client NVARCHAR(200) NOT NULL,
                type_conteneur NVARCHAR(10),
                numero_bl NVARCHAR(100),
                navire NVARCHAR(200),
                voyage NVARCHAR(100),
                port_chargement NVARCHAR(100),
                port_dechargement NVARCHAR(100),
                date_eta DATETIME,
                date_arrivee DATETIME,
                est_imo BIT DEFAULT 0,
                priorite INT DEFAULT 0,
                statut_transit BIT DEFAULT 0,
                statut_documentation BIT DEFAULT 0,
                valide_par_transit_id INT,
                valide_par_doc_id INT,
                created_at DATETIME DEFAULT GETDATE(),
                updated_at DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (valide_par_transit_id) REFERENCES users(id),
                FOREIGN KEY (valide_par_doc_id) REFERENCES users(id)
            )
        """)
        conn.commit()
        print("✓ Table 'dossiers' créée")
        
        # Créer la table avis_arrivees
        print("\nCréation de la table 'avis_arrivees'...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'avis_arrivees')
            CREATE TABLE avis_arrivees (
                id INT IDENTITY(1,1) PRIMARY KEY,
                dossier_id INT NOT NULL,
                version INT DEFAULT 1,
                contenu NVARCHAR(MAX),
                est_envoye BIT DEFAULT 0,
                date_envoi DATETIME,
                envoye_par_id INT,
                created_at DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (dossier_id) REFERENCES dossiers(id),
                FOREIGN KEY (envoye_par_id) REFERENCES users(id)
            )
        """)
        conn.commit()
        print("✓ Table 'avis_arrivees' créée")
        
        # Créer la table password_reset_tokens
        print("\nCréation de la table 'password_reset_tokens'...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'password_reset_tokens')
            CREATE TABLE password_reset_tokens (
                id INT IDENTITY(1,1) PRIMARY KEY,
                user_id INT NOT NULL,
                token NVARCHAR(255) UNIQUE NOT NULL,
                expiration DATETIME NOT NULL,
                utilise BIT DEFAULT 0,
                created_at DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
        print("✓ Table 'password_reset_tokens' créée")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✓ BASE DE DONNÉES INITIALISÉE AVEC SUCCÈS!")
        print("="*60)
        print("\nProchaine étape: Créez un utilisateur admin avec:")
        print("  python cli.py create-user")
        
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
