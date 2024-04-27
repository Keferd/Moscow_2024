import requests
from bs4 import BeautifulSoup
from text_preprocessing import preprocess_text, remove_punct, extract_number
from const import KEY_SKILLS


class ParsingManager:
    url = "https://gb.ru/courses/programming"
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._courses = None

    @property
    def courses(self):
        if self._courses is None:
            self._courses = self._get_parsing_courses_data(self.url)
        return self._courses

    def _get_parsing_courses_data(self, url):
        response = requests.get(url)
        courses = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            links = soup.find_all('a', class_='card_full_link')

            for link in links:
                link_url = link['href']
                link_response = requests.get(link_url)

                if link_response.status_code == 200:
                    link_soup = BeautifulSoup(link_response.text, 'html.parser')
                    if link_url == "https://gb.ru/geek_university/engineer/blockchain":
                        continue

                    course = {
                        "link": link_url,
                        "tittle": self._get_tittle(link_soup),
                        "skills": self._get_skills(link_soup),
                        "text": self._get_text(link_soup),
                        "formats": self._get_formats(),
                        "duration": self._get_duration(link_soup),
                        "price": self._get_price(link_soup),
                        "description": self._get_description(link_soup)
                    }

                    courses.append(course)

        return courses

    @staticmethod
    def _get_text(link_soup):
        key_text_divs = link_soup.find_all('div', class_=lambda x: x and (
                'gkb-promo__title' in x
                or 'gkb-promo__text' in x
                or "gkb-promo__tag-wrapper" in x
                # or "gkb-about__column" in x
                or "gkb-acc__wrapper" in x
                or "resume-update__content-container" in x
                or "cover__content" in x
                or "resume-example" in x
                or "promo__content" in x
                or "profession-info-card" in x
                or "profession-task-card" in x
                or "learn-instruments" in x
                or "gkb-spec-po__card-tag" in x
                or "program" in x
                or "want-card" in x
                or "making__decor" in x
                or "path-program__column-right" in x
                or "training-program__accordion" in x
                or "gkb-spec-po__card" in x))

        parsing_text = ' '.join(div.get_text(separator=" ", strip=True) for div in key_text_divs)
        text = preprocess_text(parsing_text)
        return text

    @staticmethod
    def _get_skills(link_soup):
        skills = set()
        key_skills_divs = link_soup.find_all('div', class_=lambda x: x and (
                'promo-tech__item' in x
                or 'learn-instruments__item' in x
                or 'resume-update-instruments__instrument' in x
                or "resume-instruments__wrapper" in x
                or "gkb-spec-po__card-tag" in x
                or "gkb-promo__tag-wrapper" in x))

        if not key_skills_divs:
            skills.add("No skills")

        for div in key_skills_divs:
            spans = div.find_all('span')
            for span in spans:
                if span.text.strip() != 'и другие':
                    skill = span.text.strip()
                    if skill in KEY_SKILLS:
                        skills.add(span.text.strip())
        return list(skills)

    @staticmethod
    def _get_description(link_soup):
        description = ""
        key_description = link_soup.find_all(class_=lambda x: x and (
                'gkb-promo__text' in x
                or 'cover__description' in x
                or "promo__description" in x))

        for div in sorted(key_description, key=len):
            description = div.get_text(separator=" ", strip=True)
            if description and "Длительность" not in description:
                break
        return description

    @staticmethod
    def _get_tittle(link_soup):
        key_tittle = link_soup.find_all(class_=lambda x: x and (
                'gkb-promo__title' in x
                or 'cover__title' in x
                or "promo__title" in x))

        tittle = [div.get_text(separator=" ", strip=True) for div in key_tittle]
        return tittle[0]

    @staticmethod
    def _get_price(link_soup):
        key_price = link_soup.find_all(class_=lambda x: x and (
                'promo-price-card__current' in x
                or 'gkb-promo__price-current' in x
                or "price__value" in x))

        price = [div.get_text(separator=" ", strip=True) for div in key_price]
        new_price = extract_number(price[0])
        return new_price

    @staticmethod
    def _get_duration(link_soup):
        key_duration = link_soup.find_all(class_=lambda x: x and (
                'promo__info' in x
                or 'gkb-promo__text-secondary' in x))

        duration = [div.get_text(separator=" ", strip=True) for div in key_duration]
        if not duration:
            return None
        return extract_number(duration[0])

    @staticmethod
    def _get_formats():
        formats = ["Занятие в группе с преподавателем", "Онлайн-встречи с экспертами", "Онлайн-лекции и вебинары",
                   "Видеоуроки с обратной связью от экспертов", "Практические занятия", "Домашние работы"]
        return formats

    @staticmethod
    def get_vacancy_data_from_hh(url):
        headers = {
            "Accept": "*/*",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        skills = set()
        text = ""

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            key_text_divs = soup.find_all('div', class_=lambda x: x and (
                    'tmpl_hh_about' in x
                    or 'tmpl_hh_content' in x
                    or 'vacancy-branded-user-content' in x
                    # or "g-user-content" in x
                    or 'bloko-tag-list' in x
                    or 'vacancy-title' in x))
            text = ' '.join(div.get_text(separator=" ", strip=True) for div in key_text_divs)
            text = remove_punct(text)

            for word in text.split():
                if word.lower() in [skill.lower() for skill in KEY_SKILLS]:
                    skills.add(word)

        return text.lower(), list(skills)


if __name__ == "__main__":
    parsing_manager = ParsingManager()
