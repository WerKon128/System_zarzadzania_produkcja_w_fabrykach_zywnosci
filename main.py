from tkinter import *
from tkinter import ttk
import tkintermapview
from factory_lib.model import factories, clients, employees, users
from factory_lib.controller import *

root = Tk()
root.title("System zarządzania produkcją w fabrykach żywności")
root.geometry("1200x800")
root.withdraw()

notebook = ttk.Notebook(root)

tab_factories = Frame(notebook)
tab_clients = Frame(notebook)
tab_employees = Frame(notebook)
tab_views = Frame(notebook)

notebook.add(tab_factories, text="Fabryki")
notebook.add(tab_clients, text="Klienci")
notebook.add(tab_employees, text="Pracownicy")
notebook.add(tab_views, text="Wyszukiwarka")

notebook.pack(fill=BOTH, expand=True)

# ========== FABRYKI ==========

frame_factory_list = Frame(tab_factories)
frame_factory_form = Frame(tab_factories)
frame_factory_details = Frame(tab_factories)
frame_factory_map = Frame(tab_factories)

frame_factory_list.grid(row=0, column=0, padx=10, pady=10, sticky=N)
frame_factory_form.grid(row=0, column=1, padx=10, pady=10, sticky=N)
frame_factory_details.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
frame_factory_map.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

