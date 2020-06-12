from quokka import db


class ServiceStatusTS(db.Model):

    service_id = db.Column(db.Text, primary_key=True)
    timestamp = db.Column(db.Text, primary_key=True)

    availability = db.Column(db.Boolean)
    response_time = db.Column(db.Integer)

    def __repr__(self):
        return f"Status {self.service_id}"
