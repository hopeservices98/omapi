# 📁 Structure du Projet OMAPI

## Répertoires

```
omapi-website-main/
└── omapi-website-main/          ← RÉPERTOIRE DE TRAVAIL
    ├── manage.py                 ← Django management
    ├── omapi_website/           ← Configuration Django
    ├── content_management/      ← App content management  
    ├── frontend/                ← App frontend
    ├── static/                  ← Fichiers statiques
    ├── media/                   ← Fichiers médias
    ├── requirements.txt         ← Dépendances Python
    ├── build.sh                 ← Script build Render
    ├── render.yaml              ← Config Render
    └── Scripts de migration...
```

## 🚀 Pour travailler sur le projet

**Toujours naviguer dans le bon répertoire :**

```powershell
cd C:\Users\AZENIK\Downloads\omapi-website-main\omapi-website-main
```

**Puis exécuter les commandes :**

```powershell
# Migration MySQL (WAMP)
python migrate_to_mysql_wamp.py

# Migration PostgreSQL
python migrate_to_postgresql.py  

# Gestion production
python manage_production_data.py

# Serveur développement
python manage.py runserver
```

## ⚠️ Erreur Commune

Si vous obtenez `can't open file`, c'est que vous êtes dans le mauvais répertoire !

**Vérifiez votre répertoire courant :**
```powershell
pwd  # Doit afficher: C:\Users\AZENIK\Downloads\omapi-website-main\omapi-website-main
```

**Listez les fichiers :**
```powershell
dir  # Doit montrer manage.py, requirements.txt, etc.