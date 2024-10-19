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
    
    # Extraire tout le texte de la page
    page_text = soup.get_text()
    
    # Chercher la section qui contient "Tononkalo" et extraire les lignes suivantes
    start_index = page_text.find("Tononkalo (")
    
    # Si trouvé, découper cette partie du texte
    if start_index != -1:
        # Prendre uniquement la partie qui contient les poèmes après "Tononkalo ("
        poems_section = page_text[start_index:]
        
        # Diviser le texte par lignes
        lines = poems_section.splitlines()
        
        # Initialiser une liste pour stocker les poèmes
        poems_list = []
        index = 0
        
        # Parcourir les lignes pour extraire les titres de poèmes et le nombre de commentaires
        for line in lines:
            # Nettoyer chaque ligne de tout espace superflu
            line = line.strip()
            
            # Ignorer les lignes vides ou sans importance
            if line and not line.startswith("Tononkalo (") and not line.startswith("tohiny"):
                # Diviser la ligne en deux parties : titre et nombre de commentaires
                parts = line.rsplit(' ', 1)
                if len(parts) == 2:
                    title, comments = parts
                    # Ajouter un poème au format JSON à la liste
                    poems_list.append({
                        "title": title,
                        "comments": comments,
                        "index": index
                    })
                    index += 1
        
        # Convertir la liste en JSON et afficher le résultat
        json_output = json.dumps(poems_list, ensure_ascii=False, indent=4)
        print(json_output)
    else:
        print("Section 'Tononkalo' non trouvée dans le texte.")
else:
    print(f"Échec de la requête, code de statut : {response.status_code}")
