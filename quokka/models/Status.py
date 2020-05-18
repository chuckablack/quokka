from quokka import db


class Status(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)

    reachable = db.Column(db.Boolean)
    response_time = db.Column(db.Float)

    def __repr__(self):
        return f"Status {self.device_id}: reachable: {self.reachable} rsp-time: {self.response_time}"
