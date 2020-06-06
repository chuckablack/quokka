from quokka import db


class Service(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text)
    target = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    def __repr__(self):
        return f"Service: {self.name}"
