from django.core.management.base import BaseCommand
from django.utils import timezone
from django.template.defaultfilters import slugify

from content_management.models import Actualite, GOPI, Publication, Formation, Service, DocumentTelechargeable

class Command(BaseCommand):
    help = 'Populates the database with test data for OMAPI website.'

    def handle(self, *args, **options):
        self.stdout.write("Populating database with test data...")

        # Clear existing data
        Actualite.objects.all().delete()
        GOPI.objects.all().delete()
        Publication.objects.all().delete()
        Formation.objects.all().delete()
        Service.objects.all().delete()
        DocumentTelechargeable.objects.all().delete()

        # Actualites
        Actualite.objects.create(
            titre="Lancement de la nouvelle plateforme OMAPI",
            slug=slugify("Lancement de la nouvelle plateforme OMAPI"),
            contenu="Nous sommes ravis d'annoncer le lancement de notre toute nouvelle plateforme en ligne, conçue pour faciliter l'accès à nos services et informations.",
            date_publication=timezone.now() - timezone.timedelta(days=10),
            type_actualite='article'
        )
        Actualite.objects.create(
            titre="Webinaire sur la protection des marques",
            slug=slugify("Webinaire sur la protection des marques"),
            contenu="Rejoignez notre webinaire gratuit pour tout savoir sur l'importance et les procédures d'enregistrement des marques.",
            date_publication=timezone.now() - timezone.timedelta(days=5),
            type_actualite='evenement'
        )
        Actualite.objects.create(
            titre="Communiqué : Changement d'horaires d'ouverture",
            slug=slugify("Communiqué : Changement d'horaires d'ouverture"),
            contenu="Suite aux récentes mesures sanitaires, nos horaires d'ouverture sont ajustés. Veuillez consulter notre page Contact pour plus de détails.",
            date_publication=timezone.now() - timezone.timedelta(days=2),
            type_actualite='communique'
        )

        # GOPI
        GOPI.objects.create(
            numero="2024-01",
            date_publication=timezone.now() - timezone.timedelta(days=30),
            description="Première édition de la Gazette Officielle de la Propriété Industrielle pour l'année 2024."
        )
        GOPI.objects.create(
            numero="2024-02",
            date_publication=timezone.now() - timezone.timedelta(days=15),
            description="Deuxième édition de la Gazette, incluant les dernières décisions et enregistrements."
        )

        # Publications
        Publication.objects.create(
            titre="Rapport Annuel 2023 de l'OMAPI",
            slug=slugify("Rapport Annuel 2023 de l'OMAPI"),
            description="Synthèse des activités et des réalisations de l'Office Malagasy de la Propriété Industrielle pour l'année 2023.",
            type_publication='Rapport annuel'
        )
        Publication.objects.create(
            titre="Étude sur l'impact économique des brevets à Madagascar",
            slug=slugify("Étude sur l'impact économique des brevets à Madagascar"),
            description="Analyse approfondie de la contribution des brevets à l'économie nationale.",
            type_publication='Étude'
        )

        # Formations
        Formation.objects.create(
            titre="Initiation à la Propriété Industrielle",
            slug=slugify("Initiation à la Propriété Industrielle"),
            description="Formation de base pour comprendre les concepts fondamentaux de la PI.",
            date_debut=timezone.now() + timezone.timedelta(days=10),
            date_fin=timezone.now() + timezone.timedelta(days=12),
            lieu="En ligne",
            formateurs="Équipe de l'OMAPI",
            type_formation='general'
        )
        Formation.objects.create(
            titre="Maîtriser le dépôt de marque",
            slug=slugify("Maîtriser le dépôt de marque"),
            description="Formation pratique sur les étapes et les astuces pour un dépôt de marque réussi.",
            date_debut=timezone.now() + timezone.timedelta(days=20),
            date_fin=timezone.now() + timezone.timedelta(days=21),
            lieu="Antananarivo",
            formateurs="Experts externes",
            type_formation='marques'
        )
        Formation.objects.create(
            titre="Droit des Brevets : Fondamentaux et Pratique",
            slug=slugify("Droit des Brevets Fondamentaux et Pratique"),
            description="Explorez les principes fondamentaux du droit des brevets, de la recherche d'antériorité à la délivrance et à la défense de vos inventions.",
            date_debut=timezone.now() + timezone.timedelta(days=30),
            date_fin=timezone.now() + timezone.timedelta(days=32),
            lieu="En ligne",
            formateurs="Expert en brevets",
            type_formation='brevets'
        )
        Formation.objects.create(
            titre="Stratégies de Protection des Marques",
            slug=slugify("Strategies de Protection des Marques"),
            description="Apprenez à élaborer une stratégie efficace pour l'enregistrement, la gestion et la défense de vos marques commerciales.",
            date_debut=timezone.now() + timezone.timedelta(days=45),
            date_fin=timezone.now() + timezone.timedelta(days=47),
            lieu="Antananarivo",
            formateurs="Consultant en marques",
            type_formation='marques'
        )
        Formation.objects.create(
            titre="Dessins et Modèles Industriels : Création et Enregistrement",
            slug=slugify("Dessins et Modeles Industriels Creation et Enregistrement"),
            description="Maîtrisez le processus de protection de l'apparence de vos produits par les dessins et modèles industriels.",
            date_debut=timezone.now() + timezone.timedelta(days=60),
            date_fin=timezone.now() + timezone.timedelta(days=61),
            lieu="En ligne",
            formateurs="Designer et juriste PI",
            type_formation='dessins_modeles'
        )
        Formation.objects.create(
            titre="Contentieux en Propriété Industrielle",
            slug=slugify("Contentieux en Propriete Industrielle"),
            description="Comprenez les bases des litiges en PI, de la contrefaçon aux actions en nullité, et les stratégies de résolution.",
            date_debut=timezone.now() + timezone.timedelta(days=75),
            date_fin=timezone.now() + timezone.timedelta(days=77),
            lieu="Antananarivo",
            formateurs="Avocat spécialisé PI",
            type_formation='contentieux'
        )
        Formation.objects.create(
            titre="Valorisation des Actifs Immatériels (PI)",
            slug=slugify("Valorisation des Actifs Immateriels PI"),
            description="Découvrez comment identifier, évaluer et valoriser vos actifs de propriété industrielle pour maximiser leur potentiel commercial.",
            date_debut=timezone.now() + timezone.timedelta(days=90),
            date_fin=timezone.now() + timezone.timedelta(days=91),
            lieu="En ligne",
            formateurs="Expert en valorisation PI",
            type_formation='valorisation'
        )

        # Services
        Service.objects.create(
            nom='brevet',
            slug=slugify('Brevets d\'Invention'),
            description_generale="Les brevets protègent les inventions techniques. Ils confèrent à leur titulaire un monopole d'exploitation sur l'invention.",
            pourquoi_proteger="Protéger votre brevet vous assure l'exclusivité de votre invention et vous permet d'en tirer profit.",
            procedure_depot="La procédure de dépôt implique plusieurs étapes : recherche d'antériorité, rédaction de la demande, dépôt et examen.",
            documents_requis="Description de l'invention, revendications, dessins techniques, résumé."
        )
        Service.objects.create(
            nom='marque',
            slug=slugify('Marques'),
            description_generale="Une marque est un signe distinctif qui permet d'identifier les produits ou services d'une entreprise.",
            pourquoi_proteger="L'enregistrement d'une marque vous donne le droit exclusif de l'utiliser et de la défendre contre la contrefaçon.",
            procedure_depot="La procédure d'enregistrement comprend le dépôt, l'examen de la demande et la publication.",
            documents_requis="Représentation de la marque, liste des produits et services."
        )
        Service.objects.create(
            nom='dessin_modele',
            slug=slugify('Dessins & Modèles Industriels'),
            description_generale="Les dessins et modèles industriels protègent l'apparence ornementale ou esthétique d'un produit.",
            pourquoi_proteger="La protection de votre dessin ou modèle vous confère un droit exclusif d'exploitation et vous permet de lutter contre la contrefaçon.",
            procedure_depot="La procédure de dépôt implique le dépôt de la demande, l'examen et la publication.",
            documents_requis="Représentations visuelles du dessin ou modèle, description, indication des produits concernés."
        )
        Service.objects.create(
            nom='nom_commercial',
            slug=slugify('Noms Commerciaux'),
            description_generale="Le nom commercial est le nom sous lequel une entreprise est connue et exerce son activité.",
            pourquoi_proteger="L'enregistrement de votre nom commercial vous donne le droit exclusif de l'utiliser dans votre activité et de vous opposer à son utilisation non autorisée par des tiers.",
            procedure_depot="La procédure d'enregistrement implique le dépôt d'une demande auprès de l'OMAPI.",
            documents_requis="Justificatifs d'identité, adresse de l'entreprise, description de l'activité, exemplaire du nom commercial."
        )

        # Documents Telechargeables
        DocumentTelechargeable.objects.create(
            titre="Formulaire de Demande de Brevet",
            description="Formulaire officiel à remplir pour déposer une demande de brevet d'invention.",
            type_document='formulaire'
        )
        DocumentTelechargeable.objects.create(
            titre="Guide du Déposant de Marque",
            description="Guide complet pour accompagner les déposants dans leurs démarches d'enregistrement de marque.",
            type_document='guide'
        )
        DocumentTelechargeable.objects.create(
            titre="Loi sur la Propriété Industrielle",
            description="Texte intégral de la loi régissant la propriété industrielle à Madagascar.",
            type_document='legislation'
        )
        DocumentTelechargeable.objects.create(
            titre="Offre de Formation OMAPI 2024",
            description="Catalogue des formations proposées par l'OMAPI pour l'année 2024.",
            type_document='formation'
        )

        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))