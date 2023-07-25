FROM python:3.10-slim-bullseye 


WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 5000


CMD ["python", "flask", "run", "--host=0.0.0.0"]
