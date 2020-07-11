from quokka import db


class Service(db.Model):

    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text)
    target = db.Column(db.Text, nullable=False)
    data = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    availability = db.Column(db.Boolean)
    response_time = db.Column(db.Integer)
    sla_availability = db.Column(db.Integer)
    sla_response_time = db.Column(db.Integer)

    last_heard = db.Column(db.Text)

    def __repr__(self):
        return f"Service: {self.name}"
