FROM python:latest

COPY . .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

WORKDIR /bot/
