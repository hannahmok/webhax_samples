#!/usr/bin/env python3

import os
import pickle
import urllib.parse

# parse the query string (?x=1&y=2) into the parameters dict {'x': ['1'], 'y': ['2']}
parameters = urllib.parse.parse_qs(os.environ['QUERY_STRING'])

# send headers to start response

print('Content-type: text/html\n')
print('<html><body>')

# handle ?act=math to do math
# dict.get(x, y) will get the parameter x or return y if it doesn't exist
if parameters.get('act', [''])[0] == 'math':
    try:
        num1 = float(parameters.get('num1', [''])[0])
        num2 = float(parameters.get('num2', [''])[0])
        op = parameters.get('op', [''])[0]
        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        elif op == '/':
            result = num1 / num2
        else:
            raise KeyError
    except ValueError:
        print('<p><strong>Those are not numbers!</strong></p>')
    except KeyError:
        print('<p><strong>That is not an operation!</strong></p>')
    except ZeroDivisionError:
        print('<p><strong>Please do not divide by zero omg!!</strong></p>')
    else:
        print('<p>%f %s %f = <strong>%f</strong></p>' % (num1, op, num2, result))
        print('<p>Share this computation: <a href="index.py?token=%s">Permalink</a></p>' % pickle.dumps((num1, op, num2, result), -1).hex())

# handle ?token=xxx to share a math
elif 'token' in parameters:
    try:
        num1, op, num2, result = pickle.loads(bytes.fromhex(parameters['token'][0]))
        print('<p>%f %s %f = <strong>%f</strong></p>' % (num1, op, num2, result))
        print('<p>Share this computation: <a href="index.py?token=%s">Permalink</a></p>' % pickle.dumps((num1, op, num2, result), -1).hex())
    except Exception as e:
        print("<p><strong>Bad token! %s</strong></p>" % e)

# show form always
print('''\
<p>Do some math!</p>
<form action="index.py" method="GET">
    <input placeholder="Number" name="num1" size="1" />
    <select name="op">
        <option value="+">+</option>
        <option value="+">-</option>
        <option value="+">*</option>
        <option value="+">/</option>
    </select>
    <input placeholder="Number" name="num2" size="1" />
    <button type="submit" name="act" value="math">Get post</button><br />
</form>
</body></html>''')
