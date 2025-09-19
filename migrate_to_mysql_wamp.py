#!/usr/bin/env python3
"""
Script de migration de SQLite vers MySQL (WAMP) pour le projet OMAPI
"""
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

def setup_django():
    """Configure Django pour la migration"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omapi_website.settings')
    django.setup()

def check_wamp_status():
    """Vérifier que WAMP est actif"""
    print("\n=== VÉRIFICATION WAMP ===")
    print("Assurez-vous que :")
    print("✅ WAMPServer est démarré (icône verte)")
    print("✅ MySQL est actif (port 3306)")
    print("✅ Apache est actif (port 80)")
    print("\nTestez l'accès à phpMyAdmin : http://localhost/phpmyadmin/")
    
def create_mysql_database():
    """Instructions pour créer la base de données MySQL"""
    print("\n=== CRÉATION DE LA BASE DE DONNÉES MYSQL ===")
    print("Option 1 - Via phpMyAdmin (Recommandée):")
    print("1. Ouvrez http://localhost/phpmyadmin/")
    print("2. Créez une nouvelle base : 'omapi_database'")
    print("3. Onglet 'Comptes utilisateurs' → 'Ajouter un compte utilisateur'")
    print("   - Nom : omapi_user")
    print("   - Mot de passe : omapi_password")
    print("   - Cochez 'Créer une base de données portant son nom'")
    print("\nOption 2 - Via ligne de commande:")
    print("mysql -u root -p")
    print("CREATE DATABASE omapi_database CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print("CREATE USER 'omapi_user'@'localhost' IDENTIFIED BY 'omapi_password';")
    print("GRANT ALL PRIVILEGES ON omapi_database.* TO 'omapi_user'@'localhost';")
    print("FLUSH PRIVILEGES;")
    print("EXIT;")

def backup_sqlite_data():
    """Sauvegarde les données SQLite"""
    print("\n=== SAUVEGARDE DES DONNÉES SQLITE ===")
    if os.path.exists('db.sqlite3'):
        print("Création d'une sauvegarde de la base de données SQLite...")
        execute_from_command_line(['manage.py', 'dumpdata', '--output', 'sqlite_backup.json'])
        print("✓ Sauvegarde créée dans sqlite_backup.json")
    else:
        print("❌ Fichier db.sqlite3 non trouvé")

def update_settings_for_mysql():
    """Met à jour settings.py pour MySQL"""
    print("\n=== MISE À JOUR DE LA CONFIGURATION ===")
    print("Modification du fichier settings.py pour MySQL...")
    
    settings_path = 'omapi_website/settings.py'
    
    # Lire le fichier actuel
    with open(settings_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remplacer la configuration PostgreSQL par MySQL
    postgresql_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'omapi_database'),
        'USER': os.getenv('DB_USER', 'omapi_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'omapi_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}"""

    mysql_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'omapi_database'),
        'USER': os.getenv('DB_USER', 'omapi_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'omapi_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}"""
    
    # Remplacer dans le contenu
    if 'django.db.backends.postgresql' in content:
        content = content.replace(postgresql_config, mysql_config)
        
        # Écrire le fichier modifié
        with open(settings_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print("✅ Configuration MySQL appliquée dans settings.py")
    else:
        print("⚠️  Configuration PostgreSQL non trouvée, modification manuelle nécessaire")

def run_mysql_migrations():
    """Lance les migrations pour MySQL"""
    print("\n=== CRÉATION DES TABLES MYSQL ===")
    print("Suppression des anciens fichiers de migration...")
    
    # Optionnel : supprimer les migrations existantes (sauf __init__.py)
    import glob
    for app in ['content_management', 'frontend']:
        migration_files = glob.glob(f'{app}/migrations/[0-9]*.py')
        for file in migration_files:
            os.remove(file)
            print(f"Supprimé : {file}")
    
    print("Création des nouvelles migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    print("Application des migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    print("✅ Tables créées dans MySQL")

def load_data_to_mysql():
    """Charge les données dans MySQL"""
    print("\n=== CHARGEMENT DES DONNÉES ===")
    if os.path.exists('sqlite_backup.json'):
        try:
            execute_from_command_line(['manage.py', 'loaddata', 'sqlite_backup.json'])
            print("✅ Données chargées avec succès dans MySQL")
        except Exception as e:
            print(f"❌ Erreur lors du chargement des données: {e}")
            print("Les données peuvent être importées manuellement via phpMyAdmin")
    else:
        print("❌ Fichier de sauvegarde non trouvé")

def create_superuser():
    """Crée un superutilisateur si nécessaire"""
    print("\n=== CRÉATION DU SUPERUTILISATEUR ===")
    print("Voulez-vous créer un superutilisateur ? (y/N)")
    response = input().lower()
    if response in ['y', 'yes', 'oui']:
        execute_from_command_line(['manage.py', 'createsuperuser'])

def test_connection():
    """Test la connexion MySQL"""
    print("\n=== TEST DE CONNEXION ===")
    try:
        execute_from_command_line(['manage.py', 'dbshell', '--', '-e', 'SELECT VERSION();'])
        print("✅ Connexion MySQL réussie!")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")

def main():
    """Fonction principale de migration"""
    print("=== MIGRATION SQLite vers MySQL (WAMP) ===\n")
    
    check_wamp_status()
    print("Appuyez sur Entrée pour continuer...")
    input()
    
    # Configuration de Django
    setup_django()
    
    # Étapes de migration
    create_mysql_database()
    print("Appuyez sur Entrée après avoir créé la base de données MySQL...")
    input()
    
    backup_sqlite_data()
    update_settings_for_mysql()
    
    print("Redémarrage requis pour prendre en compte les nouveaux paramètres.")
    print("Appuyez sur Entrée pour continuer...")
    input()
    
    # Re-setup Django avec la nouvelle config
    setup_django()
    
    run_mysql_migrations()
    load_data_to_mysql()
    test_connection()
    create_superuser()
    
    print("\n=== MIGRATION TERMINÉE ===")
    print("✅ Votre application utilise maintenant MySQL avec WAMP!")
    print("🌐 Interface phpMyAdmin : http://localhost/phpmyadmin/")
    print("🚀 Testez votre application : python manage.py runserver")

if __name__ == "__main__":
    main()