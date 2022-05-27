import json
import os
from flask import Flask, Response
from users.blueprint import user_routes
from leagues.blueprint import league_routes
from teams.blueprint import team_routes

app = Flask(__name__)
app.register_blueprint(user_routes)
app.register_blueprint(league_routes)
app.register_blueprint(team_routes)


@app.route('/')
def index():
    return Response(
        json.dumps({
            'app': 'Cartola API',
            'version': 0.1,
        }),
        200,
        content_type='application/json'
    )


if __name__ == '__main__':
    app.run(debug=True)
