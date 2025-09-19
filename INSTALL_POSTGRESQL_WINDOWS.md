# Installation PostgreSQL sur Windows 10

## ⚠️ Winget non disponible - Alternatives

### Option 1: Installation manuelle (Recommandée)

1. **Télécharger PostgreSQL :**
   - Allez sur : https://www.postgresql.org/download/windows/
   - Cliquez sur "Download the installer"
   - Choisissez la version 16.x pour Windows x86-64

2. **Lancer l'installation :**
   - Exécutez le fichier `.exe` téléchargé
   - Suivez l'assistant d'installation :
     - Composants : Cochez tout (PostgreSQL Server, pgAdmin 4, Stack Builder, Command Line Tools)
     - Répertoire : Laissez par défaut `C:\Program Files\PostgreSQL\16`
     - **IMPORTANT** : Notez le mot de passe que vous définissez pour l'utilisateur `postgres`
     - Port : Laissez 5432
     - Locale : French, France

### Option 2: Chocolatey (si vous l'avez)

```powershell
# Vérifiez si Chocolatey est installé
choco --version

# Si oui, installez PostgreSQL
choco install postgresql
```

### Option 3: Téléchargement direct via PowerShell

```powershell
# Télécharger l'installateur
Invoke-WebRequest -Uri "https://get.enterprisedb.com/postgresql/postgresql-16.6-1-windows-x64.exe" -OutFile "postgresql-installer.exe"

# Lancer l'installation (interface graphique)
.\postgresql-installer.exe
```

## ✅ Vérification de l'installation

Après installation, redémarrez votre terminal et testez :

```cmd
psql --version
```

Si la commande n'est pas reconnue, ajoutez manuellement au PATH :
- Ouvrez "Variables d'environnement système"
- Ajoutez `C:\Program Files\PostgreSQL\16\bin` au PATH

## 🗄️ Configuration de la base de données

1. **Ouvrez l'invite de commandes en tant qu'administrateur**

2. **Connectez-vous à PostgreSQL :**
```cmd
psql -U postgres -h localhost
```

3. **Créez la base de données et l'utilisateur :**
```sql
CREATE DATABASE omapi_database;
CREATE USER omapi_user WITH PASSWORD 'omapi_password';
GRANT ALL PRIVILEGES ON DATABASE omapi_database TO omapi_user;
ALTER USER omapi_user CREATEDB;
\q
```

## 🚀 Lancer la migration

Une fois PostgreSQL installé et configuré :

```cmd
cd omapi-website-main
python migrate_to_postgresql.py
```

## 🔧 Dépannage Windows 10

### Service PostgreSQL
Si PostgreSQL ne démarre pas :
1. Appuyez sur `Win + R`, tapez `services.msc`
2. Cherchez "postgresql-x64-16"
3. Clic droit → "Démarrer"

### Problème de firewall
Si connexion refusée :
1. Panneau de configuration → Pare-feu Windows
2. Autoriser PostgreSQL à travers le pare-feu

### Alternative locale : Docker (optionnel)
Si vous avez Docker Desktop :
```cmd
docker run -d --name postgres-omapi -e POSTGRES_PASSWORD=omapi_password -e POSTGRES_USER=omapi_user -e POSTGRES_DB=omapi_database -p 5432:5432 postgres:16