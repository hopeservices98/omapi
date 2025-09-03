from django.shortcuts import render, get_object_or_404, redirect
from content_management.models import Actualite, GOPI, Publication, Formation, Service, DocumentTelechargeable, Annonce, Statistique, CarouselSlide, Mandataire, InscriptionFormation, Renouvellement, InscriptionRegistre, DemandeUtilisateur
from django.utils import timezone
from django.core.mail import send_mail
from itertools import groupby
from operator import attrgetter

def index(request):
    latest_actualites = Actualite.objects.all().order_by('-date_publication')[:3]
    annonces = Annonce.objects.filter(est_active=True).order_by('date_creation')
    statistiques = Statistique.objects.all().order_by('ordre')
    carousel_slides = CarouselSlide.objects.all().order_by('ordre') # Récupérer les slides du carrousel
    context = {
        'latest_actualites': latest_actualites,
        'annonces': annonces,
        'statistiques': statistiques,
        'carousel_slides': carousel_slides, # Ajouter les slides au contexte
    }
    return render(request, 'frontend/index.html', context)

def actualites_list(request):
    actualites = Actualite.objects.all()
    return render(request, 'frontend/actualites_list.html', {'actualites': actualites})

def actualite_detail(request, slug):
    actualite = get_object_or_404(Actualite, slug=slug)
    return render(request, 'frontend/actualite_detail.html', {'actualite': actualite})

def gopi_list(request):
    gopis = GOPI.objects.all().order_by('-date_publication')
    renouvellements = Renouvellement.objects.all().order_by('-date_publication')
    inscriptions_registre = InscriptionRegistre.objects.all().order_by('-date_publication')
    context = {
        'gopis': gopis,
        'renouvellements': renouvellements,
        'inscriptions_registre': inscriptions_registre,
    }
    return render(request, 'frontend/gopi_list.html', context)



def gopi_request_form(request, numero):
    gopi = get_object_or_404(GOPI, numero=numero)
    if request.method == 'POST':
        nom = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        DemandeUtilisateur.objects.create(
            type_demande='gopi',
            nom=nom,
            email=email,
            message=message,
            gopi_concernee=gopi
        )
        success_message = 'Votre demande a été envoyée avec succès. Nous vous contacterons bientôt.'
        return render(request, 'frontend/gopi_request_form.html', {'gopi': gopi, 'success_message': success_message})
    else:
        return render(request, 'frontend/gopi_request_form.html', {'gopi': gopi})

def publications_list(request):
    publications = Publication.objects.all()
    return render(request, 'frontend/publications_list.html', {'publications': publications})

def formations_list(request):
    type_filter = request.GET.get('type')
    lieu_filter = request.GET.get('lieu')

    formations = Formation.objects.all() # Afficher toutes les formations

    if type_filter:
        formations = formations.filter(type_formation=type_filter)

    if lieu_filter:
        formations = formations.filter(lieu__icontains=lieu_filter)

    formations = formations.order_by('date_debut') # Supprimer la limite de 5 formations
    
    context = {
        'formations': formations,
        'selected_type': type_filter,
        'selected_lieu': lieu_filter,
    }
    return render(request, 'frontend/formations_list.html', context)


def publication_detail(request, slug):
    publication = get_object_or_404(Publication, slug=slug)
    return render(request, 'frontend/publication_detail.html', {'publication': publication})


def formation_detail(request, slug):
    formation = get_object_or_404(Formation, slug=slug)
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        message = request.POST.get('message')

        # Enregistrer l'inscription dans DemandeUtilisateur
        DemandeUtilisateur.objects.create(
            type_demande='inscription_formation',
            nom=f"{nom} {prenom}", # Concaténer nom et prénom
            email=email,
            telephone=telephone,
            message=message,
            formation_concernee=formation
        )
        
        # Afficher un message de succès
        success_message = "Votre inscription a été enregistrée avec succès. Nous vous contacterons bientôt."
        return render(request, 'frontend/formation_detail.html', {
            'formation': formation,
            'success_message': success_message
        })
    else:
        return render(request, 'frontend/formation_detail.html', {'formation': formation})

def formation_request_form(request):
    if request.method == 'POST':
        # Process the form data
        # In a real application, you would send an email here
        return render(request, 'frontend/formation_request_form.html', {'success_message': 'Votre demande de formation a été envoyée avec succès. Nous vous contacterons bientôt.'})
    else:
        return render(request, 'frontend/formation_request_form.html')

