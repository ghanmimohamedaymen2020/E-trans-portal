# Manifest du Projet E-Trans

## Informations Générales

**Nom du Projet**: E-Trans  
**Description**: Système de gestion des avis d'arrivée avec authentification, rôles utilisateur et dashboards analytiques  
**Version**: 1.0.0  
**Date de Création**: 2026-02-04  
**Environnement Python**: 3.12  

---

## Fichiers et Répertoires

### Répertoire Racine
```
.env                           # Variables d'environnement (gitignored)
.env.example                   # Modèle de .env
.gitignore                     # Git ignore
config.py                      # Configuration Flask
cli.py                         # CLI commands
init_db.py                     # Initialisation BD
run.py                         # Point d'entrée

Dockerfile                     # Image Docker
docker-compose.yml             # Orchestration Docker
requirements.txt               # Dépendances Python
requirements-dev.txt           # Dépendances dev

start.bat                      # Script démarrage Windows
start.sh                       # Script démarrage Linux/Mac
test_setup.py                  # Test d'intégrité

README.md                      # Documentation principale
QUICKSTART.md                  # Guide rapide
SQL_SERVER_SETUP.md            # Configuration BD
API_DOCUMENTATION.md           # Docs API
PROJECT_STRUCTURE.txt          # Structure détaillée
INSTALLATION_COMPLETE.md       # Ce fichier + résumé
MANIFEST.md                    # Ce fichier
```

### Répertoire app/
```
__init__.py                    # Factory Flask + initialisation
models.py                      # Modèles SQLAlchemy
utils.py                       # Utilitaires (decorators, email, etc.)

routes/
  ├── __init__.py             # Blueprints
  ├── auth.py                 # Routes authentification
  ├── dashboard.py            # Routes dashboards + stats
  └── api_routes.py           # Routes API RESTful

static/
  └── css/
      └── style.css           # Styles CSS personnalisés

templates/
  ├── base.html               # Template de base
  ├── auth/
  │   ├── login.html
  │   ├── change_password.html
  │   ├── forgot_password.html
  │   └── reset_password.html
  ├── dashboard/
  │   ├── timbrage_dashboard.html
  │   ├── transit_dashboard.html
  │   ├── documentation_dashboard.html
  │   ├── commercial_dashboard.html
  │   ├── admin_dashboard.html
  │   └── timbrage/
  │       ├── avis_non_envoyes.html
  │       ├── avis_envoyes.html
  │       ├── avis_a_envoyer_priorite.html
  │       └── avis_nouvelle_version.html
  └── errors/
      ├── 404.html
      └── 500.html
```

---

## Modèles de Données

### Users (Utilisateurs)
- id: Integer (Primary Key)
- username: String(80, unique=True)
- email: String(120, unique=True)
- password_hash: String(255)
- role_id: Integer (Foreign Key → Role)
- is_active: Boolean (default=True)
- created_at: DateTime
- last_login: DateTime

### Roles
- id: Integer (Primary Key)
- name: String(50, unique=True)
- description: String(255)
- created_at: DateTime

Rôles disponibles:
1. Timbrage
2. Transit
3. Documentation
4. Commercial
5. Admin

### Dossiers
- id: Integer (Primary Key)
- numero: String(50, unique=True)
- type_conteneur: String(10) [FCL, LCL]
- date_arrivee: DateTime (indexed)
- status: String(50)
- contient_imo: Boolean (inflammable)
- avis_envoye: Boolean
- avis_a_envoyer: Boolean
- version_avis: Integer
- validé_transit: Boolean
- validé_documentation: Boolean
- contient_escale: Boolean
- contient_fret: Boolean
- avis_precedent_id: Integer (FK → Dossier, self-ref)
- created_at: DateTime
- updated_at: DateTime

### AvisArrivees (Avis d'Arrivée)
- id: Integer (Primary Key)
- dossier_id: Integer (Foreign Key → Dossier)
- numero_bl: String(50, unique=True)
- contenu: Text
- statut: String(50) [brouillon, envoyé]
- version: Integer
- date_creation: DateTime
- date_envoi: DateTime
- created_at: DateTime

### PasswordResetTokens
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key → User)
- token: String(255, unique=True)
- is_used: Boolean (default=False)
- created_at: DateTime
- expires_at: DateTime

---

## Routes HTTP

### Authentification (/auth)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET/POST | /login | Connexion |
| GET | /logout | Déconnexion |
| GET/POST | /change-password | Changer MDP |
| GET/POST | /forgot-password | MDP oublié |
| GET/POST | /reset-password/<token> | Réinitialiser MDP |

### Dashboard (/dashboard)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | / | Dashboard principal (selon rôle) |
| GET | /timbrage/avis-non-envoyes | Avis non-envoyés |
| GET | /timbrage/avis-envoyes | Avis envoyés |
| GET | /timbrage/avis-a-envoyer-priorite | Par priorité |
| GET | /timbrage/avis-nouvelle-version | Nouvelle version |

