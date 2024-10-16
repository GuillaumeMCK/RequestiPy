from typing import Dict, Optional, Tuple

import http_client


def _parse_headers(header_str: str) -> Dict[str, str]:
    headers = {}
    lines = header_str.strip().splitlines()

    method, path, version = lines[0].split(' ', 2)
    headers.update({'Method': method.strip(), 'Path': path.strip(), 'Version': version.strip()})

    # Parse subsequent headers
    for line in lines[1:]:
        if ':' in line:
            key, value = map(str.strip, line.split(':', 1))
            headers[key] = value

    if 'Host' not in headers:
        raise ValueError("Missing 'Host' header.")

    return headers


def fetch(req_header: str, req_body: Optional[str] = None, port: int = 443) -> Tuple[str, int]:
    headers = _parse_headers(req_header)
    host = headers['Host']
    path = headers['Path']
    method = headers['Method']
    scheme = "https" if port == 443 else "http"
    url = f"{scheme}://{host}{path}"
    header_list = [f"{key}: {value}" for key, value in headers.items() if key not in {'Method', 'Path', 'Version'}]
    data, code = http_client.fetch(method, url, header_list, req_body)
    return data, code


def ensure_code(code: int) -> None:
    if code not in range(200, 300):
        raise Exception(f"HTTP request failed with status code {code}")