def services_list(request):
    services = Service.objects.all()
    for service in services:
        if service.nom == 'brevet':
            service.redirect_url = '/depot-brevet/' # Using direct path for simplicity, can use reverse('depot_brevet')
        elif service.nom == 'marque':
            service.redirect_url = '/depot-marque/' # Using direct path for simplicity, can use reverse('depot_marque')
        elif service.nom == 'dessin_modele':
            service.redirect_url = '/depot-dessin-modele/' # Using direct path for simplicity, can use reverse('depot_dessin_modele')
        elif service.nom == 'nom_commercial':
            service.redirect_url = '/depot-nom-commercial/' # Using direct path for simplicity, can use reverse('depot_nom_commercial')
        else:
            service.redirect_url = f'/services/{service.slug}/' # Default to service_detail
    return render(request, 'frontend/services_list.html', {'services': services})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'frontend/service_detail.html', {'service': service})

def documents_list(request):
    documents = DocumentTelechargeable.objects.all()
    return render(request, 'frontend/documents_list.html', {'documents': documents})

def about(request):
    return render(request, 'frontend/about.html')
def missions(request):
    return render(request, 'frontend/missions.html')


def document_detail(request, pk): # Utilisation de pk pour les documents
    document = get_object_or_404(DocumentTelechargeable, pk=pk)
    return render(request, 'frontend/document_detail.html', {'document': document})


def organisation(request):
    return render(request, 'frontend/organisation.html')
def depot_marque(request):
    return render(request, 'frontend/depot_marque.html')

def depot_brevet(request):
    return render(request, 'frontend/depot_brevet.html')

def depot_dessin_modele(request):
    return render(request, 'frontend/depot_dessin_modele.html')

def depot_nom_commercial(request):
    return render(request, 'frontend/depot_nom_commercial.html')

def formulaires(request):
    formulaires_list = DocumentTelechargeable.objects.filter(type_document='formulaire').order_by('categorie_pi', 'pk')
    
    grouped_formulaires = {}
    for key, group in groupby(formulaires_list, attrgetter('categorie_pi')):
        display_name = dict(DocumentTelechargeable.CATEGORIE_PI_CHOICES).get(key, key)
        grouped_formulaires[display_name] = list(group)

    context = {
        'grouped_formulaires': grouped_formulaires,
        'CATEGORIE_PI_CHOICES': DocumentTelechargeable.CATEGORIE_PI_CHOICES
    }
    return render(request, 'frontend/formulaires.html', context)

from itertools import groupby
from operator import attrgetter

def guides(request):
    guides_list = DocumentTelechargeable.objects.filter(type_document='guide').order_by('categorie_pi', '-date_publication')
    
    grouped_guides = {}
    for key, group in groupby(guides_list, attrgetter('categorie_pi')):
        display_name = dict(DocumentTelechargeable.CATEGORIE_PI_CHOICES).get(key, key)
        grouped_guides[display_name] = list(group)

    context = {
        'grouped_guides': grouped_guides,
        'CATEGORIE_PI_CHOICES': DocumentTelechargeable.CATEGORIE_PI_CHOICES # Passer les choix au template pour les titres
    }
    return render(request, 'frontend/guides.html', context)


def legislation(request):
    return render(request, 'frontend/legislation.html')

