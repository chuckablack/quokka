from quokka import db


class DeviceFacts(db.Model):

    __tablename__ = "device_facts"

    device_name = db.Column(db.Text, primary_key=True)
    fqdn = db.Column(db.Text)
    hostname = db.Column(db.Text)
    model = db.Column(db.Text)
    os_version = db.Column(db.Text)
    serial_number = db.Column(db.Text)
    vendor = db.Column(db.Text)
    uptime = db.Column(db.Integer)

    def __repr__(self):
        return f"Device: {self.hostname}"
