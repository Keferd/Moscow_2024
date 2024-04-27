from parsing_manager import ParsingManager
from text_preprocessing import preprocess_text
from nlp import compare_texts

PARSING_MANAGER = ParsingManager()


# vacancy_text, vacancy_skills = PARSING_MANAGER.get_vacancy_data_from_hh("https://ufa.hh.ru/vacancy/96482951")
# vacancy_text = preprocess_text(vacancy_text)
# print(vacancy_text)
# print(vacancy_skills)

course_texts = PARSING_MANAGER.courses
#
# res = {}
# for key, value in course_texts.items():
#     res[key] = compare_texts(vacancy_text, value)
#
# sorted_res = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
# for key, value in sorted_res.items():
#     print(value, key)
