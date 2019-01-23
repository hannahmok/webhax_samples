#!/usr/bin/env python3

import os
import random
import urllib.parse

# make the /tmp/content directory if it doesn't exist
try:
    os.mkdir('/tmp/content/')
except OSError:
    pass

# parse the query string (?x=1&y=2) into the parameters dict {'x': ['1'], 'y': ['2']}
parameters = urllib.parse.parse_qs(os.environ['QUERY_STRING'])

# send headers to start response

print('Content-type: text/html\n')
print('<html><body>')

# handle ?act=new to create a post
# dict.get(x, y) will get the parameter x or return y if it doesn't exist
if parameters.get('act', [''])[0] == 'new':
    postid = random.randrange(1000, 100000000)
    with open('/tmp/content/' + str(postid), 'w') as fp:
        fp.write(parameters.get('text', [''])[0])
    print('<p><strong>Post uploaded with id %d</strong></p>' % postid)

# handle ?act=get to look up a post
elif parameters.get('act', [''])[0] == 'get':
    try:
        with open('/tmp/content/' + parameters.get('id', [''])[0]) as fp:
            print("<p><strong>Here's your post!</strong></p>")
            print("<p>" + fp.read() + "</p>")
    except OSError:
        print("<p><strong>Could not find post!</strong></p>")

# show form always
print('<form action="index.py" method="GET">')
print('<input placeholder="post id" name="id" /> <button type="submit" name="act" value="get">Get post</button><br />')
print('<input placeholder="post text" name="text" /> <button type="submit" name="act" value="new">Submit post</button><br />')
print('</form>')

print('</body></html>')
