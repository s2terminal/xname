FROM python:3.8-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    git \
    gcc \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# poetry install
RUN pip install poetry
RUN poetry config virtualenvs.in-project true

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install

CMD poetry run jupyter notebook --no-browser --ip=0.0.0.0 --port=8888 --allow-root --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.disable_check_xsrf=True
