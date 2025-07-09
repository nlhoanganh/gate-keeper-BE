from datetime import datetime
from app import db


class WorkDate(db.Model):
    __tablename__ = 'work_date'

    id = db.Column(db.Integer, primary_key=True)
    is_work_date = db.Column(db.Boolean, nullable=False)  # True = regular workday
    day_of_week = db.Column(db.String(10))  # 'Monday', 'Tuesday', etc.
    day = db.Column(db.Integer, nullable=False)  # 1-31
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)
    month_name = db.Column(db.String(10))  # 'January', etc.
    is_weekend = db.Column(db.Boolean)
    is_holiday = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)  # Optional notes

    # Relationship to work logs
    work_logs = db.relationship('WorkLog', backref='date_info', lazy=True)

    def __init__(self, date=None, **kwargs):
        if date:
            self._set_date_attributes(date)
        super().__init__(**kwargs)

    def _set_date_attributes(self, date):
        """Automatically populate date-related fields"""
        self.day = date.day
        self.month = date.month
        self.year = date.year
        self.day_of_week = date.strftime('%A')
        self.month_name = date.strftime('%B')
        self.is_weekend = date.weekday() >= 5  # 5=Sat, 6=Sun

    def __repr__(self):
        return f'<WorkDate {self.day}-{self.month}-{self.year} ({self.day_of_week})>'