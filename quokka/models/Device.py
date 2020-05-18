from quokka import db


class Device(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    ip_address = db.Column(db.Text, unique=True, nullable=False)
    vendor = db.Column(db.Text)
    os = db.Column(db.Text)
    ssh_hostname = db.Column(db.Text)
    ssh_port = db.Column(db.Integer)
    ssh_username = db.Column(db.Text)
    ssh_password = db.Column(db.Text)

    def __repr__(self):
        return f"Device: {self.name}"
