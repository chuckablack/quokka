from quokka import db


class Compliance(db.Model):

    vendor = db.Column(db.Text, primary_key=True)
    os = db.Column(db.Text, primary_key=True)

    standard_version = db.Column(db.Text)
    standard_config_file = db.Column(db.Text)

    def __repr__(self):
        return f"Compliance: {self.vendor}:{self.os}"
