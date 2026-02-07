"""Import all models so SQLAlchemy metadata discovers tables."""

from app.models.announcement import Announcement
from app.models.attendance import Attendance, AttendanceStatus
from app.models.class_ import LearningClass
from app.models.enrollment import Enrollment
from app.models.plan import QuarterlyPlan
from app.models.qna import QnAQuestion, QnAReply
from app.models.session import ClassSession
from app.models.user import User, UserRole

__all__ = [
    "Announcement",
    "Attendance",
    "AttendanceStatus",
    "ClassSession",
    "Enrollment",
    "LearningClass",
    "QnAQuestion",
    "QnAReply",
    "QuarterlyPlan",
    "User",
    "UserRole",
]
