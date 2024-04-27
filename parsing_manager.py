import requests
import json
from collections import defaultdict
from bs4 import BeautifulSoup
from text_preprocessing import preprocess_text


class ParsingManager:
    url = "https://gb.ru/courses/programming"
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._texts = None
        self._skills = None

    @property
    def texts(self):
        if self._texts is None:
            self._texts, self._skills = self._get_parsing_data(self.url)
        return self._texts

    @property
    def skills(self):
        if self._skills is None:
            self._texts, self._skills = self._get_parsing_data(self.url)
        return self._skills

    @staticmethod
    def _get_parsing_data(url):
        response = requests.get(url)
        skills = defaultdict(set)
        texts = {}

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            links = soup.find_all('a', class_='card_full_link')

            for link in links:
                link_url = link['href']
                link_response = requests.get(link_url)

                if link_response.status_code == 200:
                    link_soup = BeautifulSoup(link_response.text, 'html.parser')
                    parsing_text = link_soup.get_text(separator=" ", strip=True)
                    texts[link_url] = preprocess_text(parsing_text)

                    divs = link_soup.find_all('div', class_=lambda x: x and (
                            'promo-tech__item' in x
                            or 'learn-instruments__item' in x
                            or "resume-instruments__wrapper" in x
                            or "gkb-promo__tag-wrapper" in x
                            or "gkb-promo__tag-wrapper" in x))

                    if not divs:
                        skills[link_url].add("No stacks")

                    for div in divs:
                        spans = div.find_all('span')
                        for span in spans:
                            if span.text.strip() != 'и другие':
                                skills[link_url].add(span.text.strip())
        return texts, skills


if __name__ == "__main__":
    parsing_manager = ParsingManager()
    res = parsing_manager.skills

    print()
    print(len(res.values()))
    for key, value in res.items():
        print(f"{key} содержит: {value}")
        res[key] = list(value)

    with open("stack.json", 'w', encoding="utf-8") as json_file:
        json.dump(res, json_file, indent=4, ensure_ascii=False)

    print()
    print(list(parsing_manager.texts.values())[0], sep="\n")
