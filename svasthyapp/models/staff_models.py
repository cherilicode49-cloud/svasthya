from django.db import models
from svasthyapp import validators
from svasthyapp.models.masters_models import (
    StaffDepartment,
    TypeOfAccess,
    StaffLevel,
    StaffType,
)

class StaffDetail(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name",  null=True )
    staff_code = models.CharField(max_length=200, verbose_name="Staff Code",  null=True )
    type_of_access = models.ForeignKey(TypeOfAccess, verbose_name="type_of_access", null=True, on_delete=models.CASCADE, default=None, blank=True)
    staff_type = models.ForeignKey(StaffType, verbose_name="staff_type", null=True, on_delete=models.CASCADE, default=None, blank=True)
    staff_level = models.ForeignKey(StaffLevel, verbose_name="staff_level", null=True, on_delete=models.CASCADE, default=None, blank=True)
    department = models.ForeignKey(StaffDepartment, verbose_name="department", null=True, on_delete=models.CASCADE, default=None, blank=True)
    mobile = models.CharField(max_length=200, verbose_name="mobile", null=True)    
    staff_access = models.CharField(max_length=200, verbose_name="staff_access", null=True)    
    email = models.CharField(max_length=200, verbose_name="email", null=True)    
    OTP = models.CharField(max_length=200, verbose_name="OTP", null=True )    
    assign_to = models.CharField(max_length=200, verbose_name="assign_to", null=True )    
    profile_image = models.FileField(upload_to='image/staff/profile', verbose_name='profile_image', null=True, blank=True,validators=[validators.validate_file_extension_image])  

    status = models.CharField(max_length=200, verbose_name="Status", null=True )    
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
    
    def __str__(self):
        return "%s" % self.email


class NewStaffDetailsRequestData(models.Model):
    staff = models.ForeignKey(StaffDetail, verbose_name="staff", null=True, on_delete=models.CASCADE, default=None, blank=True)
    name = models.CharField(max_length=200, verbose_name="name",  null=True )
    email = models.CharField(max_length=200, verbose_name="email",  null=True )
    mobile = models.CharField(max_length=200, verbose_name="mobile",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
    def __str__(self):
        return "%s" % self.id


class StaffLoginHistory(models.Model):
    email = models.CharField(max_length=200, verbose_name="User Email",  null=True, default="null")
    staff = models.ForeignKey(StaffDetail, verbose_name="Staff", null=True, on_delete=models.CASCADE, default=None, blank=True)
    time = models.CharField(max_length=200, verbose_name="login time",  null=True, default="null")
    
    def __str__(self):
        return "%s" % self.id


