from app.extensions import db


class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    person = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    state = db.Column(db.String(1))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    def to_dict(self) -> dict:
        return {"id": self.id, "user_id": self.user_id, "name": self.name, "person": self.person, "phone": self.phone,
                "state": self.state, "start_date": self.start_date.isoformat(), "end_date": self.end_date.isoformat()}
