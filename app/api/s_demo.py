from os import abort
import random
from flask import request,jsonify
import re
import json
from flask_restx import Resource
from ipss_utils.ipss_db import query_to_dict
from pyexpat.errors import messages
from sqlalchemy import false,text

from ..s_api_doc import search_params
from ..models.student import Student
from app import db_client
from app.routes.demo_route import studentinfo,post_model

primary_key = 'std_id'


def valid_email(std_email):
    pattern = r'^[a-z]+[0-9]*@[a-z0-9-]+\.[a-z]{2,}$'
    # r'^[a-z]+[0-9]*@[a-z0-9-]+\.[a-z]{2,}$'

    #print("HI")
    try:
        if re.match(pattern, std_email):
            return {"success":True}

        return {"success":False,"message": "Invalid email"}

    except Exception as e:
            return {"error": str(e)}

def rand():
    prefix = 'std_'
    rand = str(random.randint(1111, 9999))
    return prefix + rand

def valid_number(std_phone):
    if len(std_phone) ==10:
        if std_phone.isdigit():
            number_query = ('''select std_phone from student_info''')
            number_query = query_to_dict(db_client.engine.execute(number_query))
            existing_numbers = [row['std_phone'] for row in number_query]
            if std_phone not in existing_numbers:
                return {"success":True}
            return {"messages":"Already Exist Phone Number"}
    return{"success":False,"message":"Invalid mobile number"}

def name_validation(std_name):
    upper_case = std_name.upper()

    print(type(upper_case))

    name_query = text('''select std_name from student_info where std_name =:upper_case''')
    name_query = query_to_dict(db_client.engine.execute(name_query,
                                                        upper_case=upper_case))
    print(name_query)
    if name_query:
        return {"success": False, "message": "Student name Already exist"}
    else:
        return {"success":True}

@studentinfo.route('/')
class StudentApi(Resource):
    #@studentinfo.marshal_with(post_model)
    @studentinfo.doc(params= search_params)
    def get(self):
        std_code = request.args.get("std_code")
        sql_condition = "0=0"
        paged = int(request.args.get('paged')) if request.args.get('paged') else 1
        results_per_page = int(request.args.get('results_per_page')) if request.args.get(
            'results_per_page') else 2



        offset = (paged - 1) * results_per_page
        if results_per_page:
            sql_condition+= f" limit {results_per_page}"

        if paged:
            sql_condition+= f" offset {offset}"
        count_query = ('''select count (std_id) from student_info''')
        count_query =query_to_dict(db_client.engine.execute(count_query))
        sql_query = (f'''select * from student_info where {sql_condition}''')

        sql_query = query_to_dict(db_client.engine.execute(sql_query,limit=results_per_page,
                                                   offset=offset))

      #  print(students_list)  # Debug print statement
        return{
            "primary_key": primary_key,
            "total_result": len(sql_query),
            "page": paged,
            'result':sql_query
        }

    @studentinfo.expect(post_model)
    def post(self):
        data = request.json
        std_name = data.get("std_name")
        std_dept = data.get("std_dept")
        std_phone = data.get("std_phone")
        std_email = data.get("std_email")
        result_name = name_validation(std_name)
        result = valid_email(std_email)
        result_phone = valid_number(std_phone)
        #name validation
        if not result_name.get('success'):
            return result_name
        #email validation
        if not result.get('success'):
            return result
        #phone number validation
        if not result_phone.get('success'):
            return result_phone

        std_code = rand()
        code_query =('''Select std_code from student_info''')
        code_query=query_to_dict(db_client.engine.execute(code_query))
        if std_code not in code_query:
            student = Student(std_name=std_name, std_dept=std_dept,std_email= std_email,std_code =std_code,std_phone = std_phone)
        else:
            std_code = rand()
        db_client.session.add(student)
        db_client.session.commit()

        return {"message":"Student added"}



    @studentinfo.route('/<int:id>')
    class StudentsApi(Resource):
        def get(self,id):
            student = db_client.session.query(Student).filter(Student.std_id==id).first()
            #students_list = [student.to_dict() for student in student]
            return student.to_dict()

        def delete(self,id):
            student = db_client.session.query(Student).filter(Student.std_id == id).first()
            db_client.session.delete(student)
            db_client.session.commit()
            return {"message":"Deleted Sucess"}

        @studentinfo.expect(post_model)
        def put(self,id):
            data = request.json
            student = db_client.session.query(Student).filter(Student.std_id == id).first()
            #Student.std_id = data['std_id']
            student.std_name = data['std_name']
            student.std_dept = data['std_dept']
            db_client.session.commit()
            return{"message":"table updated"}