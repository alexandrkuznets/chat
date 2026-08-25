FROM python:3.12-slim

WORKDIR /

RUN pip install poetry

COPY poetry.lock pyproject.toml .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

CMD ["uvicorn", "application.main:app", "--host", "0.0.0.0", "--port", "3535"]

