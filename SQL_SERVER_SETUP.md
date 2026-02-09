# Guide de Configuration SQL Server

## Installation du Driver ODBC

### Windows

1. Télécharger le driver ODBC:
   - [ODBC Driver 17 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

2. Exécuter l'installateur

3. Vérifier l'installation:
```bash
sqlcmd -S . -U sa -P <password>
```

## Configuration de la Base de Données

### 1. Créer la base de données

```sql
CREATE DATABASE etrans;
GO
```

### 2. Créer un utilisateur (optionnel)

```sql
USE etrans;
GO

CREATE LOGIN etrans_user WITH PASSWORD = 'YourStrongPassword123!';
GO

CREATE USER etrans_user FOR LOGIN etrans_user;
GO

ALTER ROLE db_owner ADD MEMBER etrans_user;
GO
```

### 3. Connection String

**Avec authentification SQL Server:**
```
mssql+pyodbc://etrans_user:YourPassword123!@localhost/etrans?driver=ODBC+Driver+17+for+SQL+Server
```

**Avec authentification Windows:**
```
mssql+pyodbc://localhost/etrans?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes
```

**Avec instance nommée:**
```
mssql+pyodbc://sa:password@localhost\SQLEXPRESS/etrans?driver=ODBC+Driver+17+for+SQL+Server
```

## Configuration du fichier .env

Éditer le fichier `.env`:

```env
DATABASE_URL=mssql+pyodbc://sa:password@localhost/etrans?driver=ODBC+Driver+17+for+SQL+Server
```

## Initialiser la base de données

```bash
# Activer l'environnement virtuel (Windows)
venv\Scripts\activate

# Initialiser les rôles
python init_db.py

# Créer un utilisateur
python cli.py create-user
```

## Vérification

Pour vérifier que tout fonctionne:

```bash
python run.py
```

Accédez à: `http://localhost:5000`

## Dépannage

### Erreur: "Driver not found"
- Assurez-vous que le driver ODBC est installé
- Vérifier le nom du driver avec `sqlcmd`

### Erreur: "Connection refused"
- Vérifier que SQL Server est en cours d'exécution
- Vérifier le hostname et le port

### Erreur: "Authentication failed"
- Vérifier le username et password
- Vérifier que l'utilisateur a les permissions sur la BD

## Ressources

- [SQLAlchemy MSSQL Documentation](https://docs.sqlalchemy.org/en/20/dialects/mssql.html)
- [Python ODBC](https://github.com/mkleehammer/pyodbc)
- [SQL Server Documentation](https://learn.microsoft.com/en-us/sql/sql-server/)
