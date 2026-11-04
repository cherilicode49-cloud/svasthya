from django.db import models
from svasthyapp import validators
from django.template.defaultfilters import slugify

# Create your models here.
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

# class Duration(models.Model):
#     duration = models.CharField(max_length=200, verbose_name="duration",  null=True )
#     status = models.CharField(max_length=200, verbose_name="status",  null=True )
    
#     def __str__(self):
#         return "%s" % self.id

# class Platform(models.Model):
#     platform = models.CharField(max_length=200, verbose_name="platform",  null=True )
#     status = models.CharField(max_length=200, verbose_name="status",  null=True )
    
#     def __str__(self):
#         return "%s" % self.id

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


# class CorporateDetail(models.Model):
#     # parent_company = models.CharField(max_length=200, verbose_name="parent_company",  null=True )
#     parent_company = models.ForeignKey(ParentCompany, verbose_name="parent_company", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     corporate_code = models.CharField(max_length=200, verbose_name="corporate_code",  null=True )
#     corporate_name = models.CharField(max_length=200, verbose_name="corporate_name",  null=True )
#     type_of_corporation = models.CharField(max_length=200, verbose_name="type_of_corporation",  null=True )
#     industry = models.CharField(max_length=200, verbose_name="industry",  null=True )
#     spoke_person = models.CharField(max_length=200, verbose_name="spoke_person",  null=True )
#     mobile = models.CharField(max_length=200, verbose_name="mobile",  null=True )
#     email = models.CharField(max_length=200, verbose_name="email",  null=True )
#     pan_card = models.CharField(max_length=200, verbose_name="pan_card",  null=True )
#     GST_no = models.CharField(max_length=200, verbose_name="GST_no",  null=True )
#     billing_cycle = models.ForeignKey(BillingCycle, verbose_name="billing_cycle", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     start_date = models.CharField(max_length=200, verbose_name="start_date",  null=True )
#     address = models.CharField(max_length=200, verbose_name="address",  null=True )
#     pincode = models.CharField(max_length=200, verbose_name="pincode",  null=True )
#     state = models.CharField(max_length=200, verbose_name="state",  null=True )
#     city = models.CharField(max_length=200, verbose_name="city",  null=True )
#     billing_email = models.CharField(max_length=200, verbose_name="billing_email",  null=True )
#     # level1 = models.ForeignKey(StaffDetail, related_name= 'level1', verbose_name="Level 1", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     # level2 = models.ForeignKey(StaffDetail, related_name= 'level2', verbose_name="Level 2", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     level1 = models.ManyToManyField(StaffDetail,verbose_name="level1", related_name= 'level1',blank= True)
#     level2 = models.ManyToManyField(StaffDetail,verbose_name="level2", related_name= 'level2',blank= True)
    
#     status = models.CharField(max_length=200, verbose_name="status", null=True )    
#     login_via = models.CharField(max_length=200, verbose_name="login_via", null=True , default='email')    
#     created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
#     def __str__(self):
#         return "%s" % self.id

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

# class PackageDetail(models.Model):
#     package_type = models.CharField(max_length=200, verbose_name="package_type", null=True, default = 'Corporate' )
#     package_name = models.CharField(max_length=200, verbose_name="package_name",  null=True )
#     package_code = models.CharField(max_length=200, verbose_name="package_code",  null=True )
#     MRP = models.CharField(max_length=200, verbose_name="MRP",  null=True )
#     discount_price = models.CharField(max_length=200, verbose_name="discount_price",  null=True )
#     corporate_selection = models.CharField(max_length=200, verbose_name="corporate_selection",  null=True )
#     offer_price = models.CharField(max_length=200, verbose_name="offer_price",  null=True )
#     type_of_service = models.ForeignKey(TypeOfService, verbose_name="type_of_services", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     type_of_visit = models.ForeignKey(TypeOfVisit, verbose_name="type_of_visit", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     # corporate = models.ForeignKey(CorporateDetail, related_name="corporate_details", verbose_name="Corporate", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     corporate = models.ManyToManyField(CorporateDetail, verbose_name="Corporate", blank=True)
#     age_category = models.ForeignKey(AgeCategory, verbose_name="age_category", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     gender = models.ForeignKey(Gender,verbose_name="gender", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     start_date = models.CharField(max_length=200, verbose_name="start_date",  null=True )
#     end_date = models.CharField(max_length=200, verbose_name="end_date",  null=True )
#     billing_cycle = models.ForeignKey(BillingCycle, verbose_name="billing_cycle", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     tags = models.ForeignKey(PaymentTags, verbose_name="tags", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     description = models.TextField(verbose_name="description",  null=True )
#     relation_with_employee = models.ManyToManyField(Relation,verbose_name="Relation", blank= True)
    
