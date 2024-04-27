from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score

import re
import pandas as pd
from const import KEY_SKILLS

from parsing_manager import ParsingManager

PARSING_MANAGER = ParsingManager()

link = "https://ufa.hh.ru/vacancy/90803714?query=iOS-%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA&hhtmFrom=vacancy_search_list"
_, vacancy_skills = PARSING_MANAGER.get_vacancy_data_from_hh(link)

print(vacancy_skills)
course_texts = PARSING_MANAGER.courses

title = []
skills = []
for course in course_texts:
    title.append(course['tittle'])
    skills.append(course['skills'])
df = pd.DataFrame()
df['tittle'] = title
df['skills'] = skills

df['skills_text'] = df['skills'].apply(lambda x: ' '.join(x))
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['skills_text'])
new_object_vector = vectorizer.transform([' '.join(vacancy_skills)])

similarities = cosine_similarity(new_object_vector, X)
df['cosine'] = similarities[0] * 100

def get_set_similarity(course_skills, vacancy_skills):
    intersection = set(course_skills).intersection(set(vacancy_skills))
    union = set(course_skills).union(set(vacancy_skills))
    return float(len(intersection)) / len(union)


df['set'] = df['skills'].apply(lambda x: get_set_similarity(course_skills=x, vacancy_skills=vacancy_skills))
# Отсортировать результаты по убыванию процента схожести
print(df.sort_values(by='cosine', ascending=False)[['tittle', 'cosine']].head(5))
print(df.sort_values(by='set', ascending=False)[['tittle', 'set']].head(5))

