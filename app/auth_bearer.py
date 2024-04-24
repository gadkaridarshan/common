from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .internal.common import logger

class JWTBearer(HTTPBearer):
    def __init__(self, token: str):
        self.token = token
        logger.info(self.token)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self) -> bool:
        logger.info(self.token)

        if self.token == "ICjgxQXFB9_UjD7UKP5-Qti4ymx1dfH5YyOdHIT04LZCycRPuXSZpLeVfWgYC4KjMaqA1nPLXwq3c6CVw07dXw":
            return True
        else:
            return False

