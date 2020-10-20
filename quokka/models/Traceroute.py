from quokka import db


class Traceroute(db.Model):

    __tablename__ = "traceroute"

    target = db.Column(db.Text, primary_key=True)
    source = db.Column(db.Text, primary_key=True)
    timestamp = db.Column(db.Text, primary_key=True)
    token = db.Column(db.Text)

    traceroute_img = db.Column(db.Text)

    def __repr__(self):
        return f"Status {self.host_id}"
