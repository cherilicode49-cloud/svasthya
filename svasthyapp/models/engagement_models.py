from django.db import models
from svasthyapp import validators
from svasthyapp.models.masters_models import TypeOfVisit
from svasthyapp.models.center_models import CenterDetail
from svasthyapp.models.package_models import PackageDetail
from svasthyapp.models.employee_models import EmployeeDetail
from svasthyapp.models.individual_models import IndividualUserDetail

class HealthTips(models.Model):
    title = models.CharField(max_length=200, verbose_name="title",  null=True )
    start_date = models.CharField(max_length=200, verbose_name="start_date",  null=True )
    end_date = models.CharField(max_length=200, verbose_name="end_date",  null=True)
    redirection_url = models.CharField(max_length=200, verbose_name="redirection_url",  null=True )
    media = models.FileField(upload_to='image/health_tips', verbose_name='media', null=True, blank=True,
                             validators=[validators.validate_file_extension_image]) 
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % self.id


class NotificationDetail(models.Model):
    title = models.CharField(max_length=200, verbose_name="title",  null=True)
    notification_type = models.CharField(max_length=200, verbose_name="notification_type",  null=True)
    preferred_appointment_date1 = models.CharField(max_length=200, verbose_name="preferred_date",  null=True)
    preferred_appointment_date2 = models.CharField(max_length=200, verbose_name="preferred_date",  null=True)
    user_type = models.CharField(max_length=200, verbose_name="user_type",  null=True)
    individual = models.ForeignKey(IndividualUserDetail, verbose_name="individual", null=True, on_delete=models.CASCADE, default=None, blank=True)
    employee = models.ForeignKey(EmployeeDetail, verbose_name="employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    center = models.ForeignKey(CenterDetail, verbose_name="center", null=True, on_delete=models.CASCADE, default=None, blank=True)
    package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    type_of_visit = models.ForeignKey(TypeOfVisit, verbose_name="type_of_visit", null=True, on_delete=models.CASCADE, default=None, blank=True)
    appointment_date = models.CharField(max_length=200, verbose_name="appointment_date",  null=True )
    appointment_time = models.CharField(max_length=200, verbose_name="appointment_time",  null=True )
    recipient_name = models.CharField(max_length=200, verbose_name="recipient_name",  null=True )
    location = models.CharField(max_length=200, verbose_name="location",  null=True )
    user_read = models.CharField(max_length=200, verbose_name="user_read", null=True )    
    created_date = models.CharField(max_length=200, verbose_name="created_date", null=True )    
    created_time = models.CharField(max_length=200, verbose_name="created_time", null=True )    

    def __str__(self):
        return "%s" % self.id


