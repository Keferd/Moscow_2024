import os

from flaskapp import app
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for, send_file
import json
from utils import get_json_data, get_json_data_text, get_json_data_file


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/file')
def file():
    return render_template('file.html')


@app.route('/text')
def text():
    return render_template('text.html')

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
    
@app.route('/api/file', methods=['POST'])
def post_file():
    try:
        file = request.files["file"]
        if file:
            response_data = get_json_data_file(file=file)
            return response_data

        else:
            return "Ой-йой, что-то пошло не так", 400

    except Exception as e:
        print("error:", e)
        return str(e), 500
    
@app.route('/api/text', methods=['POST'])
def post_text():
    try:
        text = request.json['link_vacancy']

        if text:
            response_data = get_json_data_text(raw_text=text)
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