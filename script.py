import schedule
import time
from datetime import datetime, timedelta
from svasthyapp import models




def active_inactive_health_tips():
    now = datetime.now()
    current_date_data = now.strftime('%Y-%m-%d')
    current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
    # print('Cheril')
    list_data = []
    all_health = models.HealthTips.objects.all().order_by('-id')
    for health in all_health:
        health_tips_id = models.HealthTips.objects.get(id = health.id)
        start_date = health_tips_id.start_date
        health_tips_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = health_tips_id.end_date
        health_tips_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        if current_date >= health_tips_start_date and current_date <= health_tips_end_date:
            health_tips_id.status = 'Active'
            health_tips_id.save()

        else:
            health_tips_id.status = 'Inactive'
            health_tips_id.save()


# schedule.every(10).seconds.do(active_inactive_health_tips)
schedule.every(30).minutes.do(active_inactive_health_tips)


def darwinbox_report_data_sync():
    now = datetime.now()
    current_time_str = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{current_time_str}] Running Darwinbox report data sync...")
    try:
        from svasthyapp.views import fetch_and_process_darwinbox_report
        result = fetch_and_process_darwinbox_report()
        import_info = result.get('import', {})
        created_count = import_info.get('created', 0)
        updated_count = import_info.get('updated', 0)
        failed_count = import_info.get('failed', 0)
        mail_sent = import_info.get('mail_sent_to_hr', False)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Darwinbox report sync completed: {result.get('message')}")
        print(f"Import summary -> New Registrations: {created_count}, Updated: {updated_count}, Failed: {failed_count}, Email sent to HR: {mail_sent}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error in Darwinbox report data sync: {str(e)}")


def send_tomorrow_candidate_appointment_reminders():
    now = datetime.now()
    tomorrow = now.date() + timedelta(days=1)
    tomorrow_iso = tomorrow.strftime('%Y-%m-%d')
    tomorrow_dmy = tomorrow.strftime('%d-%m-%Y')
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Checking tomorrow's ({tomorrow_dmy}) appointments for reminders...")

    try:
        from django.core.mail import send_mail
        from django.template.loader import get_template
        from django.conf import settings

        appointments = models.DarwinboxCandidateAppointment.objects.exclude(
            status__in=['Cancel', 'Cancelled', 'Reports Uploaded']
        )

        sent_count = 0
        for appointment in appointments:
            raw_date = (appointment.confirm_appointment_date or appointment.appointment_date_1 or appointment.date_of_appointment or '').strip()
            if not raw_date:
                continue

            is_tomorrow = False
            if raw_date in [tomorrow_iso, tomorrow_dmy]:
                is_tomorrow = True
            else:
                for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'):
                    try:
                        parsed_d = datetime.strptime(raw_date, fmt).date()
                        if parsed_d == tomorrow:
                            is_tomorrow = True
                            break
                    except Exception:
                        pass

            if is_tomorrow:
                emp_obj = appointment.hoh_employee
                recipient_email = emp_obj.personal_email if emp_obj else None
                if recipient_email and recipient_email != 'null' and recipient_email != '':
                    employee_name = f"{emp_obj.first_name or ''} {emp_obj.last_name or ''}".strip() or "Employee"
                    appointment_date = tomorrow_dmy
                    appointment_time = "08:00 AM to 11:00 AM"

                    center_name = appointment.center.center_name if appointment.center else 'Clinic'
                    center_address = appointment.center.address if appointment.center else ''

                    context = {
                        "employee_name": employee_name,
                        "appointment_date": appointment_date,
                        "appointment_time": appointment_time,
                        "center_name": center_name,
                        "center_address": center_address,
                    }

                    htmlgen = get_template("darwinbox_candidate_appointment_reminder.html").render(context)
                    send_mail(
                        "Reminder: Tomorrow’s Pre-Employment Health Check-up Appointment",
                        f"Dear {employee_name},\n\nThis is a friendly reminder about your tomorrow’s pre-employment health check-up appointment:\n\nDate: {appointment_date}\nTime: {appointment_time}\nLocation: {center_name} {center_address}\n\nPlease arrive 15 minutes early and bring any necessary documents (Government ID & voucher printout).\n\nFor any query feel free to contact us:\nSheetal Ambre – 9076103125\nEmail: wellness@vakare.in\n\nBest regards,\nSvasthya Team\nVakare Management Consultants LLP",
                        getattr(settings, 'EMAIL_HOST_USER', 'wellness@vakare.in'),
                        [recipient_email],
                        fail_silently=False,
                        html_message=htmlgen
                    )
                    sent_count += 1
                    print(f"Reminder email sent to {employee_name} ({recipient_email}) for appointment on {appointment_date}")

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Appointment reminder check completed. Total reminders sent: {sent_count}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error in sending tomorrow appointment reminders: {str(e)}")


