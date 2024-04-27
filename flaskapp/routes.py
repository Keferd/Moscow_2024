import os

from flaskapp import app
import pandas as pd
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for, send_file
import functools
import json



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/api/link', methods=['POST'])
def post_link():
    try:
        link = request.json['link_vacancy']

        if link:
            return jsonify(response_data)
        
        else:
            return "Ой-йой, что-то пошло не так", 400

    except Exception as e:
        print(e)
        return str(e), 500

def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))


def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)