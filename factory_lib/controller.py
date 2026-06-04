import requests
from bs4 import BeautifulSoup


def get_coordinates(location: str) -> list:
    url = f'https://pl.wikipedia.org/wiki/{location}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response_html = BeautifulSoup(response.text, 'html.parser')
    latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
    longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
    return [latitude, longitude]


def login(users: list, login_input: str, password_input: str) -> bool:
    for user in users:
        if user['login'] == login_input and user['password'] == password_input:
            return True
    return False

# ========== FABRYKI ==========

def add_factory(factories: list, name: str, location: str, production: str) -> None:
    factories.append({'name': name, 'location': location, 'production': production})


def remove_factory(factories: list, index: int) -> None:
    factories.pop(index)


def update_factory(factories: list, index: int, name: str, location: str, production: str) -> None:
    factories[index]['name'] = name
    factories[index]['location'] = location
    factories[index]['production'] = production


def get_factories(factories: list) -> list:
    return factories