FROM python:3.10.8

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
COPY ./.env /code/.env

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
SHELL ["/bin/bash", "-c", "source /usr/local/bin/virtualenvwrapper.sh"]

# 
COPY ./app /code/app

# 
# CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]
CMD ["gunicorn" ,"app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]
