FROM python:3.8.18
RUN mkdir /app
WORKDIR /app

COPY requirements.txt .  

RUN pip install -r requirements.txt  

ADD ./web .  

EXPOSE 8080
CMD ["python", "app.py", "runserver"]

