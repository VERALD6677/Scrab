import json
import requests
from bs4 import BeautifulSoup
import unicodedata

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
headers = {'Accept': '*/*', 'User-Agent': 'Chrome'}

def get_vacancies(url):
    vacancies = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    vacancy_elements = soup.find_all('div', class_='vacancy-serp-item')
    
    for vacancy_elem in vacancy_elements:
        title_elem = vacancy_elem.find('a', class_='bloko-link')
        if title_elem:
            title = title_elem.text.strip()
            link = title_elem['href']
            salary_elem = vacancy_elem.find('div', class_='vacancy-serp-item__sidebar')
            if salary_elem:
                salary = unicodedata.normalize('NFKD', salary_elem.text.strip())
            else:
                salary = 'З/П не указана'
            
            company_elem = vacancy_elem.find('a', class_='bloko-link bloko-link_secondary')
            if company_elem:
                company_name = company_elem.text.strip()
            else:
                company_name = 'Название компании не указано'
                
            location_elem = vacancy_elem.find('span', class_='vacancy-serp-item__meta-info')
            if location_elem:
                location = location_elem.text.strip()
            else:
                location = 'Местоположение не указано'
            
            vacancies.append({
                'title': title,
                'link': link,
                'salary': salary,
                'company_name': company_name,
                'location': location
            })
    return vacancies

def filter_vacancies(vacancies):
    filtered_vacancies = []
    for vacancy in vacancies:
        response = requests.get(vacancy['link'], headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        description_elem = soup.find('div', class_='g-user-content')
        if description_elem and any(keyword in description_elem.text for keyword in ['Django', 'django', 'Flask', 'flask']):
            filtered_vacancies.append(vacancy)
    return filtered_vacancies

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    vacancies = get_vacancies(url)
    filtered_vacancies = filter_vacancies(vacancies)
    save_to_json(filtered_vacancies, 'vacancies.json')

if __name__ == "__main__":
    main()

