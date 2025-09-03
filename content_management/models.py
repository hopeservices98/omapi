from django.db import models
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class TypeActualite(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    couleur = ColorField(default='#FF0000')

    class Meta:
        verbose_name = "Type d'Actualité"
        verbose_name_plural = "Types d'Actualités"

    def __str__(self):
        return self.nom

class InscriptionFormation(models.Model):
    formation = models.ForeignKey('content_management.Formation', on_delete=models.CASCADE, related_name='inscriptions')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_inscription']
        verbose_name = "Inscription Formation"
        verbose_name_plural = "Inscriptions Formations"

    def __str__(self):
        return f"Inscription de {self.nom} {self.prenom} à {self.formation.titre}"

class Actualite(models.Model):
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    contenu = RichTextUploadingField()
    date_publication = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='actualites/', blank=True, null=True)
    type_actualite = models.ForeignKey(TypeActualite, on_delete=models.SET_NULL, null=True, blank=True, related_name='actualites')

    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"

    def __str__(self):
        return self.titre

class GOPI(models.Model):
    numero = models.CharField(max_length=50, unique=True, verbose_name="Numéro de la GOPI")
    date_publication = models.DateField(verbose_name="Date de publication")
    # Nouveaux champs pour les types de publication dans la GOPI
    contient_brevet = models.CharField(max_length=255, blank=True, null=True, verbose_name="Informations Brevet")
    contient_marque = models.CharField(max_length=255, blank=True, null=True, verbose_name="Informations Marque")
    contient_dessin_modele = models.CharField(max_length=255, blank=True, null=True, verbose_name="Informations Dessin ou Modèle")
    contient_nom_commercial = models.CharField(max_length=255, blank=True, null=True, verbose_name="Informations Nom Commercial")

    class Meta:
        ordering = ['-date_publication']
        verbose_name = "GOPI"
        verbose_name_plural = "GOPI"

    def __str__(self):
        return f"GOPI n°{self.numero} du {self.date_publication}"

class Publication(models.Model):
    titre = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=250)
    description = models.TextField(blank=True, null=True)
    fichier = models.FileField(upload_to='publications/', blank=True, null=True)
    date_publication = models.DateField(auto_now_add=True)
    type_publication = models.CharField(max_length=100, blank=True, null=True) # Ex: Rapport annuel, Étude, Statistique

    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Publication"
        verbose_name_plural = "Publications"

    def __str__(self):
        return self.titre

class Formation(models.Model):
    titre = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=250)
    description = models.TextField()
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    lieu = models.CharField(max_length=200, blank=True, null=True)
    formateurs = models.CharField(max_length=250, blank=True, null=True) # Noms des formateurs
    programme = models.FileField(upload_to='programmes_formation/', blank=True, null=True)
    est_active = models.BooleanField(default=True, verbose_name="Formation active")
    public_cible = models.TextField(blank=True, null=True, verbose_name="Public Cible")
    objectifs_apprentissage = models.TextField(blank=True, null=True, verbose_name="Objectifs d'Apprentissage")
    prix = models.CharField(max_length=100, blank=True, null=True, verbose_name="Coût")
    modalites_inscription = models.TextField(blank=True, null=True, verbose_name="Modalités d'Inscription")
    image_presentation = models.ImageField(upload_to='formations/', blank=True, null=True, verbose_name="Image de Présentation")
    duree_heures = models.CharField(max_length=50, blank=True, null=True, verbose_name="Durée en Heures")
    
    TYPE_FORMATION_CHOICES = [
        ('general', 'Général'),
        ('brevets', 'Brevets'),
        ('marques', 'Marques'),
        ('dessins_modeles', 'Dessins & Modèles'),
        ('contentieux', 'Contentieux PI'),
        ('valorisation', 'Valorisation PI'),
    ]
    type_formation = models.CharField(max_length=50, choices=TYPE_FORMATION_CHOICES, default='general', verbose_name="Type de Formation")

    class Meta:
        ordering = ['date_debut']
        verbose_name = "Formation"
        verbose_name_plural = "Formations"

    def __str__(self):
        return self.titre

class Service(models.Model):
    NOM_SERVICE_CHOICES = [
        ('brevet', 'Brevets d\'Invention'),
        ('marque', 'Marques'),
        ('dessin_modele', 'Dessins & Modèles Industriels'),
        ('nom_commercial', 'Noms Commerciaux'),
        ('indication_geographique', 'Indications Géographiques'),
    ]

    nom = models.CharField(max_length=100, choices=NOM_SERVICE_CHOICES, unique=True, verbose_name="Nom du Service")
    slug = models.SlugField(unique=True, max_length=100)
    description_generale = models.TextField(verbose_name="Description Générale")
    pourquoi_proteger = models.TextField(verbose_name="Pourquoi Protéger ?")
    procedure_depot = models.TextField(verbose_name="Procédure de Dépôt/Enregistrement")
    documents_requis = models.TextField(verbose_name="Documents Requis")
    couts_tarifs = models.TextField(blank=True, null=True, verbose_name="Coûts & Tarifs")
    faq = models.TextField(blank=True, null=True, verbose_name="Foire Aux Questions")

    class Meta:
        verbose_name = "Service de Propriété Intellectuelle"
        verbose_name_plural = "Services de Propriété Intellectuelle"

    def __str__(self):
        return self.get_nom_display()


