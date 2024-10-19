from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/recherche', methods=['GET'])
def recherche():
    mpanoratra = request.args.get('mpanoratra', default='', type=str)

    # URL de base, ajustez-le si nécessaire
    url = f'https://vetso.serasera.org/mpanoratra/{mpanoratra.lower()}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Auteur non trouvé'}), 404
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    tononkalo_list = []
    
    # Vérification de la présence de l'élément
    row_div = soup.find('div', class_='row')
    if row_div:
        col_divs = row_div.find_all('div', class_='col-12')
        if col_divs:
            # Supposons que le tononkalo_count est dans le premier div.col-12
            tononkalo_count_text = col_divs[0].get_text()
            tononkalo_count = tononkalo_count_text.split('(')[1].strip(') ') if '(' in tononkalo_count_text else "0"
            
            # Recherchez les titres des tononkalo
            for index, tononkalo in enumerate(col_divs):
                title = tononkalo.get_text().strip()
                comments = tononkalo.find('span').get_text().strip() if tononkalo.find('span') else "0"
                tononkalo_list.append({
                    'title': title,
                    'comments': comments,
                    'index': index
                })
        else:
            return jsonify({'error': 'Aucun tononkalo trouvé pour cet auteur'}), 404
    else:
        return jsonify({'error': 'Erreur lors de l\'extraction des données'}), 500

    return jsonify(tononkalo_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
