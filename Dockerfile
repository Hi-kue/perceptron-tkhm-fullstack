FROM python@latest AS base

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]