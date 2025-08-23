from app.extensions import db


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    state = db.Column(db.String(1))

    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "release_date": self.release_date.isoformat(), "state": self.state}