class DocumentTelechargeable(models.Model):
    titre = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    fichier = models.FileField(upload_to='documents_telechargeables/')
    type_document = models.CharField(max_length=100, choices=[('formulaire', 'Formulaire'), ('guide', 'Guide'), ('rapport', 'Rapport'), ('legislation', 'Législation')], blank=True, null=True)
    CATEGORIE_PI_CHOICES = [
        ('marque', 'Marques'),
        ('brevet', 'Brevets'),
        ('dessin_modele', 'Dessins & Modèles Industriels'),
        ('nom_commercial', 'Noms Commerciaux'),
        ('indication_geographique', 'Indications Géographiques'),
        ('procedures_speciales', 'Procédures Spéciales'),
        ('general', 'Général / Divers'),
    ]
    categorie_pi = models.CharField(max_length=50, choices=CATEGORIE_PI_CHOICES, default='general', verbose_name="Catégorie de Propriété Industrielle")
    date_publication = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)

    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Document Téléchargeable"
        verbose_name_plural = "Documents Téléchargeables"

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug: # Générer le slug s'il n'existe pas
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs) # Appeler la méthode save originale
class Annonce(models.Model):
    TYPE_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('info', 'Info'),
        ('alerte', 'Alerte'),
    ]
    
    type_annonce = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    message = models.CharField(max_length=255)
    lien = models.URLField(blank=True, null=True)
    texte_lien = models.CharField(max_length=50, blank=True, null=True)
    est_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Annonce Défilante"
        verbose_name_plural = "Annonces Défilantes"

    def __str__(self):
        return f"[{self.get_type_annonce_display()}] {self.message}"

class Statistique(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la Statistique")
    valeur = models.CharField(max_length=50, verbose_name="Valeur (ex: +44 000)")
    icone_fa = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icône Font Awesome (ex: fas fa-trademark)")
    description = models.CharField(max_length=255, blank=True, null=True)
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        ordering = ['ordre']
        verbose_name = "Statistique Clé"
        verbose_name_plural = "Statistiques Clés"

    def __str__(self):
        return f"{self.nom}: {self.valeur}"

class CarouselSlide(models.Model):
    image = models.ImageField(upload_to='carousel_slides/')
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    lien = models.URLField(blank=True, null=True)
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        ordering = ['ordre']
        verbose_name = "Slide de Carrousel"
        verbose_name_plural = "Slides de Carrousel"

    def __str__(self):
        return self.titre

class Mandataire(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom complet")
    adresse = models.TextField(blank=True, null=True, verbose_name="Adresse")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone 1")
    telephone_2 = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone 2")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Email 1")
    email_2 = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Email 2")
    numero_agrement = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Numéro d'agrément")
    date_agrement = models.DateField(blank=True, null=True, verbose_name="Date d'agrément")
    qualite = models.CharField(max_length=255, blank=True, null=True, verbose_name="Qualité")

    class Meta:
        ordering = ['nom']
        verbose_name = "Mandataire"
        verbose_name_plural = "Mandataires"

    def __str__(self):
        return self.nom


class InscriptionRegistre(models.Model):
    numero_gopi = models.CharField(max_length=50, verbose_name="Numéro de la GOPI")
    date_publication = models.DateField(verbose_name="Date de publication")
    annee_depot_demande = models.IntegerField(verbose_name="Année de dépôt de la demande d'inscription")

    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Inscription au Registre"
        verbose_name_plural = "Inscriptions au Registre"

    def __str__(self):
        return f"Inscription au Registre - GOPI n°{self.numero_gopi} ({self.annee_depot_demande})"


class Renouvellement(models.Model):
    numero_edition = models.CharField(max_length=50, verbose_name="Numéro de l’édition")
    date_publication = models.DateField(verbose_name="Date de publication")
    annee_emission_certificat = models.IntegerField(verbose_name="Année d'émission du certificat de renouvellement")

    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Renouvellement"
        verbose_name_plural = "Renouvellements"

    def __str__(self):
        return f"Renouvellement - Édition n°{self.numero_edition} ({self.annee_emission_certificat})"


class DemandeUtilisateur(models.Model):
    TYPE_DEMANDE_CHOICES = [
        ('gopi', 'Demande GOPI'),
        ('renouvellement', 'Demande Renouvellement'),
        ('inscription_registre', 'Demande Inscription au Registre'),
        ('inscription_formation', 'Inscription Formation'),
    ]

    STATUT_CHOICES = [
        ('nouvelle', 'Nouvelle'),
        ('en_cours', 'En cours'),
        ('traitee', 'Traitée'),
        ('archivee', 'Archivée'),
    ]

    type_demande = models.CharField(max_length=50, choices=TYPE_DEMANDE_CHOICES, verbose_name="Type de Demande")
    nom = models.CharField(max_length=100, verbose_name="Nom Complet")
    email = models.EmailField(verbose_name="Adresse E-mail")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    message = models.TextField(blank=True, null=True, verbose_name="Message")
    date_soumission = models.DateTimeField(auto_now_add=True, verbose_name="Date de Soumission")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='nouvelle', verbose_name="Statut")

    # Liens optionnels vers les objets spécifiques
    gopi_concernee = models.ForeignKey(GOPI, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="GOPI Concernée")
    renouvellement_concerne = models.ForeignKey(Renouvellement, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Renouvellement Concerné")
    inscription_registre_concernee = models.ForeignKey(InscriptionRegistre, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Inscription au Registre Concernée")
    formation_concernee = models.ForeignKey(Formation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Formation Concernée")

    class Meta:
        ordering = ['-date_soumission']
        verbose_name = "Demande Utilisateur"
        verbose_name_plural = "Demandes Utilisateur"

    def __str__(self):
        return f"Demande {self.get_type_demande_display()} de {self.nom} ({self.email})"
