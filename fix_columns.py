"""
Script pour ajouter les colonnes manquantes à la table users
"""
import pyodbc
import sys

def add_missing_columns():
    # Chaîne de connexion
    conn_str = r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=.\SQLEXPRESS;DATABASE=etrans;UID=sa;PWD=Qdg4d85Q"
    
    try:
        print("Connexion à SQL Server...")
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print("✓ Connexion réussie!")
        
        # Vérifier et ajouter la colonne is_active
        print("\nVérification de la colonne 'is_active'...")
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'is_active'
        """)
        if cursor.fetchone()[0] == 0:
            print("Ajout de la colonne 'is_active'...")
            cursor.execute("""
                ALTER TABLE users ADD is_active BIT DEFAULT 1 NOT NULL
            """)
            conn.commit()
            print("✓ Colonne 'is_active' ajoutée")
        else:
            print("⚠ La colonne 'is_active' existe déjà")
        
        # Vérifier et ajouter la colonne last_login
        print("\nVérification de la colonne 'last_login'...")
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'last_login'
        """)
        if cursor.fetchone()[0] == 0:
            print("Ajout de la colonne 'last_login'...")
            cursor.execute("""
                ALTER TABLE users ADD last_login DATETIME NULL
            """)
            conn.commit()
            print("✓ Colonne 'last_login' ajoutée")
        else:
            print("⚠ La colonne 'last_login' existe déjà")
        
        # Vérifier et ajouter les colonnes manquantes dans roles
        print("\nVérification des colonnes 'name' et 'created_at' dans roles...")
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'roles' AND COLUMN_NAME = 'name'
        """)
        if cursor.fetchone()[0] == 0:
            print("Ajout de la colonne 'name' dans roles...")
            cursor.execute("""
                ALTER TABLE roles ADD name NVARCHAR(50) NULL
            """)
            conn.commit()
            # Copier les données depuis la colonne 'nom' si elle existe
            cursor.execute("""
                IF EXISTS (
                    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = 'roles' AND COLUMN_NAME = 'nom'
                )
                UPDATE roles SET name = nom WHERE name IS NULL
            """)
            conn.commit()
            # Rendre la colonne non nulle si possible
            cursor.execute("""
                IF EXISTS (
                    SELECT 1 FROM roles WHERE name IS NULL
                )
                    UPDATE roles SET name = 'Unknown' WHERE name IS NULL
            """)
            conn.commit()
            cursor.execute("""
                ALTER TABLE roles ALTER COLUMN name NVARCHAR(50) NOT NULL
            """)
            conn.commit()
            print("✓ Colonne 'name' ajoutée et synchronisée")
        else:
            print("⚠ La colonne 'name' existe déjà")

        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'roles' AND COLUMN_NAME = 'created_at'
        """)
        if cursor.fetchone()[0] == 0:
            print("Ajout de la colonne 'created_at' dans roles...")
            cursor.execute("""
                ALTER TABLE roles ADD created_at DATETIME NULL
            """)
            conn.commit()
            cursor.execute("""
                UPDATE roles SET created_at = GETDATE() WHERE created_at IS NULL
            """)
            conn.commit()
            print("✓ Colonne 'created_at' ajoutée")
        else:
            print("⚠ La colonne 'created_at' existe déjà")

        # Vérifier et corriger les colonnes dans password_reset_tokens
        print("\nVérification des colonnes 'is_used' et 'expires_at' dans password_reset_tokens...")

        # Ajouter is_used si manquant
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'password_reset_tokens' AND COLUMN_NAME = 'is_used'
        """)
        if cursor.fetchone()[0] == 0:
            print("Ajout de la colonne 'is_used'...")
            cursor.execute("""
                ALTER TABLE password_reset_tokens ADD is_used BIT DEFAULT 0 NOT NULL
            """)
            conn.commit()
            print("✓ Colonne 'is_used' ajoutée")
        else:
            print("⚠ La colonne 'is_used' existe déjà")

        # Si la colonne 'expiration' existe, la renommer en 'expires_at'
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'password_reset_tokens' AND COLUMN_NAME = 'expiration'
        """)
        expiration_exists = cursor.fetchone()[0] == 1

        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'password_reset_tokens' AND COLUMN_NAME = 'expires_at'
        """)
        expires_at_exists = cursor.fetchone()[0] == 1

        if expiration_exists and not expires_at_exists:
            print("Renommage de la colonne 'expiration' en 'expires_at'...")
            cursor.execute("""
                EXEC sp_rename 'password_reset_tokens.expiration', 'expires_at', 'COLUMN'
            """)
            conn.commit()
            print("✓ Colonne 'expires_at' renommée")
        elif expiration_exists and expires_at_exists:
            print("Suppression de la colonne 'expiration' (obsolète)...")
            cursor.execute("""
                ALTER TABLE password_reset_tokens DROP COLUMN expiration
            """)
            conn.commit()
            print("✓ Colonne 'expiration' supprimée")
        elif not expires_at_exists:
            print("Ajout de la colonne 'expires_at'...")
            cursor.execute("""
                ALTER TABLE password_reset_tokens ADD expires_at DATETIME NULL
            """)
            conn.commit()
            print("✓ Colonne 'expires_at' ajoutée")
        else:
            print("⚠ La colonne 'expires_at' existe déjà")

        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✓ COLONNES AJOUTÉES AVEC SUCCÈS!")
        print("="*60)
        print("\nRedémarrez l'application avec: python run.py")
        
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    add_missing_columns()
