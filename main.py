import requests
from bs4 import BeautifulSoup
import json

# URL de la page à scraper
url = "https://vetso.serasera.org/mpanoratra/aorn"

# Envoyer la requête HTTP GET
response = requests.get(url)

# Vérifier que la requête est réussie
if response.status_code == 200:
    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Sélectionner tous les éléments contenant les poèmes
    poem_elements = soup.select('.poems ul li')  # À ajuster en fonction de la structure exacte du HTML

    # Initialiser une liste pour stocker les données
    tononkalo_list = []
    
    # Boucler sur les éléments <li> pour extraire les titres et les commentaires
    for index, elem in enumerate(poem_elements):
        # Extraire le lien <a> contenant le titre du poème
        title_elem = elem.find('a')
        if title_elem:
            title = title_elem.get_text(strip=True)
        else:
            title = "Titre non trouvé"
        
        # Extraire le nombre de commentaires dans la balise <span> ou autre
        comments_elem = elem.find('span')
        if comments_elem:
            comments = comments_elem.get_text(strip=True)
        else:
            comments = "0"  # Si le nombre de commentaires n'est pas trouvé, on met "0" par défaut
        
        # Ajouter les informations dans la liste sous forme de dictionnaire
        tononkalo_list.append({
            "title": title,
            "comments": comments,
            "index": index
        })
    
    # Afficher le résultat sous forme de JSON
    print(json.dumps(tononkalo_list, ensure_ascii=False, indent=4))

else:
    print(f"Échec de la requête, code de statut : {response.status_code}")
        
