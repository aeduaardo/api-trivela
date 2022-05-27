from flask import Blueprint, Response, request
import json

from utils.database_connection import DataBase

user_routes = Blueprint('user', __name__, url_prefix='/user')

@user_routes.route('')
def getUsers():
    connection = DataBase().get_connection()
    db = connection.cursor()
    try:
        SQL = 'SELECT * FROM users'
        db.execute(SQL)
        users = db.fetchall()
        connection.close()
        return Response(
            json.dumps(users),
            status=200,
            content_type='application/json'
        )

    except Exception as error:
        return 'Error: %s' % (error)
    connection.close()


@user_routes.route('/register', methods=['POST'])
def register():
    connection = DataBase().get_connection()
    db = connection.cursor()
    user = request.get_json()
    try:
        SQL = 'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)'
        db.execute(
            SQL, (user['username'], user['email'], user['password']))
        connection.commit()
        
        response = {
            'message': 'Usuário cadastrado com sucesso!',
            'status': True
        }
        connection.close()
        return Response(
            json.dumps(response),
            status=201,
            content_type='application/json',
            
        )

    except Exception as error:
        connection.rollback()
        if 'Duplicate' in error.args[1] and 'username' in error.args[1]:
            return {
                'message': 'O nome de usuário informado já está em uso.',
                'status': False
            }
        elif 'Duplicate' in error.args[1] and 'email' in error.args[1]:
            return {
                'message': 'O email informado já está em uso.',
                'status': False
            }
        else:
            return {
                'message': 'Não foi possível realizar o cadastro. Tente novamente mais tarde!',
                'status': False
            }
    connection.close()


@user_routes.route('/login', methods=['POST'])
def login():
    connection = DataBase().get_connection()
    db = connection.cursor()
    user = request.get_json()

    try:
        SQL = 'SELECT username, password FROM users WHERE username = %s AND password = %s'
        db.execute(SQL, (
            user['username'],
            user['password']))
        if db.rowcount == 1:
            response = {
                'message': 'Usuário verificado com sucesso!',
                'status': True
            }
        else:
            response = {
                'message': 'Usuário e/ou senha inválidos!',
                'status': False
            }
        connection.close()
        return Response(
            json.dumps(response),
            status=200,
            content_type='application/json'
        )

    except Exception as error:
        return 'Error: %s' % (error)
    connection.close()