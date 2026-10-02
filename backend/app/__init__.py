from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()


def create_app():

    app = Flask(__name__)

    # Secret key
    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "job-portal-secret-key"
    )

    # JWT secret key
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY",
        "job-portal-jwt-secret"
    )

    # MySQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Import models
    from app.models.user import User
    from app.models.job import Job
    from app.models.application import Application

    # Import routes
    from app.routes.auth import auth_bp
    from app.routes.jobs import jobs_bp
    from app.routes.applications import applications_bp

    # Register routes
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        jobs_bp,
        url_prefix="/api/jobs"
    )

    app.register_blueprint(
        applications_bp,
        url_prefix="/api/applications"
    )

    # Create tables if they don't already exist
    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():

        return {
            "message": "Job Portal API is running",
            "status": "success",
            "version": "1.0"
        }

    @app.route("/health")
    def health():

        return {
            "status": "healthy",
            "service": "job-portal-backend"
        }

    return app