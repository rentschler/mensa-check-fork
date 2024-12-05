FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY src/ .
CMD [ "fastapi", "run", "api.py" ]