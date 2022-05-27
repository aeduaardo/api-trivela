#!/user/bin/ebv python3

import requests

from utils.database_connection import DataBase

connection = DataBase().get_connection()
db = connection.cursor()


def get_points_round(id):
    points = 0
    athletes_punctuated = requests.get('http://www.json-generator.com/api/json/get/ceQBfKzWWa?indent=2').json()['atletas']
    team = requests.get('https://api.cartolafc.globo.com/time/id/%s' % (id)).json()
    captain_id = team['capitao_id']
    athletes_team = team['atletas']

    for athlete_team in athletes_team:
        for athlete_punctuated in athletes_punctuated:
            if athlete_team['atleta_id'] == int(athlete_punctuated):
                if captain_id == int(athlete_punctuated):
                    points = points + athletes_punctuated[athlete_punctuated]['pontuacao'] * 2
                else:
                    points = points + athletes_punctuated[athlete_punctuated]['pontuacao']

    return {
            'name': team['time']['nome'],
            'cartola_id': team['time']['time_id'],
            'image_url': team['time']['url_escudo_png'],
            'partial': round(points, 2)
        }

def get_points_monthly(id, league_id):
    partial = get_points_round(id)
    try:
        SQL = 'SELECT DISTINCT payments.cartola_id As cartola_id, points As accumulated_points FROM points \
               JOIN payments ON payments.id = points.id \
               WHERE payments.cartola_id = %s AND payments.league_id = %s'

        db.execute(SQL, (id, league_id))
        result = db.fetchone()
        partial['accumulated_points'] = round((result['accumulated_points'] + partial['partial']), 2)
        
        return partial
    except Exception as error:
        return 'Error: %s' % (error)
    connection.close()
