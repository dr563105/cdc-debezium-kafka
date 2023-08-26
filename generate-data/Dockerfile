FROM python:3.9.17-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "user_product_data.py" , "./" ]

CMD ["python" ,"user_product_data.py"]