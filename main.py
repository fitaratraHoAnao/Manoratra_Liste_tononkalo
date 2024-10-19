from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_all_poems(term):
    all_poems = []
    page_number = 1

    while True:
        # URL de la page à scraper avec pagination
        url = f"https://vetso.serasera.org/mpanoratra/{term}?page={page_number}"
        response = requests.get(url)

        # Vérifier que la requête est réussie
        if response.status_code != 200:
            break  # Sortir si on ne peut pas accéder à la page
        
        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraire tout le texte de la page
        page_text = soup.get_text()
        start_index = page_text.find("Tononkalo (")

        # Si la section 'Tononkalo' n'est pas trouvée, sortir de la boucle
        if start_index == -1:
            break

        # Prendre uniquement la partie qui contient les poèmes après "Tononkalo ("
        poems_section = page_text[start_index:]
        lines = poems_section.splitlines()

        # Extraction des poèmes
        poems_found = False
        for line in lines:
            line = line.strip()
            if line and not line.startswith("Tononkalo (") and not line.startswith("tohiny"):
                parts = line.rsplit(' ', 1)
                if len(parts) == 2 and parts[1].isdigit():
                    title, comments = parts
                    all_poems.append({
                        "title": title.strip(),
                        "comments": comments,
                    })
                    poems_found = True

        # Si aucun poème n'a été trouvé sur cette page, arrêter la boucle
        if not poems_found:
            break

        page_number += 1  # Passer à la page suivante

    return all_poems

@app.route('/recherche', methods=['GET'])
def recherche():
    # Obtenir le terme de recherche à partir des paramètres de requête
    term = request.args.get('term', default='aorn')  # Défaut à 'aorn' si aucun terme n'est fourni
    page = int(request.args.get('page', default=1))  # Page par défaut est 1
    page_size = int(request.args.get('page_size', default=10))  # Taille de page par défaut est 10

    # Récupérer tous les poèmes
    all_poems = get_all_poems(term)

    # Calculer le total de poèmes
    total_poems = len(all_poems)

    # Implémenter la pagination
    start = (page - 1) * page_size
    end = start + page_size
    paginated_poems = all_poems[start:end]

    # Préparer la réponse avec la pagination
    response_data = {
        "page": page,
        "page_size": page_size,
        "total": total_poems,
        "poems": paginated_poems
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
