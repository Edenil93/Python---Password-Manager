from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_lts = [random.choice(letters) for _ in range(nr_letters)]

    password_nums = [random.choice(numbers) for _ in range(nr_numbers)]

    password_sym = [random.choice(symbols) for _ in range(nr_symbols)]

    password_list = password_lts + password_nums + password_sym

    random.shuffle(password_list)

    password = "".join(password_list)

    if len(pass_entry.get()) > 10:
        return

    pass_entry.insert(0, password)
    pyperclip.copy(password)


def close_window():
    window.destroy()


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_entry.get()
    email = mail_entry.get()
    password = pass_entry.get()

    new_data = {
        website: {
            "Email": email,
            "Password": password
        }
    }

    if len(website) == 0:
        messagebox.showinfo(title="Invalid Input", message="You haven't specified a website")
        return
    elif len(email) == 0:
        messagebox.showinfo(title="Invalid Input", message="You haven't specified an Email address")
        return
    elif len(password) == 0:
        messagebox.showinfo(title="Invalid Input", message="You haven't specified a password")
        return
    else:
        try:
            with open("passwords.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("passwords.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("passwords.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            mail_entry.delete(0, END)
            pass_entry.delete(0, END)
            mail_entry.insert(0, "eden.ilan93@gmail.com")


def find_password():
    website = website_entry.get()

    with open("passwords.json", mode="r") as data_file:
        data = json.load(data_file)
        if website in data:
            messagebox.showinfo(title=website,
                                message="Email: " + data[website]['Email'] + "\nPassword: " + data[website]['Password'])
        else:
            messagebox.showinfo(title="No data found for this website",
                                message="You haven't saved any data for this website yet.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200)
photo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo_image)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_entry = Entry(width=33)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=1)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=1, columnspan=2)

mail_label = Label(text="Email/Username:")
mail_label.grid(column=0, row=2, pady=5)
mail_entry = Entry(width=52)
mail_entry.insert(0, "eden.ilan93@gmail.com")
mail_entry.grid(column=1, row=2, columnspan=2)

pass_label = Label(text="Password:")
pass_label.grid(column=0, row=3, pady=5)
pass_entry = Entry(width=33)
pass_entry.grid(column=1, row=3)

pass_gen_button = Button(text="Generate Password", command=gen_password)
pass_gen_button.grid(column=2, row=3)

add_button = Button(text="Add", width=45, command=save_data)
add_button.grid(column=1, row=4, columnspan=2, pady=5)

close_button = Button(text="Done", width=15, command=close_window)
close_button.grid(column=1, row=5, columnspan=2, pady=5)

window.mainloop()
