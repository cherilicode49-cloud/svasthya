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


schedule.every(48).hours.do(darwinbox_report_data_sync)


while True:
    schedule.run_pending()
    time.sleep(1)



