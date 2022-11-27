FROM python:3.10

# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1
ENV DOCKER 1

RUN pip install poetry

# setting work directory
WORKDIR /home/app

COPY pyproject.toml poetry.lock ./

# install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY . .

# lint
RUN flake8 --ignore=E501,F401 .