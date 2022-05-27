from flask import Blueprint, Response, request
import json, requests

from utils.database_connection import DataBase

team_routes = Blueprint('team', __name__, url_prefix = '/team')


@team_routes.route('')
def getTeams():
    connection = DataBase().get_connection()
    db = connection.cursor()
    try:      
        SQL = 'SELECT * FROM teams'
        db.execute(SQL)
        teams = []
        connection.commit()
        for team in db.fetchall():
            data = requests.get('https://api.cartolafc.globo.com/time/id/%s' % (team['cartola_id'])).json()['time']
            teams.append(
                {   
                    'id': team['id'],
                    'name': data['nome'],
                    'cartola_id': data['time_id'],
                    'image_url': data['url_escudo_png']
                }
            )
        connection.close()
        return Response(
            json.dumps(teams),
            status = 200,
            content_type = 'application/json'
        )
    except Exception as error:
        return 'Error: %s' % (error)
    connection.close()

@team_routes.route('/insert', methods = ['POST'])
def postTeam():
    connection = DataBase().get_connection()
    db = connection.cursor()
    user = request.get_json()

    try:
        data = {
                "payload": {
                    "email": user['email'],
                    "password": user['password'],
                    "serviceId": 438,
                }
            }
        s = requests.Session()

        response = s.post('https://login.globo.com/api/authentication', json = data)
        token = response.json()['glbId']
        
        data = s.get('https://api.cartolafc.globo.com/auth/time', headers = {'X-GLB-Token': token }).json()['time']

        SQL = 'INSERT INTO teams (user_id, cartola_id) VALUES (%s, %s)'
        db.execute(SQL, (
            user['user_id'], 
            data['time_id'], 
            ))
        connection.commit()

        response = {
            'message': 'Time adicionado com sucesso!'
        }
        
        connection.close()
        return Response(
            json.dumps(response),
            status = 201,
            content_type = 'application/json'
        )

    except Exception as error:
        connection.rollback()
        return 'Error: %s' % (error)    
    connection.close()

@team_routes.route('/remove', methods = ['POST'])
def removeTeam():
    connection = DataBase().get_connection()
    db = connection.cursor()
    team = request.get_json()

    try:
        SQL = 'DELETE FROM teams WHERE cartola_id = %s'
        db.execute(SQL, (
            team['cartola_id'] 
            ))
        connection.commit()

        response = {
            'message': 'Time removido com sucesso!'
        }
        
        connection.close()
        return Response(
            json.dumps(response),
            status = 200,
            content_type = 'application/json'
        )

    except Exception as error:
        connection.rollback()
        return 'Error: %s' % (error)    
    connection.close()

@team_routes.route('/details/<int:id>')
def detailTeam(id):
    connection = DataBase().get_connection()
    db = connection.cursor()
    points = 0
    details = []
    captain = False
    try:
        athletes_punctuated = requests.get('https://api.cartolafc.globo.com/atletas/pontuados').json()['atletas']
        team = requests.get('https://api.cartolafc.globo.com/time/id/%s' % (id)).json()
        captain_id = team['capitao_id']
        athletes_team = team['atletas']

        for athlete_team in athletes_team:
            for athlete_punctuated in athletes_punctuated:
                if athlete_team['atleta_id'] == int(athlete_punctuated):
                    if captain_id == int(athlete_punctuated):
                        captain = True
                        points = points + athletes_punctuated[athlete_punctuated]['pontuacao'] * 2
                    else:
                        points = points + athletes_punctuated[athlete_punctuated]['pontuacao']

            details.append({
                    'name': athlete_team['apelido'],
                    'position_id': athlete_team['posicao_id'],
                    'abbrev': team['posicoes'][str(athlete_team['posicao_id'])]['abreviacao'].upper(),
                    'image_url': team['clubes'][str(athlete_team['clube_id'])]['escudos']['60x60'],
                    'captain': captain,
                    'partial': round(points, 3)
                    })

            points = 0
            captain = False

        details = sorted(details, key = lambda i: i['position_id'], reverse = False)

        connection.close()
        return Response(
            json.dumps(details),
            status = 200,
            content_type = 'application/json'
            )
    except Exception as error:
        connection.rollback()
        return 'Error: %s' % (error)
    connection.close()