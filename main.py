import requests
from bs4 import BeautifulSoup

# URL de la page à scraper
url = "https://vetso.serasera.org/mpanoratra/aorn"

# Envoyer la requête HTTP GET
response = requests.get(url)

# Vérifier que la requête est réussie
if response.status_code == 200:
    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Afficher tous les textes présents sur la page pour diagnostic
    all_text = soup.get_text()
    print(all_text)
else:
    print(f"Échec de la requête, code de statut : {response.status_code}")
