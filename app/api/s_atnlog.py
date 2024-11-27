
from apscheduler.schedulers.background import BackgroundScheduler
from flask import request, make_response

from flask_restx import Resource
from ipss_utils.ipss_db import query_to_dict
from sqlalchemy import text
from app import db_client, ipss_db, scheduler
from app.api.s_atns import primary_key
from app.models.attendancelog import AttendenceLog
from app.routes.demo_route import attendencelog
import datetime

def insert_data(datas):
    for data in datas:
        std_name = data.get('std_name')
        status = data.get('status')
        atn_date = data.get('atn_date')
        current_date = datetime.datetime.now()


        insert_query = text('''insert into attendance_log(student_name,status,date) 
                            values (:std_name,:status,:atn_date)''')

        db_client.engine.execute(insert_query,std_name=std_name,status=status,atn_date=atn_date)



@scheduler.task('cron', id='daily_task', hour=16, minute=48)
def daily_task():
    with scheduler.app.app_context():
        print('sheduler started-----------------')
        cur = datetime.datetime.today()
        print(cur)
        date = cur.date()
        print(date)
        # start = cur + "00:00:00"
        # end = cur + "23:59:59"

        task_query = text('''select student_info.std_name,attendance_tb.status,attendance_tb.atn_date from attendance_tb
                            join student_info on student_info.std_id = attendance_tb.std_id 
                            where (attendance_tb.status = 'half day' or attendance_tb.status = 'absent')
                            and DATE(attendance_tb.atn_date)= :date ''')

        datas = query_to_dict(db_client.engine.execute(task_query,date=date))
        print(datas)

        if datas:
            insert_data(datas)

# /@attendencelog.route('/')
# class AttendencelogAPI(Resource):
#     def get(self):




