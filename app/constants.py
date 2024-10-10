req_header = '''GET /posts?_page=1&_limit=10 HTTP/1.1
Host: jsonplaceholder.typicode.com
User-Agent: curl/8.7.1
Accept: application/json
Connection: keep-alive
'''

req_body = ''''''

# language=python
default_code = '''
import re

from services.request import fetch
from utils.io import save

console: any
header: str
body: str | None

index = 0
limit = 10


vars = []
reg = re.compile(r"\$\$(.*?)\$\$")

console.info("Sending request")
console.log(header)
console.log(str(body)[:500])

try:
    response = fetch(header, body)
    if not response:
        console.warning("No response received")
    else:
        console.success("Request sent successfully")
        console.log(response[:80] + "...")
        console.info("Saving response to file")
        save(response, file="response.json")
except Exception as e:
    console.error(str(e))
    console.error("Failed to send request")
'''
