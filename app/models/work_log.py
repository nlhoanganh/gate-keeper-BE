from app import db
from datetime import datetime, timezone


class WorkLog(db.Model):
    __tablename__ = 'work_log'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.employee_id'), nullable=False)
    work_date_id = db.Column(db.Integer, db.ForeignKey('work_date.id'), nullable=False)

    # Check-in/out fields with geolocation
    check_in = db.Column(db.DateTime)
    check_in_lat = db.Column(db.Float)
    check_in_lng = db.Column(db.Float)
    check_in_location = db.Column(db.String(200))

    check_out = db.Column(db.DateTime)
    check_out_lat = db.Column(db.Float)
    check_out_lng = db.Column(db.Float)
    check_out_location = db.Column(db.String(200))

    # Session descriptions
    morning_description = db.Column(db.Text)
    afternoon_description = db.Column(db.Text)

    # Calculated fields
    work_duration = db.Column(db.Integer)  # in seconds
    status = db.Column(db.String(20))  # 'present', 'late', 'left_early', 'half_day'

    __table_args__ = (
        db.UniqueConstraint('user_id', 'work_date_id', name='unique_user_date'),
        db.Index('idx_worklog_user_date', 'user_id', 'work_date_id'),
    )

    def calculate_duration(self):
        if self.check_in and self.check_out:
            self.work_duration = (self.check_out - self.check_in).total_seconds()
            return self.work_duration
        return 0

    def update_status(self):
        if not self.check_in:
            self.status = 'absent'
        elif not self.check_out:
            self.status = 'present'
        else:
            duration_hours = self.work_duration / 3600
            if duration_hours < 4:
                self.status = 'half_day'
            elif duration_hours < 8:
                self.status = 'left_early'
            else:
                self.status = 'present'

    def __repr__(self):
        return f'<WorkLog {self.user_id} {self.work_date_id}>'