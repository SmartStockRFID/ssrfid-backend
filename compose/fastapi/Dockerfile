# Imagem base com Python
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${PORT:-8000}

COPY ./compose/fastapi/start /start.sh
RUN chmod +x /start.sh

ENTRYPOINT [ "/start.sh" ]
