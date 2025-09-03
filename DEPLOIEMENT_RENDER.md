# 🚀 Guide de Déploiement sur Render

## Stratégie de déploiement
- **Développement local** : MySQL avec WAMP
- **Production (Render)** : PostgreSQL automatique
- **Migration de données** : SQLite → MySQL → PostgreSQL

## 🔧 Prérequis

1. **Compte Render** : https://render.com (gratuit)
2. **Git Repository** : Code sur GitHub/GitLab
3. **WAMP local fonctionnel** avec votre base MySQL

## 📋 Étape 1 : Préparation locale

### 1.1 Migration vers MySQL (si pas déjà fait)
```bash
# Lancez WAMP, créez la base de données via phpMyAdmin
python migrate_to_mysql_wamp.py
```

### 1.2 Sauvegarde des données
```bash
# Exportez vos données depuis MySQL
python manage.py dumpdata --output=production_data.json --indent=2
```

### 1.3 Test local avec PostgreSQL
```bash
# Copiez le template d'environnement
copy .env.template .env.production

# Éditez .env.production avec :
DB_ENGINE=postgresql
DEBUG=false
```

## 📋 Étape 2 : Configuration Git

### 2.1 Repository GitHub
```bash
git init
git add .
git commit -m "Initial commit - OMAPI Website ready for Render"
git remote add origin https://github.com/VOTRE_USERNAME/omapi-website.git
git push -u origin main
```

### 2.2 Fichiers importants à vérifier
- ✅ `requirements.txt` - Toutes les dépendances
- ✅ `build.sh` - Script de construction
- ✅ `render.yaml` - Configuration Render
- ✅ `manage.py` - Django management
- ✅ Dossier `static/` - Fichiers statiques
- ✅ Dossier `media/` - Fichiers médias

## 📋 Étape 3 : Déploiement Render

### 3.1 Créer le service web
1. Connectez-vous sur https://render.com
2. **New** → **Web Service**
3. Connectez votre repository GitHub
4. Configurez :
   - **Name** : `omapi-website`
   - **Runtime** : `Python 3`
   - **Build Command** : `./build.sh`
   - **Start Command** : `gunicorn omapi_website.wsgi:application`

### 3.2 Variables d'environnement Render
```
PYTHON_VERSION=3.11
RENDER=true
DEBUG=false
SECRET_KEY=[Généré automatiquement par Render]
ALLOWED_HOSTS=.onrender.com
```

### 3.3 Base de données PostgreSQL
1. **New** → **PostgreSQL**
2. **Name** : `omapi-database`
3. **Plan** : Free
4. Copiez la **Database URL** générée

### 3.4 Connecter la base de données
Dans les variables d'environnement du web service :
```
DATABASE_URL=[URL de la base PostgreSQL]
```

## 📋 Étape 4 : Migration des données

### 4.1 Via interface Render
1. Ouvrez la **Web Shell** de votre service
2. Chargez vos données :
```bash
# Si vous avez un fichier de données
python manage.py loaddata production_data.json

# Ou créez un superutilisateur
python manage.py createsuperuser
```

### 4.2 Via script local (alternative)
```bash
# Connectez-vous à la base Render depuis votre PC
python manage_production_data.py upload
```

## 📋 Étape 5 : Configuration post-déploiement

### 5.1 Vérifications
- ✅ Site accessible : https://omapi-website.onrender.com
- ✅ Admin accessible : https://omapi-website.onrender.com/admin/
- ✅ Fichiers statiques (CSS/JS) chargés
- ✅ Uploads de médias fonctionnels

### 5.2 Domaine personnalisé (optionnel)
1. Dans Render → Settings → Custom Domains
2. Ajoutez votre domaine : `www.omapi.mg`
3. Configurez les DNS chez votre registrar

## 🔄 Étape 6 : Workflow de développement

### 6.1 Développement local
```bash
# Développez avec MySQL local (WAMP)
python manage.py runserver
```

### 6.2 Déploiement automatique
```bash
git add .
git commit -m "Nouvelle fonctionnalité"
git push origin main
# Render redéploiera automatiquement
```

### 6.3 Migration de données régulière
```bash
# Export local → Import production
python manage.py dumpdata > latest_data.json
# Uploadez via Render Web Shell
```

## ⚙️ Configuration avancée

### Stockage des médias (recommandé pour production)
Pour les fichiers uploadés, configurez AWS S3 ou Cloudinary :
```python
# Dans settings.py
if IS_PRODUCTION:
    # Configuration AWS S3
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_REGION_NAME = 'us-east-1'
    # ...
```

### Monitoring et logs
1. Render → Logs : Surveillez les erreurs
2. Alertes email en cas de down
3. Métriques de performance

## 🐛 Dépannage

### Erreur 500
```bash
# Vérifiez les logs Render
# Variables d'environnement correctes ?
# Base de données connectée ?
```

### Fichiers statiques non chargés
```bash
# Vérifiez STATIC_URL et STATICFILES_STORAGE
# Relancez collectstatic
```

### Migration de base échoue
```bash
# Vérifiez les modèles Django
# Supprimez les migrations conflictuelles
# Recréez les migrations
```

## 💰 Coûts Render

- **Plan Gratuit** : 750h/mois (suffisant pour tests)
- **Plan Starter** : $7/mois (production légère)
- **PostgreSQL** : Gratuit jusqu'à 1GB

## 🔐 Sécurité Production

- ✅ HTTPS automatique
- ✅ Variables d'environnement chiffrées
- ✅ Sauvegardes automatiques base de données
- ✅ Isolement des environnements

Votre application OMAPI sera maintenant accessible mondialement avec une architecture professionnelle !