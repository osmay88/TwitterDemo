FROM python:3.10

WORKDIR /app
COPY ./* /app/

RUN pip install pipenv

RUN pipenv install --system

#CMD ["uvicorn", "main.main:app", "--host", "0.0.0.0", "--port", "80"]