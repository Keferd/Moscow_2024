from parsing_manager import ParsingManager
from text_preprocessing import preprocess_text
from nlp import compare_texts, complex_compare
import json
import copy

PARSING_MANAGER = ParsingManager()


def get_json_data(url):
    vacancy_text, vacancy_skills = PARSING_MANAGER.get_vacancy_data_from_hh(url)

    vacancy_text = preprocess_text(vacancy_text)

    courses = copy.deepcopy(PARSING_MANAGER.courses)
    max_accuracy = -1

    for course in courses:
        course["formats"] = {int(n): format for n, format in enumerate(course["formats"])}
        raw_course_skills = course["skills"]
        course["skills"] = {int(n): skill for n, skill in enumerate(list(course["skills"] & vacancy_skills))}

        result = complex_compare(vacancy_text, vacancy_skills, course['text'], raw_course_skills)#compare_texts(vacancy_text, course["text"])
        course['accuracy'] = result['final_score']
        course['skills_accuracy'] = result['skills_score']

        max_accuracy = course["accuracy"] if max_accuracy < course["accuracy"] else max_accuracy
        course.pop('text', 'Key not found')
    for course in courses:
        course["accuracy"] = round(((course["accuracy"]/max_accuracy)*100), 2)

    courses = {"courses": {int(n): data for n, data in enumerate(courses)}}

    vacancy_skills = {"skills": {int(n): skill for n, skill in enumerate(list(vacancy_skills))}}
    json_data = json.dumps({**vacancy_skills, **courses}, ensure_ascii=False)
    return json_data
