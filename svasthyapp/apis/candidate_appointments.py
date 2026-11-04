import os
import io
import json
import zipfile
import requests
from datetime import datetime, date, timedelta
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from svasthyapp import models
from svasthyapp.models import hoh_models, center_models, vendor_models
from svasthyapp.serializer import (
    DarwinboxCandidateAppointmentSerializer,
    RescheduleDarwinboxCandidateAppointmentSerializer,
)
from svasthyapp.apis.darwinbox_sync import (
    get_darwinbox_access_token,
    upload_darwinbox_candidate_report_to_api,
)

# ============================================================
# SWAGGER SCHEMAS FOR DARWINBOX & APPOINTMENT APIS
# ============================================================

candidate_appointment_create_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['hoh_employee', 'package'],
    properties={
        'hoh_employee': openapi.Schema(type=openapi.TYPE_INTEGER, description='Candidate ID (HohEmployee ID)', example=1),
        'package': openapi.Schema(type=openapi.TYPE_INTEGER, description='Package ID (PackageDetail ID)', example=2),
        'center': openapi.Schema(type=openapi.TYPE_INTEGER, description='Diagnostic Center ID (CenterDetail ID)', example=1),
        'vendor': openapi.Schema(type=openapi.TYPE_INTEGER, description='Vendor ID (optional, auto-derived from package)', example=1),
        'type_of_visit': openapi.Schema(type=openapi.TYPE_STRING, description='Type of Visit: "At Home", "At Center", "Hybrid" (or TypeOfVisit ID)', example='At Center'),
        'appointment_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 1 (YYYY-MM-DD) - Mandatory for At Center & Hybrid', example='2026-10-15'),
        'appointment_time_slot_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup time slot 1 (e.g. 11:00 AM to 01:00 PM, 2:00 PM to 4:00 PM)', example='11:00 AM to 01:00 PM'),
        'appointment_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Optional Preferred checkup date 2 (YYYY-MM-DD)', example='2026-10-16'),
        'appointment_time_slot_2': openapi.Schema(type=openapi.TYPE_STRING, description='Optional Preferred checkup time slot 2', example='02:00 PM to 04:00 PM'),
        'home_sample_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 1 (YYYY-MM-DD) - Mandatory for At Home & Hybrid', example='2026-10-14'),
        'home_sample_time_slot_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample time slot 1', example='08:00 AM to 10:00 AM'),
        'home_sample_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Optional Preferred home sample date 2 (YYYY-MM-DD)', example='2026-10-15'),
        'home_sample_time_slot_2': openapi.Schema(type=openapi.TYPE_STRING, description='Optional Preferred home sample time slot 2', example='10:00 AM to 12:00 PM'),
        'time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='General appointment time slot', example='11:00 AM to 01:00 PM'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status (default: Pending)', example='Pending'),
        'reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason / Note', example='Annual Pre-Employment checkup'),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description='Additional remark', example='Fasting required'),
    }
)

candidate_appointment_update_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['id'],
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='DarwinboxCandidateAppointment ID', example=1),
        'hoh_employee': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Candidate ID', example=1),
        'package': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Package ID', example=2),
        'center': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Center ID', example=1),
        'vendor': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Vendor ID', example=1),
        'type_of_visit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Type of Visit ID', example=1),
        'appointment_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 1', example='2026-10-15'),
        'appointment_time_slot_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup time slot 1', example='11:00 AM to 01:00 PM'),
        'appointment_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 2', example='2026-10-16'),
        'appointment_time_slot_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup time slot 2', example='02:00 PM to 04:00 PM'),
        'home_sample_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 1', example='2026-10-14'),
        'home_sample_time_slot_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample time slot 1', example='08:00 AM to 10:00 AM'),
        'home_sample_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 2', example='2026-10-15'),
        'home_sample_time_slot_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample time slot 2', example='10:00 AM to 12:00 PM'),
        'confirm_appointment_date': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmed checkup date', example='2026-10-15'),
        'confirm_appointment_time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmed checkup time slot', example='11:00 AM to 01:00 PM'),
        'confirm_home_sample_date': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmed home sample date', example='2026-10-14'),
        'confirm_home_sample_time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmed home sample time slot', example='08:00 AM to 10:00 AM'),
        'date_of_appointment': openapi.Schema(type=openapi.TYPE_STRING, description='Date of appointment', example='2026-10-15'),
        'time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='Appointment time slot', example='11:00 AM to 01:00 PM'),
        'reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason', example='Updated schedule'),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description='Remark', example='Morning slot'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status', example='Confirmed'),
        'report_date': openapi.Schema(type=openapi.TYPE_STRING, description='Report date', example='2026-10-17'),
    }
)

candidate_appointment_reschedule_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['appointment', 'status'],
    properties={
        'appointment': openapi.Schema(type=openapi.TYPE_INTEGER, description='DarwinboxCandidateAppointment ID (or id)', example=1),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status: "Confirmed" or "Rescheduled"', example='Rescheduled'),
        'confirm_appointment_date': openapi.Schema(type=openapi.TYPE_STRING, description='New appointment date (YYYY-MM-DD)', example='2026-10-20'),
        'confirm_appointment_time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='New appointment time slot', example='11:00 AM to 01:00 PM'),
        'confirm_home_sample_date': openapi.Schema(type=openapi.TYPE_STRING, description='New home sample date (YYYY-MM-DD)', example='2026-10-19'),
        'confirm_home_sample_time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='New home sample time slot', example='08:00 AM to 10:00 AM'),
        'new_appointment_date': openapi.Schema(type=openapi.TYPE_STRING, description='New appointment date (YYYY-MM-DD)', example='2026-10-20'),
        'new_appointment_time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='New appointment time slot', example='11:00 AM to 01:00 PM'),
        'new_home_sample_date': openapi.Schema(type=openapi.TYPE_STRING, description='New home sample date (YYYY-MM-DD)', example='2026-10-19'),
        'new_home_sample_time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='New home sample time slot', example='08:00 AM to 10:00 AM'),
        'time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='New appointment time slot', example='11:00 AM to 01:00 PM'),
        'new_time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='New appointment time slot', example='11:00 AM to 01:00 PM'),
        'rescheduled_by': openapi.Schema(type=openapi.TYPE_STRING, description='Role/entity that rescheduled (Staff / Candidate / Vendor / Admin)', example='Staff'),
        'reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason for reschedule', example='Candidate requested later date due to travel'),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description='Remark', example='Rescheduled to next Monday 11 AM to 01 PM'),
        'center': openapi.Schema(type=openapi.TYPE_INTEGER, description='Center ID if center changed', example=1),
    }
)

candidate_appointment_cancel_done_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['appointment', 'status'],
    properties={
        'appointment': openapi.Schema(type=openapi.TYPE_INTEGER, description='DarwinboxCandidateAppointment ID (or id)', example=1),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status: "Reports Uploaded" or "Cancel"', example='Reports Uploaded'),
        'fitness_status': openapi.Schema(type=openapi.TYPE_STRING, description='Candidate fitness status for Darwinbox (Process Initiated / Fit / Fit with Recommendation / Temporarily Unfit)', enum=['Process Initiated', 'Fit', 'Fit with Recommendation', 'Temporarily Unfit'], example='Fit'),
        'group_company': openapi.Schema(type=openapi.TYPE_STRING, description='Darwinbox group company name (defaults to candidate company or "Roma Builders Private Limited")', example='Roma Builders Private Limited'),
        'report': openapi.Schema(type=openapi.TYPE_FILE, description='PDF/Image health checkup report file'),
        'report_date': openapi.Schema(type=openapi.TYPE_STRING, description='Date report was generated/uploaded (YYYY-MM-DD)', example='2026-10-21'),
        'reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason for cancellation (if status is Cancel)', example='Candidate declined offer'),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description='Additional remarks', example='Normal results'),
    }
)

