FROM python:3.13-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]
