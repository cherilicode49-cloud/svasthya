from django.db import models
from svasthyapp.models.masters_models import (
    ParentCompany,
    TypeOfIndustry,
    BillingCycle,
)
from svasthyapp.models.staff_models import StaffDetail

class CorporateDetail(models.Model):
    # parent_company = models.CharField(max_length=200, verbose_name="parent_company",  null=True )
    parent_company = models.ForeignKey(ParentCompany, verbose_name="parent_company", null=True, on_delete=models.CASCADE, default=None, blank=True)
    corporate_code = models.CharField(max_length=200, verbose_name="corporate_code",  null=True )
    corporate_name = models.CharField(max_length=200, verbose_name="corporate_name",  null=True )
    type_of_corporation = models.CharField(max_length=200, verbose_name="type_of_corporation",  null=True )
    industry = models.ForeignKey(TypeOfIndustry, verbose_name="industry", null=True, on_delete=models.CASCADE, default=None, blank=True)
    spoke_person = models.CharField(max_length=200, verbose_name="spoke_person",  null=True )
    mobile = models.CharField(max_length=200, verbose_name="mobile",  null=True )
    email = models.CharField(max_length=200, verbose_name="email",  null=True )
    pan_card = models.CharField(max_length=200, verbose_name="pan_card",  null=True )
    GST_no = models.CharField(max_length=200, verbose_name="GST_no",  null=True )
    billing_cycle = models.ForeignKey(BillingCycle, verbose_name="billing_cycle", null=True, on_delete=models.CASCADE, default=None, blank=True)
    start_date = models.CharField(max_length=200, verbose_name="start_date",  null=True )
    end_date = models.CharField(max_length=200, verbose_name="end_date",  null=True )
    address = models.CharField(max_length=200, verbose_name="address",  null=True )
    pincode = models.CharField(max_length=200, verbose_name="pincode",  null=True )
    state = models.CharField(max_length=200, verbose_name="state",  null=True )
    city = models.CharField(max_length=200, verbose_name="city",  null=True )
    billing_email = models.CharField(max_length=200, verbose_name="billing_email",  null=True )
    # level1 = models.ForeignKey(StaffDetail, related_name= 'level1', verbose_name="Level 1", null=True, on_delete=models.CASCADE, default=None, blank=True)
    # level2 = models.ForeignKey(StaffDetail, related_name= 'level2', verbose_name="Level 2", null=True, on_delete=models.CASCADE, default=None, blank=True)
    level1 = models.ManyToManyField(StaffDetail,verbose_name="level1", related_name= 'level1',blank= True)
    level2 = models.ManyToManyField(StaffDetail,verbose_name="level2", related_name= 'level2',blank= True)
    
    status = models.CharField(max_length=200, verbose_name="status", null=True )    
    login_via = models.CharField(max_length=200, verbose_name="login_via", null=True , default='email')    
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
    def __str__(self):
        return "%s" % self.id + '--> ' +self.corporate_code


