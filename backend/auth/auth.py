"""Auth Module"""

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext


class AuthHandler():
    """AuthHandler class for handling authentication"""

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = "SUPER_SECRET_KEY"

    def get_password_hash(self, password):
        """Gets the hashed password"""
        return self.pwd_context.hash(password)

    def verify_password(self, password, hashed_password):
        """Verifies the password"""
        return self.pwd_context.verify(password, hashed_password)

    def encode_token(self, username, exp=timedelta(minutes=30)):
        """Encodes the token"""
        payload = {
                'username': username,
                'exp': datetime.now(timezone.utc) + exp,
                'iat': datetime.now(timezone.utc)
            }

        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_token(self, token):
        """Decodes the token"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['username']
        except jwt.ExpiredSignatureError as caught_exception:
            raise HTTPException(
                status_code=401,
                detail="Signature expired. Please log in again."
                ) from caught_exception

        except jwt.InvalidTokenError as caught_exception:
            raise HTTPException(
                status_code=401,
                detail="Invalid token. Please log in again."
                ) from caught_exception
    def auth_wrapper (self, auth: HTTPAuthorizationCredentials = Security(security)):
        """Wrapper for authentication"""
        return self.decode_token(auth.credentials)
