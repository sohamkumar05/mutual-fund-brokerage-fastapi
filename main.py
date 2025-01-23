from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from db import Connection, CURSOR_FACTORY
from middleware import TokenDecodeMiddleware, validation_exception_handler
from models import *
from utils import *
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(TokenDecodeMiddleware)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

conn = Connection().get_connection()
cur = conn.cursor(cursor_factory=CURSOR_FACTORY)


@app.post("/register")
def register(data: Register):
    try:
        password_hash = generate_hash(data.password)
        insert_data = {
            "name": data.name,
            "email": data.email,
            "password": password_hash,
            "timestamp": datetime.now()
        }

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (name, email, password, created_at, updated_at)
            VALUES (%(name)s, %(email)s, %(password)s, %(timestamp)s, %(timestamp)s)
            RETURNING id
        """, insert_data)
        conn.commit()
        user_data = cur.fetchone()

        token = generate_jwt_token(
            {"email": data.email, "id": user_data["id"]}
        )
        return JSONResponse(content={"token": token})
    except Exception as e:
        conn.rollback()
        print(e)
        return JSONResponse(
            content={"Error": "Internal Server Error"},
            status_code=500
        )


@app.post("/login")
def login(data: Login):
    try:
        fetch_data = {
            "email": data.email
        }
        cur.execute(
            """SELECT id, password FROM users where email = %(email)s""",
            fetch_data
        )
        user_data = cur.fetchone()
        if user_data is None:
            return JSONResponse(
                content={"Error": "User Not Found"},
                status_code=404
            )

        if not verify_hash(data.password, user_data["password"]):
            return JSONResponse(
                content={"Error": "Invalid password"},
                status_code=401
            )

        token = generate_jwt_token(
            {"email": data.email, "id": user_data["id"]}
        )
        return JSONResponse(content={"token": token})

    except Exception as e:
        print(e)
        return JSONResponse(
            content={"Error": "Internal Server Error"},
            status_code=500
        )


@app.get("/fund-families")
def get_fund_families():
    try:
        response = call_api({"Scheme_Type": "Open"})
        print(response)
        return {
            "fund_families": list(
                set(
                    [
                        scheme["Mutual_Fund_Family"] for scheme in response
                    ]
                )
            )
        }
    except Exception as e:
        print(e)
        return JSONResponse(
            content={"Error": "Internal Server Error"},
            status_code=500
        )

@app.get("/schemes")
def get_all_schemes(mutual_fund_family: str):
    try:
        response = call_api({"Scheme_Type": "Open", "Mutual_Fund_Family": mutual_fund_family})
        return {
            "schemes": response
        }
    except Exception as e:
        print(e)
        return JSONResponse(
            content={"Error": "Internal Server Error"},
            status_code=500
        )


@app.get("/portfolio")
def get_portfolio(req: Request):
    pass


@app.post("/portfolio")
def invest_in_scheme(req: Request, data: Portfolio):
    try:
        id = req.state.user["id"]
        scheme_code = data.scheme_code
        response = call_api({"Scheme_Type": "Open", "Scheme_Code": [scheme_code]})

        investment_data = {
            "user_id": id,
            "investment_value": response[0]["Net_Asset_Value"],
            "scheme_code": scheme_code,
            "timestamp": datetime.now()
        }
        cur.execute("""
        INSERT INTO portfolio (
                user_id, investment_value, scheme_code, is_delete,
                created_at, updated_at
            ) values (
                %(user_id)s, %(investment_value)s, %(scheme_code)s, true,
                %(timestamp)s, %(timestamp)s
            )
        """, investment_data)
        conn.commit()

        return {"message": "Scheme successfully added to portfolio."}
    except Exception as e:
        print(e)
        return JSONResponse(
            content={"Error": "Internal Server Error"},
            status_code=500
        )


@app.delete("/portfolio")
def withdraw_from_scheme(req: Request, data: Portfolio):
    try:
        id = req.state.user["id"]
        scheme_code = data.scheme_code

        investment_data = {
            "user_id": id,
            "scheme_code": scheme_code,
            "timestamp": datetime.now()
        }
        cur.execute("""
            UPDATE portfolio set is_delete = false, updated_at = %(timestamp)s
            where user_id = %(user_id)s and scheme_code = %(scheme_code)s
        """, investment_data)
        conn.commit()

        return {"message": "Scheme successfully removed from portfolio."}
    except Exception as e:
        print(e)
        return JSONResponse(
            content={"Error": "Internal Server Error"},
            status_code=500
        )
