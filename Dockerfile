FROM python:3.10
# RUN mkdir app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN apt-get -y update
#RUN apk update \
#		&& apk add --virtual build-essential gcc python3-dev musl-dev
RUN apt install build-essential gcc python3-dev musl-dev -y
RUN pip install psycopg2

RUN apt install iverilog -y
# RUN apk add iverilog

RUN pip install django 

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

#collect static files
RUN python manage.py collectstatic --noinput

# RUN adduser -D myuser
# USER myuser

# CMD python manage.py runserver 0.0.0.0:8000
CMD gunicorn myupweb.wsgi:application --bind 0.0.0.0:$PORT

