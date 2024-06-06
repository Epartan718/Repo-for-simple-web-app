FROM python:3.8-slim

RUN apt-get update && apt-get install -y python3-pip libpq-dev gcc

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
