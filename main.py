from tkinter import *
from factory_lib.model import users
from factory_lib.controller import login


def try_login():
    if login(users, entry_login.get(), entry_pass.get()):
        label_error.config(text="Zalogowano!")
    else:
        label_error.config(text="Nieprawidłowy login lub hasło!")


root = Tk()
root.title("Logowanie")
root.geometry("300x200")

Label(root, text="Login:").grid(row=0, column=0, padx=10, pady=10)
Label(root, text="Hasło:").grid(row=1, column=0, padx=10, pady=10)

entry_login = Entry(root)
entry_pass = Entry(root, show="*")
entry_login.grid(row=0, column=1, padx=10, pady=10)
entry_pass.grid(row=1, column=1, padx=10, pady=10)

label_error = Label(root, text="")
label_error.grid(row=2, column=0, columnspan=2)

Button(root, text="Zaloguj", command=try_login).grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()

