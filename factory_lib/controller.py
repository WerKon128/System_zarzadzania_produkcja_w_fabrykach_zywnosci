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

# ========== KLIENCI ==========

def add_client(clients: list, name: str, location: str, company: str, purchases: list) -> None:
    clients.append({'name': name, 'location': location, 'company': company, 'purchases': purchases})


def remove_client(clients: list, index: int) -> None:
    clients.pop(index)


def update_client(clients: list, index: int, name: str, location: str, company: str, purchases: list) -> None:
    clients[index]['name'] = name
    clients[index]['location'] = location
    clients[index]['company'] = company
    clients[index]['purchases'] = purchases


def get_clients(clients: list) -> list:
    return clients


def get_clients_by_factory(clients: list, factory_name: str) -> list:
    return [c for c in clients if c['company'] == factory_name]