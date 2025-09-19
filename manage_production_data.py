#!/usr/bin/env python3
"""
Gestionnaire de données pour la production Render
"""
import os
import sys
import django
import subprocess
import json
from datetime import datetime

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omapi_website.settings')
    django.setup()

def export_local_data():
    """Exporte les données locales vers un fichier JSON"""
    print("\n=== EXPORT DES DONNÉES LOCALES ===")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_export_{timestamp}.json"
    
    try:
        subprocess.run([
            'python', 'manage.py', 'dumpdata', 
            '--output', filename,
            '--indent', '2',
            '--natural-foreign', 
            '--natural-primary'
        ], check=True)
        
        print(f"✅ Données exportées vers {filename}")
        return filename
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'export: {e}")
        return None

def prepare_for_render():
    """Prépare les fichiers pour le déploiement Render"""
    print("\n=== PRÉPARATION POUR RENDER ===")
    
    # Export des données
    data_file = export_local_data()
    if not data_file:
        return False
    
    # Création d'un script d'import pour Render
    import_script = f"""#!/usr/bin/env python3
# Script d'import automatique pour Render
import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omapi_website.settings')
django.setup()

print("Chargement des données en production...")
try:
    execute_from_command_line(['manage.py', 'loaddata', '{data_file}'])
    print("✅ Données chargées avec succès!")
except Exception as e:
    print(f"❌ Erreur: {{e}}")
    # Créer un superutilisateur par défaut
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@omapi.mg', 'admin123')
        print("✅ Superutilisateur créé: admin/admin123")
"""
    
    with open('import_production_data.py', 'w', encoding='utf-8') as f:
        f.write(import_script)
    
    print("✅ Script d'import créé: import_production_data.py")
    print(f"✅ Données prêtes: {data_file}")
    
    return True

def create_git_ignore():
    """Crée un fichier .gitignore approprié"""
    gitignore_content = """# Django
*.pyc
__pycache__/
db.sqlite3
/media/
/staticfiles/

# Environnement
.env
*.env
.venv/
venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Données sensibles
data_export_*.json
backup_*.json

# WAMP spécifique
*.wamp
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore créé")

def check_deployment_readiness():
    """Vérifie que tout est prêt pour le déploiement"""
    print("\n=== VÉRIFICATION DE DÉPLOIEMENT ===")
    
    checks = [
        ('requirements.txt', 'Dépendances Python'),
        ('build.sh', 'Script de build'),
        ('render.yaml', 'Configuration Render'),
        ('manage.py', 'Django management'),
        ('omapi_website/settings.py', 'Configuration Django'),
    ]
    
    all_good = True
    for file_path, description in checks:
        if os.path.exists(file_path):
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} - MANQUANT")
            all_good = False
    
    if all_good:
        print("\n🚀 Prêt pour le déploiement sur Render!")
    else:
        print("\n⚠️ Certains fichiers sont manquants")
    
    return all_good

def main():
    """Menu principal"""
    print("=== GESTIONNAIRE DE DONNÉES PRODUCTION ===\n")
    print("1. Exporter les données locales")
    print("2. Préparer pour Render")
    print("3. Créer .gitignore")
    print("4. Vérifier la préparation")
    print("5. Tout faire")
    
    choice = input("\nChoisissez une option (1-5): ").strip()
    
    setup_django()
    
    if choice == '1':
        export_local_data()
    elif choice == '2':
        prepare_for_render()
    elif choice == '3':
        create_git_ignore()
    elif choice == '4':
        check_deployment_readiness()
    elif choice == '5':
        create_git_ignore()
        prepare_for_render()
        check_deployment_readiness()
    else:
        print("Option non valide")

if __name__ == "__main__":
    main()