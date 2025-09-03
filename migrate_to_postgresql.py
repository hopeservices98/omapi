#!/usr/bin/env python3
"""
Script de migration de SQLite vers PostgreSQL pour le projet OMAPI
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

def create_postgresql_database():
    """Instructions pour créer la base de données PostgreSQL"""
    print("\n=== CRÉATION DE LA BASE DE DONNÉES POSTGRESQL ===")
    print("Exécutez les commandes suivantes dans psql (en tant qu'utilisateur postgres):")
    print("CREATE DATABASE omapi_database;")
    print("CREATE USER omapi_user WITH PASSWORD 'omapi_password';")
    print("GRANT ALL PRIVILEGES ON DATABASE omapi_database TO omapi_user;")
    print("ALTER USER omapi_user CREATEDB;")  # Nécessaire pour les tests
    print("\n")

def backup_sqlite_data():
    """Sauvegarde les données SQLite"""
    print("\n=== SAUVEGARDE DES DONNÉES SQLITE ===")
    if os.path.exists('db.sqlite3'):
        print("Création d'une sauvegarde de la base de données SQLite...")
        execute_from_command_line(['manage.py', 'dumpdata', '--output', 'sqlite_backup.json'])
        print("✓ Sauvegarde créée dans sqlite_backup.json")
    else:
        print("❌ Fichier db.sqlite3 non trouvé")

def run_postgresql_migrations():
    """Lance les migrations pour PostgreSQL"""
    print("\n=== CRÉATION DES TABLES POSTGRESQL ===")
    print("Création des migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    print("Application des migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    print("✓ Tables créées dans PostgreSQL")

def load_data_to_postgresql():
    """Charge les données dans PostgreSQL"""
    print("\n=== CHARGEMENT DES DONNÉES ===")
    if os.path.exists('sqlite_backup.json'):
        try:
            execute_from_command_line(['manage.py', 'loaddata', 'sqlite_backup.json'])
            print("✓ Données chargées avec succès dans PostgreSQL")
        except Exception as e:
            print(f"❌ Erreur lors du chargement des données: {e}")
            print("Vous devrez peut-être charger les données manuellement.")
    else:
        print("❌ Fichier de sauvegarde non trouvé")

def create_superuser():
    """Crée un superutilisateur si nécessaire"""
    print("\n=== CRÉATION DU SUPERUTILISATEUR ===")
    print("Voulez-vous créer un superutilisateur ? (y/N)")
    response = input().lower()
    if response in ['y', 'yes', 'oui']:
        execute_from_command_line(['manage.py', 'createsuperuser'])

def main():
    """Fonction principale de migration"""
    print("=== MIGRATION SQLite vers PostgreSQL ===\n")
    
    # Configuration de Django
    setup_django()
    
    # Étapes de migration
    create_postgresql_database()
    
    print("Appuyez sur Entrée après avoir créé la base de données PostgreSQL...")
    input()
    
    backup_sqlite_data()
    run_postgresql_migrations()
    load_data_to_postgresql()
    create_superuser()
    
    print("\n=== MIGRATION TERMINÉE ===")
    print("Votre application utilise maintenant PostgreSQL!")
    print("N'oubliez pas de tester votre application avec: python manage.py runserver")

if __name__ == "__main__":
    main()