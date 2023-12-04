import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, \
    create_access_token, jwt_required, get_jwt_identity

import requests
from flask_cors import CORS, cross_origin

from mongoengine import connect, Document, StringField, DoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash
import secrets  # For generating a session key

from datetime import datetime

from db_access import User
from db_access import Image


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.config['JWT_SECRET_KEY'] = "CHANGE_TO_SECURE_KEY"
jwt = JWTManager(app)

DB_ACCESS_URL = (  # This is where db_access.py is running.
    "http://127.0.0.1:5001"
)


@app.route("/generate_image", methods=["POST"])
def generate_image():
    data = request.get_json()
    url = "https://imagegolf.io/api/generate"
    url_data = {"inputValue": data["prompt"]}

    r = requests.post(url, json=url_data)

    return r.json()


@app.route("/store_image", methods=["POST"])
def store_image():
    data = request.get_json()
    # Validate required fields
    required_fields = ["creator", "prompt", "url"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    # Retrieve creator user by user
    try:
        creator = User.objects.get(username=data["creator"])
    except DoesNotExist:
        return jsonify({"error": "Creator user does not exist."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    try:
        # votes default to 0 as defined in the Image class
        # timestamp can be added if we want to have more variation
        # between similar objects
        image = Image(creator=creator, prompt=data["prompt"], url=data["url"])
        image.save()
        return (
            jsonify(
                {
                    "message": "Image submitted successfully!",
                    "image_id": str(image.id),
                    # if you wish to return the timestamp when the image was stored
                    "timestamp": datetime.utcnow(),
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    data = request.get_json()
    text = data["text"]

    print(text)
    return jsonify({"message": "Text logged successfully!"})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    try:
        # Authenticate the user
        user = User.objects.get(username=data["username"])
        # Verify password (assuming passwords are hashed before storing)
        if check_password_hash(user.encrypted_password, data["password"]):
            # Generate session key/token
            # This is just a placeholder for an actual session key/token
            # session_key = secrets.token_hex(16)
            access_token = create_access_token(identity=str(user.username))
            # You would store this session key in a session store or database
            # with a reference to the user and a valid time period

            # Return success response with session key
            return (
                jsonify(
                    {
                        "message": "Logged in successfully!",
                        "access_token": access_token,
                    }
                ),
                200,
            )
        else:
            # Incorrect password
            return (
                jsonify(
                    {"message": "Login failed, incorrect username or password"}
                ),
                401,
            )
    except DoesNotExist:
        # Username does not exist
        return (
            jsonify(
                {"message": "Login failed, incorrect username or password"}
            ),
            401,
        )
    except KeyError:
        # Username or password not provided
        return (
            jsonify(
                {"message": "Login failed, must provide username and password"}
            ),
            400,
        )
    except Exception as e:
        # Catch any other errors
        print(f"Error during login: {str(e)}")
        return jsonify({"message": str(e)}), 500


@app.route("/create_user", methods=["POST"])
def create_user():
    print("received register request")
    print(request, request.data)
    return jsonify(
        {
            """message": "No endpoint called create_user,
            perhaps you meant: /register"""
        }
    )


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Validate required fields
    required_fields = ["username", "password", "email"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return (
            jsonify(
                {
                    "message": "Request missing required fields",
                    "missing_fields": missing_fields,
                }
            ),
            400,
        )

    username = data["username"]
    plain_text_password = data["password"]
    email = data["email"]

    # Hash the password
    hashed_password = generate_password_hash(
        plain_text_password, method="sha256"
    )

    # Prepare the user data with the hashed password
    user_data = {
        "username": username,
        "email": email,
        "password": hashed_password,
    }
    response = requests.get(f"{DB_ACCESS_URL}/users", json=user_data)
    if response.status_code == 401:
        print(f"responsey={response.text}")
        return (
            jsonify({"message": response.text}),
            400,
        )
    # Send the user data with the hashed password to the database access layer
    response = requests.post(f"{DB_ACCESS_URL}/create_user", json=user_data)
    # Handle the response from the database access layer
    if response.status_code == 201:
        print("User created successfully!")
        return jsonify({"message": "User logged successfully!"})
    else:
        print("Failed to create user!")
        return jsonify({"message": "Failed to create user!!"}), 500


if __name__ == "__main__":
    try:
        app.run(port=5000, debug=True)
    except OSError as e:
        print(f"Error: {e}. Is port 5000 already in use?")
