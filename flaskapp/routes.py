import os

from flaskapp import app
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for, send_file
import json
from utils import get_json_data


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/api/link', methods=['POST'])
def post_link():
    try:
        url = request.json['link_vacancy']

        if url:
            response_data = get_json_data(url)
            return response_data

        else:
            return "Ой-йой, что-то пошло не так", 400

    except Exception as e:
        print("error:", e)
        return str(e), 500

def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))


def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)