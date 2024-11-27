
from flask_restx import Namespace, fields
from ..s_api_doc import post_fields,attendence_fields,attendencelog_fields
from ..models.attendancelog import AttendenceLog

studentinfo=Namespace('studentinfo', path='/student_info', description='Student API controller')
attendence = Namespace('Attendence', path='/attendence',description='Studetn Attendence' )
attendencelog = Namespace('AttendenceLog', path='/attendencelog', description='Student Attendence Log' )

csv_file = Namespace('uploadData', path='/upload_csv', description='Student data')


post_model = studentinfo.model('studentPost', post_fields)
a_post_model = attendence.model('attendencePost', attendence_fields)
log_post = attendencelog.model('attendencelogPost', attendencelog_fields)
csv_response =csv_file.model('csv',{**{'data':fields.List(fields.Nested(post_model))}})

# list_response = attendence.model('listresponce', {'result':fields.List(fields.Nested(a_post_model))})
# #a_post_model1= attendence.model('Post', studentname_fields)
# date_response = attendence.model('responceModel',date_fields)




