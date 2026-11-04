import os
import io
import json
import requests
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from svasthyapp import models
from svasthyapp.models import hoh_models, center_models
from svasthyapp.serializer import HohEmployeeSerializer, CenterDetailSerializer
from svasthyapp.apis.darwinbox_sync import get_darwinbox_access_token

def all_hoh_employee_list(request):
    if request.method in ['POST', 'GET']:
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
        except Exception:
            python_data = {}
        page_number = int(python_data.get('page_number', 1))
        row_size = int(python_data.get('row_size', 10))
        last_row = row_size * page_number
        first_row = last_row - row_size

        status_filter = python_data.get('status')
        if status_filter:
            if str(status_filter).strip().lower() == 'blank':
                qs = qs.filter(
                    models.Q(status='Blank') | 
                    models.Q(status__isnull=True) | 
                    models.Q(status='')
                )
            else:
                qs = qs.filter(status=status_filter)
        search_filter = python_data.get('search')
        if search_filter:
            qs = qs.filter(
                models.Q(first_name__icontains=search_filter) |
                models.Q(last_name__icontains=search_filter) |
                models.Q(unique_user_id__icontains=search_filter) |
                models.Q(recruiter_name__icontains=search_filter) |
                models.Q(company__icontains=search_filter)
            )

        total_records = qs.count()
        hoh_employee = qs.order_by('-id')[first_row:last_row]
        serialiser = HohEmployeeSerializer(hoh_employee, many=True)
        
        res = {
            'statuscode': 200,
            'status': 'true',
            'data': serialiser.data,
            'total_records': total_records
        }
       
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')



@csrf_exempt
def vendor_center_list_hoh(request):
    if request.method in ['POST', 'GET']:
        python_data = JSONParser().parse(io.BytesIO(request.body))
        vendor = python_data.get('vendor')
        
        center_list = models.CenterDetail.objects.filter(vendor = vendor)
        serialiser = CenterDetailSerializer(center_list, many=True).data
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser
            }
       
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


hoh_employee_id_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['id'],
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='HohEmployee primary key ID (or unique_user_id / employee_id)', example=1),
    }
)


@swagger_auto_schema(
    method='post',
    operation_description="Get detailed view of a single HOH Employee by ID (or unique_user_id / employee_id).",
    request_body=hoh_employee_id_schema,
    responses={200: "HOH Employee details"}
)
@swagger_auto_schema(
    method='get',
    operation_description="Get detailed view of a single HOH Employee by ID (or unique_user_id / employee_id).",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="HohEmployee ID (or unique_user_id / employee_id)", type=openapi.TYPE_STRING, required=True),
    ],
    responses={200: "HOH Employee details"}
)
@api_view(['GET', 'POST'])
@csrf_exempt
def get_hoh_employee_detail(request):
    if request.method in ['POST', 'GET']:
        emp_id = None
        if request.method == 'POST':
            try:
                python_data = JSONParser().parse(io.BytesIO(request.body))
            except Exception:
                python_data = {}
                for i, j in request.POST.items():
                    python_data.update({i: j})
            emp_id = python_data.get('id') or python_data.get('employee_id') or python_data.get('unique_user_id')
        else:
            emp_id = request.GET.get('id') or request.GET.get('employee_id') or request.GET.get('unique_user_id')

        if not emp_id:
            res = {'statuscode': 400, 'status': 'false', 'message': 'id is required'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        emp = None
        if str(emp_id).isdigit():
            emp = models.HohEmployee.objects.filter(id=int(emp_id)).first()

        if not emp:
            emp = models.HohEmployee.objects.filter(
                models.Q(unique_user_id=str(emp_id)) | models.Q(employee_id=str(emp_id))
            ).first()

        if not emp:
            res = {'statuscode': 404, 'status': 'false', 'message': 'HOH Employee not found'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        serializer = HohEmployeeSerializer(emp)
        res = {
            'statuscode': 200,
            'status': 'true',
            'data': serializer.data
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json') 


hoh_employee_status_update_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['hoh_employee'],
    properties={
        'hoh_employee': openapi.Schema(type=openapi.TYPE_INTEGER, description='Candidate ID / unique_user_id (HohEmployee ID, unique_user_id, or employee_id)', example=1),
        'status': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Candidate Status: "Blank", "Contacted", "Person Not Approachable", or "Pending from Employee". Pushed to Darwinbox Import API.',
            enum=['Blank', 'Contacted', 'Person Not Approachable', 'Pending from Employee'],
            example='Blank'
        ),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description='Internal comments / details (strictly internal, NOT pushed to Darwinbox)', example='Candidate contacted and requested appointment for tomorrow.'),
        'member_address': openapi.Schema(type=openapi.TYPE_STRING, description='Candidate address / home location', example='163/9, Mullai Nagar, West Tambram, Chennai 600045'),
        'recruiter_name': openapi.Schema(type=openapi.TYPE_STRING, description='Assigned Recruiter Name', example='Rushyandhan S'),
        'recruiter_mobile': openapi.Schema(type=openapi.TYPE_STRING, description='Recruiter Mobile Number', example='+919876543210'),
        'recruiter_email': openapi.Schema(type=openapi.TYPE_STRING, description='Recruiter Email ID', example='recruiter@company.com'),
        'personal_mobile': openapi.Schema(type=openapi.TYPE_STRING, description='Candidate Mobile Number', example='+917845153409'),
        'personal_email': openapi.Schema(type=openapi.TYPE_STRING, description='Candidate Personal Email', example='candidate@example.com'),
        'office_location': openapi.Schema(type=openapi.TYPE_STRING, description='Candidate Office Location', example='Chennai, Tamil Nadu'),
    }
)


