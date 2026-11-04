from django.db import models
from svasthyapp.models.staff_models import StaffDetail

class AdminUser(models.Model):
    email = models.CharField(max_length=200, verbose_name="User Email",  null=True, default="null")
    mobile = models.CharField(max_length=200, verbose_name="Mobile",  null=True, default="null")
    firstName = models.CharField(max_length=200, verbose_name="First Name", null=True, default="null")
    lastName = models.CharField(max_length=200, verbose_name="Last Name", null=True, default="null")    
    OTP = models.CharField(max_length=200, verbose_name="OTP", null=True, default="null")    
    
    def __str__(self):
        return "%s" % self.id


class AdminUserLoginHistory(models.Model):
    email = models.CharField(max_length=200, verbose_name="User Email",  null=True, default="null")
    admin_user = models.ForeignKey(AdminUser, related_name="AdminUser_login", verbose_name="AdminUser", null=True, on_delete=models.CASCADE, default=None, blank=True)
    time = models.CharField(max_length=200, verbose_name="login time",  null=True, default="null")
    
    def __str__(self):
        return "%s" % self.id


class Module(models.Model):
    module = models.CharField(max_length=200, verbose_name="Module",  null=True, default="null")
    
    def __str__(self):
        return "%s" % self.module


class AdminModuleRights(models.Model):
    module = models.ForeignKey(Module, verbose_name="Module", null=True, on_delete=models.CASCADE, default=None, blank=True)
    staff = models.ForeignKey(StaffDetail, verbose_name="Staff", null=True, on_delete=models.CASCADE, default=None, blank=True)
    module_access = models.CharField(max_length=200, verbose_name="module_access",  null=True)
    edit_access = models.CharField(max_length=200, verbose_name="edit_access",  null=True)
    view_access = models.CharField(max_length=200, verbose_name="view_access",  null=True)
    delete_access = models.CharField(max_length=200, verbose_name="delete_access",  null=True)
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
    
    def __str__(self):
        return "%s" % self.id 


