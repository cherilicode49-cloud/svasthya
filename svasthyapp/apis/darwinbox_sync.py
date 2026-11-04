import os
import io
import csv
import json
import requests
from datetime import datetime, date
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from svasthyapp import models
from svasthyapp.models import hoh_models

# ============================================================
# DARWINBOX ACCESS TOKEN
# ============================================================

def get_darwinbox_access_token(flag):

    if flag is True:
        payload = {
            "grant_type": "client_credentials",
            "client_id": settings.DARWINBOX_CLIENT_ID,
            "client_secret": settings.DARWINBOX_REPORT_CLIENT_SECRET,
        }

    else:
        payload = {
            "grant_type": "client_credentials",
            "client_id": settings.DARWINBOX_CLIENT_ID,
            "client_secret": settings.DARWINBOX_IMPORT_CLIENT_SECRET,
        }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        settings.DARWINBOX_TOKEN_URL,
        data=payload,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    token_data = response.json()

    access_token = token_data.get("access_token")

    if not access_token:
        raise KeyError("access_token")

    return access_token


# ============================================================
# DARWINBOX REPORT DATA + DATABASE IMPORT
# ============================================================

def fetch_and_process_darwinbox_report(report_id="4789d215e4aa8a", get_latest_report=1):
    """
    Fetches latest Darwinbox candidate report CSV, parses candidate rows,
    updates or creates HohEmployee records, and triggers HR notification
    email using pre_employment_new_registrations.html if new candidates are registered.
    """
    if not report_id:
        return {
            "status": False,
            "message": "report_id is required"
        }

    try:
        # Step 1: Get Darwinbox OAuth token
        access_token = get_darwinbox_access_token(flag=True)

        # Step 2: Prepare report payload
        payload = {
            "report_id": report_id,
            "get_latest_report": get_latest_report,
        }

        # Step 3: Prepare headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        if getattr(settings, "DARWINBOX_COOKIE", None):
            headers["Cookie"] = settings.DARWINBOX_COOKIE

        # Step 4: Get report information
        response = requests.post(
            settings.DARWINBOX_REPORT_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()

        # Step 5: Parse Darwinbox response
        try:
            response_data = response.json()
        except ValueError:
            return {
                "status": False,
                "message": "Invalid response received from Darwinbox",
                "raw_response": response.text,
            }

        # Step 6: Get download URL
        download_url = (
            response_data
            .get("response", {})
            .get("data_download_link")
        )

        if not download_url:
            return {
                "status": False,
                "message": "data_download_link not found",
                "darwinbox_response": response_data,
            }

        # Step 7: Download CSV from Darwinbox
        download_response = requests.get(
            download_url,
            timeout=60,
        )
        download_response.raise_for_status()

        # Step 8: Read CSV
        csv_content = download_response.content.decode("utf-8-sig")
        csv_file = io.StringIO(csv_content)
        reader = csv.DictReader(csv_file)
        rows = list(reader)

        # Step 9: Import into database
        created_count = 0
        updated_count = 0
        failed_count = 0
        errors = []

        with transaction.atomic():
            for row_number, row in enumerate(rows, start=2):
                try:
                    company = (row.get("Company") or "").strip()
                    employee_id = (row.get("Employee Id") or "").strip()
                    unique_user_id = (row.get("Unique User Id") or "").strip()
                    first_name = (row.get("First Name") or "").strip()
                    last_name = (row.get("Last Name") or "").strip()
                    gender = (row.get("Gender") or "").strip()
                    date_of_birth = (row.get("Date Of Birth") or "").strip()
                    date_of_joining = (row.get("Date Of Joining") or "").strip()
                    personal_email = (row.get("Personal Email Id") or row.get("Personal Email") or "").strip()
                    personal_mobile = (row.get("Personal Mobile Number") or row.get("Personal Mobile") or "").strip()
                    office_location = (row.get("Office Location") or "").strip()
                    member_address = (row.get("Current Address") or row.get("Member Address") or row.get("Address") or "").strip()
                    recruiter_name = (row.get("Recruiter") or row.get("Recruiter Name") or "").strip()
                    recruiter_mobile = (row.get("Recruiter Mobile Number") or row.get("Recruiter Mobile") or "").strip()
                    recruiter_email = (row.get("Recruiter Email Id") or row.get("Recruiter Email") or "").strip()

                    if not unique_user_id:
                        failed_count += 1
                        errors.append({
                            "row": row_number,
                            "error": "Unique User Id is missing",
                        })
                        continue

                    dob = None
                    doj = None

                    if date_of_birth:
                        for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
                            try:
                                dob = datetime.strptime(date_of_birth, fmt).date()
                                break
                            except Exception:
                                pass

                    if date_of_joining:
                        for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
                            try:
                                doj = datetime.strptime(date_of_joining, fmt).date()
                                break
                            except Exception:
                                pass

                    defaults_dict = {
                        "company": company,
                        "employee_id": employee_id or None,
                        "first_name": first_name,
                        "last_name": last_name,
                        "gender": gender,
                        "date_of_birth": dob,
                        "date_of_joining": doj,
                        "personal_email": personal_email,
                        "personal_mobile": personal_mobile,
                        "office_location": office_location,
                        "member_address": member_address or None,
                        "recruiter_name": recruiter_name or None,
                        "recruiter_mobile": recruiter_mobile or None,
                        "recruiter_email": recruiter_email or None,
                    }

                    employee, created = models.HohEmployee.objects.update_or_create(
                        unique_user_id=unique_user_id,
                        defaults=defaults_dict
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except Exception as row_error:
                    failed_count += 1
                    errors.append({
                        "row": row_number,
                        "error": str(row_error),
                    })

        # Trigger HR notification email if new candidates registered
        mail_sent_to_hr = False
        if created_count > 0:
            try:
                hr_emails = ['wellness@vakare.in']
                configured_emails = getattr(settings, 'DARWINBOX_HR_REPORT_EMAILS', None)
                if configured_emails:
                    if isinstance(configured_emails, list):
                        hr_emails.extend(configured_emails)
                    elif isinstance(configured_emails, str):
                        hr_emails.extend([x.strip() for x in configured_emails.split(',') if x.strip()])
                hr_emails = list(dict.fromkeys(hr_emails))

                context = {
                    "team_name": "Team",
                    "new_count": created_count,
                }
                htmlgen = get_template("pre_employment_new_registrations.html").render(context)
                # send_mail(
                #     "Pre-Employment New Registrations Received.",
                #     "Dear Team,\n\nThis is to inform you that new registrations received for the pre-employment health checkups.\n\nBest regards,\nSvasthya Team\nVakare Management Consultants LLP",
                #     getattr(settings, 'EMAIL_HOST_USER', 'wellness@vakare.in'),
                #     hr_emails,
                #     fail_silently=False,
                #     html_message=htmlgen
                # )
                # mail_sent_to_hr = True

                email = EmailMessage(
                    subject="Pre-Employment New Registrations Received.",
                    body=htmlgen,
                    from_email=getattr(
                        settings,
                        'EMAIL_HOST_USER',
                        'wellness@vakare.in'
                    ),
                    to=hr_emails,
                    cc=['wellness@vakare.in'],
                )

                email.content_subtype = "html"
                email.send(fail_silently=False)

                mail_sent_to_hr = True
            except Exception as mail_err:
                print("Error sending new registrations email to HR:", str(mail_err))

        return {
            "status": True,
            "message": "Darwinbox report fetched and processed successfully",
            "download_url": download_url,
            "report": {
                "report_id": report_id,
                "report_name": response_data.get("response", {}).get("summary", {}).get("report_name"),
                "data_count": response_data.get("response", {}).get("summary", {}).get("data_count"),
            },
            "import": {
                "total_records": len(rows),
                "created": created_count,
                "updated": updated_count,
                "failed": failed_count,
                "mail_sent_to_hr": mail_sent_to_hr,
            },
            "errors": errors,
        }

    except requests.exceptions.Timeout:
        return {
            "status": False,
            "message": "Darwinbox API request timed out"
        }
    except requests.exceptions.HTTPError as e:
        return {
            "status": False,
            "message": "Darwinbox API authentication/request failed",
            "error": str(e)
        }
    except KeyError:
        return {
            "status": False,
            "message": "Access token was not returned by Darwinbox"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": False,
            "message": "Unable to connect to Darwinbox",
            "error": str(e)
        }
    except Exception as e:
        return {
            "status": False,
            "message": "Something went wrong",
            "error": str(e)
        }


@csrf_exempt
def darwinbox_report_data(request):
    try:
        python_data = JSONParser().parse(io.BytesIO(request.body))
    except Exception:
        python_data = {}

    report_id = python_data.get("report_id") or "4789d215e4aa8a"
    get_latest_report = python_data.get("get_latest_report", 1)

    res = fetch_and_process_darwinbox_report(report_id=report_id, get_latest_report=get_latest_report)
    json_data = JSONRenderer().render(res)
    return HttpResponse(json_data, content_type='application/json') 
    
# ============================================================
# DARWINBOX IMPORT DATA
# ============================================================

@csrf_exempt
def darwinbox_import_data(request):
    python_data = JSONParser().parse(io.BytesIO(request.body))
    import_id = python_data.get("import_id")
    group_company = python_data.get("group_company")
    import_data = python_data.get("import_data")


    # --------------------------------------------------------
    # Validate import_id
    # --------------------------------------------------------

    if not import_id:
        res = {
                "status": False,
                "message": "import_id is required",
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

    # --------------------------------------------------------
    # Validate group_company
    # --------------------------------------------------------

    if not group_company:
        res = {
                "status": False,
                "message": "group_company is required",
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

    # --------------------------------------------------------
    # Validate import_data
    # --------------------------------------------------------

    if not isinstance(import_data, list):
        res = {
                "status": False,
                "message": "import_data must be a list",
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

    try:

        # ----------------------------------------------------
        # Step 1: Get OAuth access token
        # ----------------------------------------------------

        access_token = get_darwinbox_access_token(flag=False)

        # ----------------------------------------------------
        # Step 2: Prepare payload
        # ----------------------------------------------------

        payload = {
            "api_key": settings.DARWINBOX_IMPORT_API_KEY,
            "import_id": import_id,
            "group_company": group_company,
            "import_data": import_data,
        }

        # ----------------------------------------------------
        # Step 3: Prepare headers
        # ----------------------------------------------------

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # Add Cookie only if configured
        if getattr(settings, "DARWINBOX_COOKIE", None):
            headers["Cookie"] = settings.DARWINBOX_COOKIE

        # ----------------------------------------------------
        # Step 4: Call Darwinbox Import API
        # ----------------------------------------------------

        response = requests.post(
            settings.DARWINBOX_IMPORT_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )

        # ----------------------------------------------------
        # Step 5: Parse response
        # ----------------------------------------------------

        try:
            response_data = response.json()

        except ValueError:
            response_data = {
                "raw_response": response.text
            }

        print(
            "Darwinbox Import Status:",
            response.status_code
        )

        print(
            "Darwinbox Import Response:",
            response_data
        )

        # ----------------------------------------------------
        # Return Darwinbox response
        # ----------------------------------------------------

        # return Response(
        #     response_data,
        #     status=response.status_code,
        # )
        json_data = JSONRenderer().render(response_data)
        return HttpResponse(json_data, content_type= 'application/json') 

    except requests.exceptions.Timeout:

        res = {
                "status": False,
                "message": "Darwinbox API request timed out",
            }
        json_data = JSONRenderer().render(response_data)
        return HttpResponse(json_data, content_type= 'application/json') 

    except requests.exceptions.HTTPError as e:

        res = {
                "status": False,
                "message": "Darwinbox authentication/request failed",
                "error": str(e),
            }
        json_data = JSONRenderer().render(response_data)
        return HttpResponse(json_data, content_type= 'application/json') 

    except KeyError:

        res = {
                "status": False,
                "message": "Access token was not returned by Darwinbox",
            }
        json_data = JSONRenderer().render(response_data)
        return HttpResponse(json_data, content_type= 'application/json') 

    except requests.exceptions.RequestException as e:

        res = {
                "status": False,
                "message": "Unable to connect to Darwinbox",
                "error": str(e),
            }
        json_data = JSONRenderer().render(response_data)
        return HttpResponse(json_data, content_type= 'application/json') 

    except Exception as e:

        res = {
                "status": False,
                "message": "Something went wrong",
                "error": str(e),
            }
        json_data = JSONRenderer().render(response_data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt

# ============================================================
# DARWINBOX PRE-EMPLOYMENT HEALTH REPORT API SYNC HELPER
# ============================================================

def upload_darwinbox_candidate_report_to_api(appointments_list, group_company=None, fitness_status=None):
    """
    Submits candidate Pre-Employment Health Checkup status to Darwinbox Import API.
    Endpoint: https://hoh.darwinbox.in/darwinbox/import-data/
    Auth: OAuth Bearer Token in headers & api_key in payload
    Allowed Fitness Status values for 'a6aa003de51453':
      - 'Process Initiated'
      - 'Fit'
      - 'Fit with Recommendation'
      - 'Temporarily Unfit'
    Payload:
      - api_key: settings.DARWINBOX_IMPORT_API_KEY
      - import_id: 'employeesdata' (fixed)
      - group_company: Dynamic (from request / candidate hoh_employee.company / default 'Roma Builders Private Limited')
      - import_data: [{'user_id': '<candidate_id>', 'a6aa003de51453': '<fitness_status>'}]
    """
    darwinbox_url = getattr(settings, 'DARWINBOX_IMPORT_URL', 'https://hoh.darwinbox.in/darwinbox/import-data/')
    api_key = getattr(settings, 'DARWINBOX_IMPORT_API_KEY', getattr(settings, 'DARWINBOX_API_KEY', os.environ.get('DARWINBOX_IMPORT_API_KEY', os.environ.get('DARWINBOX_API_KEY', ''))))

    if not isinstance(appointments_list, (list, tuple)):
        appointments_list = [appointments_list]

    FITNESS_STATUS_MAP = {
        'process initiated': 'Process Initiated',
        'process_initiated': 'Process Initiated',
        'fit': 'Fit',
        'fits': 'Fit',
        'fit with recommendation': 'Fit with Recommendation',
        'fit with recommendations': 'Fit with Recommendation',
        'fit_with_recommendation': 'Fit with Recommendation',
        'fit_with_recommendations': 'Fit with Recommendation',
        'temporarily unfit': 'Temporarily Unfit',
        'temporary unfit': 'Temporarily Unfit',
        'temporarily_unfit': 'Temporarily Unfit',
        'unfit': 'Temporarily Unfit',
    }

    def resolve_fitness_value(val):
        if not val:
            return 'Fit'
        val_clean = str(val).strip()
        return FITNESS_STATUS_MAP.get(val_clean.lower(), val_clean)

    company_buckets = {}
    total_candidate_ids = []

    for appt in appointments_list:
        if not appt:
            continue

        user_id = None
        candidate_company = group_company
        candidate_fitness = fitness_status

        if isinstance(appt, models.DarwinboxCandidateAppointment):
            hoh_emp = appt.hoh_employee
            if hoh_emp:
                user_id = hoh_emp.unique_user_id or hoh_emp.employee_id or str(hoh_emp.id)
                if not candidate_company and hoh_emp.company:
                    candidate_company = hoh_emp.company
            else:
                user_id = str(appt.id)

        elif isinstance(appt, dict):
            user_id = appt.get('user_id') or appt.get('unique_user_id') or appt.get('employee_id')
            if not candidate_company:
                candidate_company = appt.get('group_company') or appt.get('company')
            if not candidate_fitness:
                candidate_fitness = appt.get('fitness_status') or appt.get('fitness') or appt.get('a6aa003de51453')
        elif isinstance(appt, (int, str)):
            user_id = str(appt)

        if not candidate_company:
            candidate_company = 'Roma Builders Private Limited'

        resolved_fitness = resolve_fitness_value(candidate_fitness)

        if user_id:
            user_id = str(user_id).strip()
            if candidate_company not in company_buckets:
                company_buckets[candidate_company] = []
            company_buckets[candidate_company].append({
                "user_id": user_id,
                "a6aa003de51453": resolved_fitness
            })
            total_candidate_ids.append(user_id)

    if not total_candidate_ids:
        return {
            'status': False,
            'message': 'No valid candidate user IDs found to sync with Darwinbox.',
            'darwinbox_response': None,
            'synced_candidates_count': 0
        }

    try:
        access_token = get_darwinbox_access_token(flag=False)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        if getattr(settings, 'DARWINBOX_COOKIE', None):
            headers['Cookie'] = settings.DARWINBOX_COOKIE

        all_responses = []
        overall_success = True

        for comp, items in company_buckets.items():
            payload = {
                "api_key": api_key,
                "import_id": "employeesdata",
                "group_company": comp,
                "import_data": items,
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
                response_data = {
                    'raw_response': response.text
                }

            print(f'Darwinbox Candidate Status Sync ({comp}) Status:', response.status_code)
            print(f'Darwinbox Candidate Status Sync ({comp}) Response:', response_data)

            is_item_success = response.status_code in [200, 201] and (
                isinstance(response_data, dict) and response_data.get('status') in [1, '1', True, 'true', 200]
            )
            if not is_item_success:
                overall_success = False

            all_responses.append({
                "group_company": comp,
                "status_code": response.status_code,
                "response": response_data,
                "count": len(items)
            })

        main_resp = all_responses[0]["response"] if len(all_responses) == 1 else all_responses
        err_msg = None
        if not overall_success:
            if isinstance(main_resp, dict) and main_resp.get('message'):
                err_msg = main_resp.get('message')
            elif isinstance(main_resp, list):
                err_msgs = [r.get('response', {}).get('message') for r in main_resp if isinstance(r, dict) and r.get('response', {}).get('status') in [0, '0', False, 'false']]
                err_msg = ', '.join([m for m in err_msgs if m]) or 'Darwinbox sync failed.'
            else:
                err_msg = 'Darwinbox sync failed.'

        return {
            'status': overall_success,
            'status_code': 200 if overall_success else 400,
            'message': err_msg or ('Data loaded.' if overall_success else 'Darwinbox sync failed.'),
            'darwinbox_response': main_resp,
            'synced_candidates_count': len(total_candidate_ids) if overall_success else 0,
            'candidate_user_ids': total_candidate_ids,
            'group_company': list(company_buckets.keys())[0] if len(company_buckets) == 1 else list(company_buckets.keys()),
        }

    except requests.exceptions.Timeout:
        return {
            'status': False,
            'message': 'Darwinbox API request timed out',
            'darwinbox_response': None
        }
    except requests.exceptions.RequestException as e:
        return {
            'status': False,
            'message': f'Darwinbox API request failed: {str(e)}',
            'darwinbox_response': None
        }
    except Exception as e:
        return {
            'status': False,
            'message': f'Something went wrong during Darwinbox candidate sync: {str(e)}',
            'darwinbox_response': None
        }
