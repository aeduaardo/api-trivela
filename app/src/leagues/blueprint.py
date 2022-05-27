from flask import Blueprint, Response, request
import json
import requests

from utils.database_connection import DataBase
from . import functions as f

league_routes = Blueprint('league', __name__, url_prefix='/league')


@league_routes.route('')
def get_leagues():
    connection = DataBase().get_connection()
    db = connection.cursor()
    try:
        SQL = 'SELECT * FROM leagues'
        db.execute(SQL)
        leagues = db.fetchall()
        
        connection.close()
        return Response(
            json.dumps(leagues),
            status=200,
            content_type='application/json'
        )

    except Exception as error:
        return 'Error: %s' % (error)
    connection.close()


@league_routes.route('/create', methods=['POST'])
def create_league():
    connection = DataBase().get_connection()
    db = connection.cursor()
    data = request.get_json()

    try:
        SQL = 'INSERT INTO leagues (name, image_url, type, round) VALUES (%s, %s, %s, %s)'
        db.execute(SQL, (
            data['name'],
            data['image_url'],
            data['type'],
            data['round']
        ))
        connection.commit()

        response = {
            'message': 'Liga criada com sucesso!',
            'status': True
        }

        connection.close()
        return Response(
            json.dumps(response),
            status=201,
            content_type='application/json'
        )

    except Exception as error:
        connection.rollback()
        return 'Error: %s' % (error)
    connection.close()


@league_routes.route('/partial/<int:league_id>')
def partial_round(league_id):
    connection = DataBase().get_connection()
    db = connection.cursor()
    partials = []

    # Recupera os ID's dos times cadastrados na liga.
    try:

        SQL = 'SELECT cartola_id FROM payments WHERE league_id = %s AND status = %s'
        db.execute(SQL, (league_id, 'approved'))
        teams = db.fetchall()
        for team in teams:
            partials.append(f.get_points_round(team['cartola_id']))
        partials = sorted(partials, key=lambda i: i['partial'], reverse=True)
        points = 0.0
        position = 1
        for partial in partials:
            if partial['partial'] > points:
                points = partial['partial']
                partial['position'] = position
            elif partial['partial'] == points:
                partial['position'] = position
            else:
                position = position + 1
                partial['position'] = position
        
        connection.close()
        return Response(
            json.dumps(partials),
            status=200,
            content_type='application/json'
        )
    except Exception as error:
        connection.rollback()
        return 'Error: %s' % (error)
    connection.close()


@league_routes.route('/monthly/<int:league_id>')
def partial_monthly(league_id):
    connection = DataBase().get_connection()
    db = connection.cursor()
    partials = []

    try:
        SQL = 'SELECT cartola_id FROM payments WHERE league_id = %s AND status = %s'
        db.execute(SQL, (league_id, 'approved'))
        teams = db.fetchall()
        for team in teams:
            partials.append(f.get_points_monthly(
                db, team['cartola_id'], league_id))
        partials = sorted(
            partials, key=lambda i: i['accumulated_points'], reverse=True)

        points = 0.0
        position = 1
        for partial in partials:
            if partial['accumulated_points'] > points:
                points = partial['accumulated_points']
                partial['position'] = position
            elif partial['accumulated_points'] == points:
                partial['position'] = position
            else:
                position = position + 1
                partial['position'] = position

        connection.close()
        return Response(
            json.dumps(partials),
            status=200,
            content_type='application/json'
        )
    except Exception as error:
        return 'Error: %s' % (error)
    connection.close()

