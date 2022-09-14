from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def generate():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_numbers = [random.choice(numbers) for _ in range(nr_symbols)]
    password_symbols = [random.choice(symbols) for _ in range(nr_numbers)]

    password_list = password_letters + password_numbers + password_symbols

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)    
    password_entry.insert(END, string=password)
    pyperclip.copy(password)
    
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    
    website = website_entry.get()
    password = password_entry.get()
    user = user_entry.get()
    new_data = {
        website.capitalize(): {
            "email": user,
            "password": password,
        }
    }

    if len(user) == 0 or len(password) == 0 or len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
        is_full = False
    else:
        is_full = True
    
    if is_full:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {user} \nPassword: {password} \nWebsite: {website} \nIs it okay to save?")

    if is_ok:

        try:
            with open("passwords.json", "r") as data:
                store = json.load(data)
                
        except FileNotFoundError:
            with open("passwords.json", "w") as data:    
                json.dump(new_data, data, indent=4)
        else:
           
            store.update(new_data)

            with open("passwords.json", "w") as data: 
                json.dump(store, data, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH INFORMATION ------------------------------- #
def find_password():
    website = website_entry.get().capitalize()

    try:
        with open("passwords.json", "r") as data:
            store = json.load(data)
        email = store[website]["email"]
        
    except FileNotFoundError:
        messagebox.showinfo(title="Error!", message="No data file found.")
    except KeyError:
       messagebox.showinfo(title="Error!", message="No details for the website exists.")
    else:
        passw = store[website]["password"]
        messagebox.showinfo(title="Website details", message=f"Website: {website}\nUsername: {email} \nPassword: {passw}")

# ---------------------------- UI SETUP ------------------------------- #
window=Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas=Canvas(width=200,height=200, highlightthickness=0)
logo_image=PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo_image)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row = 1, column = 0)
user_label = Label(text="Email/Username:")
user_label.grid(row = 2, column = 0)
password_label = Label(text="Password:")
password_label.grid(row = 3, column = 0)

website_entry = Entry(width=51)
website_entry.insert(END, string="Enter website")
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
user_entry = Entry(width=51)
user_entry.insert(END, string="asanka_sub@hotmail.com")
user_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=51)
password_entry.insert(END, string="Enter password")
password_entry.grid(row=3, column=1)
add_button = Button(text="Add", width=43, highlightthickness=0, command=save)
add_button.grid(row = 4, column = 1, columnspan=2)
search_button = Button(text="Search", highlightthickness=0, width=14, command=find_password)
search_button.grid(row=1, column = 3)
generate_button = Button(text="Generate Password", width=14, highlightthickness=0, command=generate)
generate_button.grid(row = 3, column = 3)



window.mainloop()