from django.db import models
from svasthyapp import validators
from svasthyapp.models.corporate_models import CorporateDetail
from svasthyapp.models.package_models import PackageDetail
from svasthyapp.models.employee_models import EmployeeDetail, EmployeeDependent
from svasthyapp.models.individual_models import IndividualUserDetail, IndividualDependent
from svasthyapp.models.appointment_models import AppointmentDetail

class Transaction(models.Model):
    transaction_type = models.CharField(max_length=200, verbose_name="transaction_type",  null=True, default='Employee' )
    is_payment  = models.CharField(max_length=200, verbose_name="is_payment ",  null=True )
    booking_id = models.CharField(max_length=200, verbose_name="booking_id",  null=True)
    invoice_id = models.CharField(max_length=200, verbose_name="invoice_id",  null=True)
    method = models.CharField(max_length=200, verbose_name="method",  null=True)
    transaction_id = models.CharField(max_length=200, verbose_name="transaction_id",  null=True)
    appointment = models.ForeignKey(AppointmentDetail, verbose_name="AppointmentDetail", null=True, on_delete=models.CASCADE, default=None, blank=True)
    individual = models.ForeignKey(IndividualUserDetail, verbose_name="IndividualUserDetail", null=True, on_delete=models.CASCADE, default=None, blank=True)
    corporate = models.ForeignKey(CorporateDetail, verbose_name="corporate", null=True, on_delete=models.CASCADE, default=None, blank=True)
    employee = models.ForeignKey(EmployeeDetail, verbose_name="EmployeeDetail", null=True, on_delete=models.CASCADE, default=None, blank=True)
    package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    amount = models.CharField(max_length=100, verbose_name="amount", null=True, default=None )
    platform_charge = models.CharField(max_length=100, verbose_name="Plat Form Charge", null=True, default=None )
    total_amount = models.CharField(max_length=100, verbose_name="Total Amount", null=True, default=None )
    invoice = models.FileField(upload_to='image/Invoice', verbose_name='invoice', null=True, blank=True,validators=[validators.validate_file_extension_image_and_pdf])  
    individual_patient = models.ForeignKey(IndividualDependent, verbose_name="individual_patient", null=True, on_delete=models.CASCADE, default=None, blank=True)
    patient = models.ForeignKey(EmployeeDependent, verbose_name="Employee Dependent", null=True, on_delete=models.CASCADE, default=None, blank=True)
    reason = models.CharField(max_length=200, verbose_name="reason",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % self.id


class TransactionHistory(models.Model):
    transaction_type = models.CharField(max_length=200, verbose_name="transaction_type",  null=True, default='Employee' )
    user = models.CharField(max_length=100, verbose_name="user", null=True, default=None )
    corporate = models.CharField(max_length=100, verbose_name="corporate", null=True, default=None )
    package = models.CharField(max_length=100, verbose_name="package", null=True, default=None )
    amount = models.CharField(max_length=100, verbose_name="amount", null=True, default=None )
    invoice = models.FileField(upload_to='image/Invoice', verbose_name='invoice', null=True, blank=True,validators=[validators.validate_file_extension_image_and_pdf])  
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % self.id


class AddToCart(models.Model):
    user_type = models.CharField(max_length=200, verbose_name="user_type",  null=True)
    appointment = models.ForeignKey(AppointmentDetail, verbose_name="appointment", null=True, on_delete=models.CASCADE, default=None, blank=True)
    individual = models.ForeignKey(IndividualUserDetail, verbose_name="individual", null=True, on_delete=models.CASCADE, default=None, blank=True)
    individual_patient = models.ForeignKey(IndividualDependent, verbose_name="individual_patient", null=True, on_delete=models.CASCADE, default=None, blank=True)
    employee = models.ForeignKey(EmployeeDetail, verbose_name="employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    patient = models.ForeignKey(EmployeeDependent, verbose_name="Employee Dependent", null=True, on_delete=models.CASCADE, default=None, blank=True)
    package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    amount = models.CharField(max_length=100, verbose_name="amount", null=True, default=None )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
    
    def __str__(self):
        return "%s" % self.id


