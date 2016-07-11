FROM python:2.7.12

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -v -r requirements.txt

CMD ["nameko","run","watch_url"]
