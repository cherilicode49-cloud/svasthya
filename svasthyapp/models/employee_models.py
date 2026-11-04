from django.db import models
from svasthyapp import validators
from svasthyapp.models.masters_models import Gender, Relation
from svasthyapp.models.corporate_models import CorporateDetail

class EmployeeDetail(models.Model):
    corporate = models.ForeignKey(CorporateDetail, verbose_name="corporate", null=True, on_delete=models.CASCADE, default=None, blank=True)
    employee_name = models.CharField(max_length=200, verbose_name="employee_name",  null=True )
    employee_code = models.CharField(max_length=200, verbose_name="employee_code",  null=True )
    department = models.CharField(max_length=200, verbose_name="department",  null=True )
    date_of_join = models.CharField(max_length=200, verbose_name="date_of_join",  null=True )
    date_of_birth = models.CharField(max_length=200, verbose_name="date_of_birth",  null=True )
    gender = models.ForeignKey(Gender,related_name='employee_gender', verbose_name="gender", null=True, on_delete=models.CASCADE, default=None, blank=True)
    mobile = models.CharField(max_length=200, verbose_name="mobile",  null=True )
    email = models.CharField(max_length=200, verbose_name="email",  null=True )
    hr_employee = models.CharField(max_length=200, verbose_name="hr_employee",  null=True )
    hr_corporate_code = models.CharField(max_length=200, verbose_name="hr_corporate_code",  null=True )
    address = models.CharField(max_length=200, verbose_name="address",  null=True )
    pincode = models.CharField(max_length=200, verbose_name="pincode",  null=True )
    state = models.CharField(max_length=200, verbose_name="state",  null=True )
    city = models.CharField(max_length=200, verbose_name="city",  null=True ) 
    OTP = models.CharField(max_length=200, verbose_name="OTP", null=True, default="null")   
    employee_from = models.CharField(max_length=200, verbose_name="employee_from", null=True, default="null")   
    profile_image = models.FileField(upload_to='image/employee/profile', verbose_name='profile_image', null=True, blank=True,validators=[validators.validate_file_extension_image])  
    status = models.CharField(max_length=200, verbose_name="status", null=True )    
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
    def __str__(self):
        return "%s" % self.id + ' --> ' + self.employee_name


class EmployeeAddressDetail(models.Model):
    employee = models.ForeignKey(EmployeeDetail, verbose_name="employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    address_type = models.CharField(max_length=200, verbose_name="address_type",  null=True )
    address = models.CharField(max_length=200, verbose_name="address",  null=True )
    latitude = models.CharField(max_length=200, verbose_name="latitude",  null=True )
    longitude = models.CharField(max_length=200, verbose_name="longitude",  null=True )
    state = models.CharField(max_length=200, verbose_name="state",  null=True )
    pincode = models.CharField(max_length=200, verbose_name="pincode",  null=True )
    city = models.CharField(max_length=200, verbose_name="city",  null=True ) 
    is_selected = models.BooleanField(default=True)
    mobile = models.CharField(max_length=200, verbose_name="mobile",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
    def __str__(self):
        return "%s" % self.id


class EmployeeUpdateHistory(models.Model):
    employee = models.ForeignKey(EmployeeDetail, verbose_name="employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    employee_name = models.CharField(max_length=200, verbose_name="employee_name",  null=True )
    date_of_birth = models.CharField(max_length=200, verbose_name="date_of_birth",  null=True )
    gender = models.ForeignKey(Gender, verbose_name="gender", null=True, on_delete=models.CASCADE, default=None, blank=True)
    mobile = models.CharField(max_length=200, verbose_name="mobile",  null=True )
    email = models.CharField(max_length=200, verbose_name="email",  null=True )
    address = models.CharField(max_length=200, verbose_name="address",  null=True )
    pincode = models.CharField(max_length=200, verbose_name="pincode",  null=True )
    status = models.CharField(max_length=200, verbose_name="status", null=True )    
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
    def __str__(self):
        return "%s" % self.id


class EmployeeDependent(models.Model):
    employee = models.ForeignKey(EmployeeDetail, verbose_name="Employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    dependent_name = models.CharField(max_length=200, verbose_name="dependent_name1",  null=True )
    dependent_relation = models.ForeignKey(Relation, verbose_name="corporate", null=True, on_delete=models.CASCADE, default=None, blank=True)
    date_of_birth = models.CharField(max_length=200, verbose_name="date_of_birth1",  null=True )
    gender = models.ForeignKey(Gender, verbose_name="gender1", null=True, on_delete=models.CASCADE, default=None, blank=True)
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
    def __str__(self):
        return "%s" % self.id


class NewEmployeeDependentRequest(models.Model):
    employee = models.ForeignKey(EmployeeDetail, verbose_name="Employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    dependent_name = models.CharField(max_length=200, verbose_name="dependent_name1",  null=True )
    dependent_relation = models.ForeignKey(Relation, verbose_name="corporate", null=True, on_delete=models.CASCADE, default=None, blank=True)
    date_of_birth = models.CharField(max_length=200, verbose_name="date_of_birth1",  null=True )
    gender = models.ForeignKey(Gender, verbose_name="gender1", null=True, on_delete=models.CASCADE, default=None, blank=True)
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
    def __str__(self):
        return "%s" % self.id


class EmployeeLoginHistory(models.Model):
    email = models.CharField(max_length=200, verbose_name="User Email",  null=True, default="null")
    employee = models.ForeignKey(EmployeeDetail, verbose_name="Employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    time = models.CharField(max_length=200, verbose_name="login time",  null=True, default="null")
    
    def __str__(self):
        return "%s" % self.id


