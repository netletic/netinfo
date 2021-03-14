import ipaddress
import json
import socket
import time

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response

POSSIBLE_PROXY_HEADERS = [
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


def respond(content):
    if isinstance(content, dict):
        content = json.dumps(content)
        media_type = "application/json"
    else:
        content = f"{content}\n"
        media_type = "text/plain"
    return Response(content, media_type=media_type)


def _ip(request):
    ip_address = ipaddress.ip_address(request.client.host)
    ip_address_in_header = request.headers.get("X-Client-Ip")
    return ip_address if ip_address.is_global else ip_address_in_header


def ip(request):
    ip = _ip(request)
    return respond(content=ip)


def ptr(request):
    try:
        ip = _ip(request)
        ptr, _, _ = socket.gethostbyaddr(ip)
    except socket.herror:
        return Response("", status_code=204)
    else:
        return respond(content=ptr)


def epoch(request):
    epoch_time = str(int(time.time()))
    return respond(content=epoch_time)


def headers(request):
    headers = dict(request.headers)
    return respond(content=headers)


def proxy(request):
    proxy_headers = {
        proxy_header: request.headers.get(proxy_header).strip()
        for proxy_header in POSSIBLE_PROXY_HEADERS
        if request.headers.get(proxy_header)
    }
    return (
        respond(content=proxy_headers)
        if proxy_headers
        else Response("", status_code=204)
    )


def test(request):
    return Response("bumblebee\n", media_type="text/plain")


REQUEST_TYPES = {
    "ip": ip,
    "ptr": ptr,
    "epoch": epoch,
    "headers": headers,
    "proxy": proxy,
    "test": test,
}

app = FastAPI()


@app.get("/")
def netinfo(request: Request):
    for request_type, func in REQUEST_TYPES.items():
        if request_type in request.base_url.hostname:
            return func(request)
    return ip(request)
