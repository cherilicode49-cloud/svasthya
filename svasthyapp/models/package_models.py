from django.db import models
from django.template.defaultfilters import slugify
from svasthyapp.models.masters_models import (
    TypeOfService,
    TypeOfVisit,
    AgeCategory,
    Gender,
    BillingCycle,
    PaymentTags,
    Relation,
    TestCategory,
    TestSubCategory,
)
from svasthyapp.models.corporate_models import CorporateDetail
from svasthyapp.models.vendor_models import VendorDetail

class PackageDetail(models.Model):
    package_type = models.CharField(max_length=200, verbose_name="package_type", null=True, default = 'Corporate' )
    package_name = models.CharField(max_length=200, verbose_name="package_name",  null=True )
    package_code = models.CharField(max_length=200, verbose_name="package_code",  null=True )
    vendor = models.ForeignKey(VendorDetail, verbose_name="Vendor", null=True, on_delete=models.CASCADE, default=None, blank=True)
    
    MRP = models.CharField(max_length=200, verbose_name="MRP",  null=True )
    base_amount = models.CharField(max_length=200, verbose_name="base_amount",  null=True )
    profit = models.CharField(max_length=200, verbose_name="profit",  null=True )
    tax = models.CharField(max_length=200, verbose_name="tax",  null=True )
    tax_amount = models.CharField(max_length=200, verbose_name="tax_amount",  null=True )
    igst = models.CharField(max_length=200, verbose_name="igst",  null=True )
    igst_amount = models.CharField(max_length=200, verbose_name="igst_amount",  null=True )
    sgst = models.CharField(max_length=200, verbose_name="sgst",  null=True )
    sgst_amount = models.CharField(max_length=200, verbose_name="sgst_amount",  null=True )
    cgst = models.CharField(max_length=200, verbose_name="cgst",  null=True )
    cgst_amount = models.CharField(max_length=200, verbose_name="cgst_amount",  null=True )
    discount_price = models.CharField(max_length=200, verbose_name="discount_price",  null=True )
    offer_price = models.CharField(max_length=200, verbose_name="offer_price",  null=True )
    
    total_test_number = models.CharField(max_length=200, verbose_name="total_test_number",  null=True )
    test_list = models.TextField(verbose_name="test_list",  null=True , blank=True)
 
    corporate_selection = models.CharField(max_length=200, verbose_name="corporate_selection",  null=True , blank=True)
    type_of_service = models.ForeignKey(TypeOfService, verbose_name="type_of_services", null=True, on_delete=models.CASCADE, default=None, blank=True)
    type_of_visit = models.ForeignKey(TypeOfVisit, verbose_name="type_of_visit", null=True, on_delete=models.CASCADE, default=None, blank=True)
    corporate = models.ManyToManyField(CorporateDetail, verbose_name="Corporate", blank=True)
    age_category = models.ForeignKey(AgeCategory, verbose_name="age_category", null=True, on_delete=models.CASCADE, default=None, blank=True)
    gender = models.ForeignKey(Gender,verbose_name="gender", null=True, on_delete=models.CASCADE, default=None, blank=True)
    start_date = models.CharField(max_length=200, verbose_name="start_date",  null=True )
    end_date = models.CharField(max_length=200, verbose_name="end_date",  null=True )
    billing_cycle = models.ForeignKey(BillingCycle, verbose_name="billing_cycle", null=True, on_delete=models.CASCADE, default=None, blank=True)
    tags = models.ForeignKey(PaymentTags, verbose_name="tags", null=True, on_delete=models.CASCADE, default=None, blank=True)
    description = models.TextField(verbose_name="description",  null=True )
    preparation_description = models.TextField(verbose_name="preparation",  null=True )
    detail_description = models.TextField(verbose_name="detail_description",  null=True , blank=True)
    relation_with_employee = models.ManyToManyField(Relation,verbose_name="Relation", blank= True)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % self.id + '--> ' + self.package_code
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = f"{slugify(self.package_name)}-{self.pk}"
            super().save(update_fields=["slug"])


class TestsProductDetail(models.Model):
    test_category = models.ForeignKey(TestCategory,verbose_name="TestCategory", null=True, on_delete=models.CASCADE, default=None, blank=True)
    test_subcategory = models.ForeignKey(TestSubCategory,verbose_name="TestSubCategory", null=True, on_delete=models.CASCADE, default=None, blank=True)
    package = models.ForeignKey(PackageDetail,verbose_name="PackageDetail", null=True, on_delete=models.CASCADE, default=None, blank=True)
    value = models.CharField(max_length=200, verbose_name="value",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % self.id


