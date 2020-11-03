from quokka import db


class Worker(db.Model):

    __tablename__ = "worker"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    host = db.Column(db.Text, nullable=False)
    serial = db.Column(db.Text)

    worker_type = db.Column(db.Text)
    connection_type = db.Column(db.Text)

    availability = db.Column(db.Boolean)
    response_time = db.Column(db.Integer)
    sla_availability = db.Column(db.Integer, default=0)
    sla_response_time = db.Column(db.Integer, default=99999)

    last_heard = db.Column(db.Text)

    cpu = db.Column(db.Integer)
    memory = db.Column(db.Integer)
    uptime = db.Column(db.Integer)

    def __repr__(self):
        return f"Worker: {self.name}"
