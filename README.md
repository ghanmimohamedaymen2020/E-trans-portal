# E-Trans - Système de Gestion des Avis d'Arrivée

Plateforme web pour la gestion des avis d'arrivée avec authentification, rôles utilisateur et tableaux de bord.

## Fonctionnalités

### Authentification
- ✅ Login/Logout avec Flask-Login
- ✅ Tokens JWT pour l'API
- ✅ Changement de mot de passe
- ✅ Réinitialisation de mot de passe par email

### Gestion des Rôles
- **Timbrage**: Gestion des avis d'arrivée
- **Transit**: Validation des dossiers transit
- **Documentation**: Validation de la documentation
- **Commercial**: Gestion commerciale
- **Admin**: Gestion système

### Dashboard Timbrage
- Avis non-envoyés (dossiers sans avis)
- Avis envoyés (BLS avec avis)
- Avis à envoyer par priorité
- Avis nouvelle version (changement fret/surcharge)

#### Priorités
**FCL:**
1. Inflammable (contient une ou plusieurs partidas IMO)
2. Sinon priorité par date d'arrivée

**LCL:**
1. Inflammable
2. Sinon priorité par date d'arrivée

### Base de Données
- SQL Server (via SQLAlchemy + pyodbc)
- Modèles: User, Role, Dossier, AvisArrivee, PasswordResetToken

### Charts et Visualisations
- Répartition FCL vs LCL (Pie chart)
- Distribution par priorité (Pie chart)
- Tendance d'envoi (7 derniers jours)

## Installation

### 1. Cloner le projet
```bash
cd "Project E-Trans"
```

### 2. Créer un environnement virtuel (Windows)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer l'environnement
```bash
# Copier .env.example en .env
copy .env.example .env

# Éditer .env avec vos paramètres:
# - DATABASE_URL (SQL Server)
# - MAIL_SERVER et credentials
# - SECRET_KEY
```

### 5. Initialiser la base de données
```bash
python init_db.py
```

### 6. Créer un utilisateur administrateur
```bash
python cli.py create-user
# Suivre les prompts
```

## Lancement

```bash
python run.py
```

L'application sera disponible sur `http://localhost:5000`

## Structure du Projet

```
Project E-Trans/
├── app/
│   ├── __init__.py           # Factory Flask
│   ├── models.py             # Modèles SQLAlchemy
│   ├── utils.py              # Fonctions utilitaires
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py           # Routes authentification
│   │   ├── dashboard.py      # Routes dashboard
│   │   └── api_routes.py     # Routes API
│   ├── static/
│   │   └── css/style.css
│   └── templates/
│       ├── base.html
│       ├── auth/
│       ├── dashboard/
│       └── errors/
├── config.py                 # Configuration
├── run.py                    # Point d'entrée
├── init_db.py               # Initialisation DB
├── cli.py                   # CLI commands
└── requirements.txt         # Dépendances
```

## Configuration SQL Server

### Connection String
```
mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
```

### Driver requis
- ODBC Driver 17 for SQL Server

## Variables d'Environnement

```
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
DATABASE_URL=mssql+pyodbc://...
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## API Endpoints

### Authentification
- `POST /api/dossiers` - Créer dossier
- `GET /api/dossiers` - Liste dossiers
- `GET /api/dossiers/<id>` - Récupérer dossier
- `PUT /api/dossiers/<id>/valider-transit` - Valider transit
- `PUT /api/dossiers/<id>/valider-doc` - Valider doc
- `PUT /api/avis/<id>/envoyer` - Envoyer avis
- `GET /api/profile` - Profil utilisateur

## À Faire

- [ ] Ajouter dashboard pour autres rôles
- [ ] Intégration email pour avis
- [ ] Historique des modifications
- [ ] Logs système
- [ ] Tests unitaires
- [ ] Documentation API (Swagger)

---

**Version**: 1.0.0  
**Dernière mise à jour**: 2026-02-04
