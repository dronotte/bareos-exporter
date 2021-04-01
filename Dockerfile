FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN apk add postgresql postgresql-dev gcc musl-dev
RUN pip install -r requirements.txt
EXPOSE 9118
CMD python ./exporter.py $CONFIG_PATH
