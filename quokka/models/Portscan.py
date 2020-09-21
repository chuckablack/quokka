from quokka import db


class Portscan(db.Model):

    __tablename__ = "portscan"

    host_ip = db.Column(db.Text, primary_key=True)
    host_name = db.Column(db.Text, primary_key=True)
    source = db.Column(db.Text, primary_key=True)
    timestamp = db.Column(db.Text, primary_key=True)
    token = db.Column(db.Text)

    # addresses = db.Column(db.Text)
    # hostnames = db.Column(db.Text)
    # osmatch = db.Column(db.Text)
    # portused = db.Column(db.Text)
    # status = db.Column(db.Text)
    # vendor = db.Column(db.Text)
    # tcp = db.Column(db.Text)
    # udp = db.Column(db.Text)
    # ip = db.Column(db.Text)

    scan_output = db.Column(db.Text)

    def __repr__(self):
        return f"Status {self.host_id}"
