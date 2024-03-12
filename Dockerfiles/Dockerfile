####### Development stage ######
FROM python:3.12.2-bookworm as dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry add debugpy

RUN poetry install --no-root

COPY ./djweather/ /app

COPY ./poetry.lock ./pyproject.toml /app/

EXPOSE 8000

#CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


###### Production stage ######
FROM python:3.12.2-slim-bookworm as prod

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY --from=dev /app/ /app

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY ./pyproject.toml ./poetry.lock /app/

#RUN ls -la /app && sleep 20

RUN poetry install --no-root

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "djweather.wsgi:application"]
#CMD ["poetry", "run", "gunicorn", "-w", "2", "--bind", "0.0.0.0:8000", "djweather.wsgi:application"]
#CMD ["poetry", "run", "gunicorn", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-", "--bind", "0.0.0.0:8000", "djweather.wsgi:application"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:$PORT"]
