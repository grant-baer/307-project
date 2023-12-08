import os
from flask import Flask, jsonify, request
from mongoengine import (
    connect,
    Document,
    StringField,
    BinaryField,
    IntField,
    ListField,
    ReferenceField,
    NotUniqueError,
)
from werkzeug.security import check_password_hash
import secrets
from mongoengine.errors import DoesNotExist


from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
# db_lock = 0


@app.before_request
def db_connect(DB_URL=None):
    # MongoDB connection
    mongo_uri = DB_URL or os.environ.get("MONGO_URI")
    connect(alias="default", host=mongo_uri)
    return True


class Response:
    def __init__(self, message, status_code, data) -> None:
        self.status_code = status_code
        self.message = message
        self.data = data


class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True)
    encrypted_password = StringField(required=True)
    ranking = IntField()
    portfolio = ListField(ReferenceField("Image"))  # List of image references

    meta = {"collection": "users"}


class Image(Document):
    creator = ReferenceField(User, required=True)
    prompt = StringField(required=True)
    url = StringField(required=True)
    elo = IntField(required=True)

    meta = {"collection": "images"}


def create_user(data):
    data = data
    user = User(
        username=data["username"],
        encrypted_password=data["password"],
        email=data["email"],
        portfolio=[],  # Initialize an empty portfolio
    )
    try:
        user.save()
        return Response("User created successfully!", 201, {})
    except Exception as e:
        return Response(f"Internal server error {e}", 500, {})


def get_user(data):
    # only called in backend, assumes user exists
    user = User.objects.get(username=data["username"])
    return Response("User found.", 200, user)


def check_user(data):
    user = User.objects(username=data["username"]).first()
    if user:
        return Response("Username already exists. Choose another.", 401, {})
    user = User.objects(email=data["email"]).first()
    if user:
        return Response("Email already exists. Choose another.", 401, {})
    if user is None:
        return Response("User credentials are unique.", 200, {})


def create_image(data):
    try:
        # Create and save the image
        image = Image(
            creator=data["creator"],
            prompt=data["prompt"],
            url=data["url"],
            elo=1000,
        )
        image.save()

        creator = User.objects.get(pk=data["creator"])

        # Optionally, you can also append this image to the user's portfolio
        # here
        creator.update(push__portfolio=image)

        return Response("Image created successfully!", 201, {})
    except DoesNotExist:
        return Response("Creator user does not exist.", 404, {})
    except Exception as e:
        return Response(f"Internal server error: {e}", 500, {})


def get_random_image():
    try:
        image = Image.objects.aggregate([{"$sample": {"size": 1}}]).next()
        return Response("Image found.", 200, image)
    except Exception as e:
        return Response(f"Internal server error: {e}", 500, {})


def get_images(data):
    try:
        if "id" in data:
            images = Image.objects(id=data["id"]).first()
            return Response("Images found.", 200, images)
        else:
            images = list(Image.objects.order_by("-elo").limit(data["limit"]))
            print("got images")
            return Response("Images found.", 200, images)
    except Exception as e:
        return Response(f"Internal server error: {e}", 500, {})
