# app/models/__init__.py
from .user import User
from .work_date import WorkDate
from .work_log import WorkLog

# Now that both models are defined, set up the relationship
# User.work_logs = db.relationship('WorkLog', backref='user', lazy=True)

__all__ = ['User', 'WorkLog', 'WorkDate']