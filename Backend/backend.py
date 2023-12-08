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
from bson import json_util
from mongoengine.errors import DoesNotExist

from werkzeug.security import generate_password_hash, check_password_hash
import secrets  # For generating a session key
import json

from datetime import datetime

import db_access
from db_access import User, Image, get_random_image as random_image, get_images

import base64


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.config["JWT_SECRET_KEY"] = "CHANGE_TO_SECURE_KEY"
jwt = JWTManager(app)


@app.route("/generate_image", methods=["POST"])
@jwt_required()
def generate_image():
    current_user = get_jwt_identity()  # Gets the identity of the current user
    data = request.get_json()
    url = "https://imagegolf.io/api/generate"
    url_data = {"inputValue": data["prompt"]}

    r = requests.post(url, json=url_data)

    return r.json()


@app.route("/get_random_image", methods=["GET"])
def get_random_image():
    try:
        # Randomly select an image
        image = random_image().data
        if image:
            # Serialize the MongoDB document including ObjectId fields
            return json.loads(json_util.dumps(image)), 200
        else:
            return jsonify({"error": "No images available"}), 404
    except StopIteration:
        return jsonify({"error": "No images available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update_image_elo", methods=["POST"])
def update_image_elo():
    data = request.get_json()
    try:
        # Update Image One
        image_one = get_images({"id": data["imageIdOne"], "limit": 1}).data
        if not image_one:
            return jsonify({"error": "Image One not found"}), 404

        image_one.update(set__elo=data["newEloOne"])

        # Update Image Two
        image_two = get_images({"id": data["imageIdTwo"], "limit": 1}).data
        if not image_two:
            return jsonify({"error": "Image Two not found"}), 404

        image_two.update(set__elo=data["newEloTwo"])

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

    image_res = requests.post(
        "https://api.imgur.com/3/image",
        data={"image": data["url"]},
        headers={"Authorization": "Client-ID " +
                 os.environ["IMGUR_CLIENT_ID"]},
    )

    # Prepare the data for creating an image
    image_data = {
        "creator": current_user,  # Assuming the creator is the logged-in user
        "prompt": data["prompt"],
        "url": image_res.json()["data"]["link"],
    }

    # Call the create_image function from db_access
    response = db_access.create_image(image_data)

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
        portfolio = [
            {
                "image_id": str(image.id),
                "prompt": image.prompt,
                "creator": user,
                "url": image.url,
            }
            for image in portfolio_images
        ]

        return jsonify(portfolio), 200

    except DoesNotExist:
        # If the user is not found
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        # Handle any other exceptions
        return jsonify({"error": str(e)}), 500


@app.route("/top_elo_images", methods=["GET"])
def top_elo_images():
    try:
        # Fetch the top 20 images with the highest ELO, or fewer if less than
        # 20 images are available
        top_images = get_images({"limit": 100}).data

        # Serialize the MongoDB documents, including ObjectId fields, in the
        # list
        serialized_images = []
        for image in top_images:
            # Convert ObjectId to a string for JSON serialization
            creator_id = str(image.creator.id)

            try:
                # Fetch the user by ObjectId
                creator = User.objects.get(id=image.creator.id)
                creator_username = creator.username
            except DoesNotExist:
                creator_username = "Unknown User"

            image_data = {
                "id": str(image.id),
                "creator": creator_username,
                "prompt": image.prompt,
                "url": image.url,
                "elo": image.elo,
            }
            serialized_images.append(image_data)

        return jsonify(serialized_images), 200
    except Exception as e:
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
    print("IN REGISTER!!!")
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
    portfolio = []  # initialized to []

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
    response = db_access.check_user(user_data)
    if response.status_code == 401:
        print(f"responsey={response.message}")
        return (
            jsonify({"message": response.message}),
            400,
        )
    # Send the user data with the hashed password to the database access layer
    response = db_access.create_user(user_data)
    # Handle the response from the database access layer
    if response.status_code == 201:
        print("User created successfully!")
        return jsonify({"message": "User logged successfully!"})
    else:
        print("Failed to create user!")
        return jsonify({"message": "Failed to create user!!"}), 500


@app.route("/api/verify_user", methods=["GET"])
@jwt_required()
def verify_user():
    try:
        # Retrieve the user by username
        user = get_jwt_identity()
        temp = User.objects.get(pk=user).username
        return jsonify({"authenticated": True}), 200

    except DoesNotExist:
        # If the user is not found
        return jsonify({"error": "User not found"}), 404
    except jwt.ExpiredSignatureError:
        # Token has expired
        return jsonify({"authenticated": False}), 200
    except jwt.InvalidTokenError:
        # Invalid token
        return jsonify({"authenticated": False}), 200
    except Exception as e:
        # Handle any other exceptions
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting server...")
    db_access.db_connect()
    try:
        app.run(port=5000, debug=True)
    except OSError as e:
        print(f"Error: {e}. Is port 5000 already in use?")
