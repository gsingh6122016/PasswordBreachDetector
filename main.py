import requests
import hashlib
import sys

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

def main(args) :
    for password in args :
        count = pwned_api_check(password)
        if count :
            print(f'{password} was FOUND {count} times... you should change your password')
        else:
            print(f'{password} was NOT FOUND . carry on !')
    return 'Program Complete!'
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
