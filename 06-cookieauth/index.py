#!/usr/bin/env python3

import os
import random
import scrypt
import string
import urllib.parse
import http.cookies

# parse HTTP params
parameters = urllib.parse.parse_qs(os.environ['QUERY_STRING'])
cookies = http.cookies.SimpleCookie(os.environ.get('HTTP_COOKIE', ''))

# make the /tmp/users directory if it doesn't exist
try:
    os.mkdir('/tmp/users/')
except OSError:
    pass

scrypt_N = 2**14  # 50ms
def hash_pw(pw):
    salt = ''.join(random.choice(string.ascii_letters) for _ in range(8))
    return salt + '$' + scrypt.hash(pw, salt, N=scrypt_N).hex()

def verify_pw(pw, saltenc):
    salt, enc = saltenc.split('$')
    return scrypt.hash(pw, salt) == bytes.fromhex(enc)

def sanitized(name):
    return all(c in string.ascii_letters + string.digits for c in name)

def db_lookup(name):
    if not sanitized(name):
        return False
    try:
        with open('/tmp/users/' + name, 'r') as fp:
            return fp.read()
    except OSError:
        return None

def db_insert(name, val):
    if not sanitized(name):
        return False
    try:
        with open('/tmp/users/' + name, 'x') as fp:
            fp.write(val)
        return True
    except OSError:
        return False

def set_logged_in(user):
    cookies['USERNAME'] = user
    cookies['TOKEN'] = hash_pw(user)

def set_logged_out():
    if 'USERNAME' in cookies:
        cookies['USERNAME']['expires'] = -1
    if 'TOKEN' in cookies:
        cookies['TOKEN']['expires'] = -1

def get_auth():
    if 'USERNAME' in cookies and \
        'TOKEN' in cookies and \
        cookies['USERNAME']['expires'] != -1 and \
        verify_pw(cookies['USERNAME'].value, cookies['TOKEN'].value):
        return cookies['USERNAME'].value
    return None

message = None

# handle ?act=signup to register a user
if parameters.get('act', [''])[0] == 'signup':
    username = parameters.get('username', [''])[0]
    password = parameters.get('password', [''])[0]
    if db_insert(username, hash_pw(password)):
        message = 'Signup success!'
        set_logged_in(username)
    else:
        message = 'Bad username - already in use or not alphanumeric'

# handle ?act=login to log in
elif parameters.get('act', [''])[0] == 'login':
    username = parameters.get('username', [''])[0]
    password = parameters.get('password', [''])[0]

    dbval = db_lookup(username)
    if dbval is not None and verify_pw(password, dbval):
        message = 'Login success!'
        set_logged_in(username)
    else:
        message = 'Login failed'

# handle ?act=logout to log out
elif parameters.get('act', [''])[0] == 'logout':
    set_logged_out()
    message = 'Goodbye!'

print('Content-type: text/html')
print(cookies)
print('')
print('<html><body>')

if message is not None:
    print('<p><strong>%s</strong></p>' % message)

# check auth cookie
auth = get_auth()

# if logged out, show login form
if auth is None:
    print('''\
<form action="index.py" method="GET">
    <input placeholder="username" name="username" /> <br />
    <input placeholder="password" type="password" name="password" /> <br />
    <button type="submit" name="act" value="login">Login</button>
    <button type="submit" name="act" value="signup">Sign up</button>
</form>''')

# otherwise, show greeting
else:
    print('''\
<p>Hello, %s!</p>
<p><a href="index.py?act=logout">Logout</a></p>''' % auth)

print('</body></html>')
