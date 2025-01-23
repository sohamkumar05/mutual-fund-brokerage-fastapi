import bcrypt
from dotenv import load_dotenv
import jwt
import os
import requests

load_dotenv()


def generate_jwt_token(payload: dict):
    try:
        return jwt.encode(
            payload,
            os.getenv("JWT_SECRET"),
            algorithm="HS256"
        )
    except Exception as e:
        raise e


def decode_jwt_token(token: str):
    try:
        return jwt.decode(
            token,
            os.getenv("JWT_SECRET"),
            algorithms=["HS256"]
        )
    except Exception as e:
        raise e


def generate_hash(password: str):
    try:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    except Exception as e:
        raise e


def verify_hash(password: str, hash: str):
    try:
        return bcrypt.checkpw(password.encode(), hash.encode())
    except Exception as e:
        raise e


def call_api(querystring):

    url = f"https://{os.getenv('RAPID_API_HOST')}/latest"

    # querystring = {"Mutual_Fund_Family":"mmm","Scheme_Type":"Open","Scheme_Code":"12111,86888"}

    headers = {
        "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
        "x-rapidapi-host": os.getenv("RAPID_API_HOST")
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()
