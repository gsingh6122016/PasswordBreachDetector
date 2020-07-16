import requests
import hashlib
import sys
import random
from tkinter import *
from tkinter import messagebox ,Menu

password_check = Tk()
password_check.title("Check Your password")


def request_api_data(first_char):
    url = 'https://api.pwnedpasswords.com/range/' + first_char
    res = requests.get(url)
    if res.status_code != 200 :
        raise RuntimeError(f'Error fenching : {res.status_code} ,check api and try again ')
    return res

def get_password_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h ,count in hashes :
        if h == hash_to_check :
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char ,tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leak_count(response ,tail)

def generator(password) :
    digits = "0123456789!@#$%^&*()"
    new_password=""
    for x in password :
        if not x.isdigit() :
            new_password = new_password + x
    if len(new_password) > 6 :
        new_password = new_password[:6]

    length = 10 - len(new_password)
    count = 1
    for i in range(0, length):
        new_password = new_password + random.choice(digits)
    count = pwned_api_check(new_password)
    while(count):
        new_password = new_password[:(len(new_password) - length)]
        for i in range(0, length):
            new_password = new_password + random.choice(digits)
        count = pwned_api_check(new_password)

    return new_password


# def main(args) :
#     for password in args :
#         count = pwned_api_check(password)
#         if count :
#             print(f'{password} was FOUND {count} times... you should change your password')
#             result = generator(password)
#             print(f'You can try {result}')
#         else:
#             print(f'{password} was NOT FOUND . carry on !')
#     return 'Program Complete!'
#
# if __name__ == '__main__':
#     sys.exit(main(sys.argv[1:]))


def main():
    count = pwned_api_check(enter_password.get())
    if count :
        result = generator(enter_password.get())
        messagebox.showinfo("Notification" ,f'{enter_password.get()} was FOUND {count} times...    You can try {result}')
    else:
        messagebox.showinfo("Notification" ,f'{enter_password.get()} was NOT FOUND . carry on !')

password_text = Label(password_check ,text = "  Enter Your password  " ,bg = "white" ,fg = "black" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove" )
password_text.grid(row = 0 ,column = 0,sticky = N+W+E+S ,padx = 5, pady = 5)

enter_password = Entry(password_check , borderwidth = 2 ,relief = "groove" ,width = 30 )
enter_password.grid(row = 0 ,column = 1,sticky = N+W+E+S ,padx = 5, pady = 5)

submit_button= Button(password_check ,text = "Submit" ,command = main  ,bg = "grey" ,fg = "blue" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove"  )
submit_button.grid(row = 1 ,column = 0 , columnspan = 2 ,padx = 5, pady = 5)


# password_text = Label(password_check ,text = f'{password} was FOUND {count} times...' ,bg = "white" ,fg = "black" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
# password_text.grid(row = 2 ,column = 0 ,columnspan = 2,sticky = N+W+E+S ,padx = 5, pady = 5)
#
# text = Label(password_check ,text = f'You can try {result}' ,bg = "white" ,fg = "black" ,font = "Lato 12 bold" ,padx = "2" ,pady = "2" ,borderwidth = 2 ,relief = "groove")
# text.grid(row = 3 ,column = 0 ,columnspan = 2,sticky = N+W+E+S ,padx = 5, pady = 5)

password_check.mainloop()
