FROM python:3.11-slim

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80"]
