from django.db import models
from svasthyapp import validators
from svasthyapp.models.masters_models import (
    TypeOfService,
    TypeOfVisit,
    BillingCycle,
)

class VendorDetail(models.Model):
    vendor_name = models.CharField(max_length=200, verbose_name="vendor_name",  null=True )
    vendor_code = models.CharField(max_length=200, verbose_name="vendor_code",  null=True )
    # type_of_service = models.ForeignKey(TypeOfService, verbose_name="type_of_service", null=True, on_delete=models.CASCADE, default=None, blank=True)
    type_of_service = models.ManyToManyField(TypeOfService, verbose_name="type_of_service", blank=True)
    type_of_visit = models.ForeignKey(TypeOfVisit, verbose_name="type_of_visit", null=True, on_delete=models.CASCADE, default=None, blank=True)
    billing_cycle = models.ForeignKey(BillingCycle, verbose_name="billing_cycle", null=True, on_delete=models.CASCADE, default=None, blank=True)
    GST_no = models.CharField(max_length=200, verbose_name="GST_no",  null=True )
    start_date = models.CharField(max_length=200, verbose_name="start_date",  null=True )
    end_date = models.CharField(max_length=200, verbose_name="end_date",  null=True )
    mobile = models.CharField(max_length=200, verbose_name="mobile",  null=True )
    email = models.CharField(max_length=200, verbose_name="email",  null=True )
    pincode = models.CharField(max_length=200, verbose_name="pincode",  null=True )
    address = models.CharField(max_length=200, verbose_name="address",  null=True )
    state = models.CharField(max_length=200, verbose_name="state",  null=True )
    city = models.CharField(max_length=200, verbose_name="city",  null=True )
    OTP = models.CharField(max_length=200, verbose_name="otp",  null=True )
    billing_email = models.CharField(max_length=200, verbose_name="billing_email",  null=True )
    login_via = models.CharField(max_length=200, verbose_name="login_via",  null=True )
    stakeholder_name = models.CharField(max_length=200, verbose_name="stakeholder_name",  null=True )
    stakeholder_mobile = models.CharField(max_length=200, verbose_name="stakeholder_mobile",  null=True )
    stakeholder_email = models.CharField(max_length=200, verbose_name="stakeholder_email",  null=True )
    contact_person1 = models.CharField(max_length=200, verbose_name="contact person1",  null=True )
    contact_person_designation1 = models.CharField(max_length=200, verbose_name="designation1",  null=True )
    contact_person_mobile1 = models.CharField(max_length=200, verbose_name="contact_person_mobile1",  null=True )
    contact_person_email1 = models.CharField(max_length=200, verbose_name="contact_person_email1",  null=True )
    contact_person2 = models.CharField(max_length=200, verbose_name="contact person2",  null=True )
    contact_person_designation2 = models.CharField(max_length=200, verbose_name="designation2",  null=True )
    contact_person_mobile2 = models.CharField(max_length=200, verbose_name="contact_person_mobile2",  null=True )
    contact_person_email2 = models.CharField(max_length=200, verbose_name="contact_person_email2",  null=True )
    contact_person3 = models.CharField(max_length=200, verbose_name="contact person3",  null=True )
    contact_person_designation3 = models.CharField(max_length=200, verbose_name="designation3",  null=True )
    contact_person_mobile3 = models.CharField(max_length=200, verbose_name="contact_person_mobile3",  null=True )
    contact_person_email3 = models.CharField(max_length=200, verbose_name="contact_person_email3",  null=True )
    profile_image = models.FileField(upload_to='image/vendor/profile', verbose_name='profile_image', null=True, blank=True,validators=[validators.validate_file_extension_image])  
    status = models.CharField(max_length=200, verbose_name="status", null=True )    
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
    def __str__(self):
        return "%s" % self.id + '-->' + self.vendor_code


class VendorLoginHistory(models.Model):
    email = models.CharField(max_length=200, verbose_name="User Email",  null=True, default="null")
    vendor = models.ForeignKey(VendorDetail, verbose_name="vendor", null=True, on_delete=models.CASCADE, default=None, blank=True)
    time = models.CharField(max_length=200, verbose_name="login time",  null=True, default="null")
    
    def __str__(self):
        return "%s" % self.id