def upload_hoh_employee_status_to_darwinbox(hoh_employee, status_value):
    """
    Submits candidate pre-employment status to Darwinbox Import API.
    Field: 'pre_employment_status'
    Allowed status values:
      - 'Blank'
      - 'Contacted'
      - 'Person Not Approachable'
      - 'Pending from Employee'
    """
    darwinbox_url = getattr(settings, 'DARWINBOX_IMPORT_URL', 'https://hoh.darwinbox.in/importapi/importdata')
    api_key = getattr(settings, 'DARWINBOX_IMPORT_API_KEY', getattr(settings, 'DARWINBOX_API_KEY', os.environ.get('DARWINBOX_IMPORT_API_KEY', os.environ.get('DARWINBOX_API_KEY', ''))))

    user_id = hoh_employee.unique_user_id or hoh_employee.employee_id or str(hoh_employee.id)
    group_company = hoh_employee.company or 'Roma Builders Private Limited'

    try:
        access_token = get_darwinbox_access_token(flag=False)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        if getattr(settings, 'DARWINBOX_COOKIE', None):
            headers['Cookie'] = settings.DARWINBOX_COOKIE

        payload = {
            "api_key": api_key,
            "import_id": "employeesdata",
            "group_company": group_company,
            "import_data": [
                {
                    "user_id": str(user_id).strip(),
                    "pre_employment_status": str(status_value).strip()
                }
            ],
        }

        response = requests.post(
            darwinbox_url,
            json=payload,
            headers=headers,
            timeout=30,
        )

        try:
            response_data = response.json()
        except ValueError:
            response_data = {'raw_response': response.text}

        print(f"Darwinbox Status Sync ({group_company}) Status:", response.status_code)
        print(f"Darwinbox Status Sync ({group_company}) Response:", response_data)

        is_success = response.status_code in [200, 201] and (
            isinstance(response_data, dict) and response_data.get('status') in [1, '1', True, 'true', 200]
        )

        return {
            'status': is_success,
            'status_code': response.status_code,
            'darwinbox_response': response_data,
            'message': 'Status successfully synced to Darwinbox' if is_success else (
                response_data.get('message') if isinstance(response_data, dict) else 'Darwinbox sync failed'
            )
        }
    except Exception as e:
        return {
            'status': False,
            'status_code': 500,
            'darwinbox_response': None,
            'message': f'Error syncing status to Darwinbox: {str(e)}'
        }


