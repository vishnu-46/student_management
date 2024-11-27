from logging import exception

from alembic.util import status
from flask import request, make_response
from flask_restx import Resource
from ipss_utils.ipss_api_doc import list_api_params
from ipss_utils.ipss_db import query_to_dict
from pyexpat.errors import messages
from select import select
from sqlalchemy import text
from app import db_client, ipss_db
from app.s_api_doc import studentname_fields, response_fields, leads_report_list_request
from app.models.attendance import Attendence
from app.models.student import Student
from app.routes.demo_route import attendence, a_post_model, studentinfo
import datetime

#Primary key
primary_key = 'atn_id'

def atten_status(mrng_atn,evng_atn):
    if(mrng_atn and evng_atn):
        return "full day"
    elif(mrng_atn or evng_atn):
        return "half day"
    else:
        return "absent"


def convert_dates(row):
    """
    Convert any date or datetime objects in the row to string format.
    """
    for key, value in row.items():
        if isinstance(value, (datetime.date, datetime.datetime)):
            row[key] = value.isoformat()  # Convert to ISO format string
    return row


@attendence.route('/')
class AttendenceApi(Resource):
  #  @attendence.marshal_with(list_response)
    @attendence.doc(params = leads_report_list_request)
    def get(self, CURRENT_TIMESTAMP=None):
       # data = request.json
        attendance_id = request.args.get("atn_id")
        attendance_sid = request.args.get("std_id")
        attendance_sdate = request.args.get("start_date")
        attendance_edate = request.args.get("end_date")
        attendance_status = request.args.get("atn_status")
        paged = int(request.args.get('paged')) if request.args.get('paged') else 1
        results_per_page = int(request.args.get('results_per_page')) if request.args.get(
        'results_per_page') else 2
        offset = (paged - 1) * results_per_page

        sql_condition = "0=0"
        # sql_condition1=""
        print(attendance_id)
        if attendance_id:
            sql_condition += f" AND attendance_tb.atn_id = {attendance_id}"
            #params['atn_id'] = attendence_id
        if attendance_sid:
            sql_condition += f" AND attendance_tb.std_id = {attendance_sid}"
        # # if attendance_edate:
        #     sql_condition += f" AND attendance_tb.atn_date = {attendance_edate}"

        if attendance_status:
            sql_condition+= f" AND attendance_tb.status = {attendance_status}"

        if attendance_sdate and attendance_edate:
            try:
                # start_date = datetime.datetime.strptime(attendance_sdate, "%Y-%m-%d").date()
                # end_date = datetime.datetime.strptime(attendance_edate, "%Y-%m-%d").date()
                sql_condition += f" and attendance_tb.atn_date BETWEEN '{attendance_sdate}' AND '{attendance_edate}'"
            except ValueError:
                return {"error":"Invalid date formate"}

        elif attendance_sdate:
            try:
                # start_date = datetime.datetime.strptime(attendance_sdate, "%Y-%m-%d").date()
                c_date = datetime.date.today()
                sql_condition += f" AND attendance_tb.atn_date BETWEEN '{attendance_sdate}' AND '{c_date}'"
            except ValueError:
                return {"error":"Invalid date formate"}

        if results_per_page:
            sql_condition+= f" limit {results_per_page}"

        if paged:
            sql_condition+= f" offset {offset}"

        sql_query = text(
            f'''select
        attendance_tb.*,student_info.std_name
        from attendance_tb
            join student_info
        on
        student_info.std_id = attendance_tb.std_id
        where {sql_condition}
        '''
        )
        print(sql_condition)

        # print(students)
        #result = db_client.engine.execute(sql_query, atn_id=attendence_id)
        with db_client.engine.connect() as connection:
            result =connection.execute(sql_query,)
            # result = db_client.engine.execute(students,).fetchall()
        print(result)
       # db_client.session.commit()

        result_dicts = [convert_dates(dict(row._mapping)) for row in result]

  # Return the result as a JSON response
        return {
            "primary_key":primary_key,
            "total_result":len(result_dicts),
            "page":paged,
            'result': result_dicts}


    @attendence.expect(a_post_model)
    def post(self):
        data = request.json
        std_id = data.get("std_id")
        mrng_atn = data.get("mrng_atn")
        evng_atn = data.get("evng_atn")
        data['atn_date']=datetime.datetime.now()
        #print( data['atn_date'])
        status = atten_status(mrng_atn, evng_atn)
        student = Attendence(atn_date=data['atn_date'], std_id= std_id, mrng_atn= mrng_atn, evng_atn= evng_atn, status= status)
        #print(student)
        try:

            db_client.session.add(student)
            db_client.session.commit()
            return make_response({'messages':'Sucess'})
        except Exception as e:
            db_client.session.rollback()
            return {"error":e}


@attendence.route('/<std_id>')
class AttendenceApi(Resource):
    @attendence.expect(a_post_model)
    def patch(self,std_id):
        data = request.json
        evng_atn = data.get("evng_atn")
        mrng_atn = text(f'''select mrng_atn from attendance_tb where std_id = {std_id} ''')
        mrng_atn = query_to_dict(db_client.engine.execute(mrng_atn))
        print(mrng_atn[0].get('mrng_atn'))
        status = atten_status(mrng_atn[0].get('mrng_atn'), evng_atn)
        data['status'] = status
        result = ipss_db.update_record(
            model=Attendence,
            condition=Attendence.std_id == std_id,
            values=data)
        # mrng_atn = text(f'''select mrng_atn from attendance_tb where std_id = {std_id} ''')
        # mrng_atn = query_to_dict(db_client.engine.execute(mrng_atn))
        # print(mrng_atn[0].get('mrng_atn'))
        # status = atten_status(mrng_atn[0].get('mrng_atn'), evng_atn)
        # print(status)
        return result

