# Notifications-flask

This is as per a set of requirements. It use flask (a  microframework for Python). It have one endpoint: POST `/notifications/<notification_type>` with following Request body params:
```user_id:12
notification_text:Testing notification
notification_type:sms
```

As per our docker settings, URL will be like: `http://0.0.0.0:5000/notification/sms`

## Setup

If you have docker installed, simply go to flask-compose directory and run:
``` 
> docker-compose build
> docker-compose up
```

Then inside docker contianer you will once need to run python shell and run 
```from models import db
db.create_all()
```
That will create DB.

other than that, this has an activemq consumer which work on queue and acknowledge in case notification service provider works (as there is a limit from notifiication provider).  So to run consumer, run:

`docker exec -i flask-compose_web_1 python consumer.py`
This console will keep running, and will log data in this console.
 
 Now go to `/notifications/<notification_type>` . It will log data in MySQL and will queue in ActiveMQ and its consumer will process it.

