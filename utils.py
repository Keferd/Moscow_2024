from parsing_manager import ParsingManager
from text_preprocessing import preprocess_text
from nlp import compare_texts
import json
import copy

PARSING_MANAGER = ParsingManager()


def get_json_data(url):
    vacancy_text, vacancy_skills = PARSING_MANAGER.get_vacancy_data_from_hh(url)

    vacancy_text = preprocess_text(vacancy_text)

    courses = copy.deepcopy(PARSING_MANAGER.courses)

    for course in courses:
        course["formats"] = {int(n): format for n, format in enumerate(course["formats"])}
        course["skills"] = {int(n): skill for n, skill in enumerate(list(course["skills"] & vacancy_skills))}
        course["accuracy"] = compare_texts(vacancy_text, course["text"])
        course.pop('text', 'Key not found')
    courses = {"courses": {int(n): data for n, data in enumerate(courses)}}

    vacancy_skills = {"skills": {int(n): skill for n, skill in enumerate(list(vacancy_skills))}}
    json_data = json.dumps({**vacancy_skills, **courses}, ensure_ascii=False)
    return json_data
