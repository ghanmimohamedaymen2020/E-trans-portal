# 📚 INDEX - E-Trans Documentation

Bienvenue dans la documentation du projet E-Trans!

## 🚀 Commencez par ici

1. **[QUICKSTART.md](QUICKSTART.md)** ⭐ START HERE
   - Guide de démarrage rapide (5 minutes)
   - Installation, configuration, lancement
   - Pour utilisateurs impatients

2. **[README.md](README.md)**
   - Documentation générale complète
   - Fonctionnalités, structure, technos
   - À lire après quickstart

## 📖 Documentation Technique

### Installation & Configuration
- **[SQL_SERVER_SETUP.md](SQL_SERVER_SETUP.md)** - Configuration SQL Server
  - Installation du driver ODBC
  - Création de la BD
  - Connection strings

- **[INSTALLATION_COMPLETE.md](INSTALLATION_COMPLETE.md)** - Résumé complet
  - Toutes les étapes d'installation
  - Checklist de vérification
  - Dépannage courant

### Architecture & Structure
- **[PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt)** - Vue détaillée
  - Structure complète du projet
  - Répertoires et fichiers
  - Rôles et responsabilités

- **[MANIFEST.md](MANIFEST.md)** - Manifest du projet
  - Fichiers et répertoires complets
  - Modèles de données
  - Routes HTTP
  - Dépendances

### API
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Documentation API
  - Tous les endpoints
  - Exemples de requêtes
  - Modèles de données
  - Codes d'erreur

## 🔍 Référence Rapide

### Routes Principales
- `/login` - Connexion
- `/logout` - Déconnexion
- `/change-password` - Changer mot de passe
- `/dashboard/` - Dashboard (selon rôle)
- `/dashboard/timbrage/...` - Sections avis
- `/api/...` - API endpoints

### Rôles Utilisateur
1. **Timbrage** - Gestion des avis
2. **Transit** - Validation transit
3. **Documentation** - Validation docs
4. **Commercial** - Gestion commerciale
5. **Admin** - Administration système

### Commandes Utiles
```bash
# Démarrage
python run.py                    # Lancer l'app
start.bat                        # Windows (simple)
./start.sh                       # Linux/Mac (simple)

# Administration
python init_db.py               # Initialiser BD
python cli.py create-user       # Créer utilisateur
python test_setup.py            # Test intégrité

# Docker
docker-compose up               # Lancer avec Docker
```

## 🎯 Par Cas d'Usage

### "Je veux démarrer rapidement"
→ [QUICKSTART.md](QUICKSTART.md)

### "Je dois configurer SQL Server"
→ [SQL_SERVER_SETUP.md](SQL_SERVER_SETUP.md)

### "Je dois utiliser l'API"
→ [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### "Je veux connaître l'architecture"
→ [PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt)

### "Je dois déployer en production"
→ [INSTALLATION_COMPLETE.md](INSTALLATION_COMPLETE.md) (section Production)

### "Je cherche les fichiers du projet"
→ [MANIFEST.md](MANIFEST.md)

## 📁 Structure de Documentation

```
Documentation/
├── INDEX.md                    # Ce fichier
├── QUICKSTART.md              # ⭐ START HERE
├── README.md                  # Vue générale
├── INSTALLATION_COMPLETE.md   # Résumé complet
├── SQL_SERVER_SETUP.md        # Configuration BD
├── API_DOCUMENTATION.md       # Docs API
├── PROJECT_STRUCTURE.txt      # Structure projet
└── MANIFEST.md                # Manifest complet
```

## 🔐 Informations de Connexion

Par défaut après création:
- **URL**: http://localhost:5000
- **Username**: admin
- **Password**: YourPassword123! (configurable)
- **Rôle**: Admin

⚠️ Changez le mot de passe après la première connexion!

## 📋 Checklist de Démarrage

- [ ] Lire QUICKSTART.md
- [ ] Configurer .env
- [ ] Configurer SQL Server
- [ ] Exécuter start.bat ou start.sh
- [ ] Se connecter à http://localhost:5000
- [ ] Créer des utilisateurs test
- [ ] Explorer les dashboards
- [ ] Tester les APIs
- [ ] Lire le reste de la documentation

## 🆘 Problèmes Courants

### L'app ne démarre pas
→ Vérifier que Python 3.12 est installé
→ Vérifier les dépendances: `pip install -r requirements.txt`
→ Exécuter: `python test_setup.py`

### Erreur de base de données
→ Vérifier SQL Server est en cours d'exécution
→ Vérifier `DATABASE_URL` dans `.env`
→ Consulter [SQL_SERVER_SETUP.md](SQL_SERVER_SETUP.md)

### Port 5000 déjà utilisé
→ Changer le port dans `run.py`
→ Ou utiliser: `flask run --port 5001`

### Driver ODBC non trouvé
→ Installer: [ODBC Driver 17 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

## 📞 Support

Pour chaque problème:
1. Consulter la documentation pertinente (voir index)
2. Vérifier les logs dans le terminal
3. Exécuter: `python test_setup.py`
4. Consulter le section Dépannage du README

## 🎓 Pour Apprendre

Le projet utilise:
- **Flask**: Framework web
- **SQLAlchemy**: ORM pour BD
- **Flask-Login**: Authentification
- **JWT**: Tokens API
- **Bootstrap**: Frontend
- **SQL Server**: Base de données

Explorez le code dans `app/` pour apprendre comment tout fonctionne!

## 📊 Fonctionnalités Principales

✅ **Authentification**
- Login/Logout
- Changement MDP
- Reset MDP par email
- Sessions et JWT

✅ **Gestion des Dossiers**
- CRUD complet
- Validation Transit/Doc
- Gestion des versions
- Tri par priorité

✅ **Dashboards**
- 5 rôles différents
- Statistiques en temps réel
- Charts interactifs
- Filtres personnalisés

✅ **API RESTful**
- Tous les endpoints documentés
- Authentification JWT
- Pagination
- Gestion d'erreurs

✅ **Interface Web**
- Responsive design
- Bootstrap 5
- Icônes Font Awesome
- Navigation claire

## 🎉 Vous êtes Prêt!

Commencez par: **[QUICKSTART.md](QUICKSTART.md)**

Bonne chance! 🚀

---

*Dernière mise à jour: 2026-02-04*
*Projet E-Trans v1.0.0*
