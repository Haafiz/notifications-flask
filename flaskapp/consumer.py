import time, sys, stomp, json
from models import Notification, db
from pprint import pprint

subscriber_id = 1

class MyListener(stomp.ConnectionListener):

    def on_error(self, headers, message):
        print('received an error "%s"' % message)


    def on_message(self, headers, message):
        print('received an message "%s"' % message)
        if(use_notification_provider_service(message)):
            pprint(headers)

            message_id = headers['message-id']
            #acknowledge notificaiton to remove from queue
            conn.ack(message_id, subscriber_id)

            message_dict = json.loads(message)
            notification_id = message_dict['notification_id']
            notification = Notification.query.filter_by(id=notification_id).first()
            notification.acknowledged_at = time.time()
            db.session.commit()

        else:
            print('not acknowledging as notofication wasnt processed by provider')


def use_notification_provider_service(message):
    # we consider it returning true since we aren't implementing notificaiton's external provider service no matter what service type is,
    # in case it is not available as there is a limit from the provider as mentioned in requirements doc.
    # it may return false, but for now we will always be returning true.
    return True

def start_consumer():
    conn = stomp.Connection(host_and_ports = [('activemq',61613), ('activemq', 61616)])
    conn.set_listener('', MyListener())
    conn.connect('admin', 'password', wait=True)

    conn.subscribe(destination='notifications', id=subscriber_id, ack='client')
    return conn

conn = start_consumer()
while(True):
    time.sleep(10)
    conn.disconnect()
    conn = start_consumer()

