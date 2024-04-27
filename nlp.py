from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compare_texts(text1, text2):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    return similarity[0][0]


def get_set_similarity(course_skills: set[str], vacancy_skills: set[str]):
    intersection = course_skills.intersection(vacancy_skills)
    union = course_skills.union(vacancy_skills)
    return float(len(intersection)) / len(union)

def complex_compare(vacancy_text: str, vacancy_skills: set[str], course_text: str, course_skills: set[str]):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([vacancy_text, course_text])
    texts_cosine = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    skills_set_similarity = get_set_similarity(course_skills=course_skills, vacancy_skills=vacancy_skills)

    score = skills_set_similarity * 0.5 + float(texts_cosine[0]) * 0.5

    return score

