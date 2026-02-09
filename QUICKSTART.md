# Quick Start Guide - E-Trans

## Démarrage Rapide

### Windows

```bash
# 1. Accédez au dossier du projet
cd "Project E-Trans"

# 2. Exécutez le script de démarrage
start.bat
```

### Linux/Mac

```bash
# 1. Accédez au dossier du projet
cd "Project E-Trans"

# 2. Exécutez le script de démarrage
chmod +x start.sh
./start.sh
```

## Configuration Manuelle

### 1. Créer un environnement virtuel

```bash
python -m venv venv

# Activation (Windows)
venv\Scripts\activate

# Activation (Linux/Mac)
source venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer la base de données

- Éditer le fichier `.env`
- Voir [SQL_SERVER_SETUP.md](SQL_SERVER_SETUP.md) pour plus de détails
- Adapter `DATABASE_URL` à votre configuration SQL Server

### 4. Initialiser la base de données

```bash
python init_db.py
```

### 5. Créer un utilisateur administrateur

```bash
python cli.py create-user
```

Suivez les prompts:
- Nom d'utilisateur: `admin`
- Email: `admin@example.com`
- Mot de passe: `YourPassword123!`
- Rôle: `Admin`

### 6. Lancer l'application

```bash
python run.py
```

L'application sera disponible sur: **http://localhost:5000**

## Identifiants de test

- **Username**: `admin`
- **Email**: `admin@example.com`
- **Password**: `YourPassword123!` (ou celui que vous avez défini)

## Structure des rôles

1. **Timbrage** - Gestion des avis d'arrivée
2. **Transit** - Validation des dossiers
3. **Documentation** - Validation des documents
4. **Commercial** - Gestion commerciale
5. **Admin** - Administration système

## Premier démarrage

Après le login, vous verrez le dashboard correspondant à votre rôle:

- **Admin/Timbrage**: Dashboard avec statistiques et 4 sections d'avis
- **Transit**: Dashboard de validation
- **Documentation**: Dashboard de documentation
- **Commercial**: Dashboard commercial

## Arrêter l'application

Appuyez sur `Ctrl+C` dans le terminal

## Problèmes courants

### "Module not found: flask"
→ Vérifiez que l'environnement virtuel est activé
→ Réinstallez avec: `pip install -r requirements.txt`

### "Database connection error"
→ Vérifiez la variable `DATABASE_URL` dans `.env`
→ Vérifiez que SQL Server est en cours d'exécution
→ Voir [SQL_SERVER_SETUP.md](SQL_SERVER_SETUP.md)

### Port 5000 déjà utilisé
Modifier le port dans `run.py` (dernière ligne) ou depuis le terminal:
```bash
flask run --port 5001
```

## Support

Pour plus de détails:
- Consultez [README.md](README.md)
- Consultez [SQL_SERVER_SETUP.md](SQL_SERVER_SETUP.md)
