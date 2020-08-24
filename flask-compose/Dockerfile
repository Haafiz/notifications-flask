FROM python:3.7
RUN apt-get update
COPY . /flask/app
ENV FLASK_APP app.py
ENV FLASK_ENV development
ENV FLASK_RUN_HOST 0.0.0.0
RUN apt-get install gcc
RUN apt-get install python-mysqldb
# RUN apt-get install 
COPY requirements.txt requirements.txt
WORKDIR /flask/app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]
