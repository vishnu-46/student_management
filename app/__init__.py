from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from ipss_utils.ipss_db import IpssDb
from flask_apscheduler import APScheduler

# from flask_apscheduler import scheduler

db_client = SQLAlchemy()
scheduler = APScheduler()
ipss_db = IpssDb()
Rest_Api = Api(
    title='Student API',
    description='API for managing student data',
    doc='/student_info',
    validate=True  # Enables request validation for the API
)


def create_app(config):
    # Initialize Flask app
    app = Flask(__name__)

    # Load app configuration
    app.config.from_object(config)

    # migrate = Migrate(app, db_client)

    # Initialize Flask-RestX and SQLAlchemy with the app
    Rest_Api.init_app(app)
    db_client.init_app(app)
    ipss_db.init_app(app, db_client)
    scheduler.init_app(app)

    with app.app_context():
        # Import and register API namespaces after app context is initialized
        from .api.s_atnlog import daily_task
        scheduler.start()
        from .api.s_demo import studentinfo
        from .api.s_atns import attendence
        from .api.s_atnlog import attendencelog
        from .api.s_csv import csv_file
        Rest_Api.add_namespace(studentinfo) # Add the studentinfo namespace to the API
        Rest_Api.add_namespace(attendence)
        Rest_Api.add_namespace(attendencelog)
        Rest_Api.add_namespace(csv_file)
    return app
