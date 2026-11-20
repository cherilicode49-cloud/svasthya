import os
import io
import json
import requests
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Value
from django.db.models.functions import Concat
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from svasthyapp import models
from svasthyapp.models import hoh_models, center_models
from svasthyapp.serializer import HohEmployeeSerializer, CenterDetailSerializer
from svasthyapp.apis.darwinbox_sync import get_darwinbox_access_token
import openpyxl as op
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

all_hoh_employee_list_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'page_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Page number', default=1),
        'row_size': openapi.Schema(type=openapi.TYPE_INTEGER, description='Row size per page', default=10),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Filter by status (Blank, Contacted, Person Not Approachable, Pending from Employee)'),
        'company': openapi.Schema(type=openapi.TYPE_STRING, description='Filter/Search by company name (e.g. "Roma" or "Rajshila")'),
        'created_date': openapi.Schema(type=openapi.TYPE_STRING, description='Filter by created date (YYYY-MM-DD)'),
        'search': openapi.Schema(type=openapi.TYPE_STRING, description='Search by candidate name, user ID, recruiter, company, or date'),
    }
)


def parse_hoh_employee_request_params(request):
    """Extract and sanitize query/body parameters from DRF request."""
    python_data = {}

    req_data = getattr(request, 'data', None)
    if req_data:
        if hasattr(req_data, 'dict'):
            python_data.update(req_data.dict())
        elif isinstance(req_data, dict):
            python_data.update(req_data)

    if not python_data and request.body:
        try:
            parsed = JSONParser().parse(io.BytesIO(request.body))
            if isinstance(parsed, dict):
                python_data.update(parsed)
        except Exception:
            pass

    if not python_data and request.method == 'POST':
        if hasattr(request.POST, 'dict'):
            python_data.update(request.POST.dict())
        else:
            for k, v in request.POST.items():
                python_data[k] = v

    query_source = getattr(request, 'query_params', None) or request.GET
    if query_source:
        if hasattr(query_source, 'dict'):
            for k, v in query_source.dict().items():
                if k not in python_data or python_data[k] in [None, '', 'null', 'undefined']:
                    python_data[k] = v
        else:
            for k, v in query_source.items():
                if k not in python_data or python_data[k] in [None, '', 'null', 'undefined']:
                    python_data[k] = v

    for k, v in list(python_data.items()):
        if isinstance(v, (list, tuple)) and len(v) == 1 and not isinstance(v[0], dict):
            python_data[k] = v[0]

    return python_data


