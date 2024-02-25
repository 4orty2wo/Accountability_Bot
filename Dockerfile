FROM python:3.8-slim

ENV TZ='America/New_York'

WORKDIR /usr/src/bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Use build arguments to accept environment variables
ARG CONFIG_FILE
ARG BOT_TOKEN

# Environment variables to be used by your application
ENV BOT_TOKEN=${BOT_TOKEN}

COPY . .

# Remove the existing config.yml if it exists
RUN rm -f config.yml

# Replace the default config file with the one specified at build time
COPY ${CONFIG_FILE} config.yml

CMD ["python", "app.py"]

