FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "site79103.wsgi:application", "--bind", "0.0.0.0:8000"]