def build_hoh_employee_queryset(python_data):
    """Build filtered HohEmployee queryset according to search and column filter criteria."""
    qs = models.HohEmployee.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name')
    )

    # 1. STATUS FILTER
    status_filter = python_data.get('status')
    if status_filter not in [None, '', 'null', 'undefined', 'All', 'all', 'ALL']:
        val_clean = str(status_filter).strip()
        if val_clean.lower() == 'blank':
            qs = qs.filter(
                models.Q(status='Blank') | 
                models.Q(status__isnull=True) | 
                models.Q(status='')
            )
        elif val_clean.lower() not in ['all', 'none']:
            qs = qs.filter(status__iexact=val_clean)

    # 2. COMPANY SEARCH / FILTER
    company_filter = (
        python_data.get('company') or 
        python_data.get('company_name') or 
        python_data.get('corporate_name') or 
        python_data.get('group_company') or
        python_data.get('corporate')
    )
    if company_filter not in [None, '', 'null', 'undefined', 'All', 'all', 'ALL']:
        if isinstance(company_filter, (list, tuple)):
            clean_companies = [
                str(c).strip() for c in company_filter 
                if str(c).strip() and str(c).strip().lower() not in ['all', 'null', 'undefined', '']
            ]
            if clean_companies:
                comp_q = models.Q()
                for c in clean_companies:
                    comp_q |= models.Q(company__icontains=c)
                qs = qs.filter(comp_q)
        elif str(company_filter).strip():
            c_val = str(company_filter).strip()
            if c_val.lower() not in ['all', 'null', 'undefined', '']:
                qs = qs.filter(company__icontains=c_val)

    # 3. GENERAL SEARCH FILTER
    search_filter = (
        python_data.get('search') or 
        python_data.get('search_value') or 
        python_data.get('search_text') or 
        python_data.get('search_filter') or
        python_data.get('query') or
        python_data.get('q') or
        python_data.get('keyword')
    )
    if search_filter not in [None, '', 'null', 'undefined']:
        search_val = str(search_filter).strip()
        if search_val:
            search_q = (
                models.Q(first_name__icontains=search_val) |
                models.Q(last_name__icontains=search_val) |
                models.Q(full_name__icontains=search_val) |
                models.Q(unique_user_id__icontains=search_val) |
                models.Q(employee_id__icontains=search_val) |
                models.Q(recruiter_name__icontains=search_val) |
                models.Q(recruiter_email__icontains=search_val) |
                models.Q(personal_email__icontains=search_val) |
                models.Q(personal_mobile__icontains=search_val) |
                models.Q(office_location__icontains=search_val) |
                models.Q(company__icontains=search_val) |
                models.Q(created_date__icontains=search_val) |
                models.Q(created_at__icontains=search_val)
            )

            words = search_val.split()
            if len(words) > 1:
                multi_word_q = models.Q()
                for w in words:
                    multi_word_q &= (
                        models.Q(first_name__icontains=w) |
                        models.Q(last_name__icontains=w) |
                        models.Q(full_name__icontains=w) |
                        models.Q(company__icontains=w) |
                        models.Q(unique_user_id__icontains=w) |
                        models.Q(recruiter_name__icontains=w)
                    )
                search_q |= multi_word_q

            qs = qs.filter(search_q)

    # 4. SPECIFIC COLUMN FILTERS
    candidate_name = (
        python_data.get('employee_name') or 
        python_data.get('candidate_name') or 
        python_data.get('name')
    )
    if candidate_name not in [None, '', 'null', 'undefined']:
        cn = str(candidate_name).strip()
        if cn:
            qs = qs.filter(
                models.Q(first_name__icontains=cn) | 
                models.Q(last_name__icontains=cn) |
                models.Q(full_name__icontains=cn)
            )

    user_id_filter = (
        python_data.get('unique_user_id') or 
        python_data.get('user_id') or 
        python_data.get('employee_id') or
        python_data.get('employee_code')
    )
    if user_id_filter not in [None, '', 'null', 'undefined']:
        uid = str(user_id_filter).strip()
        if uid:
            qs = qs.filter(
                models.Q(unique_user_id__icontains=uid) | 
                models.Q(employee_id__icontains=uid)
            )

    recruiter_filter = python_data.get('recruiter_name') or python_data.get('recruiter')
    if recruiter_filter not in [None, '', 'null', 'undefined']:
        rec = str(recruiter_filter).strip()
        if rec:
            qs = qs.filter(recruiter_name__icontains=rec)

    mobile_filter = python_data.get('personal_mobile') or python_data.get('mobile')
    if mobile_filter not in [None, '', 'null', 'undefined']:
        mob = str(mobile_filter).strip()
        if mob:
            qs = qs.filter(personal_mobile__icontains=mob)

    email_filter = python_data.get('personal_email') or python_data.get('email')
    if email_filter not in [None, '', 'null', 'undefined']:
        em = str(email_filter).strip()
        if em:
            qs = qs.filter(personal_email__icontains=em)

    location_filter = (
        python_data.get('office_location') or 
        python_data.get('location') or 
        python_data.get('city')
    )
    if location_filter not in [None, '', 'null', 'undefined']:
        loc = str(location_filter).strip()
        if loc:
            qs = qs.filter(office_location__icontains=loc)

    created_date_filter = (
        python_data.get('created_date') or 
        python_data.get('created_at') or 
        python_data.get('createdDate') or
        python_data.get('date')
    )
    if created_date_filter not in [None, '', 'null', 'undefined', 'All', 'all']:
        cdf = str(created_date_filter).strip()
        if cdf:
            qs = qs.filter(
                models.Q(created_date__icontains=cdf) | 
                models.Q(created_at__icontains=cdf)
            )

    return qs


