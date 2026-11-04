from django.db import models
from svasthyapp import validators

class StaffDepartment(models.Model):
    staff_department = models.CharField(max_length=200, verbose_name="staff_department",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.staff_department


class TypeOfAccess(models.Model):
    type_of_access = models.CharField(max_length=200, verbose_name="type_of_access",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.type_of_access


class StaffLevel(models.Model):
    staff_level = models.CharField(max_length=200, verbose_name="staff_level",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.id


class StaffType(models.Model):
    staff_type = models.CharField(max_length=200, verbose_name="staff_type",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.staff_type


class AgeCategory(models.Model):
    age_category = models.CharField(max_length=200, verbose_name="age_category",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.age_category


class Gender(models.Model):
    gender = models.CharField(max_length=200, verbose_name="gender",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.gender


class Relation(models.Model):
    relation = models.CharField(max_length=200, verbose_name="relation",  null=True )
    gender = models.ManyToManyField(Gender,verbose_name="Gender", blank= True)
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.id + ' --> ' + self.relation


class TypeOfService(models.Model):
    type_of_service = models.CharField(max_length=200, verbose_name="type_of_service",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.id


class TypeOfVisit(models.Model):
    type_of_visit = models.CharField(max_length=200, verbose_name="type_of_visit",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.type_of_visit


class ParentCompany(models.Model):
    parent_company = models.CharField(max_length=200, verbose_name="parent_company",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.id


class BillingCycle(models.Model):
    billing_cycle = models.CharField(max_length=200, verbose_name="billing_cycle",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.id


class Weekdays(models.Model):
    weekdays = models.CharField(max_length=200, verbose_name="weekdays",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.id


class Holidays(models.Model):
    holidays = models.CharField(max_length=200, verbose_name="holidays",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.id


class PaymentTags(models.Model):
    payment_tags = models.CharField(max_length=200, verbose_name="payment_tags",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.payment_tags


class TypeOfIndustry(models.Model):
    type_of_industry = models.CharField(max_length=200, verbose_name="type_of_industry",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    def __str__(self):
        return "%s" % self.id


class TestCategory(models.Model):
    test_category = models.CharField(max_length=200, verbose_name="test_category",  null=True)
    status = models.CharField(max_length=200, verbose_name="status",  null=True)
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
    
    def __str__(self):
        return "%s" % str(self.id) + str(self.status)


class TestSubCategory(models.Model):
    test_category = models.ForeignKey(TestCategory, verbose_name="test_category", null=True, on_delete=models.CASCADE, default=None, blank=True)
    test_subcategory = models.CharField(max_length=200, verbose_name="test_subcategory",  null=True)
    status = models.CharField(max_length=200, verbose_name="status",  null=True)
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
    
    def __str__(self):
        return "%s" % str(self.id) + str(self.status)


