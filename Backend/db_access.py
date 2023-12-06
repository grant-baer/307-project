import os
from flask import Flask, jsonify, request
from mongoengine import (
    connect,
    Document,
    StringField,
    IntField,
    ReferenceField,
    NotUniqueError,
)
from werkzeug.security import check_password_hash
import secrets
from mongoengine.errors import DoesNotExist

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def db_connect(DB_URL=None):
    # MongoDB connection
    mongo_uri = DB_URL or os.environ.get("MONGO_URI")
    connect(host=mongo_uri)
    return True


class Response:
    def __init__(self, message, status_code) -> None:
        self.status_code = status_code
        self.message = message


class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True)
    encrypted_password = StringField(required=True)
    ranking = IntField()

    meta = {"collection": "users"}


class Image(Document):
    creator = ReferenceField(User, required=True)
    url = StringField(required=True)
    prompt = StringField(required=True)
    votes = IntField(default=0)

    meta = {"collection": "images"}


def create_user(data):
    data = data
    user = User(
        username=data["username"],
        encrypted_password=data["password"],
        email=data["email"],
    )
    try:
        user.save()
        return Response("User created successfully!", 201)
    except Exception as e:
        return Response(f"Internal server error {e}", 500)


def check_user(data):
    user = User.objects(username=data["username"]).first()
    if user:
        return Response(
            "Username already exists. Choose another.",
            401,
        )
    user = User.objects(email=data["email"]).first()
    if user:
        return Response(
            "Email already exists. Choose another.",
            401,
        )
    if user is None:
        return Response(
            "User credentials are unique.",
            200,
        )
