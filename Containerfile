FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    jq build-essential libxml2-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY generate.py /app/generate.py
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["entrypoint.sh"]
