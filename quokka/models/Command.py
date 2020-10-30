from quokka import db


class Command(db.Model):

    __tablename__ = "command"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    host = db.Column(db.Text)
    serial = db.Column(db.Text)

    worker_type = db.Column(db.Text)

    command = db.Column(db.Text)
    command_info = db.Column(db.Text)
    delivered = db.Column(db.Boolean)

    def __repr__(self):
        return f"Worker: {self.name}"
