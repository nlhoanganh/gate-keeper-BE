from app import db
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = 'user'

    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)

    work_logs = db.relationship('WorkLog', backref='user', lazy=True)

    images = []

    def __repr__(self):
        return f'<User {self.employee_id} - {self.name}>'

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'email': self.email
        }