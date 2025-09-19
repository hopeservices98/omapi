from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Actualite, GOPI, Publication, Formation, Service, DocumentTelechargeable, Annonce, Statistique, CarouselSlide, TypeActualite, Mandataire, Renouvellement, InscriptionRegistre, DemandeUtilisateur

class ActualiteAdminForm(forms.ModelForm):
    contenu = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Actualite
        fields = '__all__'

class ActualiteAdmin(admin.ModelAdmin):
    form = ActualiteAdminForm
    list_display = ('titre', 'date_publication', 'type_actualite')
    prepopulated_fields = {'slug': ('titre',)}

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_publication', 'type_publication')
    prepopulated_fields = {'slug': ('titre',)}

class FormationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_formation', 'date_debut', 'date_fin', 'lieu', 'est_active')
    prepopulated_fields = {'slug': ('titre',)}
    list_filter = ('type_formation', 'lieu', 'est_active')
    search_fields = ('titre', 'description', 'formateurs')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug')
    prepopulated_fields = {'slug': ('nom',)}

class DocumentTelechargeableAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_document', 'categorie_pi', 'date_publication')
    list_filter = ('type_document', 'categorie_pi')
    search_fields = ('titre', 'description')

admin.site.register(Actualite, ActualiteAdmin)
class GOPIAdmin(admin.ModelAdmin):
    list_display = ('numero', 'date_publication', 'contient_brevet', 'contient_marque', 'contient_dessin_modele', 'contient_nom_commercial')
    list_editable = ('date_publication', 'contient_brevet', 'contient_marque', 'contient_dessin_modele', 'contient_nom_commercial')
    search_fields = ('numero',)
admin.site.register(GOPI, GOPIAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Formation, FormationAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(DocumentTelechargeable, DocumentTelechargeableAdmin)
admin.site.register(Annonce)
admin.site.register(Statistique)

admin.site.register(TypeActualite)

class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ordre', 'image', 'lien')
    list_editable = ('ordre',)

admin.site.register(CarouselSlide, CarouselSlideAdmin)
admin.site.register(Mandataire)


class RenouvellementAdmin(admin.ModelAdmin):
    list_display = ('numero_edition', 'date_publication', 'annee_emission_certificat')
    list_filter = ('annee_emission_certificat',)
    search_fields = ('numero_edition',)
admin.site.register(Renouvellement, RenouvellementAdmin)

class InscriptionRegistreAdmin(admin.ModelAdmin):
    list_display = ('numero_gopi', 'date_publication', 'annee_depot_demande')
    list_filter = ('annee_depot_demande',)
    search_fields = ('numero_gopi',)

admin.site.register(InscriptionRegistre, InscriptionRegistreAdmin)

class DemandeUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('type_demande', 'nom', 'email', 'date_soumission', 'statut', 'gopi_concernee', 'renouvellement_concerne', 'inscription_registre_concernee', 'formation_concernee')
    list_filter = ('type_demande', 'statut', 'date_soumission')
    search_fields = ('nom', 'email', 'message', 'gopi_concernee__numero', 'renouvellement_concerne__numero_edition', 'inscription_registre_concernee__numero_gopi', 'formation_concernee__titre')
    raw_id_fields = ('gopi_concernee', 'renouvellement_concerne', 'inscription_registre_concernee', 'formation_concernee') # Pour les ForeignKeys, facilite la recherche

admin.site.register(DemandeUtilisateur, DemandeUtilisateurAdmin)
