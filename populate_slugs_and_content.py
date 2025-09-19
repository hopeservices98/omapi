import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omapi_website.settings')
django.setup()

from django.core.files.storage import default_storage
from django.utils.text import slugify
from content_management.models import DocumentTelechargeable
# import PyPDF2

print("Démarrage de la mise à jour des slugs des documents...")

documents_to_update = []
for doc in DocumentTelechargeable.objects.all():
    # Générer le slug si manquant ou vide
    if not doc.slug:
        doc.slug = slugify(doc.titre)
        # Assurer l'unicité du slug
        original_slug = doc.slug
        counter = 1
        while DocumentTelechargeable.objects.filter(slug=doc.slug).exclude(pk=doc.pk).exists():
            doc.slug = f"{original_slug}-{counter}"
            counter += 1
        documents_to_update.append(doc)

    # # Extraire le texte du PDF si manquant et si c'est un PDF
    # if doc.fichier and doc.fichier.name.lower().endswith('.pdf') and not doc.contenu_texte:
    #     try:
    #         with default_storage.open(doc.fichier.name, 'rb') as pdf_file:
    #             reader = PyPDF2.PdfReader(pdf_file)
    #             text = ''
    #             for page_num in range(len(reader.pages)):
    #                 page = reader.pages[page_num]
    #                 text += page.extract_text() or ''
    #             doc.contenu_texte = text
    #             documents_to_update.append(doc)
    #     except Exception as e:
    #         print(f"Erreur lors de l'extraction du texte du PDF pour '{doc.titre}': {e}")
    #         doc.contenu_texte = None
    #         documents_to_update.append(doc)

if documents_to_update:
    # Mettre à jour les documents en masse
    # Utiliser un dictionnaire pour s'assurer que les documents sont uniques
    docs_to_update_dict = {doc.pk: doc for doc in documents_to_update}
    unique_docs = list(docs_to_update_dict.values())
    
    DocumentTelechargeable.objects.bulk_update(unique_docs, ['slug'])
    print(f"{len(unique_docs)} documents mis à jour avec les slugs.")
else:
    print("Aucun document à mettre à jour.")

print("Script terminé.")