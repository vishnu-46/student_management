from sqlalchemy import Column
from sqlalchemy_serializer import SerializerMixin

from app import db_client

class AttendenceLog(db_client.Model,SerializerMixin):
    __tablename__= 'attendance_log'
    log_id = Column(db_client.Integer,primary_key=True, autoincrement=True )
    std_name = Column(db_client.String)
    status = Column(db_client.String)
    atn_date = Column(db_client.DateTime)

    db_client.create_all()