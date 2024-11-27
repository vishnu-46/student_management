from dataclasses import field
from tokenize import String

from flask_restx import fields,reqparse
from sqlalchemy.sql.util import adapt_criterion_to_null

post_fields={
    #'std_id':fields.Integer(description = 'Student Id Number'),
    'std_name':fields.String(description = 'Student Name'),
    'std_dept':fields.String(description = 'Student Department'),
    'std_email':fields.String(description = 'Student email'),
    'std_phone':fields.String()
}

search_params ={
    'std_code':{
        'type': 'str',
        'description':"student code"
    },
    'paged': {
        'type': 'int',
        'description': "Pagination number"
    },
    'results_per_page': {
        'type': 'int',
        'description': "Results per page"
    }
}

response_fields = {
    'std_id':fields.Integer(),
    'std_name':fields.String(),
    'std_dept':fields.String(),
    'std email':fields.String()
}

attendencelog_fields = {
    'std_name':fields.String,
    'atn_date':fields.String,
    'status':fields.String
}

attendence_fields = {
    'atn_id':fields.Integer(),
    'atn_date':fields.String(),
    'std_id':fields.Integer(),
    'std_name':fields.String(),
    'mrng_atn':fields.Boolean(),
    'evng_atn':fields.Boolean(),
    'status':fields.String()
}
studentname_fields = {
    'std_name':fields.String(),
    'status':fields.String()
}

form_fields = {
    'File' : {
        'name':'upload_csv',
        'in':'formData',
        'description':'upload student data as csv file',
        'type':'file',
        'required':False

}
}

date_fields = {
    'std_id':fields.Integer(),
    'std_name':fields.String(),
    'mrng_atn':fields.Boolean(),
    'evng_atn':fields.Boolean(),
    'atn_date':fields.String(),
    'status':fields.String()
}

leads_report_list_request = {
'paged': {
        'type': 'int',
        'description': "Pagination number"
    },
    'results_per_page': {
        'type': 'int',
        'description': "Results per page"
    },
    'atn_id': {
        'type': 'int',
        'description': "attendence_ID"
    },
    'std_id': {
        'type': 'int',
        'description': "student_id"
    }
    ,
    'start_date': {
        'type': 'str',
        'description': "attendence start date"
    }
    ,
    'end_date': {
        'type': 'str',
        'description': "attendence end date"
    }
    ,
    'atn_status': {
        'type':'str',
        'description':"attendence status"
    }
}
list_response = {
    'total_results': fields.Integer,
    'page':  fields.Integer,
    'results_per_page':  fields.Integer,
}


