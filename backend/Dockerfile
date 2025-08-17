FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
COPY app /app/app
RUN pip install poetry && poetry install --no-root --no-interaction --no-ansi
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]