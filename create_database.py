"""
Script pour créer la base de données SQL Server
"""
import pyodbc
import sys

def create_database():
    """Crée la base de données etrans sur SQL Server"""
    
    # Différentes chaînes de connexion à essayer
    connection_strings = [
        r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=.\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes",
        r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=(local)\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes",
        r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes",
        r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=TNRDSGTCPU001\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes",
    ]
    
    conn = None
    for conn_str in connection_strings:
        try:
            print(f"Tentative de connexion avec: {conn_str.split(';')[1]}")
            conn = pyodbc.connect(conn_str, timeout=5)
            print("✓ Connexion réussie!")
            break
        except Exception as e:
            print(f"✗ Échec: {str(e)[:100]}")
            continue
    
    if not conn:
        print("\n❌ Impossible de se connecter à SQL Server.")
        print("\nVérifiez que:")
        print("1. SQL Server est démarré")
        print("2. Le protocole TCP/IP ou Named Pipes est activé")
        print("3. Vous avez les droits d'accès")
        sys.exit(1)
    
    try:
        cursor = conn.cursor()
        
        # Activer autocommit pour CREATE DATABASE
        conn.autocommit = True
        
        # Vérifier si la base de données existe déjà
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'etrans'")
        if cursor.fetchone():
            print("\n⚠ La base de données 'etrans' existe déjà.")
            response = input("Voulez-vous la supprimer et la recréer? (oui/non): ")
            if response.lower() in ['oui', 'o', 'yes', 'y']:
                print("Suppression de la base de données existante...")
                cursor.execute("DROP DATABASE etrans")
                print("✓ Base de données supprimée")
            else:
                print("Opération annulée.")
                conn.close()
                return
        
        # Créer la base de données
        print("\nCréation de la base de données 'etrans'...")
        cursor.execute("CREATE DATABASE etrans")
        print("✓ Base de données 'etrans' créée avec succès!")
        
        # Vérifier la création
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'etrans'")
        if cursor.fetchone():
            print("✓ Vérification: la base de données existe bien")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*50)
        print("✓ SUCCÈS - Base de données prête à être utilisée")
        print("="*50)
        print("\nProchaine étape: Lancez 'python init_db.py' pour créer les tables")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la création de la base de données:")
        print(f"   {str(e)}")
        if conn:
            conn.close()
        sys.exit(1)

if __name__ == "__main__":
    create_database()