def faq(request):
    return render(request, 'frontend/faq.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Simple validation
        if not name or not email or not message:
            error_message = "Tous les champs sont obligatoires."
            return render(request, 'frontend/contact.html', {
                'error_message': error_message,
                'name': name,
                'email': email,
                'message': message
            })

        try:
            send_mail(
                f'Nouveau message de contact de {name}',
                f'Nom: {name}\nEmail: {email}\nMessage: {message}',
                email, # From email (can be a dummy email for now)
                ['daniel.razanajaona@gmail.com'], # To email (replace with your actual recipient email)
                fail_silently=False,
            )
            success_message = "Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais."
            return render(request, 'frontend/contact.html', {'success_message': success_message})
        except Exception as e:
            error_message = f"Une erreur est survenue lors de l'envoi de votre message: {e}"
            return render(request, 'frontend/contact.html', {
                'error_message': error_message,
                'name': name,
                'email': email,
                'message': message
            })
    return render(request, 'frontend/contact.html')


def procedures(request):
    return render(request, 'frontend/procedures.html')

def procedures_internationales(request):
    return render(request, 'frontend/procedures_internationales.html')

def mandataires_list(request):
    mandataires = Mandataire.objects.all().order_by('nom')
    return render(request, 'frontend/mandataires_list.html', {'mandataires': mandataires})

import csv
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





def renouvellement_request_form(request, pk):
    renouvellement = get_object_or_404(Renouvellement, pk=pk)
    if request.method == 'POST':
        nom = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        DemandeUtilisateur.objects.create(
            type_demande='renouvellement',
            nom=nom,
            email=email,
            message=message,
            renouvellement_concerne=renouvellement
        )
        success_message = 'Votre demande de renouvellement a été envoyée avec succès. Nous vous contacterons bientôt.'
        return render(request, 'frontend/renouvellement_request_form.html', {'renouvellement': renouvellement, 'success_message': success_message})
    else:
        return render(request, 'frontend/renouvellement_request_form.html', {'renouvellement': renouvellement})


def inscription_registre_request_form(request, pk):
    inscription = get_object_or_404(InscriptionRegistre, pk=pk)
    if request.method == 'POST':
        nom = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        DemandeUtilisateur.objects.create(
            type_demande='inscription_registre',
            nom=nom,
            email=email,
            message=message,
            inscription_registre_concernee=inscription
        )
        success_message = 'Votre demande d\'inscription au registre a été envoyée avec succès. Nous vous contacterons bientôt.'
        return render(request, 'frontend/inscription_registre_request_form.html', {'inscription': inscription, 'success_message': success_message})
    else:
        return render(request, 'frontend/inscription_registre_request_form.html', {'inscription': inscription})


from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import Count

@staff_member_required
def liste_demandes(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        demande_ids = request.POST.getlist('demande_ids')
        demandes_a_modifier = DemandeUtilisateur.objects.filter(id__in=demande_ids)

        if action == 'delete_selected':
            demandes_a_modifier.delete()
        elif action == 'mark_as_nouvelle':
            demandes_a_modifier.update(statut='nouvelle')
        elif action == 'mark_as_en_cours':
            demandes_a_modifier.update(statut='en_cours')
        elif action == 'mark_as_traitee':
            demandes_a_modifier.update(statut='traitee')
        elif action == 'mark_as_archivee':
            demandes_a_modifier.update(statut='archivee')

    # Calcul des KPIs avant tout filtrage
    all_demandes = DemandeUtilisateur.objects.all()
    total_demandes = all_demandes.count()
    status_counts = all_demandes.values('statut').annotate(count=Count('statut'))
    
    kpis = {
        'total': total_demandes,
        'nouvelle': 0,
        'en_cours': 0,
        'traitee': 0,
        'archivee': 0,
    }
    for item in status_counts:
        if item['statut'] in kpis:
            kpis[item['statut']] = item['count']

    # Le queryset pour la liste, qui sera filtré
    demandes_list = all_demandes.all()

    # Filtrage
    type_filter = request.GET.get('type')
    statut_filter = request.GET.get('statut')
    search_query = request.GET.get('q')

    if type_filter:
        demandes_list = demandes_list.filter(type_demande=type_filter)
    if statut_filter:
        demandes_list = demandes_list.filter(statut=statut_filter)
    if search_query:
        demandes_list = demandes_list.filter(
            Q(nom__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(message__icontains=search_query) |
            Q(gopi_concernee__numero__icontains=search_query) |
            Q(renouvellement_concerne__numero_edition__icontains=search_query) |
            Q(inscription_registre_concernee__numero_gopi__icontains=search_query) |
            Q(formation_concernee__titre__icontains=search_query)
        )

    # Tri
    sort_by = request.GET.get('sort_by', '-date_soumission') # Tri par défaut
    demandes_list = demandes_list.order_by(sort_by)

    # Pagination
    paginator = Paginator(demandes_list, 10) # 10 demandes par page
    page = request.GET.get('page')
    try:
        demandes_page = paginator.page(page)
    except PageNotAnInteger:
        demandes_page = paginator.page(1)
    except EmptyPage:
        demandes_page = paginator.page(paginator.num_pages)

    context = {
        'demandes': demandes_page,
        'kpis': kpis,
        'type_filter': type_filter,
        'statut_filter': statut_filter,
        'search_query': search_query,
        'sort_by': sort_by,
        'TYPE_DEMANDE_CHOICES': DemandeUtilisateur.TYPE_DEMANDE_CHOICES,
        'STATUT_CHOICES': DemandeUtilisateur.STATUT_CHOICES,
    }
    return render(request, 'frontend/liste_demandes.html', context)


@staff_member_required
def export_demandes(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="demandes_omapi.csv"'

    writer = csv.writer(response)
    writer.writerow(['Type de Demande', 'Nom', 'Email', 'Telephone', 'Message', 'Date de Soumission', 'Statut', 'Objet Concerne'])

    demandes = DemandeUtilisateur.objects.all()

    # Appliquer les mêmes filtres que la vue liste_demandes
    type_filter = request.GET.get('type')
    statut_filter = request.GET.get('statut')
    search_query = request.GET.get('q')

    if type_filter:
        demandes = demandes.filter(type_demande=type_filter)
    if statut_filter:
        demandes = demandes.filter(statut=statut_filter)
    if search_query:
        demandes = demandes.filter(
            Q(nom__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(message__icontains=search_query) |
            Q(gopi_concernee__numero__icontains=search_query) |
            Q(renouvellement_concerne__numero_edition__icontains=search_query) |
            Q(inscription_registre_concernee__numero_gopi__icontains=search_query) |
            Q(formation_concernee__titre__icontains=search_query)
        )

    # Pas de pagination pour l'export, on exporte tout ce qui est filtré
    for demande in demandes:
        objet_concerne = "N/A"
        if demande.gopi_concernee:
            objet_concerne = f"GOPI n°{demande.gopi_concernee.numero}"
        elif demande.renouvellement_concerne:
            objet_concerne = f"Renouvellement n°{demande.renouvellement_concerne.numero_edition}"
        elif demande.inscription_registre_concernee:
            objet_concerne = f"Inscription Registre n°{demande.inscription_registre_concernee.numero_gopi}"
        elif demande.formation_concernee:
            objet_concerne = f"Formation: {demande.formation_concernee.titre}"

        writer.writerow([
            demande.get_type_demande_display(),
            demande.nom,
            demande.email,
            demande.telephone if demande.telephone else 'N/A',
            demande.message if demande.message else 'Aucun',
            demande.date_soumission.strftime("%d/%m/%Y %H:%M"),
            demande.get_statut_display(),
            objet_concerne,
        ])

    return response


from django.http import JsonResponse

@staff_member_required
def demande_detail_ajax(request, pk):
    demande = get_object_or_404(DemandeUtilisateur, pk=pk)

    objet_concerne = "N/A"
    if demande.gopi_concernee:
        objet_concerne = f"GOPI n°{demande.gopi_concernee.numero}"
    elif demande.renouvellement_concerne:
        objet_concerne = f"Renouvellement n°{demande.renouvellement_concerne.numero_edition}"
    elif demande.inscription_registre_concernee:
        objet_concerne = f"Inscription Registre n°{demande.inscription_registre_concernee.numero_gopi}"
    elif demande.formation_concernee:
        objet_concerne = f"Formation: {demande.formation_concernee.titre}"

    data = {
        'type_demande_display': demande.get_type_demande_display(),
        'nom': demande.nom,
        'email': demande.email,
        'telephone': demande.telephone,
        'message': demande.message,
        'date_soumission': demande.date_soumission.strftime("%d/%m/%Y %H:%M"),
        'statut_display': demande.get_statut_display(),
        'objet_concerne': objet_concerne,
    }
    return JsonResponse(data)


@staff_member_required
def edit_demande(request, pk):
    demande = get_object_or_404(DemandeUtilisateur, pk=pk)
    from frontend.forms import DemandeUtilisateurForm

    if request.method == 'POST':
        form = DemandeUtilisateurForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            return redirect('liste_demandes')
    else:
        form = DemandeUtilisateurForm(instance=demande)

    context = {
        'form': form,
        'demande': demande,
    }
    return render(request, 'frontend/edit_demande.html', context)


@staff_member_required
def delete_demande(request, pk):
    demande = get_object_or_404(DemandeUtilisateur, pk=pk)
    if request.method == 'POST':
        demande.delete()
        return redirect('liste_demandes')

    context = {
        'demande': demande,
    }
    return render(request, 'frontend/delete_demande.html', context)
