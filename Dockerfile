FROM python:3.7

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 level:river_level
