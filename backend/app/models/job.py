from app import db
from datetime import datetime


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    company = db.Column(
        db.String(150),
        nullable=False
    )

    location = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    skills = db.Column(
        db.String(500),
        nullable=True
    )

    salary = db.Column(
        db.String(100),
        nullable=True
    )

    job_type = db.Column(
        db.String(50),
        nullable=False,
        default="Full-time"
    )

    recruiter_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "skills": self.skills,
            "salary": self.salary,
            "job_type": self.job_type,
            "recruiter_id": self.recruiter_id,
            "created_at": self.created_at.isoformat()
            if self.created_at else None
        }