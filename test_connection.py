"""
Test de connexion SQLAlchemy
"""
from dotenv import load_dotenv
load_dotenv()

import os
from sqlalchemy import create_engine, text

db_url = os.getenv('DATABASE_URL')
print(f"URL de connexion: {db_url}")
print("\nTentative de connexion...")

try:
    engine = create_engine(db_url, echo=True)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT @@VERSION"))
        version = result.scalar()
        print(f"\n✓ Connexion réussie!")
        print(f"Version SQL Server: {version[:80]}...")
        
        # Tester une requête sur la table users
        result = conn.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        print(f"✓ Nombre d'utilisateurs: {count}")
except Exception as e:
    print(f"\n❌ Erreur de connexion:")
    print(f"   {str(e)}")
