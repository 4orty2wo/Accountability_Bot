FROM python:3.8-slim

WORKDIR /usr/src/bot

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
