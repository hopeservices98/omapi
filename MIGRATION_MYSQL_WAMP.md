# Migration SQLite vers MySQL avec WAMP

## 🔧 Configuration WAMP pour Django

### 1. Vérifier WAMP
- Lancez WAMPServer
- Vérifiez que l'icône WAMP est verte (tous services démarrés)
- MySQL devrait être actif sur le port 3306

### 2. Créer la base de données MySQL

**Via phpMyAdmin :**
1. Ouvrez http://localhost/phpmyadmin/
2. Créez une nouvelle base de données : `omapi_database`
3. Onglet "Privilèges" → "Ajouter un compte utilisateur"
   - Nom d'utilisateur : `omapi_user`
   - Mot de passe : `omapi_password`
   - Cochez "Créer une base de données portant son nom et accorder tous les privilèges"

**Via ligne de commande MySQL :**
```sql
# Connectez-vous à MySQL (mot de passe root par défaut vide dans WAMP)
mysql -u root -p

# Créez la base et l'utilisateur
CREATE DATABASE omapi_database CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'omapi_user'@'localhost' IDENTIFIED BY 'omapi_password';
GRANT ALL PRIVILEGES ON omapi_database.* TO 'omapi_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Installer le driver MySQL pour Python

```cmd
cd omapi-website-main
pip install mysqlclient
```

Si `mysqlclient` pose problème, utilisez l'alternative :
```cmd
pip install PyMySQL
```

### 4. Configuration Django pour MySQL

Nous devons modifier le fichier settings.py pour utiliser MySQL au lieu de PostgreSQL.

### 5. Script de migration MySQL

Le script `migrate_to_mysql_wamp.py` automatisera tout le processus.

## 🚀 Avantages MySQL avec WAMP

✅ **Déjà installé** avec WAMP
✅ **Interface graphique** avec phpMyAdmin  
✅ **Configuration automatique** des services
✅ **Compatible production** 
✅ **Performance excellente** pour applications Django
✅ **Communauté importante** et documentation riche

## 🔄 Processus de migration

1. Sauvegarde SQLite → JSON
2. Création des tables MySQL
3. Import des données
4. Test de l'application

Cette solution est plus rapide car vous évitez l'installation de PostgreSQL !