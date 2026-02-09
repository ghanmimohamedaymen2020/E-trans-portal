"""
Test d'intégrité du projet E-Trans
Exécuter avec: python test_setup.py
"""

import sys
import os

def check_directories():
    """Vérifier les répertoires"""
    dirs = [
        'app',
        'app/routes',
        'app/templates',
        'app/templates/auth',
        'app/templates/dashboard',
        'app/templates/dashboard/timbrage',
        'app/templates/errors',
        'app/static',
        'app/static/css'
    ]
    
    print("🔍 Vérification des répertoires...")
    for d in dirs:
        if os.path.exists(d):
            print(f"  ✓ {d}")
        else:
            print(f"  ✗ {d} MANQUANT")
            return False
    return True

def check_files():
    """Vérifier les fichiers"""
    files = [
        'config.py',
        'run.py',
        'init_db.py',
        'cli.py',
        'requirements.txt',
        '.env',
        '.gitignore',
        'README.md',
        'QUICKSTART.md',
        'SQL_SERVER_SETUP.md',
        'API_DOCUMENTATION.md',
        'app/__init__.py',
        'app/models.py',
        'app/utils.py',
        'app/routes/__init__.py',
        'app/routes/auth.py',
        'app/routes/dashboard.py',
        'app/routes/api_routes.py',
        'app/templates/base.html',
        'app/templates/auth/login.html',
        'app/static/css/style.css',
    ]
    
    print("\n🔍 Vérification des fichiers...")
    for f in files:
        if os.path.exists(f):
            print(f"  ✓ {f}")
        else:
            print(f"  ✗ {f} MANQUANT")
            return False
    return True

def check_imports():
    """Vérifier les imports"""
    print("\n🔍 Vérification des imports...")
    
    try:
        from flask import Flask
        print("  ✓ Flask importable")
    except ImportError:
        print("  ✗ Flask non installé")
        return False
    
    try:
        from flask_login import LoginManager
        print("  ✓ Flask-Login importable")
    except ImportError:
        print("  ✗ Flask-Login non installé")
        return False
    
    try:
        from flask_sqlalchemy import SQLAlchemy
        print("  ✓ Flask-SQLAlchemy importable")
    except ImportError:
        print("  ✗ Flask-SQLAlchemy non installé")
        return False
    
    try:
        import jwt
        print("  ✓ PyJWT importable")
    except ImportError:
        print("  ✗ PyJWT non installé")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✓ python-dotenv importable")
    except ImportError:
        print("  ✗ python-dotenv non installé")
        return False
    
    return True

def check_env():
    """Vérifier les variables d'environnement"""
    print("\n🔍 Vérification de .env...")
    
    if not os.path.exists('.env'):
        print("  ⚠ .env non trouvé")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'FLASK_ENV',
        'SECRET_KEY',
        'JWT_SECRET',
        'DATABASE_URL'
    ]
    
    for var in required_vars:
        if os.getenv(var):
            print(f"  ✓ {var} configuré")
        else:
            print(f"  ⚠ {var} non configuré")
    
    return True

def main():
    """Exécuter tous les tests"""
    print("=" * 50)
    print("  Test d'intégrité - E-Trans")
    print("=" * 50)
    
    checks = [
        ("Répertoires", check_directories),
        ("Fichiers", check_files),
        ("Imports", check_imports),
        ("Environnement", check_env),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            results.append(check_func())
        except Exception as e:
            print(f"  ✗ Erreur lors du test {name}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ Tous les tests sont passés!")
        print("\nProchain pas:")
        print("  1. Configurez votre base de données SQL Server")
        print("  2. Exécutez: python init_db.py")
        print("  3. Créez un utilisateur: python cli.py create-user")
        print("  4. Lancez l'app: python run.py")
        return 0
    else:
        print("✗ Certains tests ont échoué")
        print("\nVérifiez l'installation et relancez le test")
        return 1

if __name__ == '__main__':
    sys.exit(main())
