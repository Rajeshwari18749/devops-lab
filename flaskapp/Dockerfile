FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --default-timeout=300 --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]