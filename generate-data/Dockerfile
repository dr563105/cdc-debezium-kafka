FROM python:3.9.17-slim

RUN pip install -U pip
RUN pip install pipenv

ENV POSTGRES_USER = ${POSTGRES_USER}
ENV POSTGRES_PASSWORD = ${POSTGRES_PASSWORD}
ENV POSTGRES_DB = ${POSTGRES_DB}
ENV POSTGRES_HOST = ${POSTGRES_HOST}

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "user_product_data.py" , "./" ]

CMD ["python" ,"./user_product_data.py"]