candidate_appointment_report_upload_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'appointment': openapi.Schema(type=openapi.TYPE_INTEGER, description='DarwinboxCandidateAppointment ID (or id)', example=1),
        'appointments': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description='List of DarwinboxCandidateAppointment IDs for multiple candidate upload', example=[1, 2]),
        'fitness_status': openapi.Schema(type=openapi.TYPE_STRING, description='Candidate fitness status for Darwinbox (Process Initiated / Fit / Fit with Recommendation / Temporarily Unfit)', enum=['Process Initiated', 'Fit', 'Fit with Recommendation', 'Temporarily Unfit'], example='Fit'),
        'group_company': openapi.Schema(type=openapi.TYPE_STRING, description='Darwinbox group company name (defaults to candidate company or "Roma Builders Private Limited")', example='Roma Builders Private Limited'),
        'report': openapi.Schema(type=openapi.TYPE_FILE, description='PDF health checkup report file'),
        'report_date': openapi.Schema(type=openapi.TYPE_STRING, description='Date report was generated/uploaded (YYYY-MM-DD)', example='2026-10-21'),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description='Additional remarks', example='Pre-employment health checkup completed successfully'),
    }
)

candidate_appointment_date_update_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['id'],
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='DarwinboxCandidateAppointment ID', example=1),
        'appointment_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 1', example='2026-10-22'),
        'appointment_time_slot_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup time slot 1', example='11:00 AM to 01:00 PM'),
        'appointment_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 2', example='2026-10-23'),
        'appointment_time_slot_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup time slot 2', example='02:00 PM to 04:00 PM'),
        'home_sample_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 1', example='2026-10-21'),
        'home_sample_time_slot_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample time slot 1', example='08:00 AM to 10:00 AM'),
        'home_sample_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 2', example='2026-10-22'),
        'home_sample_time_slot_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample time slot 2', example='10:00 AM to 12:00 PM'),
        'time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred appointment time slot', example='11:00 AM to 01:00 PM'),
    }
)

candidate_appointment_id_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['id'],
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='DarwinboxCandidateAppointment ID', example=1),
    }
)

candidate_appointment_full_manage_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    description='Comprehensive endpoint accepting ALL DarwinboxCandidateAppointment & Reschedule parameters in a single API call.',
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Appointment ID (optional, updates if provided, creates if omitted)', example=1),
        'hoh_employee': openapi.Schema(type=openapi.TYPE_INTEGER, description='Candidate ID (HohEmployee ID)', example=1),
        'package': openapi.Schema(type=openapi.TYPE_INTEGER, description='Package ID (PackageDetail ID)', example=2),
        'center': openapi.Schema(type=openapi.TYPE_INTEGER, description='Diagnostic Center ID (CenterDetail ID)', example=1),
        'vendor': openapi.Schema(type=openapi.TYPE_INTEGER, description='Vendor ID (VendorDetail ID)', example=1),
        'type_of_visit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Type of Visit ID (TypeOfVisit ID)', example=1),
        'appointment_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 1', example='2026-10-15'),
        'appointment_time_slot_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup time slot 1', example='11:00 AM to 01:00 PM'),
        'appointment_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 2', example='2026-10-16'),
        'appointment_time_slot_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup time slot 2', example='02:00 PM to 04:00 PM'),
        'home_sample_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 1', example='2026-10-14'),
        'home_sample_time_slot_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample time slot 1', example='08:00 AM to 10:00 AM'),
        'home_sample_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 2', example='2026-10-15'),
        'home_sample_time_slot_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample time slot 2', example='10:00 AM to 12:00 PM'),
        'confirm_appointment_date': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmed checkup date', example='2026-10-15'),
        'confirm_appointment_time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmed checkup time slot', example='11:00 AM to 01:00 PM'),
        'confirm_home_sample_date': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmed home sample date', example='2026-10-14'),
        'confirm_home_sample_time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmed home sample time slot', example='08:00 AM to 10:00 AM'),
        'date_of_appointment': openapi.Schema(type=openapi.TYPE_STRING, description='Date of appointment', example='2026-10-15'),
        'time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='Time slot', example='11:00 AM to 01:00 PM'),
        'new_appointment_date': openapi.Schema(type=openapi.TYPE_STRING, description='New appointment date (for reschedule audit)', example='2026-10-20'),
        'new_appointment_time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='New appointment time slot (for reschedule audit)', example='11:00 AM to 01:00 PM'),
        'new_home_sample_date': openapi.Schema(type=openapi.TYPE_STRING, description='New home sample date (for reschedule audit)', example='2026-10-19'),
        'new_home_sample_time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='New home sample time slot (for reschedule audit)', example='08:00 AM to 10:00 AM'),
        'new_time_slot': openapi.Schema(type=openapi.TYPE_STRING, description='New time slot (for reschedule audit)', example='11:00 AM to 01:00 PM'),
        'rescheduled_by': openapi.Schema(type=openapi.TYPE_STRING, description='Role/person who rescheduled (Staff/Candidate/Vendor)', example='Staff'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status: Request Received | Confirmed | Rescheduled | Reports Uploaded | Cancel', example='Confirmed'),
        'reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason note', example='Pre-employment checkup'),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description='Additional remark', example='Confirmed for 11 AM to 01 PM'),
        'report_date': openapi.Schema(type=openapi.TYPE_STRING, description='Report upload date', example='2026-10-21'),
    }
)


# ============================================================
# DARWINBOX CANDIDATE APPOINTMENT VIEWS
# ============================================================

def send_candidate_appointment_confirmation_email(appointment, custom_time_slot=None):
    """
    Triggers Pre-Employment Health Check-up Appointment Confirmation/Reschedule email to Candidate.
    Handles dates dynamically based on type_of_visit (At Home, At Center, Hybrid).
    """
    try:
        emp_obj = appointment.hoh_employee
        recipient_email = emp_obj.personal_email if emp_obj else None
        if recipient_email and recipient_email != 'null' and recipient_email != '':
            employee_name = f"{emp_obj.first_name or ''} {emp_obj.last_name or ''}".strip() or "Employee"

            # Helper for date formatting
            def format_date_str(raw):
                if not raw:
                    return ''
                val = str(raw).strip()
                if not val or val in ['null', 'None']:
                    return ''
                for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d'):
                    try:
                        return datetime.strptime(val, fmt).strftime('%d-%m-%Y')
                    except Exception:
                        pass
                return val

            # Determine type of visit
            type_of_visit_raw = appointment.type_of_visit or ''
            type_of_visit_name = ''
            if str(type_of_visit_raw).strip().isdigit():
                tov_obj = models.TypeOfVisit.objects.filter(id=int(type_of_visit_raw)).first()
                type_of_visit_name = tov_obj.type_of_visit if tov_obj else str(type_of_visit_raw)
            else:
                type_of_visit_name = str(type_of_visit_raw).strip()

            if not type_of_visit_name and appointment.package:
                try:
                    pkg_obj = models.PackageDetail.objects.filter(id=int(appointment.package)).first()
                    if pkg_obj and pkg_obj.type_of_visit:
                        type_of_visit_name = str(pkg_obj.type_of_visit.type_of_visit).strip()
                except Exception:
                    pass

            visit_lower = type_of_visit_name.lower()
            is_hybrid_visit = 'hybrid' in visit_lower
            is_home_visit = 'home' in visit_lower and not is_hybrid_visit
            is_center_visit = 'center' in visit_lower and not is_hybrid_visit

            # Center appointment date & time
            raw_center_date = appointment.confirm_appointment_date or appointment.appointment_date_1 or appointment.date_of_appointment or ''
            center_appointment_date = format_date_str(raw_center_date)
            center_appointment_time = (
                appointment.confirm_appointment_time_slot or 
                appointment.appointment_time_slot_1 or 
                appointment.time_slot or 
                custom_time_slot or 
                ''
            )

            # Home sample date & time
            raw_home_date = appointment.confirm_home_sample_date or appointment.home_sample_date_1 or ''
            home_sample_date = format_date_str(raw_home_date)
            home_sample_time = (
                appointment.confirm_home_sample_time_slot or 
                appointment.home_sample_time_slot_1 or 
                ''
            )

            # Main primary appointment_date & appointment_time for backward compatibility
            if is_home_visit:
                appointment_date = home_sample_date or center_appointment_date
                appointment_time = home_sample_time or center_appointment_time or '08:00 AM to 10:00 AM'
            elif is_hybrid_visit:
                appointment_date = center_appointment_date or home_sample_date
                appointment_time = center_appointment_time or home_sample_time or '11:00 AM to 01:00 PM'
            else:
                appointment_date = center_appointment_date or home_sample_date
                appointment_time = center_appointment_time or home_sample_time or '11:00 AM to 01:00 PM'

            # Calculate age from date_of_birth
            age = ""
            if emp_obj and emp_obj.date_of_birth:
                try:
                    today = datetime.now().date()
                    dob = emp_obj.date_of_birth
                    age_val = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                    age = str(age_val)
                except Exception:
                    age = ""

            gender = (emp_obj.gender or '').strip() if emp_obj else ''
            gender_age_parts = [p for p in [gender, age] if p]
            gender_age = " / ".join(gender_age_parts) if gender_age_parts else (gender or "N/A")

            center_name = appointment.center.center_name if appointment.center else ''
            center_address = appointment.center.address if appointment.center else ''

            package_name = str(appointment.package or '')
            if appointment.package:
                try:
                    pkg_obj = models.PackageDetail.objects.filter(id=int(appointment.package)).first()
                    if pkg_obj:
                        package_name = pkg_obj.package_name
                except (ValueError, TypeError):
                    package_name = str(appointment.package)

            context = {
                "employee_name": employee_name,
                "patient_name": employee_name,
                "gender": gender,
                "age": age,
                "gender_age": gender_age,
                "type_of_visit": type_of_visit_name or ("At Home" if is_home_visit else "Hybrid" if is_hybrid_visit else "At Center"),
                "is_home_visit": is_home_visit,
                "is_center_visit": is_center_visit,
                "is_hybrid_visit": is_hybrid_visit,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time,
                "center_appointment_date": center_appointment_date,
                "center_appointment_time": center_appointment_time,
                "home_sample_date": home_sample_date,
                "home_sample_time": home_sample_time,
                "center_name": center_name,
                "center_address": center_address,
                "package_name": package_name
            }

            subject = 'House of Hiranandani – Pre-Employment Health Check-up Appointment Confirmation'
            if appointment.status == 'Rescheduled':
                subject = 'House of Hiranandani – Pre-Employment Health Check-up Appointment Rescheduled'

            htmlgen = get_template("darwinbox_candidate_appointment_confirmation.html").render(context)

            email = EmailMessage(
                subject=subject,
                body=htmlgen,
                from_email=getattr(settings, 'EMAIL_HOST_USER', 'wellness@vakare.in'),
                to=[recipient_email],
                cc=['wellness@vakare.in', 'trishali.jadhav@houseofhiranandani.com','sandesh.chalke@houseofhiranandani.com'],
            )

            email.content_subtype = "html"
            email.send(fail_silently=False)

    except Exception as mail_error:
        print("Error triggering appointment confirmation email to hoh_employee:", str(mail_error))


