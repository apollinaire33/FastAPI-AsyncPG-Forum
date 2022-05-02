FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /code
COPY . /code

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

RUN chmod 755 ./run_app.sh

CMD ["bash", "./run_app.sh"]