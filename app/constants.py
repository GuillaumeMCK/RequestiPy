req_header = '''GET /posts?_page=§index§&_limit=§limit§ HTTP/1.1
Host: jsonplaceholder.typicode.com
User-Agent: curl/8.7.1
Accept: application/json
Connection: keep-alive
'''

req_body = ''''''

# language=python
helpers_code = '''
import re
def values(key, value=None):
    if value is not None:
        args[key] = value
    return args.get(key)

def update(string):
    return re.sub(re.compile(r"§(.*?)§"), lambda x: str(args.get(x.group(1), x.group(0))),string)
'''

# language=python
default_code = '''
from time import sleep

from services.request import fetch, ensure_code
from utils.io import save

values('index', 1)
values('limit', 20)

while values('index') < 200:
    try:
        h, b = (update(header), update(body))
        save(h + '\\n\\n' + b, f"request_{values('index')}.log ")
        response, status_code = fetch(h, b)
        ensure_code(status_code)
        save(response, f"response_{values('index')}.json")
        console.info(f"Page {values('index')} saved successfully")
    except Exception as e:
        console.error(str(e))
    finally:
        values('index', values('index') + values('limit'))
        sleep(0.05)
'''
