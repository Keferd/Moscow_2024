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
        text = request.json['link_vacancy']

        print(text)

        if text:
            
            print(text)

            response_data = {
                "skills": {
                    0: "Python",
                    1: "SQL",
                    2: "Django",
                    3: "JavaScript",
                    4: "HTML/CSS",
                    5: "Git"
                },
                "courses": {
                0: {
                    "name": "Python-разработчик: быстрый старт в профессии",
                    "link":"https://gb.ru/geek_university/developer/programmer/python-gb",
                    "description": "Научитесь использовать язык программирования Python для создания сайтов, приложений, чат-ботов, нейросетей и даже для научных исследований",
                    "duration": "9",
                    "price": "6657",
                    "accuracy": "87",
                    "formats": {
                        0: "Занятие в группе c преподавателем",
                        1: "Онлайн-встречи c экспертами",
                        2: "Онлайн-лекции и вебинары",
                        3: "Видеозаписи занятий",
                        4: "Практические занятия",
                        5: "Домашняя работа"
                    },
                    "skills": {
                        0: "Python",
                        1: "SQL",
                        2: "Django",
                        3: "JavaScript",
                        4: "HTML/CSS",
                        5: "Git"
                    }
                },
                1: {
                    "name": "Программист c нуля до Junior",
                    "link":"https://gb.ru/geek_university/developer/programmer",
                    "description": "Выберите профессию в программировании в процессе обучения и станьте специалистом уровня Junior c зарплатой от 80 000 ₽",
                    "duration": "12",
                    "price": "5251",
                    "accuracy": "68",
                    "formats": {
                        0: "Занятие в группе c преподавателем",
                        1: "Онлайн-встречи c экспертами",
                        2: "Онлайн-лекции и вебинары",
                        3: "Видеозаписи занятий",
                        4: "Практические занятия"
                    },
                    "skills": {
                        0: "Python",
                        1: "SQL",
                        2: "JavaScript",
                        3: "HTML/CSS",
                        4: "Git"
                    }
                },
                2: {
                    "name": "Разработчик искусственного интеллекта",
                    "link":"https://gb.ru/geek_university/developer/programmer/ai-spec",
                    "description": "Научитесь c нуля создавать и управлять системами c использованием искусственного интеллекта",
                    "duration": "12",
                    "price": "5999",
                    "accuracy": "53",
                    "formats": {
                        0: "Занятие в группе c преподавателем",
                        1: "Онлайн-встречи c экспертами",
                        2: "Онлайн-лекции и вебинары"
                    },
                    "skills": {
                        0: "Python",
                        1: "SQL",
                        2: "HTML/CSS",
                        3: "Git"
                    }
                }
                }
            }

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