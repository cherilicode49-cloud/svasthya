from django.db import models
from svasthyapp import validators
from svasthyapp.models.masters_models import Gender, Relation

class IndividualUserDetail(models.Model):
    first_name = models.CharField(max_length=200, verbose_name="first_name",  null=True )
    last_name = models.CharField(max_length=200, verbose_name="last_name",  null=True )
    name = models.CharField(max_length=200, verbose_name="name",  null=True )
    individual_code = models.CharField(max_length=200, verbose_name="individual_code",  null=True )
    date_of_birth = models.CharField(max_length=200, verbose_name="date_of_birth",  null=True )
    gender = models.ForeignKey(Gender, verbose_name="gender", null=True, on_delete=models.CASCADE, default=None, blank=True)
    mobile = models.CharField(max_length=200, verbose_name="mobile",  null=True )
    email = models.CharField(max_length=200, verbose_name="email",  null=True )
    address = models.CharField(max_length=200, verbose_name="address",  null=True )
    pincode = models.CharField(max_length=200, verbose_name="pincode",  null=True )
    state = models.CharField(max_length=200, verbose_name="state",  null=True )
    city = models.CharField(max_length=200, verbose_name="city",  null=True ) 
    OTP = models.CharField(max_length=200, verbose_name="OTP", null=True, default="null")   
    profile_image = models.FileField(upload_to='image/individual/profile', verbose_name='profile_image', null=True, blank=True,validators=[validators.validate_file_extension_image])  
    status = models.CharField(max_length=200, verbose_name="status", null=True )    
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
    def __str__(self):
        return "%s" % self.id


class IndividualAddressDetail(models.Model):
    individual = models.ForeignKey(IndividualUserDetail, verbose_name="individual", null=True, on_delete=models.CASCADE, default=None, blank=True)
    address_type = models.CharField(max_length=200, verbose_name="address_type",  null=True )
    address = models.CharField(max_length=200, verbose_name="address",  null=True )
    state = models.CharField(max_length=200, verbose_name="state",  null=True )
    pincode = models.CharField(max_length=200, verbose_name="pincode",  null=True )
    city = models.CharField(max_length=200, verbose_name="city",  null=True ) 
    latitude = models.CharField(max_length=200, verbose_name="latitude",  null=True )
    longitude = models.CharField(max_length=200, verbose_name="longitude",  null=True )
    is_selected = models.BooleanField(default=True)
    mobile = models.CharField(max_length=200, verbose_name="mobile",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
    def __str__(self):
        return "%s" % self.id


class IndividualDependent(models.Model):
    individual = models.ForeignKey(IndividualUserDetail, verbose_name="Employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    dependent_name = models.CharField(max_length=200, verbose_name="dependent_name1",  null=True )
    dependent_relation = models.ForeignKey(Relation, verbose_name="corporate", null=True, on_delete=models.CASCADE, default=None, blank=True)
    date_of_birth = models.CharField(max_length=200, verbose_name="date_of_birth1",  null=True )
    gender = models.ForeignKey(Gender, verbose_name="gender1", null=True, on_delete=models.CASCADE, default=None, blank=True)
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
    def __str__(self):
        return "%s" % self.id


class IndividualLoginHistory(models.Model):
    mobile = models.CharField(max_length=200, verbose_name="User Email",  null=True, default="null")
    user = models.ForeignKey(IndividualUserDetail, verbose_name="Staff", null=True, on_delete=models.CASCADE, default=None, blank=True)
    time = models.CharField(max_length=200, verbose_name="login time",  null=True, default="null")
    
    def __str__(self):
        return "%s" % self.id


