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

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]


###### Production stage ######
FROM python:3.12.2-slim-bookworm as prod

WORKDIR /app

COPY --from=dev /app/ /app

RUN apt-get update && apt-get install -y gcc libpq-dev

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
