# Common API

This API server provides common serivces for the Really network

# Implementation Details

This is a FastAPI implementation

# Installation Requirements

Python 3.10.8

# Installation steps

1. Clone this repo **git@github.com:gadkaridarshan/common.git**
2. Navigate to the base folder of this repo
3. Run `python -m venv venv`
4. Run `source venv/bin/activate`
5. Run `pip install -r requirements.txt`

## To run without docker

6. Run `gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80`
7. Open a web browser and visit `http://127.0.0.1/docs` to see the OpenAPI / Swagger docs for this API server

## To run with docker

6. Run `docker build .`
7. Run `docker image ls`. Find the docker image <image_id>
8. Run `docker run -p 80:80 <image_id>` if you want to tail the logs OR
   Run `docker run -d -p 80:80 <image_id>` if you want to run it as a daemon in the background (Remember you will need to run `docker stop <container_id>`)
9. Open a web browser and visit `http://127.0.0.1/docs` to see the OpenAPI / Swagger docs for this API server
