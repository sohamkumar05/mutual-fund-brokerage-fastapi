from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from typing import Optional
from utils import decode_jwt_token


class TokenDecodeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip token decoding for /login or /register
        if request.url.path in ["/login", "/register", "/docs", "/redoc"]:
            response = await call_next(request)
            return response

        # Otherwise, ensure the token is present and valid
        authorization: Optional[str] = request.headers.get("Authorization")

        if authorization:
            try:
                # Assuming the token format is "Bearer <token>"
                token = authorization.split(" ")[1]
                # Decode the JWT token
                decoded = decode_jwt_token(token)
                # Add the decoded token data to request state
                request.state.user = decoded
            except jwt.ExpiredSignatureError:
                request.state.user = None
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content="Token has expired"
                )
            except jwt.InvalidTokenError:
                request.state.user = None
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content="Invalid token"
                )
        else:
            request.state.user = None
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content="Authorization token is missing"
            )

        # Proceed with the request and get the response
        response = await call_next(request)
        return response


def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"Error": "Bad Request"}
    )
