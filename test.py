from parsing_manager import ParsingManager
from text_preprocessing import preprocess_text
from nlp import compare_texts

PARSING_MANAGER = ParsingManager()


def get_json_data(url):
    vacancy_text, vacancy_skills = PARSING_MANAGER.get_vacancy_data_from_hh(url)
    vacancy_skills = {"skills": [{n: skill} for n, skill in enumerate(vacancy_skills)]}
    vacancy_text = preprocess_text(vacancy_text)

    courses = PARSING_MANAGER.courses

    for course in courses:
        course["formats"] = [{n: format} for n, format in enumerate(course["formats"])]
        course["skills"] = [{n: skill} for n, skill in enumerate(course["skills"])]
        course["accuracy"] = compare_texts(vacancy_text, course["text"])

    courses = {"courses": [{n: data} for n, data in enumerate(courses)]}
    json_data = [vacancy_skills, courses]
    print(json_data)
    return json_data


get_json_data("https://ufa.hh.ru/vacancy/96127386")
