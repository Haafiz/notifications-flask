from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@mysql/notifications'
db = SQLAlchemy(app)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)
    notification_text = db.Column(db.String(120), nullable=False)
    medium_info = db.Column(db.String(255), nullable=False)
    queued_at = db.Column(db.Integer())
    acknowledged_at = db.Column(db.Integer())
    notification_type = db.Column(db.String(50))

    def __repr__(self):
        return '<User %r>' % self.username