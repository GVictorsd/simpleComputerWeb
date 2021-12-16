FROM python:3
# RUN mkdir app
COPY . /
RUN apt-get -y update
RUN apt install iverilog -y
RUN pip install django 
RUN pip install python-dotenv
CMD python manage.py runserver 0.0.0.0:8000
