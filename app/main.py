from fastapi import Depends, FastAPI

description = """
Common API
"""

tags_metadata = [
    {
        "name": "emails",
        "description": "Email related services",
    },
    {
        "name": "root",
        "description": "Root of the API server; can be used to test whether its up",
    },
    {
        "name": "classification",
        "description": "Classification related operations / transformations",
    }
]

from fastapi.middleware.cors import CORSMiddleware

from .dependencies import get_header_token
from .routers import classifications, emails, feedbacks
from .internal.common import logger


from .internal.databases import engine
from .internal.models import Base
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.error(e)
logger.info('DB tables are recreated')

app = FastAPI(
    title="Common API for Eczemap",
    description=description,
    version="0.0.1",
    contact={
        "name": "Darshan Gadkari @Eczemap",
        "email": "darshangadkari0@gmail.com",
    },
    openapi_tags=tags_metadata,
    dependencies=[Depends(get_header_token)]
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(emails.router)
app.include_router(classifications.router)
app.include_router(feedbacks.router)


@app.on_event("startup")
def on_startup():
    pass


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to Common Service @ Eczemap"
        }

