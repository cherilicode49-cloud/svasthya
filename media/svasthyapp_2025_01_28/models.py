from django.db import models
from svasthyapp import validators

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
        return "%s" % self.id

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
        return "%s" % self.id


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
    industry = models.CharField(max_length=200, verbose_name="industry",  null=True )
    spoke_person = models.CharField(max_length=200, verbose_name="spoke_person",  null=True )
    mobile = models.CharField(max_length=200, verbose_name="mobile",  null=True )
    email = models.CharField(max_length=200, verbose_name="email",  null=True )
    pan_card = models.CharField(max_length=200, verbose_name="pan_card",  null=True )
    GST_no = models.CharField(max_length=200, verbose_name="GST_no",  null=True )
    billing_cycle = models.ForeignKey(BillingCycle, verbose_name="billing_cycle", null=True, on_delete=models.CASCADE, default=None, blank=True)
    start_date = models.CharField(max_length=200, verbose_name="start_date",  null=True )
    address = models.CharField(max_length=200, verbose_name="address",  null=True )
    pincode = models.CharField(max_length=200, verbose_name="pincode",  null=True )
    state = models.CharField(max_length=200, verbose_name="state",  null=True )
    city = models.CharField(max_length=200, verbose_name="city",  null=True )
    level1 = models.ForeignKey(StaffDetail, related_name= 'level1', verbose_name="Level 1", null=True, on_delete=models.CASCADE, default=None, blank=True)
    level2 = models.ForeignKey(StaffDetail, related_name= 'level2', verbose_name="Level 2", null=True, on_delete=models.CASCADE, default=None, blank=True)
    status = models.CharField(max_length=200, verbose_name="status", null=True )    
    login_via = models.CharField(max_length=200, verbose_name="login_via", null=True , default='email')    
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    
        
    def __str__(self):
        return "%s" % self.id



class VendorDetail(models.Model):
    vendor_name = models.CharField(max_length=200, verbose_name="vendor_name",  null=True )
    vendor_code = models.CharField(max_length=200, verbose_name="vendor_code",  null=True )
    type_of_service = models.ForeignKey(TypeOfService, verbose_name="type_of_service", null=True, on_delete=models.CASCADE, default=None, blank=True)
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
        return "%s" % self.id



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
    profile_image = models.FileField(upload_to='image/employee/profile', verbose_name='profile_image', null=True, blank=True,validators=[validators.validate_file_extension_image])  
    status = models.CharField(max_length=200, verbose_name="status", null=True )    
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