# lista
Label(frame_factory_list, text="Lista fabryk:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)
entry_factory_filter = Entry(frame_factory_list)
entry_factory_filter.grid(row=1, column=0)
Button(frame_factory_list, text="Szukaj", command=lambda: filter_factories()).grid(row=1, column=1)
listbox_factories = Listbox(frame_factory_list, width=30, height=10)
listbox_factories.grid(row=2, column=0, columnspan=2)
Button(frame_factory_list, text="Szczegóły", command=lambda: show_factory_details()).grid(row=3, column=0)
Button(frame_factory_list, text="Edytuj", command=lambda: edit_factory_gui()).grid(row=3, column=1)
Button(frame_factory_list, text="Usuń", command=lambda: delete_factory_gui()).grid(row=4, column=0, columnspan=2)

# formularz
Label(frame_factory_form, text="Formularz:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)
Label(frame_factory_form, text="Nazwa:").grid(row=1, column=0, sticky=W)
Label(frame_factory_form, text="Lokalizacja:").grid(row=2, column=0, sticky=W)
Label(frame_factory_form, text="Produkcja:").grid(row=3, column=0, sticky=W)
entry_factory_name = Entry(frame_factory_form)
entry_factory_location = Entry(frame_factory_form)
entry_factory_production = Entry(frame_factory_form)
entry_factory_name.grid(row=1, column=1)
entry_factory_location.grid(row=2, column=1)
entry_factory_production.grid(row=3, column=1)
button_add_factory = Button(frame_factory_form, text="Dodaj fabrykę", command=lambda: add_factory_gui())
button_add_factory.grid(row=4, column=0, columnspan=2, pady=5)

# szczegóły
Label(frame_factory_details, text="Szczegóły:", font=("Arial", 10, "bold")).grid(row=0, column=0)
Label(frame_factory_details, text="Nazwa:").grid(row=1, column=0)
label_factory_name_val = Label(frame_factory_details, text="...")
label_factory_name_val.grid(row=1, column=1)
Label(frame_factory_details, text="Lokalizacja:").grid(row=1, column=2)
label_factory_location_val = Label(frame_factory_details, text="...")
label_factory_location_val.grid(row=1, column=3)
Label(frame_factory_details, text="Produkcja:").grid(row=1, column=4)
label_factory_production_val = Label(frame_factory_details, text="...")
label_factory_production_val.grid(row=1, column=5)

# mapa
map_factories = tkintermapview.TkinterMapView(frame_factory_map, width=500, height=400)
map_factories.set_position(52.2, 21.0)
map_factories.set_zoom(6)
map_factories.grid(row=0, column=0)


def refresh_factories():
    listbox_factories.delete(0, END)
    for f in get_factories(factories):
        listbox_factories.insert(END, f['name'])


def show_factory_details():
    i = listbox_factories.curselection()
    if not i:
        return
    i = i[0]
    f = factories[i]
    label_factory_name_val.config(text=f['name'])
    label_factory_location_val.config(text=f['location'])
    label_factory_production_val.config(text=f['production'])
    coords = get_coordinates(f['location'])
    map_factories.set_position(coords[0], coords[1])
    map_factories.set_zoom(12)


def add_factory_gui():
    name = entry_factory_name.get()
    location = entry_factory_location.get()
    production = entry_factory_production.get()
    if not name or not location or not production:
        return
    add_factory(factories, name, location, production)
    try:
        coords = get_coordinates(location)
        marker = map_factories.set_marker(coords[0], coords[1], text=name)
        factories[-1]['marker'] = marker
    except:
        pass
    entry_factory_name.delete(0, END)
    entry_factory_location.delete(0, END)
    entry_factory_production.delete(0, END)
    refresh_factories()

def edit_factory_gui():
    i = listbox_factories.curselection()
    if not i:
        return
    i = i[0]
    entry_factory_name.delete(0, END)
    entry_factory_location.delete(0, END)
    entry_factory_production.delete(0, END)
    entry_factory_name.insert(0, factories[i]['name'])
    entry_factory_location.insert(0, factories[i]['location'])
    entry_factory_production.insert(0, factories[i]['production'])
    button_add_factory.config(text="Zapisz zmiany", command=lambda: save_factory(i))


def save_factory(i):
    update_factory(factories, i, entry_factory_name.get(),
                   entry_factory_location.get(), entry_factory_production.get())
    if factories[i]['marker']:
        factories[i]['marker'].delete()
        factories[i]['marker'] = None
    try:
        coords = get_coordinates(factories[i]['location'])
        factories[i]['marker'] = map_factories.set_marker(coords[0], coords[1], text=factories[i]['name'])
    except:
        pass
    entry_factory_name.delete(0, END)
    entry_factory_location.delete(0, END)
    entry_factory_production.delete(0, END)
    button_add_factory.config(text="Dodaj fabrykę", command=lambda: add_factory_gui())
    refresh_factories()


def delete_factory_gui():
    i = listbox_factories.curselection()
    if not i:
        return
    i = i[0]
    if factories[i]['marker']:
        factories[i]['marker'].delete()
    remove_factory(factories, i)
    refresh_factories()


def filter_factories():
    search = entry_factory_filter.get().lower()
    listbox_factories.delete(0, END)
    for f in factories:
        if search in f['name'].lower() or search in f['location'].lower():
            listbox_factories.insert(END, f['name'])


refresh_factories()

def load_factory_markers():
    for f in factories:
        try:
            coords = get_coordinates(f['location'])
            f['marker'] = map_factories.set_marker(coords[0], coords[1], text=f['name'])
        except:
            pass



# ========== KLIENCI ==========

frame_client_list = Frame(tab_clients)
frame_client_form = Frame(tab_clients)
frame_client_details = Frame(tab_clients)
frame_client_map = Frame(tab_clients)

frame_client_list.grid(row=0, column=0, padx=10, pady=10, sticky=N)
frame_client_form.grid(row=0, column=1, padx=10, pady=10, sticky=N)
frame_client_details.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
frame_client_map.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

# lista
Label(frame_client_list, text="Lista klientów:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)
entry_client_filter = Entry(frame_client_list)
entry_client_filter.grid(row=1, column=0)
Button(frame_client_list, text="Szukaj", command=lambda: filter_clients()).grid(row=1, column=1)
listbox_clients = Listbox(frame_client_list, width=30, height=10)
listbox_clients.grid(row=2, column=0, columnspan=2)
Button(frame_client_list, text="Szczegóły", command=lambda: show_client_details()).grid(row=3, column=0)
Button(frame_client_list, text="Edytuj", command=lambda: edit_client_gui()).grid(row=3, column=1)
Button(frame_client_list, text="Usuń", command=lambda: delete_client_gui()).grid(row=4, column=0, columnspan=2)

# formularz
Label(frame_client_form, text="Formularz:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)
Label(frame_client_form, text="Imię i nazwisko:").grid(row=1, column=0, sticky=W)
Label(frame_client_form, text="Lokalizacja:").grid(row=2, column=0, sticky=W)
Label(frame_client_form, text="Firma:").grid(row=3, column=0, sticky=W)
Label(frame_client_form, text="Zakupy (po przecinku):").grid(row=4, column=0, sticky=W)
entry_client_name = Entry(frame_client_form)
entry_client_location = Entry(frame_client_form)
entry_client_company = Entry(frame_client_form)
entry_client_purchases = Entry(frame_client_form)
entry_client_name.grid(row=1, column=1)
entry_client_location.grid(row=2, column=1)
entry_client_company.grid(row=3, column=1)
entry_client_purchases.grid(row=4, column=1)
button_add_client = Button(frame_client_form, text="Dodaj klienta", command=lambda: add_client_gui())
button_add_client.grid(row=5, column=0, columnspan=2, pady=5)

# szczegóły
Label(frame_client_details, text="Szczegóły:", font=("Arial", 10, "bold")).grid(row=0, column=0)
Label(frame_client_details, text="Nazwa:").grid(row=1, column=0)
label_client_name_val = Label(frame_client_details, text="...")
label_client_name_val.grid(row=1, column=1)
Label(frame_client_details, text="Lokalizacja:").grid(row=1, column=2)
label_client_location_val = Label(frame_client_details, text="...")
label_client_location_val.grid(row=1, column=3)
Label(frame_client_details, text="Firma:").grid(row=1, column=4)
label_client_company_val = Label(frame_client_details, text="...")
label_client_company_val.grid(row=1, column=5)
Label(frame_client_details, text="Zakupy:").grid(row=1, column=6)
label_client_purchases_val = Label(frame_client_details, text="...")
label_client_purchases_val.grid(row=1, column=7)

# mapa
map_clients = tkintermapview.TkinterMapView(frame_client_map, width=500, height=400)
map_clients.set_position(52.2, 21.0)
map_clients.set_zoom(6)
map_clients.grid(row=0, column=0)


def refresh_clients():
    listbox_clients.delete(0, END)
    for c in get_clients(clients):
        listbox_clients.insert(END, c['name'])


def show_client_details():
    i = listbox_clients.curselection()
    if not i:
        return
    i = i[0]
    c = clients[i]
    label_client_name_val.config(text=c['name'])
    label_client_location_val.config(text=c['location'])
    label_client_company_val.config(text=c['company'])
    label_client_purchases_val.config(text=', '.join(c['purchases']))
    coords = get_coordinates(c['location'])
    map_clients.set_position(coords[0], coords[1])
    map_clients.set_zoom(12)


def add_client_gui():
    name = entry_client_name.get()
    location = entry_client_location.get()
    company = entry_client_company.get()
    purchases = [p.strip() for p in entry_client_purchases.get().split(',')]
    if not name or not location or not company:
        return
    add_client(clients, name, location, company, purchases)
    try:
        coords = get_coordinates(location)
        marker = map_clients.set_marker(coords[0], coords[1], text=name)
        clients[-1]['marker'] = marker
    except:
        pass
    entry_client_name.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_company.delete(0, END)
    entry_client_purchases.delete(0, END)
    refresh_clients()


def edit_client_gui():
    i = listbox_clients.curselection()
    if not i:
        return
    i = i[0]
    c = clients[i]
    entry_client_name.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_company.delete(0, END)
    entry_client_purchases.delete(0, END)
    entry_client_name.insert(0, c['name'])
    entry_client_location.insert(0, c['location'])
    entry_client_company.insert(0, c['company'])
    entry_client_purchases.insert(0, ', '.join(c['purchases']))
    button_add_client.config(text="Zapisz zmiany", command=lambda: save_client(i))


def save_client(i):
    if clients[i]['marker']:
        clients[i]['marker'].delete()
    purchases = [p.strip() for p in entry_client_purchases.get().split(',')]
    update_client(clients, i, entry_client_name.get(),
                  entry_client_location.get(), entry_client_company.get(), purchases)
    try:
        coords = get_coordinates(clients[i]['location'])
        clients[i]['marker'] = map_clients.set_marker(coords[0], coords[1], text=clients[i]['name'])
    except:
        pass
    entry_client_name.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_company.delete(0, END)
    entry_client_purchases.delete(0, END)
    button_add_client.config(text="Dodaj klienta", command=lambda: add_client_gui())
    refresh_clients()


def delete_client_gui():
    i = listbox_clients.curselection()
    if not i:
        return
    i = i[0]
    if clients[i]['marker']:
        clients[i]['marker'].delete()
    remove_client(clients, i)
    refresh_clients()


def filter_clients():
    search = entry_client_filter.get().lower()
    listbox_clients.delete(0, END)
    for c in clients:
        if search in c['name'].lower() or search in c['company'].lower():
            listbox_clients.insert(END, c['name'])


def load_client_markers():
    for c in clients:
        try:
            coords = get_coordinates(c['location'])
            c['marker'] = map_clients.set_marker(coords[0], coords[1], text=c['name'])
        except:
            pass


refresh_clients()


# ========== PRACOWNICY ==========

frame_employee_list = Frame(tab_employees)
frame_employee_form = Frame(tab_employees)
frame_employee_details = Frame(tab_employees)
frame_employee_map = Frame(tab_employees)

frame_employee_list.grid(row=0, column=0, padx=10, pady=10, sticky=N)
frame_employee_form.grid(row=0, column=1, padx=10, pady=10, sticky=N)
frame_employee_details.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
frame_employee_map.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

# lista
Label(frame_employee_list, text="Lista pracowników:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)
entry_employee_filter = Entry(frame_employee_list)
entry_employee_filter.grid(row=1, column=0)
Button(frame_employee_list, text="Szukaj", command=lambda: filter_employees()).grid(row=1, column=1)
listbox_employees = Listbox(frame_employee_list, width=30, height=10)
listbox_employees.grid(row=2, column=0, columnspan=2)
Button(frame_employee_list, text="Szczegóły", command=lambda: show_employee_details()).grid(row=3, column=0)
Button(frame_employee_list, text="Edytuj", command=lambda: edit_employee_gui()).grid(row=3, column=1)
Button(frame_employee_list, text="Usuń", command=lambda: delete_employee_gui()).grid(row=4, column=0, columnspan=2)

# formularz
Label(frame_employee_form, text="Formularz:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)
Label(frame_employee_form, text="Imię i nazwisko:").grid(row=1, column=0, sticky=W)
Label(frame_employee_form, text="Lokalizacja:").grid(row=2, column=0, sticky=W)
Label(frame_employee_form, text="Firma:").grid(row=3, column=0, sticky=W)
Label(frame_employee_form, text="Stanowisko:").grid(row=4, column=0, sticky=W)
entry_employee_name = Entry(frame_employee_form)
entry_employee_location = Entry(frame_employee_form)
entry_employee_company = Entry(frame_employee_form)
entry_employee_role = Entry(frame_employee_form)
entry_employee_name.grid(row=1, column=1)
entry_employee_location.grid(row=2, column=1)
entry_employee_company.grid(row=3, column=1)
entry_employee_role.grid(row=4, column=1)
button_add_employee = Button(frame_employee_form, text="Dodaj pracownika", command=lambda: add_employee_gui())
button_add_employee.grid(row=5, column=0, columnspan=2, pady=5)

# szczegóły
Label(frame_employee_details, text="Szczegóły:", font=("Arial", 10, "bold")).grid(row=0, column=0)
Label(frame_employee_details, text="Nazwa:").grid(row=1, column=0)
label_employee_name_val = Label(frame_employee_details, text="...")
label_employee_name_val.grid(row=1, column=1)
Label(frame_employee_details, text="Lokalizacja:").grid(row=1, column=2)
label_employee_location_val = Label(frame_employee_details, text="...")
label_employee_location_val.grid(row=1, column=3)
Label(frame_employee_details, text="Firma:").grid(row=1, column=4)
label_employee_company_val = Label(frame_employee_details, text="...")
label_employee_company_val.grid(row=1, column=5)
Label(frame_employee_details, text="Stanowisko:").grid(row=1, column=6)
label_employee_role_val = Label(frame_employee_details, text="...")
label_employee_role_val.grid(row=1, column=7)

# mapa
map_employees = tkintermapview.TkinterMapView(frame_employee_map, width=500, height=400)
map_employees.set_position(52.2, 21.0)
map_employees.set_zoom(6)
map_employees.grid(row=0, column=0)


def refresh_employees():
    listbox_employees.delete(0, END)
    for e in get_employees(employees):
        listbox_employees.insert(END, e['name'])


def show_employee_details():
    i = listbox_employees.curselection()
    if not i:
        return
    i = i[0]
    e = employees[i]
    label_employee_name_val.config(text=e['name'])
    label_employee_location_val.config(text=e['location'])
    label_employee_company_val.config(text=e['company'])
    label_employee_role_val.config(text=e['role'])
    coords = get_coordinates(e['location'])
    map_employees.set_position(coords[0], coords[1])
    map_employees.set_zoom(12)


def add_employee_gui():
    name = entry_employee_name.get()
    location = entry_employee_location.get()
    company = entry_employee_company.get()
    role = entry_employee_role.get()
    if not name or not location or not company or not role:
        return
    add_employee(employees, name, location, company, role)
    try:
        coords = get_coordinates(location)
        marker = map_employees.set_marker(coords[0], coords[1], text=name)
        employees[-1]['marker'] = marker
    except:
        pass
    entry_employee_name.delete(0, END)
    entry_employee_location.delete(0, END)
    entry_employee_company.delete(0, END)
    entry_employee_role.delete(0, END)
    refresh_employees()

def edit_employee_gui():
    i = listbox_employees.curselection()
    if not i:
        return
    i = i[0]
    e = employees[i]
    entry_employee_name.delete(0, END)
    entry_employee_location.delete(0, END)
    entry_employee_company.delete(0, END)
    entry_employee_role.delete(0, END)
    entry_employee_name.insert(0, e['name'])
    entry_employee_location.insert(0, e['location'])
    entry_employee_company.insert(0, e['company'])
    entry_employee_role.insert(0, e['role'])
    button_add_employee.config(text="Zapisz zmiany", command=lambda: save_employee(i))


def save_employee(i):
    if employees[i]['marker']:
        employees[i]['marker'].delete()
    update_employee(employees, i, entry_employee_name.get(),
                    entry_employee_location.get(), entry_employee_company.get(),
                    entry_employee_role.get())
    try:
        coords = get_coordinates(employees[i]['location'])
        employees[i]['marker'] = map_employees.set_marker(coords[0], coords[1], text=employees[i]['name'])
    except:
        pass
    entry_employee_name.delete(0, END)
    entry_employee_location.delete(0, END)
    entry_employee_company.delete(0, END)
    entry_employee_role.delete(0, END)
    button_add_employee.config(text="Dodaj pracownika", command=lambda: add_employee_gui())
    refresh_employees()


def delete_employee_gui():
    i = listbox_employees.curselection()
    if not i:
        return
    i = i[0]
    if employees[i]['marker']:
        employees[i]['marker'].delete()
    remove_employee(employees, i)
    refresh_employees()


def filter_employees():
    search = entry_employee_filter.get().lower()
    listbox_employees.delete(0, END)
    for e in employees:
        if search in e['name'].lower() or search in e['company'].lower():
            listbox_employees.insert(END, e['name'])


def load_employee_markers():
    for e in employees:
        try:
            coords = get_coordinates(e['location'])
            e['marker'] = map_employees.set_marker(coords[0], coords[1], text=e['name'])
        except:
            pass


refresh_employees()


# ========== WYSZUKIWARKA ==========

frame_views_filters = Frame(tab_views)
frame_views_results = Frame(tab_views)
frame_views_map = Frame(tab_views)

frame_views_filters.grid(row=0, column=0, padx=10, pady=10, sticky=N)
frame_views_results.grid(row=0, column=1, padx=10, pady=10, sticky=N)
frame_views_map.grid(row=0, column=2, padx=10, pady=10, sticky=N)

Label(frame_views_filters, text="Filtry:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)

Label(frame_views_filters, text="Nazwa fabryki:").grid(row=1, column=0, sticky=W)
entry_filter_factory = Entry(frame_views_filters)
entry_filter_factory.grid(row=1, column=1)
Button(frame_views_filters, text="Klienci tej fabryki", command=lambda: show_clients_by_factory()).grid(row=2, column=0, columnspan=2, pady=3)
Button(frame_views_filters, text="Pracownicy tej fabryki", command=lambda: show_employees_by_factory()).grid(row=3, column=0, columnspan=2, pady=3)

Label(frame_views_filters, text="Imię i nazwisko klienta:").grid(row=4, column=0, sticky=W, pady=(15, 0))
entry_filter_client = Entry(frame_views_filters)
entry_filter_client.grid(row=4, column=1, pady=(15, 0))
Button(frame_views_filters, text="Zakupy klienta", command=lambda: show_purchases_by_client()).grid(row=5, column=0, columnspan=2, pady=3)

Label(frame_views_results, text="Wyszukiwarka:", font=("Arial", 10, "bold")).grid(row=0, column=0)
listbox_views = Listbox(frame_views_results, width=50, height=20)
listbox_views.grid(row=1, column=0)

map_views = tkintermapview.TkinterMapView(frame_views_map, width=500, height=400)
map_views.set_position(52.2, 21.0)
map_views.set_zoom(6)
map_views.grid(row=0, column=0)


def show_clients_by_factory():
    factory_name = entry_filter_factory.get()
    listbox_views.delete(0, END)
    map_views.delete_all_marker()
    result = get_clients_by_factory(clients, factory_name)
    if not result:
        listbox_views.insert(END, "Brak klientów dla tej fabryki")
        return
    for c in result:
        listbox_views.insert(END, f"{c['name']} – {c['location']}")
        try:
            coords = get_coordinates(c['location'])
            map_views.set_marker(coords[0], coords[1], text=c['name'])
        except:
            pass


def show_employees_by_factory():
    factory_name = entry_filter_factory.get()
    listbox_views.delete(0, END)
    map_views.delete_all_marker()
    result = get_employees_by_factory(employees, factory_name)
    if not result:
        listbox_views.insert(END, "Brak pracowników dla tej fabryki")
        return
    for e in result:
        listbox_views.insert(END, f"{e['name']} – {e['role']}")
        try:
            coords = get_coordinates(e['location'])
            map_views.set_marker(coords[0], coords[1], text=e['name'])
        except:
            pass

def show_purchases_by_client():
    client_name = entry_filter_client.get()
    listbox_views.delete(0, END)
    map_views.delete_all_marker()
    result = get_purchases_by_client(clients, client_name)
    if not result:
        listbox_views.insert(END, "Brak zakupów dla tego klienta")
        return
    for c in clients:
        if c['name'] == client_name:
            try:
                coords = get_coordinates(c['location'])
                map_views.set_marker(coords[0], coords[1], text=c['name'])
            except:
                pass
    for p in result:
        listbox_views.insert(END, p)

def show_login():
    login_window = Toplevel(root)
    login_window.title("Logowanie")
    login_window.geometry("300x180")
    login_window.grab_set()
    login_window.protocol("WM_DELETE_WINDOW", root.destroy)

    Label(login_window, text="Login:").grid(row=0, column=0, padx=10, pady=10)
    Label(login_window, text="Hasło:").grid(row=1, column=0, padx=10, pady=10)

    entry_login = Entry(login_window)
    entry_pass = Entry(login_window, show="*")
    entry_login.grid(row=0, column=1, padx=10, pady=10)
    entry_pass.grid(row=1, column=1, padx=10, pady=10)

    label_error = Label(login_window, text="", fg="red")
    label_error.grid(row=2, column=0, columnspan=2)

    def try_login():
        if login(users, entry_login.get(), entry_pass.get()):
            login_window.destroy()
            root.deiconify()
            load_factory_markers()
            load_client_markers()
            load_employee_markers()
        else:
            label_error.config(text="Nieprawidłowy login lub hasło!")

    Button(login_window, text="Zaloguj", command=try_login).grid(row=3, column=0, columnspan=2, pady=10)


show_login()

root.mainloop()