from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models.job import Job

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.route("", methods=["GET"])
def get_jobs():

    search = request.args.get("search", "")
    location = request.args.get("location", "")

    query = Job.query

    if search:
        query = query.filter(
            Job.title.ilike(f"%{search}%")
        )

    if location:
        query = query.filter(
            Job.location.ilike(f"%{location}%")
        )

    jobs = query.order_by(
        Job.created_at.desc()
    ).all()

    return {
        "count": len(jobs),
        "jobs": [job.to_dict() for job in jobs]
    }, 200


@jobs_bp.route("/<int:job_id>", methods=["GET"])
def get_job(job_id):

    job = db.session.get(Job, job_id)

    if not job:
        return {
            "message": "Job not found"
        }, 404

    return job.to_dict(), 200


@jobs_bp.route("", methods=["POST"])
@jwt_required()
def create_job():

    claims = get_jwt()

    if claims.get("role") != "recruiter":
        return {
            "message": "Only recruiters can post jobs"
        }, 403

    data = request.get_json()

    required_fields = [
        "title",
        "company",
        "location",
        "description"
    ]

    for field in required_fields:
        if not data.get(field):
            return {
                "message": f"{field} is required"
            }, 400

    job = Job(
        title=data["title"],
        company=data["company"],
        location=data["location"],
        description=data["description"],
        skills=data.get("skills"),
        salary=data.get("salary"),
        job_type=data.get("job_type", "Full-time"),
        recruiter_id=int(get_jwt_identity())
    )

    db.session.add(job)
    db.session.commit()

    return {
        "message": "Job posted successfully",
        "job": job.to_dict()
    }, 201


@jobs_bp.route("/<int:job_id>", methods=["DELETE"])
@jwt_required()
def delete_job(job_id):

    job = db.session.get(Job, job_id)

    if not job:
        return {
            "message": "Job not found"
        }, 404

    if job.recruiter_id != int(get_jwt_identity()):
        return {
            "message": "You can delete only your own jobs"
        }, 403

    db.session.delete(job)
    db.session.commit()

    return {
        "message": "Job deleted successfully"
    }, 200