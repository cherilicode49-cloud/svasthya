from django.db import models
from svasthyapp.models.masters_models import TypeOfService
from svasthyapp.models.vendor_models import VendorDetail
from svasthyapp.models.package_models import PackageDetail

class CenterDetail(models.Model):
    center_name = models.CharField(max_length=200, verbose_name="center_name",  null=True )
    address = models.CharField(max_length=500, verbose_name="address",  null=True )
    pincode = models.CharField(max_length=200, verbose_name="pincode",  null=True )
    state = models.CharField(max_length=200, verbose_name="state",  null=True )
    city = models.CharField(max_length=200, verbose_name="city",  null=True ) 
    location = models.CharField(max_length=200, verbose_name="location",  null=True ) 
    vendor = models.ManyToManyField(VendorDetail,verbose_name="VendorDetail", blank= True)
    package = models.ManyToManyField(PackageDetail,verbose_name="PackageDetail", blank= True)
    type_of_service = models.ManyToManyField(TypeOfService,verbose_name="TypeOfService", blank= True)

    # vendor = models.ForeignKey(VendorDetail, verbose_name="Vendor", null=True, on_delete=models.CASCADE, default=None, blank=True)
    # package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    
    latitude = models.CharField(max_length=200, verbose_name="latitude",  null=True )
    longitude = models.CharField(max_length=200, verbose_name="longitude",  null=True )
    map_link = models.TextField(verbose_name="map_link",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % self.id


class HolidayDetail(models.Model):
    state_selection = models.CharField(max_length=200, verbose_name="state_selection",  null=True )
    state = models.CharField(max_length=200, verbose_name="state",  null=True )
    city_selection = models.CharField(max_length=200, verbose_name="city_selection",  null=True )
    city  = models.CharField(max_length=200, verbose_name="city",  null=True )
    center_selection = models.CharField(max_length=200, verbose_name="center_selection",  null=True )
    center = models.CharField(max_length=200, verbose_name="center",  null=True )
    holiday_name = models.CharField(max_length=200, verbose_name="holiday",  null=True )
    start_date = models.CharField(max_length=200, verbose_name="start_date",  null=True )
    end_date = models.CharField(max_length=200, verbose_name="end_date",  null=True )
    center = models.ManyToManyField(CenterDetail,verbose_name="Center", blank= True)
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % self.id


