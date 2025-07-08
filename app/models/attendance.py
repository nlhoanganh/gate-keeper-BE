from datetime import datetime
from app import db

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.employee_id'), nullable=False)
    login_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime)
    session_duration = db.Column(db.Integer)  # in seconds

    # Geolocation Fields
    login_latitude = db.Column(db.Float)
    login_longitude = db.Column(db.Float)
    logout_latitude = db.Column(db.Float)
    logout_longitude = db.Column(db.Float)

    # Location Metadata
    login_location = db.Column(db.String(200))  # Human-readable address
    logout_location = db.Column(db.String(200))

    # Other Fields
    ip_address = db.Column(db.String(45))
    device_info = db.Column(db.String(200))

    def __repr__(self):
        return f'<Attendance {self.user_id} {self.login_time.date()}>'

    def calculate_duration(self):
        if self.logout_time:
            self.session_duration = (self.logout_time - self.login_time).total_seconds()
            return self.session_duration
        return 0

    def get_login_location(self):
        return {
            'coordinates': (self.login_latitude, self.login_longitude),
            'address': self.login_location,
            'timestamp': self.login_time.isoformat()
        }

    def get_logout_location(self):
        if not self.logout_time:
            return None
        return {
            'coordinates': (self.logout_latitude, self.logout_longitude),
            'address': self.logout_location,
            'timestamp': self.logout_time.isoformat()
        }