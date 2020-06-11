from quokka import db


class HostStatusTS(db.Model):

    host_id = db.Column(db.Text, primary_key=True)
    timestamp = db.Column(db.Text, primary_key=True)

    availability = db.Column(db.Boolean)
    response_time = db.Column(db.Integer)

    def __repr__(self):
        return f"Status {self.host_id}"
