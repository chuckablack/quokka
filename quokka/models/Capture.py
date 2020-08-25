from quokka import db


class Capture(db.Model):

    __tablename__ = "capture"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.Text)
    local_timestamp = db.Column(db.Text)
    source = db.Column(db.Text)

    ether_src = db.Column(db.Text)
    ether_dst = db.Column(db.Text)
    ip_src = db.Column(db.Text)
    ip_dst = db.Column(db.Text)
    protocol = db.Column(db.Text)
    sport = db.Column(db.Text)
    dport = db.Column(db.Text)

    packet_json = db.Column(db.Text)

    def __repr__(self):
        return f"Sniff host at {self.timestamp} for host {self.host_ip} packet: {self.packet}"
