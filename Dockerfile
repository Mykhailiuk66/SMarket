FROM python:3.11.9

WORKDIR /smarket

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .