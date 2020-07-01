from quokka import db


class Event(db.Model):

    __tablename__ = "event"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time = db.Column(db.Text)
    source_type = db.Column(db.Text)
    source = db.Column(db.Text)
    severity = db.Column(db.Text)
    info = db.Column(db.Text)

    def __repr__(self):
        return f"{self.severity} + {self.time} : {self.source} : {self.info}"