#     status = models.CharField(max_length=200, verbose_name="status",  null=True )
#     created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

#     def __str__(self):
#         return "%s" % self.id
    
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



class VendorLoginHistory(models.Model):
    email = models.CharField(max_length=200, verbose_name="User Email",  null=True, default="null")
    vendor = models.ForeignKey(VendorDetail, verbose_name="vendor", null=True, on_delete=models.CASCADE, default=None, blank=True)
    time = models.CharField(max_length=200, verbose_name="login time",  null=True, default="null")
    
    def __str__(self):
        return "%s" % self.id

class EmployeeLoginHistory(models.Model):
    email = models.CharField(max_length=200, verbose_name="User Email",  null=True, default="null")
    employee = models.ForeignKey(EmployeeDetail, verbose_name="Employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    time = models.CharField(max_length=200, verbose_name="login time",  null=True, default="null")
    
    def __str__(self):
        return "%s" % self.id



class StaffLoginHistory(models.Model):
    email = models.CharField(max_length=200, verbose_name="User Email",  null=True, default="null")
    staff = models.ForeignKey(StaffDetail, verbose_name="Staff", null=True, on_delete=models.CASCADE, default=None, blank=True)
    time = models.CharField(max_length=200, verbose_name="login time",  null=True, default="null")
    
    def __str__(self):
        return "%s" % self.id
   
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


class AppointmentDetail(models.Model):
    appointment_type = models.CharField(max_length=200, verbose_name="appointment_type",  null=True, default='Employee' )
    individual = models.ForeignKey(IndividualUserDetail, verbose_name="IndividualUserDetail", null=True, on_delete=models.CASCADE, default=None, blank=True)
    individual_patient = models.ForeignKey(IndividualDependent, verbose_name="individual_patient", null=True, on_delete=models.CASCADE, default=None, blank=True)
    individual_address = models.ForeignKey(IndividualAddressDetail, verbose_name="individual_address", null=True, on_delete=models.CASCADE, default=None, blank=True)
    employee = models.ForeignKey(EmployeeDetail, verbose_name="Employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    patient = models.ForeignKey(EmployeeDependent, verbose_name="Employee Dependent", null=True, on_delete=models.CASCADE, default=None, blank=True)
    employee_address = models.ForeignKey(EmployeeAddressDetail, verbose_name="employee_address", null=True, on_delete=models.CASCADE, default=None, blank=True)
    package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    center = models.ForeignKey(CenterDetail, verbose_name="Center", null=True, on_delete=models.CASCADE, default=None, blank=True)
    vendor = models.ForeignKey(VendorDetail, verbose_name="vendor", null=True, on_delete=models.CASCADE, default=None, blank=True)
    type_of_visit = models.ForeignKey(TypeOfVisit, verbose_name="type_of_visit", null=True, on_delete=models.CASCADE, default=None, blank=True)
    appointment_date_1 = models.CharField(max_length=200, verbose_name="appointment_date_1",  null=True , blank=True)
    appointment_date_2 = models.CharField(max_length=200, verbose_name="appointment_date_2",  null=True , blank=True)
    home_sample_date_1 = models.CharField(max_length=200, verbose_name="home_sample_date_1",  null=True , blank=True)
    home_sample_date_2 = models.CharField(max_length=200, verbose_name="home_sample_date_2",  null=True , blank=True)
    confirm_appointment_date = models.CharField(max_length=200, verbose_name="confirm_appointment_date",  null=True , default=None, blank=True)
    confirm_home_sample_date = models.CharField(max_length=200, verbose_name="confirm_home_sample_date",  null=True , default=None, blank=True)
    date_of_appointment = models.CharField(max_length=200, verbose_name="date_of_appointment", null=True, default=None, blank=True)
    reason = models.CharField(max_length=500, verbose_name="reason", null=True, default=None , blank=True)
    remark = models.CharField(max_length=500, verbose_name="remark", null=True, default=None , blank=True)
    report_date = models.CharField(max_length=100, verbose_name="report_date", null=True, default=None , blank=True)
    report = models.FileField(upload_to='image/Report', verbose_name='report', null=True, blank=True,validators=[validators.validate_file_extension_image_and_pdf])  
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % str(self.id)+'--emplooyee name--->'+str(self.employee)


class RescheduleAppointment(models.Model):
    appointment = models.ForeignKey(AppointmentDetail, verbose_name="appointment", null=True, on_delete=models.CASCADE, default=None, blank=True)
    rescheduled_by = models.CharField(max_length=200, verbose_name="rescheduled_by", null=True, blank=True)  # e.g. 'Employee', 'Individual', 'Vendor', 'Staff'
    old_appointment_date = models.CharField(max_length=200, verbose_name="old_appointment_date", null=True, default=None, blank=True)
    new_appointment_date = models.CharField(max_length=200, verbose_name="new_appointment_date", null=True, default=None, blank=True)
    old_home_sample_date = models.CharField(max_length=200, verbose_name="old_home_sample_date", null=True, default=None, blank=True)
    new_home_sample_date = models.CharField(max_length=200, verbose_name="new_home_sample_date", null=True, default=None, blank=True)
    reason = models.CharField(max_length=500, verbose_name="reason", null=True, default=None, blank=True)
    remark = models.CharField(max_length=500, verbose_name="remark", null=True, default=None, blank=True)
    status = models.CharField(max_length=200, verbose_name="status", null=True, default='Rescheduled')
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True)

    def __str__(self):
        return "%s" % str(self.id) + ' --> Appointment: ' + str(self.appointment_id)


class Transaction(models.Model):
    transaction_type = models.CharField(max_length=200, verbose_name="transaction_type",  null=True, default='Employee' )
    is_payment  = models.CharField(max_length=200, verbose_name="is_payment ",  null=True )
    booking_id = models.CharField(max_length=200, verbose_name="booking_id",  null=True)
    invoice_id = models.CharField(max_length=200, verbose_name="invoice_id",  null=True)
    method = models.CharField(max_length=200, verbose_name="method",  null=True)
    transaction_id = models.CharField(max_length=200, verbose_name="transaction_id",  null=True)
    appointment = models.ForeignKey(AppointmentDetail, verbose_name="AppointmentDetail", null=True, on_delete=models.CASCADE, default=None, blank=True)
    individual = models.ForeignKey(IndividualUserDetail, verbose_name="IndividualUserDetail", null=True, on_delete=models.CASCADE, default=None, blank=True)
    corporate = models.ForeignKey(CorporateDetail, verbose_name="corporate", null=True, on_delete=models.CASCADE, default=None, blank=True)
    employee = models.ForeignKey(EmployeeDetail, verbose_name="EmployeeDetail", null=True, on_delete=models.CASCADE, default=None, blank=True)
    package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    amount = models.CharField(max_length=100, verbose_name="amount", null=True, default=None )
    platform_charge = models.CharField(max_length=100, verbose_name="Plat Form Charge", null=True, default=None )
    total_amount = models.CharField(max_length=100, verbose_name="Total Amount", null=True, default=None )
    invoice = models.FileField(upload_to='image/Invoice', verbose_name='invoice', null=True, blank=True,validators=[validators.validate_file_extension_image_and_pdf])  
    individual_patient = models.ForeignKey(IndividualDependent, verbose_name="individual_patient", null=True, on_delete=models.CASCADE, default=None, blank=True)
    patient = models.ForeignKey(EmployeeDependent, verbose_name="Employee Dependent", null=True, on_delete=models.CASCADE, default=None, blank=True)
    reason = models.CharField(max_length=200, verbose_name="reason",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % self.id

class TransactionHistory(models.Model):
    transaction_type = models.CharField(max_length=200, verbose_name="transaction_type",  null=True, default='Employee' )
    user = models.CharField(max_length=100, verbose_name="user", null=True, default=None )
    corporate = models.CharField(max_length=100, verbose_name="corporate", null=True, default=None )
    package = models.CharField(max_length=100, verbose_name="package", null=True, default=None )
    amount = models.CharField(max_length=100, verbose_name="amount", null=True, default=None )
    invoice = models.FileField(upload_to='image/Invoice', verbose_name='invoice', null=True, blank=True,validators=[validators.validate_file_extension_image_and_pdf])  
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

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


# class OfferDetail(models.Model):
#     title = models.CharField(max_length=200, verbose_name="title",  null=True)
#     offer_code = models.CharField(max_length=200, verbose_name="offer_code",  null=True)
#     type_of_discount = models.CharField(max_length=200, verbose_name="type_of_discount",  null=True)
#     discount = models.CharField(max_length=200, verbose_name="discount",  null=True)
#     type_of_service = models.ForeignKey(TypeOfService, verbose_name="type_of_service", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    
#     # duration = models.ForeignKey(Duration, verbose_name="duration", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     # platform = models.ForeignKey(Platform, verbose_name="platform", null=True, on_delete=models.CASCADE, default=None, blank=True)
#     platform = models.ManyToManyField(Platform,verbose_name="Platform", blank= True)
#     max_usage_count = models.CharField(max_length=200, verbose_name="max_usage_count",  null=True )
#     no_of_uses_per_customer = models.CharField(max_length=200, verbose_name="no_of_uses_per_customer",  null=True )
#     # duration = models.CharField(max_length=200, verbose_name="duration",  null=True )
#     publish_date = models.CharField(max_length=200, verbose_name="publish_date",  null=True )
#     publish_time = models.CharField(max_length=200, verbose_name="publish_time",  null=True )
#     start_date = models.CharField(max_length=200, verbose_name="start_date",  null=True )
#     end_date = models.CharField(max_length=200, verbose_name="end_date",  null=True )
#     # platform = models.CharField(max_length=200, verbose_name="platform",  null=True )
#     content = models.TextField(verbose_name="content",  null=True ) 
#     status = models.CharField(max_length=200, verbose_name="status",  null=True )
#     created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

#     def __str__(self):
#         return "%s" % self.id


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



class AddToCart(models.Model):
    user_type = models.CharField(max_length=200, verbose_name="user_type",  null=True)
    appointment = models.ForeignKey(AppointmentDetail, verbose_name="appointment", null=True, on_delete=models.CASCADE, default=None, blank=True)
    individual = models.ForeignKey(IndividualUserDetail, verbose_name="individual", null=True, on_delete=models.CASCADE, default=None, blank=True)
    individual_patient = models.ForeignKey(IndividualDependent, verbose_name="individual_patient", null=True, on_delete=models.CASCADE, default=None, blank=True)
    employee = models.ForeignKey(EmployeeDetail, verbose_name="employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    patient = models.ForeignKey(EmployeeDependent, verbose_name="Employee Dependent", null=True, on_delete=models.CASCADE, default=None, blank=True)
    package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    amount = models.CharField(max_length=100, verbose_name="amount", null=True, default=None )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
    
    def __str__(self):
        return "%s" % self.id

class HohEmployee(models.Model):
    company = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=100, null=True, blank=True)
    unique_user_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    personal_email = models.EmailField(null=True, blank=True)
    personal_mobile = models.CharField(max_length=30, null=True, blank=True)
    office_location = models.TextField(null=True, blank=True)


class DarwinboxCandidateAppointment(models.Model):
    hoh_employee = models.ForeignKey(HohEmployee, verbose_name="HOH Employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    center = models.ForeignKey(CenterDetail, verbose_name="Center", null=True, on_delete=models.CASCADE, default=None, blank=True)
    vendor = models.ForeignKey(VendorDetail, verbose_name="vendor", null=True, on_delete=models.CASCADE, default=None, blank=True)
    type_of_visit = models.ForeignKey(TypeOfVisit, verbose_name="type_of_visit", null=True, on_delete=models.CASCADE, default=None, blank=True)
    appointment_date_1 = models.CharField(max_length=200, verbose_name="appointment_date_1", null=True, blank=True)
    appointment_date_2 = models.CharField(max_length=200, verbose_name="appointment_date_2", null=True, blank=True)
    home_sample_date_1 = models.CharField(max_length=200, verbose_name="home_sample_date_1", null=True, blank=True)
    home_sample_date_2 = models.CharField(max_length=200, verbose_name="home_sample_date_2", null=True, blank=True)
    confirm_appointment_date = models.CharField(max_length=200, verbose_name="confirm_appointment_date", null=True, default=None, blank=True)
    confirm_home_sample_date = models.CharField(max_length=200, verbose_name="confirm_home_sample_date", null=True, default=None, blank=True)
    date_of_appointment = models.CharField(max_length=200, verbose_name="date_of_appointment", null=True, default=None, blank=True)
    reason = models.CharField(max_length=500, verbose_name="reason", null=True, default=None, blank=True)
    remark = models.CharField(max_length=500, verbose_name="remark", null=True, default=None, blank=True)
    report_date = models.CharField(max_length=100, verbose_name="report_date", null=True, default=None, blank=True)
    report = models.FileField(upload_to='image/Report', verbose_name='report', null=True, blank=True, validators=[validators.validate_file_extension_image_and_pdf])
    status = models.CharField(max_length=200, verbose_name="status", null=True)
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True)

    def __str__(self):
        return "%s" % str(self.id) + '--candidate name--->' + str(self.hoh_employee)


class RescheduleDarwinboxCandidateAppointment(models.Model):
    appointment = models.ForeignKey(DarwinboxCandidateAppointment, verbose_name="appointment", null=True, on_delete=models.CASCADE, default=None, blank=True)
    hoh_employee = models.ForeignKey(HohEmployee, verbose_name="HOH Employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    rescheduled_by = models.CharField(max_length=200, verbose_name="rescheduled_by", null=True, blank=True)  # e.g. 'Candidate', 'Vendor', 'Staff'
    old_appointment_date = models.CharField(max_length=200, verbose_name="old_appointment_date", null=True, default=None, blank=True)
    new_appointment_date = models.CharField(max_length=200, verbose_name="new_appointment_date", null=True, default=None, blank=True)
    old_home_sample_date = models.CharField(max_length=200, verbose_name="old_home_sample_date", null=True, default=None, blank=True)
    new_home_sample_date = models.CharField(max_length=200, verbose_name="new_home_sample_date", null=True, default=None, blank=True)
    reason = models.CharField(max_length=500, verbose_name="reason", null=True, default=None, blank=True)
    remark = models.CharField(max_length=500, verbose_name="remark", null=True, default=None, blank=True)
    status = models.CharField(max_length=200, verbose_name="status", null=True, default='Rescheduled')
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True)

    def __str__(self):
        return "%s" % str(self.id) + ' --> Darwinbox Appointment: ' + str(self.appointment_id)