@swagger_auto_schema(
    method='post',
    operation_description="Update Pre-Employment status and internal remarks for an HOH Employee / Candidate. Pushes status ('pre_employment_status') to Darwinbox Import API. Remark is internal only.",
    request_body=hoh_employee_status_update_schema,
    responses={200: "Status updated successfully and synced to Darwinbox"}
)
@api_view(['POST'])
@csrf_exempt
def hoh_employee_status_update(request):
    """
    Updates HOH Employee status ('Contacted', 'Person Not Approachable', 'Pending from Employee')
    and internal remark. Pushes 'pre_employment_status' to Darwinbox Import API.
    Remark remains internal and is not pushed to Darwinbox.
    """
    if request.method == 'POST':
        try:
            python_data = {}
            for i, j in request.POST.items():
                python_data.update({i: j})
            if not python_data:
                try:
                    python_data = JSONParser().parse(io.BytesIO(request.body))
                except Exception:
                    pass

            employee_identifier = (
                python_data.get('hoh_employee') or 
                python_data.get('hoh_employee_id') or 
                python_data.get('id') or 
                python_data.get('unique_user_id')
            )
            status_input = python_data.get('status')
            remark_input = python_data.get('remark') or python_data.get('remarks')

            if not employee_identifier:
                res = {
                    'statuscode': 400,
                    'status': 'false',
                    'message': 'Candidate ID / unique_user_id (hoh_employee) is required.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            hoh_emp = None
            if str(employee_identifier).isdigit():
                hoh_emp = models.HohEmployee.objects.filter(id=int(employee_identifier)).first()
            if not hoh_emp:
                hoh_emp = models.HohEmployee.objects.filter(unique_user_id=str(employee_identifier)).first()
            if not hoh_emp:
                hoh_emp = models.HohEmployee.objects.filter(employee_id=str(employee_identifier)).first()

            if not hoh_emp:
                res = {
                    'statuscode': 404,
                    'status': 'false',
                    'message': f'HOH Employee not found with identifier: {employee_identifier}'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            valid_statuses = ['Blank', 'Contacted', 'Person Not Approachable', 'Pending from Employee']
            status_synced = None
            darwinbox_result = None

            if status_input is not None:
                status_cleaned = str(status_input).strip()
                if not status_cleaned or status_cleaned.lower() in ['', 'null', 'none', 'blank']:
                    matched_status = 'Blank'
                else:
                    matched_status = next((s for s in valid_statuses if s.lower() == status_cleaned.lower()), None)

                if not matched_status:
                    res = {
                        'statuscode': 400,
                        'status': 'false',
                        'message': f'Invalid status. Allowed values: {", ".join(valid_statuses)}'
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')

                hoh_emp.status = matched_status
                status_synced = matched_status

            if remark_input is not None:
                hoh_emp.remark = remark_input

            if 'member_address' in python_data:
                hoh_emp.member_address = python_data.get('member_address')
            elif 'address' in python_data:
                hoh_emp.member_address = python_data.get('address')

            if 'recruiter_name' in python_data:
                hoh_emp.recruiter_name = python_data.get('recruiter_name')

            if 'recruiter_mobile' in python_data:
                hoh_emp.recruiter_mobile = python_data.get('recruiter_mobile')

            if 'recruiter_email' in python_data:
                hoh_emp.recruiter_email = python_data.get('recruiter_email')

            if 'personal_mobile' in python_data:
                hoh_emp.personal_mobile = python_data.get('personal_mobile')
            elif 'mobile' in python_data:
                hoh_emp.personal_mobile = python_data.get('mobile')

            if 'personal_email' in python_data:
                hoh_emp.personal_email = python_data.get('personal_email')
            elif 'email' in python_data:
                hoh_emp.personal_email = python_data.get('email')

            if 'office_location' in python_data:
                hoh_emp.office_location = python_data.get('office_location')

            hoh_emp.save()

            if status_synced:
                darwinbox_result = upload_hoh_employee_status_to_darwinbox(hoh_emp, status_synced)

            serializer = HohEmployeeSerializer(hoh_emp)
            res = {
                'statuscode': 200,
                'status': 'true',
                'message': 'HOH Employee updated successfully.',
                'darwinbox_sync': darwinbox_result,
                'data': serializer.data
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        except Exception as e:
            res = {
                'statuscode': 500,
                'status': 'false',
                'message': f'Error updating HOH employee: {str(e)}'
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')