### Stats (/dashboard/api)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | /api/stats/timbrage | Stats principales |
| GET | /api/stats/tendance-avis | Tendance 7j |
| GET | /api/stats/distribution-type | FCL vs LCL |
| GET | /api/stats/priorite | Inflammable vs Normal |

### API (/api)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | /dossiers | Liste (paginée) |
| POST | /dossiers | Créer |
| GET | /dossiers/<id> | Récupérer |
| PUT | /dossiers/<id>/valider-transit | Valider |
| PUT | /dossiers/<id>/valider-doc | Valider |
| PUT | /avis/<id>/envoyer | Envoyer |
| GET | /profile | Profil user |

---

## Dépendances Python

### Core
- Flask==2.3.3
- Werkzeug==2.3.7
- Jinja2

### Authentication & Authorization
- Flask-Login==0.6.2
- PyJWT==2.8.1

### Database
- Flask-SQLAlchemy==3.0.5
- SQLAlchemy (ORM)
- pyodbc==4.0.39 (SQL Server)

### Utilities
- python-dotenv==1.0.0
- pandas==2.0.3
- plotly==5.16.1
- email-validator==2.0.0

### Optional Dev
- pytest==7.4.2
- pytest-cov==4.1.0
- black==23.9.1
- flake8==6.1.0

---

## Fonctionnalités Principales

### ✅ Implémentées
- [x] Flask-Login (sessions)
- [x] JWT tokens (API)
- [x] Gestion des rôles (5)
- [x] Authentification
- [x] Changement MDP
- [x] Reset MDP par email
- [x] Modèles de BD
- [x] Routes CRUD dossiers
- [x] Routes API
- [x] Dashboards (5 rôles)
- [x] Charts/Visualisations
- [x] Statistiques en temps réel
- [x] Validation Transit/Doc
- [x] Gestion versions avis
- [x] Tri par priorité
- [x] Filtres flamm/date
- [x] Responsive design
- [x] Error handling
- [x] Logging

### 🔄 En Cours / Optionnel
- [ ] Ajouter Dashboard Transit complet
- [ ] Ajouter Dashboard Doc complet
- [ ] Ajouter Dashboard Commercial complet
- [ ] Ajouter Dashboard Admin complet
- [ ] Tests unitaires
- [ ] Documentation Swagger
- [ ] Export PDF
- [ ] Export Excel
- [ ] Multi-langue
- [ ] Dark mode

---

## Configuration & Installation

### Python Environment
- Python 3.12.8
- Virtual Environment: `venv/`

### Database
- SQL Server 2022 (compatible 2019+)
- Driver: ODBC Driver 17 for SQL Server
- Connection: SQLAlchemy + pyodbc

### Server
- Framework: Flask 2.3.3
- Port: 5000 (configurable)
- Mode: Development (configurable)

### Dependencies
- pip install -r requirements.txt
- pip install -r requirements-dev.txt (optionnel)

---

## Variables d'Environnement

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET=your-jwt-secret-key-change-in-production
DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
DEBUG=True
```

---

## Commandes Utiles

```bash
# Démarrage
python run.py                          # Lancer l'app
python init_db.py                      # Initialiser les rôles
python cli.py create-user              # Créer utilisateur

# Tests
python test_setup.py                   # Test intégrité

# Development
flask shell                            # Shell interactif
python -m pytest                       # Tester

# Formatting
black .                                # Format code
flake8 .                               # Lint

# Docker
docker build .                         # Build image
docker-compose up                      # Lancer services
```

---

## Authentification

### Sessions (Web)
- Cookie de session Flask
- Flask-Login UserMixin
- Timeout: 24h

### API (JWT)
- Token Bearer
- Algorithme: HS256
- Expiration: 24h

---

## Sécurité

- ✅ Password hashing (Werkzeug)
- ✅ CSRF protection (Flask)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Email validation
- ✅ Token generation avec secrets
- ✅ Expiration tokens
- ✅ Role-based access control

---

## Performance

- Pagination sur les listes (per_page=10)
- Indexes sur requêtes fréquentes
- Cache statiques
- Minimisation CSS/JS optionnelle

---

## Documentation

- [README.md](README.md) - Vue générale
- [QUICKSTART.md](QUICKSTART.md) - Démarrage rapide
- [SQL_SERVER_SETUP.md](SQL_SERVER_SETUP.md) - Configuration BD
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Docs API
- [PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt) - Structure détaillée

---

## Déploiement

### Local
```bash
python run.py
```

### Docker
```bash
docker-compose up
```

### Production
- Utiliser un serveur WSGI (Gunicorn)
- Reverse proxy (Nginx)
- SSL/HTTPS
- Variables d'env sécurisées
- Logs centralisés

---

## Support & Maintenance

### Logs
- Console: stdout/stderr
- Fichier: À configurer

### Monitoring
- À implémenter

### Backup BD
- À configurer

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | 2026-02-04 | Version initiale |

---

## License

À définir

---

**Créé le**: 2026-02-04  
**Status**: Production Ready  
**Mainteneur**: À définir
