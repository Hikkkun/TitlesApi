FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app.main:app"]