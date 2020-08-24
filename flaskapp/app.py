from flask import Flask, request
import stomp, json, time
from models import Notification, db
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@mysql/notifications'
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return 'Hello World!'

def getUserDeviceInfo(user_id):
    #since it is dummy user so return dummy user object no matter what user_id is
    user_device = {'device_type':'android', 'device_id':'zsa12312', 'phone_number':'+921212121'}
    return user_device

@app.route('/notification/<notification_type>', methods=['POST', 'GET'])
def sendNotification(notification_type):
    notification_data = {}
    user_id = request.form.get("user_id")
    notification_data['notification_text'] = request.form.get("notification_text")
    notification_data['medium_info'] = getUserDeviceInfo(user_id)
    notification_data['queued_at'] = time.time()
    notification_data['user_id'] = user_id
    notification_data['notification_type'] = notification_type

    notification = Notification(
        notification_text = notification_data['notification_text'],
        medium_info = notification_data['medium_info'],
        queued_at = notification_data['queued_at'],
        user_id = user_id,
        notification_type = notification_type
    )
    db.session.add(notification)
    db.session.commit()

    notification_data['notification_id'] = notification.id
    sendNotificationToQueue(notification_data)

    return notification_data


def sendNotificationToQueue(notification_data):
    try:
        conn = stomp.Connection(host_and_ports = [('activemq',61613), ('activemq', 61616)])
        conn.connect('admin', 'password', wait=True)
        notification_data = json.dumps(notification_data)
        conn.send(body=notification_data, destination='notifications')
        conn.disconnect()
    except Exception as e:
        raise


