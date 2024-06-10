FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app.main:app"]

