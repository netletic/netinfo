import ipaddress
import json
import socket
import time
from random import choice
from typing import Union

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response

KNOWN_PROXY_HEADERS = [
    "via",
    "forwarded",
    "client-ip",
    "useragent_via",
    "proxy_connection",
    "xproxy_connection",
    "http_pc_remote_addr",
    "http_client_ip",
    "http_x_appengine_country",
]


with open("rfc1925.txt") as fp:
    the_fundamental_truths = fp.readlines()


def respond(content: Union[str, dict]) -> Response:
    if isinstance(content, dict):
        content = json.dumps(content)
        media_type = "application/json"
    else:
        content = f"{content}\n"
        media_type = "text/plain"
    return Response(content, media_type=media_type)


def _ip(request: Request) -> str:
    ip_address = ipaddress.ip_address(request.client.host)
    ip_address_in_header = request.headers.get("X-Client-Ip")
    return str(ip_address) if ip_address.is_global else ip_address_in_header


def ip(request: Request) -> Response:
    ip = _ip(request)
    return respond(content=ip)


def ptr(request: Request) -> Response:
    try:
        ip = _ip(request)
        ptr, _, _ = socket.gethostbyaddr(ip)
    except socket.herror:
        return Response("", status_code=204)
    else:
        return respond(content=ptr)


def epoch(request: Request) -> Response:
    epoch_time = str(int(time.time()))
    return respond(content=epoch_time)


def headers(request: Request) -> Response:
    headers = dict(request.headers)
    return respond(content=headers)


def proxy(request: Request) -> Response:
    proxy_headers_found = {
        known_proxy_header: request.headers.get(known_proxy_header).strip()
        for known_proxy_header in KNOWN_PROXY_HEADERS
        if request.headers.get(known_proxy_header)
    }
    if proxy_headers_found:
        return respond(content=proxy_headers_found)
    else:
        Response("", status_code=204)


def test(request: Request) -> Response:
    return respond(content=choice(the_fundamental_truths))


lookup_types = {
    "ip": ip,
    "ptr": ptr,
    "epoch": epoch,
    "headers": headers,
    "proxy": proxy,
    "test": test,
}

app = FastAPI()


@app.get("/", include_in_schema=False)
async def netinfo(request: Request):
    for lookup_type, func in lookup_types.items():
        if lookup_type in request.base_url.hostname:
            return func(request)
    return ip(request)


if __name__ == "__main__":
    print(the_fundamental_truths)
