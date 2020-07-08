from quokka import db


class HostStatusSummary(db.Model):

    __tablename__ = "host_status_summary"

    host_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Text, primary_key=True)

    availability = db.Column(db.Integer)
    response_time = db.Column(db.Integer)

    def __repr__(self):
        return f"Status {self.host_id}"
