FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /AutoBot

WORKDIR /AutoBot

COPY web/requirements.txt /AutoBot/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /AutoBot/

CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8000", "AutoBot.wsgi:application"]
