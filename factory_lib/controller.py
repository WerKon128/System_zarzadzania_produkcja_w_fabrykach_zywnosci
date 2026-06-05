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

# ========== PRACOWNICY ==========

def add_employee(employees: list, name: str, location: str, company: str, role: str) -> None:
    employees.append({'name': name, 'location': location, 'company': company, 'role': role})


def remove_employee(employees: list, index: int) -> None:
    employees.pop(index)


def update_employee(employees: list, index: int, name: str, location: str, company: str, role: str) -> None:
    employees[index]['name'] = name
    employees[index]['location'] = location
    employees[index]['company'] = company
    employees[index]['role'] = role


def get_employees(employees: list) -> list:
    return employees


def get_employees_by_factory(employees: list, factory_name: str) -> list:
    return [e for e in employees if e['company'] == factory_name]


def get_purchases_by_client(clients: list, client_name: str) -> list:
    for client in clients:
        if client['name'] == client_name:
            return client['purchases']
    return []