import os
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

import requests
from flask_cors import CORS, cross_origin

from mongoengine import connect, Document, StringField, BinaryField, DoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash
import secrets  # For generating a session key

from datetime import datetime

from db_access import User
from db_access import Image
from db_access import check_user, create_user, db_connect, create_image

import base64


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.config["JWT_SECRET_KEY"] = "CHANGE_TO_SECURE_KEY"
jwt = JWTManager(app)

DB_ACCESS_URL = (  # This is where db_access.py is running.
    "http://127.0.0.1:5001"
)


@app.route("/generate_image", methods=["POST"])
@jwt_required()
def generate_image():
    current_user = get_jwt_identity()  # Gets the identity of the current user
    data = request.get_json()
    url = "https://imagegolf.io/api/generate"
    url_data = {"inputValue": data["prompt"]}

    r = requests.post(url, json=url_data)

    return r.json()


# gets a random image from the database
@app.route("/get_random_image", methods=["GET"])
def get_random_image():
    try:
        # Randomly select an image
        image = Image.objects.aggregate([{"$sample": {"size": 1}}]).next()
        return jsonify(image), 200
    except StopIteration:
        # No images found in the database
        return jsonify({"error": "No images available"}), 404
    except Exception as e:
        # Handle other exceptions
        return jsonify({"error": str(e)}), 500


@app.route("/update_image_elo", methods=["POST"])
def update_image_elo():
    data = request.get_json()
    try:
        # Update Image One
        image_one = Image.objects.get(id=data["imageIdOne"])
        image_one.elo = data["newEloOne"]
        image_one.save()

        # Update Image Two
        image_two = Image.objects.get(id=data["imageIdTwo"])
        image_two.elo = data["newEloTwo"]
        image_two.save()

        return jsonify({"message": "ELO ratings updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/store_image", methods=["POST"])
@jwt_required()
def store_image():
    current_user = get_jwt_identity()  # Gets the identity of the current user
    # print(current_user)

    data = request.get_json()
    # Validate required fields
    required_fields = ["prompt", "url"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    image_res = requests.get(data["url"])

    # Prepare the data for creating an image
    image_data = {
        "creator": current_user,  # Assuming the creator is the logged-in user
        "prompt": data["prompt"],
        "data": image_res.content
    }

    # Call the create_image function from db_access
    response = create_image(image_data)

    # Handle the response
    if response.status_code == 201:
        print("Image created successfully!")
        return jsonify({"message": "Image submitted successfully!"}), 201
    else:
        print(f"Failed to create image: {response.message}")
        return jsonify({"message": response.message}), response.status_code


@app.route("/fetch_portfolio", methods=["GET"])
@jwt_required()
def fetch_portfolio():
    try:
        # Retrieve the user by username
        user = get_jwt_identity()

        # Fetch all images created by this user
        portfolio_images = User.objects.get(pk=user).portfolio

        # Format the response with the list of images
        portfolio = [{
            "image_id": str(image.id),
            "prompt": image.prompt,
            "creator": user,
            "data": base64.b64encode(image.data).decode("ascii")
        } for image in portfolio_images]

        return jsonify(portfolio), 200

    except DoesNotExist:
        # If the user is not found
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        # Handle any other exceptions
        return jsonify({"error": str(e)}), 500


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
            access_token = create_access_token(identity=str(user.pk))
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
            print("bad pwd")
            return (
                jsonify({"message": "Login failed, incorrect password"}),
                401,
            )
    except DoesNotExist:
        # Username does not exist
        return (
            jsonify({"message": "Login failed, invalid username"}),
            401,
        )
    except KeyError:
        # Username or password not provided
        if not data["username"] and data["password"]:
            return (
                jsonify(
                    {"message": "Login failed, missing username and password"}
                ),
                400,
            )
        elif not data["username"]:
            return (
                jsonify({"message": "Login failed, missing username"}),
                400,
            )
        else:
            return (
                jsonify({"message": "Login failed, missing password"}),
                400,
            )
    except Exception as e:
        # Catch any other errors
        print(f"Error during login: {str(e)}")
        return jsonify({"message": str(e)}), 500


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
    portfolio = [] #initialized to []

    # Hash the password
    hashed_password = generate_password_hash(
        plain_text_password, method="scrypt"
    )

    # Prepare the user data with the hashed password
    user_data = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "portfolio": portfolio,
    }
    response = check_user(user_data)
    if response.status_code == 401:
        print(f"responsey={response.message}")
        return (
            jsonify({"message": response.message}),
            400,
        )
    # Send the user data with the hashed password to the database access layer
    response = create_user(user_data)
    # Handle the response from the database access layer
    if response.status_code == 201:
        print("User created successfully!")
        return jsonify({"message": "User logged successfully!"})
    else:
        print("Failed to create user!")
        return jsonify({"message": "Failed to create user!!"}), 500


if __name__ == "__main__":
    db_connect()
    try:
        app.run(port=5000, debug=True)
    except OSError as e:
        print(f"Error: {e}. Is port 5000 already in use?")