@swagger_auto_schema(
    method='post',
    operation_description="Create a new Darwinbox candidate appointment. Validation: If type_of_visit is 'At Home', home_sample_date_1 is mandatory. If 'At Center', appointment_date_1 is mandatory. If 'Hybrid', both appointment_date_1 and home_sample_date_1 are mandatory.",
    request_body=candidate_appointment_create_schema,
    responses={200: "Success response with created appointment data"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_create(request):
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            hoh_employee = python_data.get('hoh_employee') or python_data.get('hoh_employee_id')
            package = python_data.get('package') or python_data.get('package_id')
            center = python_data.get('center') or python_data.get('center_id')
            vendor = python_data.get('vendor') or python_data.get('vendor_id')
            type_of_visit = python_data.get('type_of_visit') or python_data.get('type_of_visit_id')
            
            appointment_date_1 = python_data.get('appointment_date_1') or python_data.get('health_checkup_date')
            appointment_time_slot_1 = python_data.get('appointment_time_slot_1') or python_data.get('time_slot_1') or python_data.get('time_slot') or python_data.get('appointment_time') or python_data.get('slot') or python_data.get('time')
            
            appointment_date_2 = python_data.get('appointment_date_2')
            appointment_time_slot_2 = python_data.get('appointment_time_slot_2') or python_data.get('time_slot_2')
            
            home_sample_date_1 = python_data.get('home_sample_date_1')
            home_sample_time_slot_1 = python_data.get('home_sample_time_slot_1')
            home_sample_date_2 = python_data.get('home_sample_date_2')
            home_sample_time_slot_2 = python_data.get('home_sample_time_slot_2')
            
            time_slot = appointment_time_slot_1 or home_sample_time_slot_1 or python_data.get('time_slot')

            # Determine normalized type_of_visit string
            visit_type_name = ''
            if type_of_visit is not None and str(type_of_visit).strip() not in ['', 'null', 'None']:
                if str(type_of_visit).strip().isdigit():
                    tov_obj = models.TypeOfVisit.objects.filter(id=int(type_of_visit)).first()
                    visit_type_name = tov_obj.type_of_visit if tov_obj else str(type_of_visit).strip()
                else:
                    visit_type_name = str(type_of_visit).strip()
            elif package:
                try:
                    pkg_obj = models.PackageDetail.objects.filter(id=int(package)).first()
                    if pkg_obj and pkg_obj.type_of_visit:
                        visit_type_name = str(pkg_obj.type_of_visit.type_of_visit).strip()
                except Exception:
                    pass

            visit_type_lower = visit_type_name.lower().strip()
            is_hybrid = 'hybrid' in visit_type_lower
            is_home = 'home' in visit_type_lower and not is_hybrid
            is_center = 'center' in visit_type_lower and not is_hybrid

            has_app_date = bool(appointment_date_1 and str(appointment_date_1).strip() not in ['', 'null', 'None'])
            has_home_date = bool(home_sample_date_1 and str(home_sample_date_1).strip() not in ['', 'null', 'None'])

            # Validation:
            # - If At Home -> home_sample_date_1 is mandatory
            # - If At Center -> appointment_date_1 is mandatory
            # - If Hybrid -> both appointment_date_1 and home_sample_date_1 are mandatory
            if is_home:
                if not has_home_date:
                    res = {'statuscode': 400, 'status': 'false', 'message': 'home_sample_date_1 is mandatory for At Home visit'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
            elif is_center:
                if not has_app_date:
                    res = {'statuscode': 400, 'status': 'false', 'message': 'appointment_date_1 is mandatory for At Center visit'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
            elif is_hybrid:
                if not has_app_date and not has_home_date:
                    res = {'statuscode': 400, 'status': 'false', 'message': 'appointment_date_1 and home_sample_date_1 are mandatory for Hybrid visit'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                elif not has_app_date:
                    res = {'statuscode': 400, 'status': 'false', 'message': 'appointment_date_1 is mandatory for Hybrid visit'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                elif not has_home_date:
                    res = {'statuscode': 400, 'status': 'false', 'message': 'home_sample_date_1 is mandatory for Hybrid visit'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
            else:
                # If visit type is unspecified or other, at least one preferred date must be provided
                if not has_app_date and not has_home_date:
                    res = {'statuscode': 400, 'status': 'false', 'message': 'appointment_date_1 or home_sample_date_1 is mandatory'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')

            now = datetime.now()
            current_date_data = now.strftime('%Y-%m-%d')
            current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()

            status = python_data.get('status', 'Pending')

            appointment = models.DarwinboxCandidateAppointment.objects.create(
                hoh_employee_id=hoh_employee,
                package=package,
                center_id=center,
                vendor_id=vendor,
                type_of_visit=type_of_visit or visit_type_name or None,
                appointment_date_1=appointment_date_1,
                appointment_time_slot_1=appointment_time_slot_1,
                appointment_date_2=appointment_date_2,
                appointment_time_slot_2=appointment_time_slot_2,
                home_sample_date_1=home_sample_date_1,
                home_sample_time_slot_1=home_sample_time_slot_1,
                home_sample_date_2=home_sample_date_2,
                home_sample_time_slot_2=home_sample_time_slot_2,
                time_slot=time_slot,
                reason=python_data.get('reason'),
                remark=python_data.get('remark') or python_data.get('remarks'),
                status=status,
                created_at=str(current_date)
            )

            # Trigger email to candidate with custom time slot
            send_candidate_appointment_confirmation_email(
                appointment, 
                custom_time_slot=appointment_time_slot_1 or home_sample_time_slot_1
            )

            # serializer = DarwinboxCandidateAppointmentSerializer(appointment)
            res = {
                'statuscode': 200,
                'status': 'true',
                'message': 'Darwinbox candidate appointment created successfully',
                # 'data': serializer.data
            }
        except Exception as e:
            res = {
                'statuscode': 400,
                'status': 'false',
                'message': str(e)
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='post',
    operation_description="Update any fields of an existing Darwinbox candidate appointment.",
    request_body=candidate_appointment_update_schema,
    responses={200: "Success response with updated appointment data"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_update(request):
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('id') or python_data.get('appointment')
            
            if not appointment_id:
                res = {'statuscode': 400, 'status': 'false', 'message': 'id is required'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).first()
            if not appointment:
                res = {'statuscode': 404, 'status': 'false', 'message': 'Appointment not found'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            if 'hoh_employee_id' in python_data or 'hoh_employee' in python_data:
                emp_id = python_data.get('hoh_employee_id') or python_data.get('hoh_employee')
                appointment.hoh_employee = models.HohEmployee.objects.filter(id=emp_id).first() if emp_id else None

            if 'vendor_id' in python_data or 'vendor' in python_data:
                vendor_id = python_data.get('vendor_id') or python_data.get('vendor')
                appointment.vendor = models.VendorDetail.objects.filter(id=vendor_id).first() if vendor_id else None

            if 'center_id' in python_data or 'center' in python_data:
                center_id = python_data.get('center_id') or python_data.get('center')
                appointment.center = models.CenterDetail.objects.filter(id=center_id).first() if center_id else None
            
            if 'type_of_visit' in python_data:
                appointment.type_of_visit = python_data.get('type_of_visit')
            if 'package' in python_data:
                appointment.package = python_data.get('package')
            if 'appointment_date_1' in python_data:
                appointment.appointment_date_1 = python_data.get('appointment_date_1')
            if 'appointment_time_slot_1' in python_data:
                appointment.appointment_time_slot_1 = python_data.get('appointment_time_slot_1')
            if 'appointment_date_2' in python_data:
                appointment.appointment_date_2 = python_data.get('appointment_date_2')
            if 'appointment_time_slot_2' in python_data:
                appointment.appointment_time_slot_2 = python_data.get('appointment_time_slot_2')
            if 'home_sample_date_1' in python_data:
                appointment.home_sample_date_1 = python_data.get('home_sample_date_1')
            if 'home_sample_time_slot_1' in python_data:
                appointment.home_sample_time_slot_1 = python_data.get('home_sample_time_slot_1')
            if 'home_sample_date_2' in python_data:
                appointment.home_sample_date_2 = python_data.get('home_sample_date_2')
            if 'home_sample_time_slot_2' in python_data:
                appointment.home_sample_time_slot_2 = python_data.get('home_sample_time_slot_2')
            if 'confirm_appointment_date' in python_data:
                appointment.confirm_appointment_date = python_data.get('confirm_appointment_date')
            if 'confirm_appointment_time_slot' in python_data:
                appointment.confirm_appointment_time_slot = python_data.get('confirm_appointment_time_slot')
            if 'confirm_home_sample_date' in python_data:
                appointment.confirm_home_sample_date = python_data.get('confirm_home_sample_date')
            if 'confirm_home_sample_time_slot' in python_data:
                appointment.confirm_home_sample_time_slot = python_data.get('confirm_home_sample_time_slot')
            if 'date_of_appointment' in python_data:
                appointment.date_of_appointment = python_data.get('date_of_appointment')
            if 'time_slot' in python_data or 'appointment_time' in python_data or 'slot' in python_data or 'time' in python_data:
                appointment.time_slot = python_data.get('time_slot') or python_data.get('appointment_time') or python_data.get('slot') or python_data.get('time')
            if 'reason' in python_data:
                appointment.reason = python_data.get('reason')
            if 'remark' in python_data or 'remarks' in python_data:
                appointment.remark = python_data.get('remark') or python_data.get('remarks')
            if 'status' in python_data:
                appointment.status = python_data.get('status')
            if 'report_date' in python_data:
                appointment.report_date = python_data.get('report_date')

            appointment.save()
            serializer = DarwinboxCandidateAppointmentSerializer(appointment)
            res = {
                'statuscode': 200,
                'status': 'true',
                'message': 'Darwinbox candidate appointment updated successfully',
                'data': serializer.data
            }
        except Exception as e:
            res = {
                'statuscode': 400,
                'status': 'false',
                'message': str(e)
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    methods=['get', 'post'],
    operation_description="Get list of all Darwinbox candidate appointments (ordered by newest first).",
    responses={200: "List of DarwinboxCandidateAppointment records"}
)
@api_view(['GET', 'POST'])
@csrf_exempt
def all_darwinbox_candidate_appointment_list(request):
    if request.method in ['POST', 'GET']:
        python_data = JSONParser().parse(io.BytesIO(request.body))
        page_number = int(python_data.get('page_number',1))
        row_size = int(python_data.get('row_size',10))
        last_row = row_size * page_number
        first_row = last_row - row_size
        
        total_records = models.DarwinboxCandidateAppointment.objects.all().count()
        appointments = models.DarwinboxCandidateAppointment.objects.all().order_by('-id')[first_row:last_row]
        serializer = DarwinboxCandidateAppointmentSerializer(appointments, many=True)
        res = {
            'statuscode': 200,
            'status': 'true',
            'data': serializer.data,
            'total_records':total_records
            
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='get',
    operation_description="Get detailed view of a single Darwinbox candidate appointment by ID.",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="Appointment ID", type=openapi.TYPE_INTEGER),
    ],
    responses={200: "DarwinboxCandidateAppointment details"}
)
@swagger_auto_schema(
    method='post',
    operation_description="Get detailed view of a single Darwinbox candidate appointment by ID.",
    request_body=candidate_appointment_id_schema,
    responses={200: "DarwinboxCandidateAppointment details"}
)
@api_view(['GET', 'POST'])
@csrf_exempt
def get_darwinbox_candidate_appointment_detail(request):
    if request.method in ['POST', 'GET']:
        if request.method == 'POST':
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('id') or python_data.get('appointment')
        else:
            appointment_id = request.GET.get('id') or request.GET.get('appointment')

        if not appointment_id:
            res = {'statuscode': 400, 'status': 'false', 'message': 'id is required'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).first()
        if not appointment:
            res = {'statuscode': 404, 'status': 'false', 'message': 'Appointment not found'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        serializer = DarwinboxCandidateAppointmentSerializer(appointment)
        res = {
            'statuscode': 200,
            'status': 'true',
            'data': serializer.data
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='get',
    operation_description="Alias of get_darwinbox_candidate_appointment_detail (data check by ID).",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="Appointment ID", type=openapi.TYPE_INTEGER),
    ],
    responses={200: "DarwinboxCandidateAppointment details"}
)
@swagger_auto_schema(
    method='post',
    operation_description="Alias of get_darwinbox_candidate_appointment_detail (data check by ID).",
    request_body=candidate_appointment_id_schema,
    responses={200: "DarwinboxCandidateAppointment details"}
)
@api_view(['GET', 'POST'])
@csrf_exempt
def darwinbox_candidate_appointment_data_check(request):
    return get_darwinbox_candidate_appointment_detail(request)


@swagger_auto_schema(
    method='post',
    operation_description="Delete a Darwinbox candidate appointment by ID.",
    request_body=candidate_appointment_id_schema,
    responses={200: "Appointment deleted successfully"}
)
@api_view(['POST'])
@csrf_exempt
def delete_darwinbox_candidate_appointment(request):
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('id') or python_data.get('appointment')
            if not appointment_id:
                res = {'statuscode': 400, 'status': 'false', 'message': 'id is required'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).first()
            if not appointment:
                res = {'statuscode': 404, 'status': 'false', 'message': 'Appointment not found'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            appointment.delete()
            res = {
                'statuscode': 200,
                'status': 'true',
                'message': 'Appointment deleted successfully'
            }
        except Exception as e:
            res = {'statuscode': 400, 'status': 'false', 'message': str(e)}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='post',
    operation_description="Alias to delete a Darwinbox candidate appointment by ID.",
    request_body=candidate_appointment_id_schema,
    responses={200: "Appointment deleted successfully"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_delete(request):
    return delete_darwinbox_candidate_appointment(request)


@swagger_auto_schema(
    method='post',
    operation_description="Upload report and mark completed ('Reports Uploaded') or Cancel an appointment ('Cancel'). When 'Reports Uploaded', syncs candidate report to Darwinbox Import API.",
    request_body=candidate_appointment_cancel_done_schema,
    responses={200: "Status update success message with Darwinbox sync result"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_cancel_done(request):
    if request.method == 'POST':
        # python_data = {}
        # for i, j in request.FILES.items():
        #     python_data.update({i: j})
        # for i, j in request.POST.items():
        #     python_data.update({i: j})

        python_data = JSONParser().parse(io.BytesIO(request.body))

        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()

        appointment_id = python_data.get('appointment') or python_data.get('id')
        status = python_data.get('status')
        fitness_status = python_data.get('fitness_status') or python_data.get('fitness') or python_data.get('a6aa003de51453')
        group_company = python_data.get('group_company')
        report = python_data.get('report')
        reason = python_data.get('reason')
        remark = python_data.get('remark') or python_data.get('remarks')
        report_date = python_data.get('report_date')

        check_appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).count()
        if check_appointment == 1:
            appointment = models.DarwinboxCandidateAppointment.objects.get(id=appointment_id)
            if status == 'Reports Uploaded':
                if report:
                    appointment.report = report
                appointment.status = 'Reports Uploaded'
                appointment.remark = remark if remark else appointment.remark
                appointment.report_date = report_date if report_date else str(current_date)
                appointment.save()

                # Trigger Darwinbox Pre-Employment Health Checkup Status Sync Task
                darwinbox_sync_result = upload_darwinbox_candidate_report_to_api(
                    [appointment],
                    group_company=group_company,
                    fitness_status=fitness_status
                )

                darwinbox_ok = darwinbox_sync_result.get('status', False)
                db_resp = darwinbox_sync_result.get('darwinbox_response')
                if isinstance(db_resp, dict) and db_resp.get('status') in [0, '0', False, 'false']:
                    darwinbox_ok = False

                if darwinbox_ok:
                    res = {
                        'statuscode': 200,
                        'status': 'true',
                        'message': 'Darwinbox candidate report Uploaded successfully.',
                        'darwinbox_status': 1,
                        'darwinbox_sync': darwinbox_sync_result
                    }
                else:
                    err_text = darwinbox_sync_result.get('message') or (db_resp.get('message') if isinstance(db_resp, dict) else 'Darwinbox sync failed.')
                    res = {
                        'statuscode': 400,
                        'status': 'false',
                        'message': f'Darwinbox Sync Error: {err_text}',
                        'darwinbox_status': 0,
                        'darwinbox_sync': darwinbox_sync_result
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            elif status == 'Cancel':
                appointment.status = 'Cancel'
                appointment.reason = reason
                appointment.remark = remark
                appointment.save()

                res = {
                    'statuscode': 200,
                    'status': 'true',
                    'message': 'Darwinbox candidate appointment Cancelled successfully.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            else:
                res = {
                    'statuscode': 406,
                    'status': 'false',
                    'message': 'Enter valid status.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
        else:
            res = {
                'statuscode': 406,
                'status': 'false',
                'message': 'Enter valid appointment.'
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')


def send_candidate_report_upload_email(appt, req=None, recipient_list=None):
    """
    Triggers Pre-Employment Health Check-up Report notification email to HR upon report upload.
    Recipient defaults to ['hr@vakare.in'] and supports multiple emails.
    """
    try:
        hr_emails = ['rushyandhan.s@houseofhiranandani.com']
        # hr_emails = ['wellness@vakare.in']
        if recipient_list:
            if isinstance(recipient_list, list):
                hr_emails.extend(recipient_list)
            elif isinstance(recipient_list, str):
                hr_emails.extend([x.strip() for x in recipient_list.split(',') if x.strip()])
        configured_emails = getattr(settings, 'DARWINBOX_HR_REPORT_EMAILS', None)
        if configured_emails:
            if isinstance(configured_emails, list):
                hr_emails.extend(configured_emails)
            elif isinstance(configured_emails, str):
                hr_emails.extend([x.strip() for x in configured_emails.split(',') if x.strip()])

        hr_emails = list(dict.fromkeys(hr_emails))

        emp_obj = appt.hoh_employee
        employee_name = f"{emp_obj.first_name or ''} {emp_obj.last_name or ''}".strip() if emp_obj else "Candidate"
        if not employee_name:
            employee_name = "Candidate"

        appointment_date = appt.confirm_appointment_date or appt.appointment_date_1 or appt.date_of_appointment or appt.report_date or ''
        company_name = emp_obj.company if (emp_obj and emp_obj.company) else "Svasthya Wellness Team"

        report_link = ""
        if appt.report:
            base_url = getattr(settings, 'SITE_MEDIA_BASE_URL', '')
            report_link = f"{base_url}{appt.report}"

        context = {
            "hr_name": "HR Team",
            "employee_name": employee_name,
            "appointment_date": appointment_date,
            "report_link": report_link,
            "company_name": company_name
        }

        subject = f"Pre-Employment Health Check-up Report - {employee_name}"
        htmlgen = get_template("pre_employment_report_upload.html").render(context)
        # send_mail(
        #     subject,
        #     f"{employee_name}'s health check-up report dated {appointment_date} has been successfully uploaded. View report: {report_link}",
        #     getattr(settings, 'EMAIL_HOST_USER', 'wellness@vakare.in'),
        #     hr_emails, cc=['wellness@vakare.in'] ,
        #     fail_silently=False,
        #     html_message=htmlgen
        # )

        email = EmailMessage(
            subject=subject,
            body=htmlgen,
            from_email=getattr(
                settings,
                'EMAIL_HOST_USER',
                'wellness@vakare.in'
            ),
            to=hr_emails,
            cc=['wellness@vakare.in', 'trishali.jadhav@houseofhiranandani.com','sandesh.chalke@houseofhiranandani.com'],
        )

        email.content_subtype = "html"
        email.send(fail_silently=False)

    except Exception as mail_err:
        print("Error triggering report upload email to HR:", str(mail_err))


@swagger_auto_schema(
    method='post',
    operation_description="Upload Pre-Employment Health Checkup Report(s) for Darwinbox candidate appointment(s) and submit status to Darwinbox Import API. Supports single and multiple candidates.",
    request_body=candidate_appointment_report_upload_schema,
    responses={200: "Report uploaded successfully with Darwinbox response"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_report_upload(request):
    if request.method == 'POST':
        try:
            python_data = {}
            for i, j in request.FILES.items():
                python_data.update({i: j})
            for i, j in request.POST.items():
                python_data.update({i: j})

            # Check if JSON body was provided instead of multipart form data
            if not python_data:
                try:
                    python_data = JSONParser().parse(io.BytesIO(request.body))
                except Exception:
                    pass

            now = datetime.now()
            current_date_data = now.strftime('%Y-%m-%d')
            current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()

            appointment_id = python_data.get('appointment') or python_data.get('id')
            appointments_input = python_data.get('appointments') or python_data.get('appointment_ids')
            fitness_status = python_data.get('fitness_status') or python_data.get('fitness') or python_data.get('a6aa003de51453')
            group_company = python_data.get('group_company')
            report = python_data.get('report') or python_data.get('file')
            remark = python_data.get('remark') or python_data.get('remarks')
            report_date = python_data.get('report_date') or str(current_date)
            hr_emails_input = python_data.get('hr_emails') or python_data.get('hr_email')

            # Parse multiple appointments if provided as json string or comma-separated string
            if isinstance(appointments_input, str):
                try:
                    appointments_input = json.loads(appointments_input)
                except Exception:
                    appointments_input = [x.strip() for x in appointments_input.split(',') if x.strip()]

            # Case 1: Multiple Appointments batch upload
            if isinstance(appointments_input, (list, tuple)) and len(appointments_input) > 0:
                updated_appointments = []
                for appt_val in appointments_input:
                    target_id = appt_val.get('id') or appt_val.get('appointment') if isinstance(appt_val, dict) else appt_val
                    appt_obj = models.DarwinboxCandidateAppointment.objects.filter(id=target_id).first()
                    if appt_obj:
                        appt_obj.status = 'Reports Uploaded'
                        if isinstance(appt_val, dict) and appt_val.get('report'):
                            appt_obj.report = appt_val.get('report')
                        elif report and len(appointments_input) == 1:
                            appt_obj.report = report
                        appt_obj.remark = remark if remark else appt_obj.remark
                        appt_obj.report_date = report_date if report_date else appt_obj.report_date
                        appt_obj.save()
                        updated_appointments.append(appt_obj)

                if not updated_appointments:
                    res = {
                        'statuscode': 404,
                        'status': 'false',
                        'message': 'No valid candidate appointments found for provided IDs.'
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')

                darwinbox_sync_result = upload_darwinbox_candidate_report_to_api(
                    updated_appointments,
                    group_company=group_company,
                    fitness_status=fitness_status
                )

                # Check if Darwinbox sync status == 1 (success)
                darwinbox_ok = darwinbox_sync_result.get('status', False)
                db_resp = darwinbox_sync_result.get('darwinbox_response')
                if isinstance(db_resp, dict) and db_resp.get('status') in [0, '0', False, 'false']:
                    darwinbox_ok = False

                if darwinbox_ok:
                    # If status = 1 then trigger email to HR for each updated appointment
                    for appt_item in updated_appointments:
                        send_candidate_report_upload_email(appt_item, request, hr_emails_input)

                    serializer = DarwinboxCandidateAppointmentSerializer(updated_appointments, many=True)
                    res = {
                        'statuscode': 200,
                        'status': 'true',
                        'message': f'Successfully updated and submitted reports for {len(updated_appointments)} candidate(s) to Darwinbox.',
                        'darwinbox_status': 1,
                        'darwinbox_sync': darwinbox_sync_result,
                        'data': serializer.data
                    }
                else:
                    # When status is 0 then show the error
                    err_text = darwinbox_sync_result.get('message') or (db_resp.get('message') if isinstance(db_resp, dict) else 'Darwinbox sync failed.')
                    res = {
                        'statuscode': 400,
                        'status': 'false',
                        'message': f'Darwinbox Sync Error: {err_text}',
                        'darwinbox_status': 0,
                        'darwinbox_sync': darwinbox_sync_result
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            # Case 2: Single Appointment upload
            if appointment_id:
                check_appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).count()
                if check_appointment == 1:
                    appointment = models.DarwinboxCandidateAppointment.objects.get(id=appointment_id)
                    if report:
                        appointment.report = report
                    appointment.status = 'Reports Uploaded'
                    appointment.remark = remark if remark else appointment.remark
                    appointment.report_date = report_date if report_date else str(current_date)
                    appointment.save()

                    darwinbox_sync_result = upload_darwinbox_candidate_report_to_api(
                        [appointment],
                        group_company=group_company,
                        fitness_status=fitness_status
                    )

                    # Check if Darwinbox sync status == 1 (success)
                    darwinbox_ok = darwinbox_sync_result.get('status', False)
                    db_resp = darwinbox_sync_result.get('darwinbox_response')
                    if isinstance(db_resp, dict) and db_resp.get('status') in [0, '0', False, 'false']:
                        darwinbox_ok = False

                    if darwinbox_ok:
                        # If status = 1 then trigger email to HR
                        send_candidate_report_upload_email(appointment, request, hr_emails_input)

                        serializer = DarwinboxCandidateAppointmentSerializer(appointment)
                        res = {
                            'statuscode': 200,
                            'status': 'true',
                            'message': 'Darwinbox candidate report Uploaded successfully.',
                            'darwinbox_status': 1,
                            'darwinbox_sync': darwinbox_sync_result,
                            'data': serializer.data
                        }
                    else:
                        # When status is 0 then show the error
                        err_text = darwinbox_sync_result.get('message') or (db_resp.get('message') if isinstance(db_resp, dict) else 'Darwinbox sync failed.')
                        res = {
                            'statuscode': 400,
                            'status': 'false',
                            'message': f'Darwinbox Sync Error: {err_text}',
                            'darwinbox_status': 0,
                            'darwinbox_sync': darwinbox_sync_result
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                else:
                    res = {
                        'statuscode': 406,
                        'status': 'false',
                        'message': 'Enter valid appointment.'
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
            res = {
                'statuscode': 400,
                'status': 'false',
                'message': 'appointment or appointments parameter is required.'
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        except Exception as e:
            res = {'statuscode': 400, 'status': 'false', 'message': str(e)}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        except Exception as e:
            res = {'statuscode': 400, 'status': 'false', 'message': str(e)}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='post',
    operation_description="Confirm or Reschedule a Darwinbox candidate appointment. When status is 'Rescheduled', an audit record is created in RescheduleDarwinboxCandidateAppointment.",
    request_body=candidate_appointment_reschedule_schema,
    responses={200: "Reschedule or Confirmation success message with updated appointment and audit record"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_booking_reschedule(request):
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('appointment') or python_data.get('id')
            status = python_data.get('status', 'Rescheduled')

            now = datetime.now()
            current_date_data = now.strftime('%Y-%m-%d')
            current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()

            check_appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).count()
            if check_appointment == 1:
                appointment = models.DarwinboxCandidateAppointment.objects.get(id=appointment_id)
                if status == 'Confirmed':
                    appointment.remark = python_data.get('remark') or python_data.get('remarks', appointment.remark)
                    appointment.confirm_appointment_date = python_data.get('confirm_appointment_date', appointment.confirm_appointment_date)
                    appointment.confirm_appointment_time_slot = python_data.get('confirm_appointment_time_slot', appointment.confirm_appointment_time_slot)
                    appointment.confirm_home_sample_date = python_data.get('confirm_home_sample_date', appointment.confirm_home_sample_date)
                    appointment.confirm_home_sample_time_slot = python_data.get('confirm_home_sample_time_slot', appointment.confirm_home_sample_time_slot)
                    if 'time_slot' in python_data or 'appointment_time' in python_data or 'slot' in python_data or 'time' in python_data or appointment.confirm_appointment_time_slot:
                        appointment.time_slot = python_data.get('time_slot') or python_data.get('appointment_time') or python_data.get('slot') or python_data.get('time') or appointment.confirm_appointment_time_slot
                    appointment.status = 'Confirmed'
                    if 'center' in python_data or 'center_id' in python_data:
                        appointment.center_id = python_data.get('center') or python_data.get('center_id')
                    appointment.save()

                    # Trigger confirmation email to candidate
                    send_candidate_appointment_confirmation_email(appointment)

                    res = {
                        'statuscode': 200,
                        'status': 'true',
                        'message': 'Your Darwinbox candidate appointment Booked successfully.'
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')

                elif status == 'Rescheduled':
                    old_appointment_date = appointment.confirm_appointment_date or appointment.appointment_date_1
                    old_appointment_time_slot = appointment.confirm_appointment_time_slot or appointment.appointment_time_slot_1 or appointment.time_slot
                    old_home_sample_date = appointment.confirm_home_sample_date or appointment.home_sample_date_1
                    old_home_sample_time_slot = appointment.confirm_home_sample_time_slot or appointment.home_sample_time_slot_1
                    old_time_slot = appointment.time_slot or old_appointment_time_slot

                    new_appointment_date = python_data.get('confirm_appointment_date') or python_data.get('new_appointment_date') or python_data.get('new_health_checkup_date') or appointment.confirm_appointment_date
                    new_appointment_time_slot = python_data.get('confirm_appointment_time_slot') or python_data.get('new_appointment_time_slot') or python_data.get('appointment_time_slot_1') or python_data.get('appointment_time') or appointment.confirm_appointment_time_slot
                    new_home_sample_date = python_data.get('confirm_home_sample_date') or python_data.get('new_home_sample_date') or appointment.confirm_home_sample_date
                    new_home_sample_time_slot = python_data.get('confirm_home_sample_time_slot') or python_data.get('new_home_sample_time_slot') or python_data.get('home_sample_time_slot_1') or appointment.confirm_home_sample_time_slot
                    new_time_slot = python_data.get('time_slot') or python_data.get('new_time_slot') or new_appointment_time_slot or appointment.time_slot
                    rescheduled_by = python_data.get('rescheduled_by', 'Staff')
                    reason = python_data.get('reason', appointment.reason)
                    remark = python_data.get('remark') or python_data.get('remarks', appointment.remark)

                    reschedule_record = models.RescheduleDarwinboxCandidateAppointment.objects.create(
                        appointment=appointment,
                        hoh_employee=appointment.hoh_employee,
                        rescheduled_by=rescheduled_by,
                        old_appointment_date=old_appointment_date,
                        old_appointment_time_slot=old_appointment_time_slot,
                        new_appointment_date=new_appointment_date,
                        new_appointment_time_slot=new_appointment_time_slot,
                        old_home_sample_date=old_home_sample_date,
                        old_home_sample_time_slot=old_home_sample_time_slot,
                        new_home_sample_date=new_home_sample_date,
                        new_home_sample_time_slot=new_home_sample_time_slot,
                        old_time_slot=old_time_slot,
                        new_time_slot=new_time_slot,
                        time_slot=new_time_slot,
                        reason=reason,
                        remark=remark,
                        status='Rescheduled',
                        created_at=str(current_date)
                    )

                    appointment.remark = remark
                    appointment.reason = reason
                    appointment.confirm_appointment_date = new_appointment_date
                    appointment.confirm_appointment_time_slot = new_appointment_time_slot
                    appointment.confirm_home_sample_date = new_home_sample_date
                    appointment.confirm_home_sample_time_slot = new_home_sample_time_slot
                    if new_time_slot:
                        appointment.time_slot = new_time_slot
                    appointment.status = 'Rescheduled'
                    if 'center' in python_data or 'center_id' in python_data:
                        appointment.center_id = python_data.get('center') or python_data.get('center_id')
                    appointment.save()

                    # Trigger reschedule email to candidate
                    send_candidate_appointment_confirmation_email(appointment)

                    serializer = DarwinboxCandidateAppointmentSerializer(appointment)
                    reschedule_serializer = RescheduleDarwinboxCandidateAppointmentSerializer(reschedule_record)

                    res = {
                        'statuscode': 200,
                        'status': 'true',
                        'message': 'Your Darwinbox candidate appointment Rescheduled successfully.',
                        'data': serializer.data,
                        'reschedule_record': reschedule_serializer.data
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                else:
                    res = {
                        'statuscode': 406,
                        'status': 'false',
                        'message': 'Enter valid Status.'
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
            else:
                res = {
                    'statuscode': 406,
                    'status': 'false',
                    'message': 'Enter valid appointment.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
        except Exception as e:
            res = {'statuscode': 400, 'status': 'false', 'message': str(e)}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='post',
    operation_description="Alias to reschedule a Darwinbox candidate appointment.",
    request_body=candidate_appointment_reschedule_schema,
    responses={200: "Reschedule success message"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_reschedule(request):
    return darwinbox_candidate_appointment_booking_reschedule(request)


@swagger_auto_schema(
    method='post',
    operation_description="Update preferred dates and time slots for a Darwinbox candidate appointment.",
    request_body=candidate_appointment_date_update_schema,
    responses={200: "Appointment date updated successfully"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_date_update(request):
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('id') or python_data.get('appointment')
            appointment_date_1 = python_data.get('appointment_date_1')
            appointment_time_slot_1 = python_data.get('appointment_time_slot_1')
            appointment_date_2 = python_data.get('appointment_date_2')
            appointment_time_slot_2 = python_data.get('appointment_time_slot_2')
            home_sample_date_1 = python_data.get('home_sample_date_1')
            home_sample_time_slot_1 = python_data.get('home_sample_time_slot_1')
            home_sample_date_2 = python_data.get('home_sample_date_2')
            home_sample_time_slot_2 = python_data.get('home_sample_time_slot_2')
            time_slot = python_data.get('time_slot') or python_data.get('appointment_time') or python_data.get('slot') or python_data.get('time') or appointment_time_slot_1

            check_appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).count()
            if check_appointment == 1:
                appointment = models.DarwinboxCandidateAppointment.objects.get(id=appointment_id)
                if appointment_date_1:
                    appointment.appointment_date_1 = appointment_date_1
                if appointment_time_slot_1:
                    appointment.appointment_time_slot_1 = appointment_time_slot_1
                if appointment_date_2 is not None:
                    appointment.appointment_date_2 = appointment_date_2
                if appointment_time_slot_2 is not None:
                    appointment.appointment_time_slot_2 = appointment_time_slot_2
                if home_sample_date_1 is not None:
                    appointment.home_sample_date_1 = home_sample_date_1
                if home_sample_time_slot_1 is not None:
                    appointment.home_sample_time_slot_1 = home_sample_time_slot_1
                if home_sample_date_2 is not None:
                    appointment.home_sample_date_2 = home_sample_date_2
                if home_sample_time_slot_2 is not None:
                    appointment.home_sample_time_slot_2 = home_sample_time_slot_2
                if time_slot:
                    appointment.time_slot = time_slot
                appointment.save()

                serializer = DarwinboxCandidateAppointmentSerializer(appointment)
                res = {
                    'statuscode': 200,
                    'status': 'true',
                    'message': 'Appointment date updated successfully',
                    'data': serializer.data
                }
            else:
                res = {
                    'statuscode': 406,
                    'status': 'false',
                    'message': 'Enter valid appointment.'
                }
        except Exception as e:
            res = {'statuscode': 400, 'status': 'false', 'message': str(e)}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    methods=['get', 'post'],
    operation_description="Get reschedule audit history for Darwinbox candidate appointments (optionally filter by appointment_id).",
    manual_parameters=[
        openapi.Parameter('appointment_id', openapi.IN_QUERY, description="Optional appointment ID to filter", type=openapi.TYPE_INTEGER),
    ],
    responses={200: "List of RescheduleDarwinboxCandidateAppointment records"}
)
@api_view(['GET', 'POST'])
@csrf_exempt
def reschedule_darwinbox_candidate_appointment_list(request):
    if request.method in ['POST', 'GET']:
        if request.method == 'POST':
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('appointment_id') or python_data.get('appointment')
        else:
            appointment_id = request.GET.get('appointment_id') or request.GET.get('appointment')

        if appointment_id:
            records = models.RescheduleDarwinboxCandidateAppointment.objects.filter(appointment_id=appointment_id).order_by('-id')
        else:
            records = models.RescheduleDarwinboxCandidateAppointment.objects.all().order_by('-id')

        serializer = RescheduleDarwinboxCandidateAppointmentSerializer(records, many=True)
        res = {
            'statuscode': 200,
            'status': 'true',
            'data': serializer.data
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


# ============================================================
# UNIFIED ALL-PARAMETER ENDPOINT FOR DARWINBOX CANDIDATE APPOINTMENTS
# ============================================================

@swagger_auto_schema(
    method='post',
    operation_description="Unified single endpoint accepting ALL Darwinbox candidate appointment parameters (create, update, reschedule, confirm, cancel, and audit logging).",
    request_body=candidate_appointment_full_manage_schema,
    responses={200: "Success response with full appointment and optional reschedule record"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_full_manage(request):
    """
    Unified endpoint accepting ALL DarwinboxCandidateAppointment & Reschedule parameters in one place.
    """
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('id') or python_data.get('appointment')
            hoh_employee = python_data.get('hoh_employee') or python_data.get('hoh_employee_id')
            package = python_data.get('package') or python_data.get('package_id')
            center = python_data.get('center') or python_data.get('center_id')
            vendor = python_data.get('vendor') or python_data.get('vendor_id')
            type_of_visit = python_data.get('type_of_visit') or python_data.get('type_of_visit_id')
            appointment_date_1 = python_data.get('appointment_date_1')
            appointment_time_slot_1 = python_data.get('appointment_time_slot_1')
            appointment_date_2 = python_data.get('appointment_date_2')
            appointment_time_slot_2 = python_data.get('appointment_time_slot_2')
            home_sample_date_1 = python_data.get('home_sample_date_1')
            home_sample_time_slot_1 = python_data.get('home_sample_time_slot_1')
            home_sample_date_2 = python_data.get('home_sample_date_2')
            home_sample_time_slot_2 = python_data.get('home_sample_time_slot_2')
            confirm_appointment_date = python_data.get('confirm_appointment_date')
            confirm_appointment_time_slot = python_data.get('confirm_appointment_time_slot')
            confirm_home_sample_date = python_data.get('confirm_home_sample_date')
            confirm_home_sample_time_slot = python_data.get('confirm_home_sample_time_slot')
            date_of_appointment = python_data.get('date_of_appointment')
            time_slot = python_data.get('time_slot') or python_data.get('appointment_time') or python_data.get('slot') or python_data.get('time') or appointment_time_slot_1 or confirm_appointment_time_slot
            new_appointment_date = python_data.get('new_appointment_date') or confirm_appointment_date
            new_appointment_time_slot = python_data.get('new_appointment_time_slot') or confirm_appointment_time_slot
            new_home_sample_date = python_data.get('new_home_sample_date') or confirm_home_sample_date
            new_home_sample_time_slot = python_data.get('new_home_sample_time_slot') or confirm_home_sample_time_slot
            new_time_slot = python_data.get('new_time_slot') or time_slot or new_appointment_time_slot
            rescheduled_by = python_data.get('rescheduled_by', 'Staff')
            reason = python_data.get('reason')
            remark = python_data.get('remark') or python_data.get('remarks')
            status = python_data.get('status')
            report_date = python_data.get('report_date')

            now = datetime.now()
            current_date_data = now.strftime('%Y-%m-%d')
            current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()

            if package:
                package_obj = models.PackageDetail.objects.filter(id=package).first()
                if package_obj:
                    if not vendor and package_obj.vendor_id:
                        vendor = package_obj.vendor_id
                    if not type_of_visit and package_obj.type_of_visit_id:
                        type_of_visit = package_obj.type_of_visit_id

            reschedule_record = None

            if appointment_id:
                appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).first()
                if not appointment:
                    res = {'statuscode': 404, 'status': 'false', 'message': 'Appointment not found'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')

                old_appointment_date = appointment.confirm_appointment_date or appointment.appointment_date_1
                old_appointment_time_slot = appointment.confirm_appointment_time_slot or appointment.appointment_time_slot_1 or appointment.time_slot
                old_home_sample_date = appointment.confirm_home_sample_date or appointment.home_sample_date_1
                old_home_sample_time_slot = appointment.confirm_home_sample_time_slot or appointment.home_sample_time_slot_1
                old_time_slot = appointment.time_slot or old_appointment_time_slot

                if hoh_employee:
                    appointment.hoh_employee_id = hoh_employee
                if package:
                    appointment.package_id = package
                if center:
                    appointment.center_id = center
                if vendor:
                    appointment.vendor_id = vendor
                if type_of_visit:
                    appointment.type_of_visit_id = type_of_visit
                if appointment_date_1 is not None:
                    appointment.appointment_date_1 = appointment_date_1
                if appointment_time_slot_1 is not None:
                    appointment.appointment_time_slot_1 = appointment_time_slot_1
                if appointment_date_2 is not None:
                    appointment.appointment_date_2 = appointment_date_2
                if appointment_time_slot_2 is not None:
                    appointment.appointment_time_slot_2 = appointment_time_slot_2
                if home_sample_date_1 is not None:
                    appointment.home_sample_date_1 = home_sample_date_1
                if home_sample_time_slot_1 is not None:
                    appointment.home_sample_time_slot_1 = home_sample_time_slot_1
                if home_sample_date_2 is not None:
                    appointment.home_sample_date_2 = home_sample_date_2
                if home_sample_time_slot_2 is not None:
                    appointment.home_sample_time_slot_2 = home_sample_time_slot_2
                if confirm_appointment_date is not None:
                    appointment.confirm_appointment_date = confirm_appointment_date
                if confirm_appointment_time_slot is not None:
                    appointment.confirm_appointment_time_slot = confirm_appointment_time_slot
                if confirm_home_sample_date is not None:
                    appointment.confirm_home_sample_date = confirm_home_sample_date
                if confirm_home_sample_time_slot is not None:
                    appointment.confirm_home_sample_time_slot = confirm_home_sample_time_slot
                if date_of_appointment is not None:
                    appointment.date_of_appointment = date_of_appointment
                if time_slot is not None:
                    appointment.time_slot = time_slot
                if reason is not None:
                    appointment.reason = reason
                if remark is not None:
                    appointment.remark = remark
                if report_date is not None:
                    appointment.report_date = report_date

                if status == 'Rescheduled':
                    appointment.status = 'Rescheduled'
                    if new_appointment_date:
                        appointment.confirm_appointment_date = new_appointment_date
                    if new_appointment_time_slot:
                        appointment.confirm_appointment_time_slot = new_appointment_time_slot
                    if new_home_sample_date:
                        appointment.confirm_home_sample_date = new_home_sample_date
                    if new_home_sample_time_slot:
                        appointment.confirm_home_sample_time_slot = new_home_sample_time_slot
                    if new_time_slot:
                        appointment.time_slot = new_time_slot

                    reschedule_record = models.RescheduleDarwinboxCandidateAppointment.objects.create(
                        appointment=appointment,
                        hoh_employee=appointment.hoh_employee,
                        rescheduled_by=rescheduled_by,
                        old_appointment_date=old_appointment_date,
                        old_appointment_time_slot=old_appointment_time_slot,
                        new_appointment_date=appointment.confirm_appointment_date,
                        new_appointment_time_slot=appointment.confirm_appointment_time_slot,
                        old_home_sample_date=old_home_sample_date,
                        old_home_sample_time_slot=old_home_sample_time_slot,
                        new_home_sample_date=appointment.confirm_home_sample_date,
                        new_home_sample_time_slot=appointment.confirm_home_sample_time_slot,
                        old_time_slot=old_time_slot,
                        new_time_slot=appointment.time_slot,
                        time_slot=appointment.time_slot,
                        reason=reason,
                        remark=remark,
                        status='Rescheduled',
                        created_at=str(current_date)
                    )
                elif status:
                    appointment.status = status

                appointment.save()
                serializer = DarwinboxCandidateAppointmentSerializer(appointment)
                res_data = {
                    'statuscode': 200,
                    'status': 'true',
                    'message': 'Darwinbox candidate appointment updated successfully',
                    'data': serializer.data
                }
                if reschedule_record:
                    res_data['reschedule_record'] = RescheduleDarwinboxCandidateAppointmentSerializer(reschedule_record).data
                json_data = JSONRenderer().render(res_data)
                return HttpResponse(json_data, content_type='application/json')
            else:
                appointment = models.DarwinboxCandidateAppointment.objects.create(
                    hoh_employee_id=hoh_employee,
                    package_id=package,
                    center_id=center,
                    vendor_id=vendor,
                    type_of_visit_id=type_of_visit,
                    appointment_date_1=appointment_date_1,
                    appointment_time_slot_1=appointment_time_slot_1,
                    appointment_date_2=appointment_date_2,
                    appointment_time_slot_2=appointment_time_slot_2,
                    home_sample_date_1=home_sample_date_1,
                    home_sample_time_slot_1=home_sample_time_slot_1,
                    home_sample_date_2=home_sample_date_2,
                    home_sample_time_slot_2=home_sample_time_slot_2,
                    confirm_appointment_date=confirm_appointment_date,
                    confirm_appointment_time_slot=confirm_appointment_time_slot,
                    confirm_home_sample_date=confirm_home_sample_date,
                    confirm_home_sample_time_slot=confirm_home_sample_time_slot,
                    date_of_appointment=date_of_appointment,
                    time_slot=time_slot,
                    reason=reason,
                    remark=remark,
                    report_date=report_date,
                    status=status or 'Request Received',
                    created_at=str(current_date)
                )
                serializer = DarwinboxCandidateAppointmentSerializer(appointment)
                res = {
                    'statuscode': 200,
                    'status': 'true',
                    'message': 'Darwinbox candidate appointment created successfully',
                    'data': serializer.data
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
        except Exception as e:
            res = {'statuscode': 400, 'status': 'false', 'message': str(e)}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')