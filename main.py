from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Route pour rechercher des poèmes par tononkalo
@app.route('/recherche', methods=['GET'])
def recherche_tononkalo():
    tononkalo = request.args.get('tononkalo', '')
    page = request.args.get('page', 1)

    url = f'https://vetso.serasera.org/vetso?tononkalo={tononkalo}&page={page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.find_all('div', class_='border p-2 mb-3'):
        title = item.find('a').get_text(strip=True)
        author = item.find_all('a')[1].get_text(strip=True)
        likes = item.find('i', class_='bi-heart-fill').next_sibling.strip()

        results.append({
            'title': title,
            'author': author,
            'likes': likes
        })

    pagination = {
        'current_page': int(page),
        'next_page': int(page) + 1,
        'previous_page': int(page) - 1 if int(page) > 1 else None,
    }

    return jsonify({
        'search': tononkalo,
        'results': results,
        'pagination': pagination
    })

# Route pour rechercher un poème par auteur et titre
@app.route('/recherche_auteur', methods=['GET'])
def recherche_auteur_titre():
    auteur = request.args.get('auteur')
    titre = request.args.get('titre')

    url = f'https://vetso.serasera.org/tononkalo/{auteur}/{titre}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        titre_page = soup.find('h2').text.strip()
        contenu_div = soup.find('div', class_='col-md-8')
        lines = contenu_div.get_text().splitlines()

        elements_a_supprimer = [
            "Rohy:", "Adikao", "Sokajy :", "Mpakafy:", 
            "Hametraka hevitra", "Midira aloha", "rina15", 
            "Fitiavana", "Mbola tsisy niantsa", "Hangataka antsa", 
            "(Nalaina tao amin'ny vetso.serasera.org)"
        ]

        contenu_poeme = [line.strip() for line in lines if line.strip() and not any(el in line for el in elements_a_supprimer)]
        tononkalo_text = ',\n'.join(contenu_poeme)

        poeme_dict = {
            "Tononkalo": tononkalo_text,
            "titre": titre_page
        }

        return jsonify(poeme_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route pour obtenir la liste des auteurs
@app.route('/auteur', methods=['GET'])
def get_auteurs():
    query = request.args.get('query')
    page = request.args.get('page', default=1, type=int)

    if query != 'mpanoratra':
        return jsonify({"error": "Query parameter must be 'mpanoratra'"}), 400

    url = 'https://vetso.serasera.org/mpanoratra'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    auteurs = []
    for div in soup.find_all("div", class_="border p-2 mb-3"):
        a_tag = div.find('a')
        if a_tag:
            nom = a_tag.text.strip()
            tononkalo_text = div.find_all('a')[1].text.strip()
            tononkalo_count = int(tononkalo_text.split()[1])
            auteurs.append({
                "nom": nom,
                "tononkalo": tononkalo_count
            })

    per_page = 10
    total_auteurs = len(auteurs)
    total_pages = (total_auteurs + per_page - 1) // per_page

    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    paginated_auteurs = auteurs[start_index:end_index]

    return jsonify({
        "page": page,
        "total_pages": total_pages,
        "total_auteurs": total_auteurs,
        "auteurs": paginated_auteurs
    })

# Route pour rechercher des poèmes par poème
@app.route('/recherche_poeme', methods=['GET'])
def recherche_poeme():
    poeme = request.args.get('poeme')
    page = request.args.get('page', default=1, type=int)

    url = f'https://vetso.serasera.org/mpanoratra/{poeme}/tononkalo?page={page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    titres = []
    for item in soup.find_all('div', class_='border p-2 mb-3 row'):
        title_element = item.find('a')
        if title_element:
            title = title_element.text.strip()
            titres.append(title)

    return jsonify(titres)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
