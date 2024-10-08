FROM python:3.12
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
CMD [ "fastapi", "run", "api.py" ]