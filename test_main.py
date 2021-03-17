import random
import time

from fastapi.testclient import TestClient
from freezegun import freeze_time

from main import app

client = TestClient(app)


DOMAIN = "example.org"
CLIENT_IP = "198.51.100.84"
RANDOM_STRING = "ouzndzh2780235ne7ewt7otf26lqzbv15bvnsv38xy0h8hk8"


def test_client_ip_in_header():
    response = client.get(
        "/", headers={"host": f"ip.{DOMAIN}", "x-client-ip": CLIENT_IP}
    )
    assert response.status_code == 200
    assert response.text == f"{CLIENT_IP}\n"


def test_client_ip_not_in_header():
    response = client.get("/", headers={"host": f"ip.{DOMAIN}"})
    assert response.status_code == 200
    assert response.text == "testclient\n"


def test_ptr_does_not_exist():
    response = client.get(
        "/", headers={"host": f"ptr.{DOMAIN}", "x-client-ip": CLIENT_IP}
    )
    assert response.status_code == 204


def test_ptr_exists():
    response = client.get(
        "/", headers={"host": f"ptr.{DOMAIN}", "x-client-ip": "127.0.0.1"}
    )
    expected_ptr = "localhost"
    assert response.status_code == 200
    assert response.text == f"{expected_ptr}\n"


@freeze_time("1997-11-11")
def test_epoch_time():
    response = client.get("/", headers={"host": f"epoch.{DOMAIN}"})
    expected_epoch_time = str(int(time.time()))
    assert response.status_code == 200
    assert response.text == f"{expected_epoch_time}\n"


def test_headers():
    headers = {
        "host": f"headers.{DOMAIN}",
        RANDOM_STRING: RANDOM_STRING,
    }
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.json().get(RANDOM_STRING) == RANDOM_STRING


def test_known_proxy_header_found():
    headers = {
        "host": f"proxy.{DOMAIN}",
        "client-ip": CLIENT_IP,
        "proxy_connection": CLIENT_IP,
    }
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.json().get("client-ip") == CLIENT_IP
    assert response.json().get("proxy_connection") == CLIENT_IP


def test_no_known_proxy_headers_found():
    headers = {"host": f"proxy.{DOMAIN}"}
    response = client.get("/", headers=headers)
    assert response.status_code == 204


def test_fundamental_networking_truth():
    headers = {"host": f"test.{DOMAIN}"}
    expected_truth = "It is more complicated than you think.\n\n"
    random.seed(11)
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.text == expected_truth


def test_unknown_lookup_type_returns_ip():
    headers = {"host": f"{RANDOM_STRING}.{DOMAIN}", "x-client-ip": CLIENT_IP}
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.text == f"{CLIENT_IP}\n"
