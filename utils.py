from parsing_manager import ParsingManager, heuristic_skills_processing, remove_punct, KEY_SKILLS
from text_preprocessing import preprocess_text
from nlp import compare_texts, complex_compare
import json
import copy
import os
from pdf_and_image_processing import get_text_from_giga_pdf, get_text_from_image

PARSING_MANAGER = ParsingManager()
COURSES = PARSING_MANAGER.courses

def get_json_data(url):
    vacancy_text, vacancy_skills = PARSING_MANAGER.get_vacancy_data_from_hh(url)

    vacancy_text = preprocess_text(vacancy_text)

    courses = copy.deepcopy(COURSES)
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

def get_json_data_text(raw_text: str):
    vacancy_text = heuristic_skills_processing(raw_text)
    vacancy_text = remove_punct(vacancy_text)
    vacancy_skills = set()
    for word in vacancy_text.split():
        if word.lower() in [skill.lower() for skill in KEY_SKILLS]:
            vacancy_skills.add(word)
    vacancy_text = preprocess_text(vacancy_text)

    courses = copy.deepcopy(COURSES)
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

def get_json_data_file(file):
    if file.filename.endswith('.pdf'):
        save_folder = "pdf_files"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        save_path = os.path.join(save_folder, file.filename)
        file.save(save_path)
        raw_text = get_text_from_giga_pdf(pdf=save_path, image_folder='media_files')
    elif file.filename.endswith('.png'):
        save_folder = "media_files"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        save_path = os.path.join(save_folder, file.filename)
        file.save(save_path)
        raw_text = get_text_from_image(img=save_path)
    vacancy_text = heuristic_skills_processing(raw_text)
    vacancy_text = remove_punct(vacancy_text)
    vacancy_skills = set()
    for word in vacancy_text.split():
        if word.lower() in [skill.lower() for skill in KEY_SKILLS]:
            vacancy_skills.add(word)
    vacancy_text = preprocess_text(vacancy_text)

    courses = copy.deepcopy(COURSES)
    max_accuracy = -1

    for course in courses:
        course["formats"] = {int(n): format for n, format in enumerate(course["formats"])}
        raw_course_skills = course["skills"]
        course["skills"] = {int(n): skill for n, skill in enumerate(list(course["skills"] & vacancy_skills))}

        result = complex_compare(vacancy_text, vacancy_skills, course['text'],
                                 raw_course_skills)  # compare_texts(vacancy_text, course["text"])
        course['accuracy'] = result['final_score']
        course['skills_accuracy'] = result['skills_score']

        max_accuracy = course["accuracy"] if max_accuracy < course["accuracy"] else max_accuracy
        course.pop('text', 'Key not found')
    for course in courses:
        course["accuracy"] = round(((course["accuracy"] / max_accuracy) * 100), 2)

    courses = {"courses": {int(n): data for n, data in enumerate(courses)}}

    vacancy_skills = {"skills": {int(n): skill for n, skill in enumerate(list(vacancy_skills))}}
    json_data = json.dumps({**vacancy_skills, **courses}, ensure_ascii=False)
    return json_data
