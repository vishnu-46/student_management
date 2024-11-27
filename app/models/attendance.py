from sqlalchemy import Column
from sqlalchemy_serializer import SerializerMixin

from app import db_client


class Attendence(db_client.Model,SerializerMixin):
    __tablename__= 'attendance_tb'
    atn_id = Column(db_client.Integer,primary_key=True, autoincrement=True )
    std_id = Column(db_client.Integer)
    mrng_atn = Column(db_client.Boolean)
    evng_atn = Column(db_client.Boolean)
    status = Column(db_client.String)
    atn_date = Column(db_client.DateTime)

    def to_dict(self):
        return {
            'atn_id':self.atn_id,
            'std_id':self.std_id,
            'mrng_atn':self.mrng_atn,
            'evng_atn':self.evng_atn,
            'status':self.status,
            'atn_date':self.atn_date
        }
