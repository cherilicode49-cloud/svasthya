from django.db import models
from svasthyapp import validators
from svasthyapp.models.vendor_models import VendorDetail
from svasthyapp.models.center_models import CenterDetail

class HohEmployee(models.Model):
    company = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=100, null=True, blank=True)
    unique_user_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    personal_email = models.EmailField(null=True, blank=True)
    personal_mobile = models.CharField(max_length=30, null=True, blank=True)
    office_location = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True, default='Blank', choices=(
        ('Blank', 'Blank'),
        ('Contacted', 'Contacted'),
        ('Person Not Approachable', 'Person Not Approachable'),
        ('Pending from Employee', 'Pending from Employee'),
    ))
    remark = models.TextField(null=True, blank=True)
    member_address = models.TextField(null=True, blank=True)
    recruiter_name = models.CharField(max_length=255, null=True, blank=True)
    recruiter_mobile = models.CharField(max_length=30, null=True, blank=True)
    recruiter_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.unique_user_id} - {self.first_name} {self.last_name}"


class DarwinboxCandidateAppointment(models.Model):
    hoh_employee = models.ForeignKey(HohEmployee, verbose_name="HOH Employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    # package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    package = models.TextField(verbose_name="package",  null=True , blank=True)
    center = models.ForeignKey(CenterDetail, verbose_name="Center", null=True, on_delete=models.CASCADE, default=None, blank=True)
    vendor = models.ForeignKey(VendorDetail, verbose_name="vendor", null=True, on_delete=models.CASCADE, default=None, blank=True)
    # type_of_visit = models.ForeignKey(TypeOfVisit, verbose_name="type_of_visit", null=True, on_delete=models.CASCADE, default=None, blank=True)
    type_of_visit = models.CharField(max_length=50, verbose_name="type_of_visit", null=True, default=None, blank=True)
    
    appointment_date_1 = models.CharField(max_length=200, verbose_name="appointment_date_1", null=True, blank=True)
    appointment_time_slot_1 = models.CharField(max_length=200, verbose_name="appointment_time_slot_1", null=True, blank=True)
    appointment_date_2 = models.CharField(max_length=200, verbose_name="appointment_date_2", null=True, blank=True)
    appointment_time_slot_2 = models.CharField(max_length=200, verbose_name="appointment_time_slot_2", null=True, blank=True)
    home_sample_date_1 = models.CharField(max_length=200, verbose_name="home_sample_date_1", null=True, blank=True)
    home_sample_time_slot_1 = models.CharField(max_length=200, verbose_name="home_sample_time_slot_1", null=True, blank=True)
    home_sample_date_2 = models.CharField(max_length=200, verbose_name="home_sample_date_2", null=True, blank=True)
    home_sample_time_slot_2 = models.CharField(max_length=200, verbose_name="home_sample_time_slot_2", null=True, blank=True)
    confirm_appointment_date = models.CharField(max_length=200, verbose_name="confirm_appointment_date", null=True, default=None, blank=True)
    confirm_appointment_time_slot = models.CharField(max_length=200, verbose_name="confirm_appointment_time_slot", null=True, default=None, blank=True)
    confirm_home_sample_date = models.CharField(max_length=200, verbose_name="confirm_home_sample_date", null=True, default=None, blank=True)
    confirm_home_sample_time_slot = models.CharField(max_length=200, verbose_name="confirm_home_sample_time_slot", null=True, default=None, blank=True)
    date_of_appointment = models.CharField(max_length=200, verbose_name="date_of_appointment", null=True, default=None, blank=True)
    time_slot = models.CharField(max_length=200, verbose_name="time_slot", null=True, default=None, blank=True)
    reason = models.CharField(max_length=500, verbose_name="reason", null=True, default=None, blank=True)
    remark = models.CharField(max_length=500, verbose_name="remark", null=True, default=None, blank=True)
    report_date = models.CharField(max_length=100, verbose_name="report_date", null=True, default=None, blank=True)
    report = models.FileField(upload_to='image/Report', verbose_name='report', null=True, blank=True, validators=[validators.validate_file_extension_image_and_pdf])
    status = models.CharField(max_length=200, verbose_name="status", null=True)
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True)

    def __str__(self):
        return "%s" % str(self.id) + '--candidate name--->' + str(self.hoh_employee)


class RescheduleDarwinboxCandidateAppointment(models.Model):
    appointment = models.ForeignKey(DarwinboxCandidateAppointment, verbose_name="appointment", null=True, on_delete=models.CASCADE, default=None, blank=True)
    hoh_employee = models.ForeignKey(HohEmployee, verbose_name="HOH Employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    rescheduled_by = models.CharField(max_length=200, verbose_name="rescheduled_by", null=True, blank=True)  # e.g. 'Candidate', 'Vendor', 'Staff'
    old_appointment_date = models.CharField(max_length=200, verbose_name="old_appointment_date", null=True, default=None, blank=True)
    old_appointment_time_slot = models.CharField(max_length=200, verbose_name="old_appointment_time_slot", null=True, default=None, blank=True)
    new_appointment_date = models.CharField(max_length=200, verbose_name="new_appointment_date", null=True, default=None, blank=True)
    new_appointment_time_slot = models.CharField(max_length=200, verbose_name="new_appointment_time_slot", null=True, default=None, blank=True)
    old_home_sample_date = models.CharField(max_length=200, verbose_name="old_home_sample_date", null=True, default=None, blank=True)
    old_home_sample_time_slot = models.CharField(max_length=200, verbose_name="old_home_sample_time_slot", null=True, default=None, blank=True)
    new_home_sample_date = models.CharField(max_length=200, verbose_name="new_home_sample_date", null=True, default=None, blank=True)
    new_home_sample_time_slot = models.CharField(max_length=200, verbose_name="new_home_sample_time_slot", null=True, default=None, blank=True)
    old_time_slot = models.CharField(max_length=200, verbose_name="old_time_slot", null=True, default=None, blank=True)
    new_time_slot = models.CharField(max_length=200, verbose_name="new_time_slot", null=True, default=None, blank=True)
    time_slot = models.CharField(max_length=200, verbose_name="time_slot", null=True, default=None, blank=True)
    reason = models.CharField(max_length=500, verbose_name="reason", null=True, default=None, blank=True)
    remark = models.CharField(max_length=500, verbose_name="remark", null=True, default=None, blank=True)
    status = models.CharField(max_length=200, verbose_name="status", null=True, default='Rescheduled')
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True)

    def __str__(self):
        return "%s" % str(self.id) + ' --> Darwinbox Appointment: ' + str(self.appointment_id)

