import hashlib
import base64
from flask import Flask, request, jsonify
from db_utils import (
    url_exists,
    insert_shortcode,
    get_url_shortcode,
    increment_clicks,
    get_stats,
)


app = Flask(__name__)


def generate_hashcode(url):
    # Generate a hash object using the SHA256 algorithm
    hash_object = hashlib.sha256(url.encode())

    # Get the first 8 bytes of the hash as a bytes object
    hash_bytes = hash_object.digest()[:8]

    # Encode the bytes as a base64 string
    hashcode = base64.urlsafe_b64encode(hash_bytes).decode("utf-8")[:6]
    return hashcode


@app.route("/")
def hello():
    return "hello!"


@app.route("/url/shorten", methods=["POST"])
def shorten_url():
    request_data = request.get_json()
    url = request_data.get("url")
    shortcode = request_data.get("shortcode")
    existing_code = url_exists(url)
    status_code = 201

    if not url:
        status_code = 400
        status = {"error": "URL not present"}

    else:
        existing_code = url_exists(url)
        if existing_code:
            status_code = 200
            status = {
                "message": "URL has an existing shortcode.",
                "shortcode": existing_code,
            }

        elif shortcode:
            if (
                shortcode is not None
                and len(shortcode) == 6
                and (all(c.isalnum() or c == "_" for c in shortcode))
            ):
                insert_shortcode(url, shortcode)
                status = {
                    "message": f"URL inserted with the user provided shortcode: {shortcode}",
                    "shortcode": shortcode,
                }
            else:
                status_code = 412
                status = {"error": "The provided shortcode is invalid"}
        else:
            shortcode = generate_hashcode(url)
            insert_shortcode(url, shortcode)
            status = {"message": "New shortcode created!", "shortcode": shortcode}
        print(status)

    return jsonify(status), status_code


@app.route("/url/get/<shortcode>")
def get_url(shortcode):
    url = get_url_shortcode(shortcode)
    status_code = 302

    if url:
        increment_clicks(shortcode)
        status = {"URL": url}
    else:
        status_code = 404
        status = {"message": "Shortcode not found"}
    return jsonify(status), status_code


@app.route("/url/<shortcode>/stats")
def get_shortcode_stats(shortcode):
    stats = get_stats(shortcode)
    status_code = 200
    if not stats:
        status_code = 404
        status = {"message": "Shortcode not found"}
        return jsonify(status), status_code

    return jsonify(stats), status_code


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
