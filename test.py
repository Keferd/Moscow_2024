from parsing_manager import ParsingManager
from text_preprocessing import preprocess_text
from nlp import compare_texts

PARSING_MANAGER = ParsingManager()


vacancy_text = """В Тинькофф Python является одним из самых распространенных языков разработки. На нем мы пишем многие сложные и нагруженные проекты. Поэтому ищем опытных разработчиков Python, которые смогут привнести экспертизу и вывести наши продукты на новый уровень

Нам всегда есть, что предложить начиная с внутренних проектов, заканчивая широко востребованными клиентскими продуктами

Задачи:

Проектирование компонентов систем
Организация процесса разработки
Написание и ревью кода
Наставление менее опытных коллег
Требования:

Отличное знание Python 3 и опыт промышленной разработки на Python от трех лет
Опыт многопоточного и асинхронного программирования
Опыт работы с фреймворками: FastApi, Flask, Tornado
Опыт работы с реляционными СУБД (PostgreSQL, Mysql)
Опыт построения распределённых высоконагруженных сервисов
Знание и применение паттернов проектирования
Условия:

Возможность работы в аккредитованной ИТ-компании
Работу в современном офисе. График работы — гибридный
3 дополнительных дня отпуска в году
Платформу обучения и развития Тинькофф Апгрейд. Курсы, тренинги, вебинары и базы знаний. Поддержка менторов и наставников, помощь в поиске точек роста и карьерном развитии

Заботу о здоровье. Оформим полис ДМС и предложим льготное страхование вашим близким
Компенсацию затрат на спорт по окончании испытательного срока
Компенсацию обедов
Достойную зарплату — обсудим ее на собеседовании
"""
vacancy_text = preprocess_text(vacancy_text)

course_texts = PARSING_MANAGER.texts

res = {}
for key, value in course_texts.items():
    res[key] = compare_texts(vacancy_text, value)

sorted_res = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
print(sorted_res, sep="\n")
