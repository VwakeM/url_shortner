"""
Pytest suite for testing the url_shortner service.
"""

import pytest
from app import app


@pytest.fixture

def client():
    """
    Yields a test client.
    """
    with app.test_client() as client:
        yield client


def test_shorten_url_no_url(client):
    """
    Test for when URL is not present.
    """
    response = client.post("/url/shorten", json={"shortcode": "16zfh3"})
    assert response.status_code == 400
    assert response.json == {"error": "URL not present"}


def test_shorten_url(client):
    """
    Test for a new URL with a valid shortcode.
    """
    response = client.post(
        "/url/shorten", json={"url": "https://example10.com", "shortcode": "p2k9hd"}
    )
    assert response.status_code == 201
    assert response.json == {
        "message": "URL inserted with the user provided shortcode: p2k9hd",
        "shortcode": "p2k9hd",
    }


def test_shorten_url_exists(client):
    """
    Test for when URL already has a shortcode mapped.
    """
    response = client.post(
        "/url/shorten", json={"url": "https://example1.com", "shortcode": "p7k9fd"}
    )
    assert response.status_code == 400
    assert response.json == {
        "error": "URL already has a shortcode.",
        "shortcode": "p7k9fd",
    }


def test_shorten_code_exists(client):
    """
    Testing for a user provides an existing shortcode.
    """
    response = client.post(
        "/url/shorten", json={"url": "https://examplenew.com", "shortcode": "p7k9fd"}
    )
    assert response.status_code == 409
    assert response.json == {
        "message": "Shortcode already in use.",
        "shortcode": "p7k9fd",
    }


def test_shorten_url_new_shortcode(client):
    """
    Testing for a user provides a new URL with no shortcode.
    """
    response = client.post("/url/shorten", json={"url": "https://example3.com"})
    assert response.status_code == 201
    assert response.json["message"] == "New shortcode created!"


def test_shorten_url_invalid_shortcode(client):
    """
    Testing for a user provides a new URL with an invalid shortcode.
    """
    response = client.post(
        "/url/shorten", json={"url": "https://example20.com", "shortcode": "p2khd"}
    )
    assert response.status_code == 412
    assert response.json == {"error": "The provided shortcode is invalid"}


def test_get_url_shortcode_not_found(client):
    """
    Testing the get shortcode service with a non-existent shortcode.
    """
    response = client.get("/url/get/16zab3")

    assert response.status_code == 404
    assert response.json == {"message": "Shortcode not found"}


def test_get_url_shortcode_found(client):
    """
    Testing the get shortcode service for an existing shortcode.
    """
    response = client.get("/url/get/p7k9gp")

    assert response.status_code == 302
    assert response.json == {"URL": "https://example2.com"}


def test_get_shortcode_stats(client):
    """
    Testing the get shortcode sztats service for an existing shortcode.
    """
    response = client.get("/url/p7k9fd/stats")

    assert response.status_code == 200


def test_get_missing_shortcode_stats(client):
    """
    Testing the get shortcode sztats service for a nonexisting shortcode.
    """
    response = client.get("/url/d7k9fd/stats")

    assert response.status_code == 404