@swagger_auto_schema(
    method='post',
    operation_description="Retrieve list of all HOH employees/candidates with pagination, company filter, status filter, and search.",
    request_body=all_hoh_employee_list_schema,
    responses={200: "List of HOH Employees"}
)
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve list of all HOH employees/candidates with pagination, company filter, status filter, and search.",
    manual_parameters=[
        openapi.Parameter('page_number', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER, default=1),
        openapi.Parameter('row_size', openapi.IN_QUERY, description="Row size per page", type=openapi.TYPE_INTEGER, default=10),
        openapi.Parameter('status', openapi.IN_QUERY, description="Filter by status", type=openapi.TYPE_STRING),
        openapi.Parameter('company', openapi.IN_QUERY, description="Filter/Search by company name", type=openapi.TYPE_STRING),
        openapi.Parameter('created_date', openapi.IN_QUERY, description="Filter by created date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        openapi.Parameter('search', openapi.IN_QUERY, description="Search term", type=openapi.TYPE_STRING),
    ],
    responses={200: "List of HOH Employees"}
)
@api_view(['GET', 'POST'])
@csrf_exempt
def all_hoh_employee_list(request):
    if request.method in ['POST', 'GET']:
        python_data = parse_hoh_employee_request_params(request)

        # Pagination parsing
        page_val = (
            python_data.get('page_number') or 
            python_data.get('page') or 
            python_data.get('pageIndex') or 
            1
        )
        size_val = (
            python_data.get('row_size') or 
            python_data.get('page_size') or 
            python_data.get('pageSize') or 
            python_data.get('limit') or 
            python_data.get('per_page') or 
            10
        )
        try:
            page_number = int(page_val)
        except (ValueError, TypeError):
            page_number = 1
        try:
            row_size = int(size_val)
        except (ValueError, TypeError):
            row_size = 10

        if page_number < 1:
            page_number = 1
        if row_size < 1:
            row_size = 10

        last_row = row_size * page_number
        first_row = last_row - row_size

        qs = build_hoh_employee_queryset(python_data)
        total_records = qs.count()
        hoh_employee = qs.order_by('-id')[first_row:last_row]
        serialiser = HohEmployeeSerializer(hoh_employee, many=True)
        
        print(f"[all_hoh_employee_list] Filters applied: {python_data}, Total records: {total_records}")

        res = {
            'statuscode': 200,
            'status': 'true',
            'data': serialiser.data,
            'total_records': total_records
        }
       
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='post',
    operation_description="Export HOH Employee records to an Excel (.xlsx) spreadsheet with filters.",
    request_body=all_hoh_employee_list_schema,
    responses={200: "Excel file download"}
)
@swagger_auto_schema(
    method='get',
    operation_description="Export HOH Employee records to an Excel (.xlsx) spreadsheet with filters.",
    manual_parameters=[
        openapi.Parameter('status', openapi.IN_QUERY, description="Filter by status", type=openapi.TYPE_STRING),
        openapi.Parameter('company', openapi.IN_QUERY, description="Filter/Search by company name", type=openapi.TYPE_STRING),
        openapi.Parameter('created_date', openapi.IN_QUERY, description="Filter by created date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        openapi.Parameter('search', openapi.IN_QUERY, description="Search term", type=openapi.TYPE_STRING),
    ],
    responses={200: "Excel file download"}
)
@api_view(['GET', 'POST'])
@csrf_exempt
def hoh_employee_export(request):
    """
    Exports HOH Employee records to an Excel (.xlsx) spreadsheet.
    Supports all search and filter parameters (POST body or GET query params).
    """
    python_data = parse_hoh_employee_request_params(request)
    qs = build_hoh_employee_queryset(python_data).order_by('-id')

    headers = [
        'ID',
        'Company',
        'Employee ID',
        'Unique User ID',
        'First Name',
        'Last Name',
        'Full Name',
        'Gender',
        'Date of Birth',
        'Date of Joining',
        'Personal Email',
        'Personal Mobile',
        'Office Location',
        'Member Address',
        'Recruiter Name',
        'Recruiter Mobile',
        'Recruiter Email',
        'Status',
        'Remark',
        'Created Date',
    ]

    wb = op.Workbook()
    ws = wb.active
    ws.title = "HOH Employees"
    ws.append(headers)

    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for emp in qs:
        full_name = f"{emp.first_name or ''} {emp.last_name or ''}".strip()
        dob_str = emp.date_of_birth.strftime('%Y-%m-%d') if emp.date_of_birth else ''
        doj_str = emp.date_of_joining.strftime('%Y-%m-%d') if emp.date_of_joining else ''

        c_date = emp.created_date or emp.created_at or ''
        if not c_date:
            try:
                appt = emp.darwinboxcandidateappointment_set.order_by('id').first()
                if appt and appt.created_at:
                    c_date = str(appt.created_at).split()[0]
            except Exception:
                pass

        row = [
            emp.id,
            emp.company or '',
            emp.employee_id or '',
            emp.unique_user_id or '',
            emp.first_name or '',
            emp.last_name or '',
            full_name,
            emp.gender or '',
            dob_str,
            doj_str,
            emp.personal_email or '',
            emp.personal_mobile or '',
            emp.office_location or '',
            emp.member_address or '',
            emp.recruiter_name or '',
            emp.recruiter_mobile or '',
            emp.recruiter_email or '',
            emp.status or 'Blank',
            emp.remark or '',
            c_date,
        ]
        ws.append(row)

    # Auto-adjust column widths
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 45)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="hoh_employee_list.xlsx"'
    wb.save(response)
    return response


@swagger_auto_schema(
    methods=['get', 'post'],
    operation_description="Retrieve list of all distinct company names from HOH employees for dropdown/autocomplete filter.",
    responses={200: "List of distinct company names"}
)
@api_view(['GET', 'POST'])
@csrf_exempt
def hoh_company_list(request):
    companies = list(
        models.HohEmployee.objects
        .exclude(company__isnull=True)
        .exclude(company='')
        .values_list('company', flat=True)
        .distinct()
        .order_by('company')
    )
    res = {
        'statuscode': 200,
        'status': 'true',
        'data': companies,
        'total_records': len(companies)
    }
    json_data = JSONRenderer().render(res)
    return HttpResponse(json_data, content_type='application/json')



@csrf_exempt
def vendor_center_list_hoh(request):
    if request.method in ['POST', 'GET']:
        python_data = {}
        if request.body:
            try:
                python_data = JSONParser().parse(io.BytesIO(request.body))
            except Exception:
                python_data = {}
        if not python_data:
            if request.method == 'POST':
                for k, v in request.POST.items():
                    python_data[k] = v
            else:
                for k, v in request.GET.items():
                    python_data[k] = v
        for k, v in request.GET.items():
            if k not in python_data:
                python_data[k] = v

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
            # python_data = {}
            # for i, j in request.POST.items():
            #     python_data.update({i: j})
            # if not python_data:
            #     try:
            #         python_data = JSONParser().parse(io.BytesIO(request.body))
            #     except Exception:
            #         pass
            python_data = JSONParser().parse(io.BytesIO(request.body))

            print(python_data, 'python_data of hoh employee')
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


