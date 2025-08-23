from app.extensions import db


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255))
    update_by = db.Column(db.String(255))
    update_time = db.Column(db.DateTime)

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "key": self.key, "value": self.value, "update_by": self.update_by,
                "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S") if self.update_time else None}
