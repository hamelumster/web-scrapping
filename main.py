import requests
import bs4
import json

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

# Добавляем headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_vacancy_links(url):
    response = requests.get(url, headers=headers)
    html_data = response.text
    soup = bs4.BeautifulSoup(html_data, features='lxml')

    # Найти все вакансии
    # all_vacancies = soup.find_all('a', class_='serp-item__title')
    all_vacancies = soup.find_all('span', class_='serp-item__title-link-wrapper')

    vacancy_links = []
    for vacancy in all_vacancies:
        link = vacancy.find('a').get('href')
        vacancy_links.append(link)
        vacancy_links.append(link)
    return vacancy_links

print('Формирую JSON-файл...')

def parsed_data(vacancy_links):
    parsed_file = []
    for vacancy in vacancy_links:
        vacancy_response = requests.get(vacancy, headers=headers)
        vacancy_html = vacancy_response.text
        vacancy_soup = bs4.BeautifulSoup(vacancy_html, features='lxml')

        # Найти описание вакансии
        description_div = vacancy_soup.find('div', class_='vacancy-description')
        description_text = description_div.get_text(strip=True) if description_div else ''

        # Проверить наличие слов "Django" и "Flask"
        if 'Django' in description_text or 'Flask' in description_text:

            # Вилка ЗП
            vacancy_wage = vacancy_soup.find('span', class_='magritte-text___pbpft_3-0-12 magritte-text_style-primary___AQ7MW_3-0-12 magritte-text_typography-label-1-regular___pi3R-_3-0-12')
            vacancy_wage_text = vacancy_wage.get_text(strip=True) if vacancy_wage else 'N/A'

            # Название компании
            company_name = vacancy_soup.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite')
            company_name_text = company_name.get_text(strip=True) if company_name else 'N/A'

            # Город
            location = vacancy_soup.find('div', class_='magritte-text___pbpft_3-0-12 magritte-text_style-primary___AQ7MW_3-0-12 magritte-text_typography-paragraph-2-regular___VO638_3-0-12')
            location_text = location.get_text(strip=True) if location else 'N/A'

            # Добавить данные вакансии в словарь
            vacancy_data = {
                'Вилка ЗП': vacancy_wage_text,
                'Название компании': company_name_text,
                'Город': location_text,
                'Ссылка': vacancy
            }

            if vacancy_data in parsed_file:
                pass
            else:
                parsed_file.append(vacancy_data)

    return parsed_file

# Получить ссылки на вакансии
vacancy_links = get_vacancy_links(url)

# Парсить данные по вакансиям
result = parsed_data(vacancy_links)

# Записать данные в JSON-файл
with open ('vacancies.json', 'w', encoding='UTF-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
print('JSON-файл готов')






