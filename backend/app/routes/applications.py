from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models.application import Application
from app.models.job import Job

applications_bp = Blueprint(
    "applications",
    __name__
)


@applications_bp.route("", methods=["POST"])
@jwt_required()
def apply_for_job():

    claims = get_jwt()

    if claims.get("role") != "candidate":
        return {
            "message": "Only candidates can apply for jobs"
        }, 403

    data = request.get_json()

    job_id = data.get("job_id")

    if not job_id:
        return {
            "message": "job_id is required"
        }, 400

    job = db.session.get(Job, job_id)

    if not job:
        return {
            "message": "Job not found"
        }, 404

    candidate_id = int(get_jwt_identity())

    existing = Application.query.filter_by(
        candidate_id=candidate_id,
        job_id=job_id
    ).first()

    if existing:
        return {
            "message": "You have already applied for this job"
        }, 409

    application = Application(
        candidate_id=candidate_id,
        job_id=job_id,
        resume=data.get("resume"),
        cover_letter=data.get("cover_letter")
    )

    db.session.add(application)
    db.session.commit()

    return {
        "message": "Application submitted successfully",
        "application": application.to_dict()
    }, 201


@applications_bp.route("", methods=["GET"])
@jwt_required()
def get_applications():

    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") == "candidate":

        applications = Application.query.filter_by(
            candidate_id=user_id
        ).all()

    else:

        recruiter_jobs = Job.query.filter_by(
            recruiter_id=user_id
        ).all()

        job_ids = [job.id for job in recruiter_jobs]

        applications = Application.query.filter(
            Application.job_id.in_(job_ids)
        ).all()

    return {
        "count": len(applications),
        "applications": [
            application.to_dict()
            for application in applications
        ]
    }, 200


@applications_bp.route(
    "/<int:application_id>/status",
    methods=["PUT"]
)
@jwt_required()
def update_application_status(application_id):

    claims = get_jwt()

    if claims.get("role") != "recruiter":
        return {
            "message": "Only recruiters can update application status"
        }, 403

    application = db.session.get(
        Application,
        application_id
    )

    if not application:
        return {
            "message": "Application not found"
        }, 404

    job = db.session.get(
        Job,
        application.job_id
    )

    if job.recruiter_id != int(get_jwt_identity()):
        return {
            "message": "You cannot update this application"
        }, 403

    data = request.get_json()

    status = data.get("status")

    allowed_statuses = [
        "Applied",
        "Shortlisted",
        "Rejected",
        "Selected"
    ]

    if status not in allowed_statuses:
        return {
            "message": "Invalid application status"
        }, 400

    application.status = status

    db.session.commit()

    return {
        "message": "Application status updated",
        "application": application.to_dict()
    }, 200