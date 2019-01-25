#!/usr/bin/env python3

import os
import time
import random
import urllib.parse

# parse the query string (?x=1&y=2) into the parameters dict {'x': ['1'], 'y': ['2']}
parameters = urllib.parse.parse_qs(os.environ['QUERY_STRING'])

# send headers to start response

print('Content-type: text/html\n')
print('<html><body>')

if 'ticket' in parameters:
    random.seed(int(time.time()))
    winner = '%04d' % random.randrange(0, 10000)
    ticket = parameters['ticket'][0]
    print("<p>You submitted the ticket <strong>%s</strong></p>" % ticket)
    print("<p>The winning number today is <strong>%s</strong></p>" % winner)

    if winner == ticket:
        print('<p><strong>Congratulations! You win!</strong></p>')

else:
    print('<form action="index.py" method="GET">')
    print('<input placeholder="ticket number" name="ticket" /> <button type="submit">Play the lottery</button>')
    print('</form>')

print('</body></html>')
