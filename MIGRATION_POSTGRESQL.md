# Migration de SQLite vers PostgreSQL - Guide Complet

## 1. Installation de PostgreSQL sur Windows

### Option A: Installation via l'installateur officiel (Recommandé)
1. Téléchargez PostgreSQL depuis : https://www.postgresql.org/download/windows/
2. Exécutez l'installateur et suivez les étapes :
   - Choisissez un mot de passe pour l'utilisateur `postgres` (notez-le !)
   - Port par défaut : 5432
   - Locale par défaut : French, France
3. Ajoutez PostgreSQL au PATH Windows (si pas fait automatiquement) :
   - `C:\Program Files\PostgreSQL\16\bin`

### Option B: Installation via Chocolatey
```powershell
choco install postgresql
```

### Option C: Installation via winget
```powershell
winget install PostgreSQL.PostgreSQL
```

## 2. Vérification de l'installation
```cmd
psql --version
```

## 3. Configuration de la base de données

### Connectez-vous à PostgreSQL
```cmd
psql -U postgres -h localhost
```

### Créez la base de données et l'utilisateur
```sql
CREATE DATABASE omapi_database;
CREATE USER omapi_user WITH PASSWORD 'omapi_password';
GRANT ALL PRIVILEGES ON DATABASE omapi_database TO omapi_user;
ALTER USER omapi_user CREATEDB;
\q
```

## 4. Lancement de la migration

Dans le répertoire du projet, exécutez :
```cmd
python migrate_to_postgresql.py
```

## 5. Configuration alternative avec variables d'environnement

Créez un fichier `.env` dans le répertoire racine :
```env
DB_NAME=omapi_database
DB_USER=omapi_user
DB_PASSWORD=omapi_password
DB_HOST=localhost
DB_PORT=5432
```

## 6. Test de l'application
```cmd
python manage.py runserver
```

## 7. Dépannage

### Erreur de connexion à PostgreSQL
- Vérifiez que le service PostgreSQL est démarré :
  ```cmd
  services.msc
  ```
- Cherchez "postgresql" et assurez-vous qu'il est démarré

### Erreur d'authentification
- Modifiez le fichier `pg_hba.conf` :
  - Localisation typique : `C:\Program Files\PostgreSQL\16\data\pg_hba.conf`
  - Changez `scram-sha-256` en `md5` pour les connexions locales

### Erreur de port
- Vérifiez que le port 5432 n'est pas utilisé par une autre application
- Modifiez le port dans settings.py si nécessaire

## 8. Avantages de PostgreSQL vs SQLite

✅ **PostgreSQL** :
- Meilleure performance pour les gros volumes
- Support complet des transactions ACID
- Types de données avancés (JSON, arrays, etc.)
- Contraintes et index plus sophistiqués
- Adapté à la production

❌ **SQLite** :
- Limité en concurrence
- Pas de gestion des utilisateurs
- Types de données limités
- Adapté uniquement au développement

## 9. Sauvegarde PostgreSQL

### Sauvegarde complète
```cmd
pg_dump -U omapi_user -h localhost omapi_database > backup.sql
```

### Restauration
```cmd
psql -U omapi_user -h localhost omapi_database < backup.sql