def send_yesterday_candidate_appointment_completion_followup():
    now = datetime.now()
    yesterday = now.date() - timedelta(days=1)
    yesterday_iso = yesterday.strftime('%Y-%m-%d')
    yesterday_dmy = yesterday.strftime('%d-%m-%Y')
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Checking yesterday's ({yesterday_dmy}) appointments for completion follow-up...")

    try:
        from django.core.mail import send_mail
        from django.template.loader import get_template
        from django.conf import settings

        appointments = models.DarwinboxCandidateAppointment.objects.exclude(
            status__in=['Cancel', 'Cancelled']
        )

        sent_count = 0
        for appointment in appointments:
            raw_date = (appointment.confirm_appointment_date or appointment.appointment_date_1 or appointment.date_of_appointment or '').strip()
            if not raw_date:
                continue

            is_yesterday = False
            if raw_date in [yesterday_iso, yesterday_dmy]:
                is_yesterday = True
            else:
                for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'):
                    try:
                        parsed_d = datetime.strptime(raw_date, fmt).date()
                        if parsed_d == yesterday:
                            is_yesterday = True
                            break
                    except Exception:
                        pass

            if is_yesterday:
                emp_obj = appointment.hoh_employee
                recipient_email = emp_obj.personal_email if emp_obj else None
                if recipient_email and recipient_email != 'null' and recipient_email != '':
                    employee_name = f"{emp_obj.first_name or ''} {emp_obj.last_name or ''}".strip() or "Employee"
                    appointment_date = yesterday_dmy

                    context = {
                        "employee_name": employee_name,
                        "appointment_date": appointment_date,
                    }

                    htmlgen = get_template("darwinbox_candidate_appointment_completion_confirmation.html").render(context)
                    send_mail(
                        "Confirm Your Health Checkup Appointment Completion",
                        f"Dear {employee_name},\n\nWe hope you are doing well.\n\nAs per our records, your Pre-Employment Health Checkup appointment was scheduled on {appointment_date}.\n\nWe kindly request you to confirm the status of your appointment:\n• If you have completed the health checkup: Please confirm the completion and share your feedback regarding your experience.\n• If you have not completed the health checkup: Kindly share your preferred reschedule date so that we can assist you in arranging a new appointment.\n\nYour prompt response will help us ensure that your pre-employment health checkup is completed smoothly and without any delay.\n\nPlease feel free to reach out to us at Sheetal - 9076103125 if you require any assistance.\n\nThank you for your cooperation.\n\nBest regards,\nSvasthya Team\nVakare Management Consultants LLP",
                        getattr(settings, 'EMAIL_HOST_USER', 'wellness@vakare.in'),
                        [recipient_email],
                        fail_silently=False,
                        html_message=htmlgen
                    )
                    sent_count += 1
                    print(f"Appointment completion follow-up email sent to {employee_name} ({recipient_email}) for appointment date {appointment_date}")

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Appointment completion follow-up check completed. Total emails sent: {sent_count}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error in sending appointment completion follow-up emails: {str(e)}")


schedule.every(48).hours.do(darwinbox_report_data_sync)
schedule.every().day.at("10:00").do(send_tomorrow_candidate_appointment_reminders)
schedule.every().day.at("10:00").do(send_yesterday_candidate_appointment_completion_followup)


while True:
    schedule.run_pending()
    time.sleep(1)




