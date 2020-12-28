from quokka import db


class Traceroute(db.Model):

    __tablename__ = "traceroute"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    target = db.Column(db.Text)
    source = db.Column(db.Text)
    timestamp = db.Column(db.Text)
    token = db.Column(db.Text)

    traceroute_img = db.Column(db.Text)

    def __repr__(self):
        return f"Status {self.host_id}"