class PackageDetail(models.Model):
    package_name = models.CharField(max_length=200, verbose_name="package_name",  null=True )
    package_code = models.CharField(max_length=200, verbose_name="package_code",  null=True )
    MRP = models.CharField(max_length=200, verbose_name="MRP",  null=True )
    discount_price = models.CharField(max_length=200, verbose_name="discount_price",  null=True )
    offer_price = models.CharField(max_length=200, verbose_name="offer_price",  null=True )
    type_of_service = models.ForeignKey(TypeOfService, verbose_name="type_of_services", null=True, on_delete=models.CASCADE, default=None, blank=True)
    type_of_visit = models.ForeignKey(TypeOfVisit, verbose_name="type_of_visit", null=True, on_delete=models.CASCADE, default=None, blank=True)
    corporate = models.ForeignKey(CorporateDetail, related_name="corporate_details", verbose_name="Corporate", null=True, on_delete=models.CASCADE, default=None, blank=True)
    age_category = models.ForeignKey(AgeCategory, verbose_name="age_category", null=True, on_delete=models.CASCADE, default=None, blank=True)
    gender = models.ForeignKey(Gender,verbose_name="gender", null=True, on_delete=models.CASCADE, default=None, blank=True)
    start_date = models.CharField(max_length=200, verbose_name="start_date",  null=True )
    end_date = models.CharField(max_length=200, verbose_name="end_date",  null=True )
    billing_cycle = models.ForeignKey(BillingCycle, verbose_name="billing_cycle", null=True, on_delete=models.CASCADE, default=None, blank=True)
    tags = models.ForeignKey(PaymentTags, verbose_name="tags", null=True, on_delete=models.CASCADE, default=None, blank=True)
    description = models.TextField(verbose_name="description",  null=True )
    relation_with_employee = models.ManyToManyField(Relation,verbose_name="Relation", blank= True)
    
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % self.id

    
class CenterDetail(models.Model):
    center_name = models.CharField(max_length=200, verbose_name="center_name",  null=True )
    address = models.CharField(max_length=200, verbose_name="address",  null=True )
    pincode = models.CharField(max_length=200, verbose_name="pincode",  null=True )
    state = models.CharField(max_length=200, verbose_name="state",  null=True )
    city = models.CharField(max_length=200, verbose_name="city",  null=True ) 
    location = models.CharField(max_length=200, verbose_name="location",  null=True ) 
    vendor = models.ForeignKey(VendorDetail, verbose_name="Vendor", null=True, on_delete=models.CASCADE, default=None, blank=True)
    package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    type_of_service = models.ForeignKey(TypeOfService, verbose_name="type_of_services", null=True, on_delete=models.CASCADE, default=None, blank=True)
    latitude = models.CharField(max_length=200, verbose_name="latitude",  null=True )
    longitude = models.CharField(max_length=200, verbose_name="longitude",  null=True )
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % self.id


    
class HolidayDetail(models.Model):
    vendor = models.ForeignKey(VendorDetail, verbose_name="Vendor", null=True, on_delete=models.CASCADE, default=None, blank=True)
    center = models.ForeignKey(CenterDetail, verbose_name="center", null=True, on_delete=models.CASCADE, default=None, blank=True)
    type_of_service = models.ForeignKey(TypeOfService, verbose_name="type_of_services", null=True, on_delete=models.CASCADE, default=None, blank=True)
    state = models.CharField(max_length=200, verbose_name="state",  null=True )
    city = models.CharField(max_length=200, verbose_name="city",  null=True ) 
    location = models.CharField(max_length=200, verbose_name="location",  null=True ) 
    weekly_off = models.CharField(max_length=200, verbose_name="weekly_off",  null=True )
    holiday = models.CharField(max_length=200, verbose_name="holiday",  null=True )
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

class AppointmentDetail(models.Model):
    employee = models.ForeignKey(EmployeeDetail, verbose_name="Employee", null=True, on_delete=models.CASCADE, default=None, blank=True)
    patient = models.ForeignKey(EmployeeDependent, verbose_name="Employee Dependent", null=True, on_delete=models.CASCADE, default=None, blank=True)
    package = models.ForeignKey(PackageDetail, verbose_name="package", null=True, on_delete=models.CASCADE, default=None, blank=True)
    center = models.ForeignKey(CenterDetail, verbose_name="Center", null=True, on_delete=models.CASCADE, default=None, blank=True)
    vendor = models.ForeignKey(VendorDetail, verbose_name="vendor", null=True, on_delete=models.CASCADE, default=None, blank=True)
    appoinment_date_1 = models.CharField(max_length=200, verbose_name="appoinment_date_1",  null=True )
    appoinment_date_2 = models.CharField(max_length=200, verbose_name="appoinment_date_2",  null=True )
    home_sample_date_1 = models.CharField(max_length=200, verbose_name="home_sample_date_1",  null=True )
    home_sample_date_2 = models.CharField(max_length=200, verbose_name="home_sample_date_2",  null=True )
    confirm_appoinment_date = models.CharField(max_length=200, verbose_name="confirm_appoinment_date",  null=True , default=None)
    confirm_home_sample_date = models.CharField(max_length=200, verbose_name="confirm_home_sample_date",  null=True , default=None)
    reason = models.CharField(max_length=500, verbose_name="reason", null=True, default=None )
    remark = models.CharField(max_length=500, verbose_name="remark", null=True, default=None )
    report_date = models.CharField(max_length=100, verbose_name="report_date", null=True, default=None )
    report = models.FileField(upload_to='image/Report', verbose_name='report', null=True, blank=True,validators=[validators.validate_file_extension_image_and_pdf])  
    status = models.CharField(max_length=200, verbose_name="status",  null=True )
    created_at = models.CharField(max_length=200, verbose_name="created_at", null=True )    

    def __str__(self):
        return "%s" % self.id
