#!/usr/bin/env python3

import os
import sys
import urllib.parse

# parse the query string (?x=1&y=2) into the parameters dict {'x': ['1'], 'y': ['2']}
parameters = urllib.parse.parse_qs(os.environ['QUERY_STRING'])

# handle ?query=xx to search for text
if 'query' in parameters:
    print('Content-type: text/plain\n')
    sys.stdout.flush()
    os.system('grep "' + parameters['query'][0] + '" books/*')
    print('<end of results>')

# show form
else:
    print('Content-type: text/html\n')
    print('<html><body>')
    print('<p>Input text to search:</p>')
    print('<form action="index.py" method="GET">')
    print('<input placeholder="search term" name="query" /> <button type="submit">Search</button><br />')
    print('</form>')
    print('</body></html>')
