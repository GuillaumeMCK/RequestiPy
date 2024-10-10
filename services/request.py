import http.client
from typing import Dict, Optional


def _parse_headers(header_str: str) -> Dict[str, str]:
    """Parse raw HTTP headers into a dictionary."""
    headers = {}
    lines = header_str.strip().splitlines()

    method, path, version = lines[0].split(' ', 2)
    headers.update({'Method': method, 'Path': path, 'Version': version})

    for line in lines[1:]:
        if ':' in line:
            key, value = map(str.strip, line.split(': ', 1))
            headers[key] = value
        else:
            print(f"Warning: Malformed header line '{line}'")

    return headers


def fetch(req_header: str, req_body: Optional[str] = None, port: int = 443) -> str:
    """Fetch an HTTP response from a server."""
    headers = _parse_headers(req_header)
    host = headers['Host']

    conn = http.client.HTTPSConnection(host, port) if port == 443 else http.client.HTTPConnection(host, port)

    try:
        conn.request(headers['Method'], headers['Path'], body=req_body, headers=headers)

        response = conn.getresponse()
        response_data = response.read()
    finally:
        conn.close()

    return response_data.decode()
