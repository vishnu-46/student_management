from sqlalchemy import Column, String, BigInteger, UniqueConstraint, CheckConstraint,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.event import listen
from .. import db_client


class Student(db_client.Model,SerializerMixin):
    __tablename__='student_info'

    std_id = Column(db_client.Integer, primary_key=True, autoincrement=True)
    std_code = Column(db_client.String(50))
    std_name = Column(db_client.String(50))
    std_dept = Column(db_client.String(50))
    std_email = Column(db_client.String(50))
    std_phone = Column(db_client.String(10))
    std_blood = Column(db_client.String(5))


    def to_dict(self):
        return {
            'std_id': self.std_id,
            'std_code': self.std_code,
            'std_name': self.std_name,
            'std_dept': self.std_dept,
            'std_email': self.std_email,
            'std_phone':self.std_phone
        }
