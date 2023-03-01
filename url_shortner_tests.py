import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_hello(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"hello!"


def test_shorten_url_no_url(client):
    response = client.post("/url/shorten", json={"shortcode": "16zfh3"})
    assert response.status_code == 400
    assert response.json == {"error": "URL not present"}


def test_shorten_url(client):
    response = client.post(
        "/url/shorten", json={"url": "https://example10.com", "shortcode": "p2k9hd"}
    )
    assert response.status_code == 201
    assert response.json == {
        "message": "URL inserted with the user provided shortcode: p2k9hd",
        "shortcode": "p2k9hd",
    }


def test_shorten_url_exists(client):
    response = client.post(
        "/url/shorten", json={"url": "https://example1.com", "shortcode": "p7k9fd"}
    )
    assert response.status_code == 200
    assert response.json == {
        "message": "URL has an existing shortcode.",
        "shortcode": "p7k9fd",
    }


def test_shorten_url_new_shortcode(client):
    response = client.post("/url/shorten", json={"url": "https://example3.com"})
    assert response.status_code == 201
    assert response.json["message"] == "New shortcode created!"


def test_shorten_url_invalid_shortcode(client):
    response = client.post(
        "/url/shorten", json={"url": "https://example20.com", "shortcode": "p2khd"}
    )
    assert response.status_code == 412
    assert response.json == {"error": "The provided shortcode is invalid"}


def test_get_url_shortcode_not_found(client):
    response = client.get("/url/get/16zab3")

    assert response.status_code == 404
    assert response.json == {"message": "Shortcode not found"}


def test_get_url_shortcode_found(client):
    response = client.get("/url/get/p7k9gp")

    assert response.status_code == 302
    assert response.json == {"URL": "https://example2.com"}


def test_get_shortcode_stats(client):
    response = client.get("/url/p7k9fd/stats")

    assert response.status_code == 200


def test_get_missing_shortcode_stats(client):
    response = client.get("/url/d7k9fd/stats")

    assert response.status_code == 404
