FROM python:3.8-slim

WORKDIR /usr/src/bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Use build arguments to accept environment variables
ARG CONFIG_FILE
ARG BOT_TOKEN

# Environment variables to be used by your application
ENV BOT_TOKEN=${DB_USERNAME}

COPY . .

# Replace the default config file with the one specified at build time
COPY ${CONFIG_FILE} config.yml

CMD ["python", "app.py"]

