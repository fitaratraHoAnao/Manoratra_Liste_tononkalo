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
    
    # Recherchez le nombre de tononkalo et les titres
    tononkalo_count = soup.find('div', class_='row').find_all('div', class_='col-12')[0].get_text().split('(')[1].strip(') ')
    
    # Recherchez les titres des tononkalo
    tononkalo_titles = soup.find_all('div', class_='col-12')
    for index, tononkalo in enumerate(tononkalo_titles):
        title = tononkalo.get_text().strip()
        comments = tononkalo.find('span').get_text().strip() if tononkalo.find('span') else "0"
        tononkalo_list.append({
            'title': title,
            'comments': comments,
            'index': index
        })

    return jsonify(tononkalo_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
