import random

import numpy as np
from flask import request
from flask_restx import Resource
import pandas as pd
from ipss_utils.ipss_db import query_to_dict
from sqlalchemy import column
from sqlalchemy.orm import sessionmaker

from  ..models.student import Student
from app import ipss_db, db_client
from app.routes.demo_route import csv_file, studentinfo, csv_response
from app.s_api_doc import form_fields, post_fields


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


@csv_file.route('/')
class Studentupload(Resource):
    @csv_file.expect(csv_response)
    def put(self):
        data = request.json
        data = data.get('data')
        for record in data:
            record['std_code'] = rand()
            # record['std_phone'] = valid_number(record['std_phone'])
            # print( record['std_phone'])
            # print(record['std_phone'])
        print(data)
        result = db_client.session.bulk_insert_mappings(Student,data)
        db_client.session.commit()
        #print("RESULT", result)
        return {'success':'insert record'}

    @csv_file.doc(params=form_fields )
    def post(self):
        file = request.files['File']
        bk_data =pd.read_csv(file)
        data1= bk_data.rename(
            columns = {
                       'Student code':'std_code',
                       'Student name':'std_name',
                       'Student department':'std_dept',
                       'Student E-Mail':'std_email',
                       'Student mobile number':'std_phone'
        },
        inplace = False)
        data2 = data1.replace(np.nan, '', regex=True)
        data2 = data2.to_dict()
        print(data2)
        length = len(data2.get('std_name',''))
        print(length)
        bulk_data = []
        for i in range(length):
            record = {
                      'std_code': data2['std_code'][i] if data2.get('std_code', {}).get(i, None) else None,
                      'std_name': data2['std_name'][i] if data2.get('std_name',{}).get(i,None) else None,
                      'std_dept': data2['std_dept'][i] if data2.get('std_dept',{}).get(i,None) else None,
                      'std_email': data2['std_email'][i] if data2.get('std_email',{}).get(i,None) else None,
                      'std_phone': str(data2['std_phone'][i]) if data2.get('std_phone',{}).get(i,None) else None
                #convert the above phone number into string

                      }
            bulk_data.append(record)
        print(bulk_data)
        return {'data': bulk_data}




