from quokka import db


class WorkerStatus(db.Model):

    __tablename__ = "worker_status"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    worker_id = db.Column(db.Integer)

    timestamp = db.Column(db.Text)
    availability = db.Column(db.Boolean)
    response_time = db.Column(db.Integer)
    cpu = db.Column(db.Integer)
    memory = db.Column(db.Integer)

    def __repr__(self):
        return f"Status {self.worker_id}"
