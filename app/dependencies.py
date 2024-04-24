from fastapi import Header, HTTPException

from .internal.settings import API_TOKEN


async def get_header_token(token: str = Header(None, description="Token provided by the Eczemap team")):
    if token != API_TOKEN:
        raise HTTPException(status_code=400, detail="Token provided is not valid")

