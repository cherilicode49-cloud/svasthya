from django.db import models
from svasthyapp import validators
from svasthyapp.models.masters_models import TypeOfVisit
from svasthyapp.models.vendor_models import VendorDetail
from svasthyapp.models.center_models import CenterDetail
from svasthyapp.models.package_models import PackageDetail
from svasthyapp.models.employee_models import (
    EmployeeDetail,
    EmployeeAddressDetail,
    EmployeeDependent,
)
from svasthyapp.models.individual_models import (
    IndividualUserDetail,
    IndividualAddressDetail,
    IndividualDependent,
)

class AppointmentDetail(models.Model):
    appointment_type = models.CharField(max_length=200, verbose_name="appointment_type",  null=True, default='Employee' )
    individual = models.ForeignKey(IndividualUserDetail, verbose_name="IndividualUserDetail", null=True, on_delete=models.CASCADE, default=None, blank=True)
    individual_patient = models.ForeignKey(IndividualDependent, verbose_name="individual_patient", null=True, on_delete=models.CASCADE, default=None, blank=True)
    individual_address = models.ForeignKey(IndividualAddressDetail, verbose_name="individual_address", null=True, on_delete=models.CASCADE, default=None, blank=True)
    employee = models.ForeignKey(EmployeeDetail, verbose_name="Employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    patient = models.ForeignKey(EmployeeDependent, verbose_name="Employee Dependent", null=True, on_delete=models.CASCADE, default=None, blank=True)
    employee_address = models.ForeignKey(EmployeeAddressDetail, verbose_name="employee_address", null=True, on_delete=models.CASCADE, default=None, blank=True)
    package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    center = models.ForeignKey(CenterDetail, verbose_name="Center", null=True, on_delete=models.CASCADE, default=None, blank=True)
    vendor = models.ForeignKey(VendorDetail, verbose_name="vendor", null=True, on_delete=models.CASCADE, default=None, blank=True)
    type_of_visit = models.ForeignKey(TypeOfVisit, verbose_name="type_of_visit", null=True, on_delete=models.CASCADE, default=None, blank=True)
    appointment_date_1 = models.CharField(max_length=200, verbose_name="appointment_date_1",  null=True , blank=True)
    appointment_date_2 = models.CharField(max_length=200, verbose_name="appointment_date_2",  null=True , blank=True)
    home_sample_date_1 = models.CharField(max_length=200, verbose_name="home_sample_date_1",  null=True , blank=True)
    home_sample_date_2 = models.CharField(max_length=200, verbose_name="home_sample_date_2",  null=True , blank=True)
    confirm_appointment_date = models.CharField(max_length=200, verbose_name="confirm_appointment_date",  null=True , default=None, blank=True)
    confirm_home_sample_date = models.CharField(max_length=200, verbose_name="confirm_home_sample_date",  null=True , default=None, blank=True)
    date_of_appointment = models.CharField(max_length=200, verbose_name="date_of_appointment", null=True, default=None, blank=True)
    reason = models.CharField(max_length=500, verbose_name="reason", null=True, default=None , blank=True)
    remark = models.CharField(max_length=500, verbose_name="remark", null=True, default=None , blank=True)
    report_date = models.CharField(max_length=100, verbose_name="report_date", null=True, default=None , blank=True)
    report = models.FileField(upload_to='image/Report', verbose_name='report', null=True, blank=True,validators=[validators.validate_file_extension_image_and_pdf])  
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % str(self.id)+'--emplooyee name--->'+str(self.employee)


class RescheduleAppointment(models.Model):
    appointment = models.ForeignKey(AppointmentDetail, verbose_name="appointment", null=True, on_delete=models.CASCADE, default=None, blank=True)
    rescheduled_by = models.CharField(max_length=200, verbose_name="rescheduled_by", null=True, blank=True)  # e.g. 'Employee', 'Individual', 'Vendor', 'Staff'
    old_appointment_date = models.CharField(max_length=200, verbose_name="old_appointment_date", null=True, default=None, blank=True)
    new_appointment_date = models.CharField(max_length=200, verbose_name="new_appointment_date", null=True, default=None, blank=True)
    old_home_sample_date = models.CharField(max_length=200, verbose_name="old_home_sample_date", null=True, default=None, blank=True)
    new_home_sample_date = models.CharField(max_length=200, verbose_name="new_home_sample_date", null=True, default=None, blank=True)
    reason = models.CharField(max_length=500, verbose_name="reason", null=True, default=None, blank=True)
    remark = models.CharField(max_length=500, verbose_name="remark", null=True, default=None, blank=True)
    status = models.CharField(max_length=200, verbose_name="status", null=True, default='Rescheduled')
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True)

    def __str__(self):
        return "%s" % str(self.id) + ' --> Appointment: ' + str(self.appointment_id)


