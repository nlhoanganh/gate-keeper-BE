from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    employee_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    # role relationship is created via backref in Role model

    def __repr__(self):
        return f'<User {self.employee_id} - {self.name}>'