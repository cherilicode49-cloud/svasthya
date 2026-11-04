from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import authenticate
from datetime import datetime
import json, ast
from django.conf import settings


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdminUser
        fields = '__all__'



class StaffDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaffDepartment
        fields = '__all__'

class TypeOfAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TypeOfAccess
        fields = '__all__'

class StaffLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaffLevel
        fields = '__all__'

class StaffTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaffType
        fields = '__all__'

class AgeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgeCategory
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gender
        fields = '__all__'

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Relation
        fields = '__all__'

class TypeOfServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TypeOfService
        fields = '__all__'

class TypeOfVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TypeOfVisit
        fields = '__all__'


class ParentCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ParentCompany
        fields = '__all__'



class BillingCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BillingCycle
        fields = '__all__'



class WeekdaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Weekdays
        fields = '__all__'


class HolidaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Holidays
        fields = '__all__'



class PaymentTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentTags
        fields = '__all__'

class TypeOfIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TypeOfIndustry
        fields = '__all__'

# class DurationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Duration
#         fields = '__all__'


# class PlatformSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Platform
#         fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    staff_type_name = serializers.ReadOnlyField(source='staff_type.staff_type')
    staff_level_name = serializers.ReadOnlyField(source='staff_level.staff_level')
    type_of_access_name = serializers.ReadOnlyField(source='type_of_access.type_of_access')
    department_name = serializers.ReadOnlyField(source='department.staff_department')
    
    class Meta:
        model = models.StaffDetail
        fields = '__all__'

    # def to_representation(self, instance):
    #     self.fields['staff_type'] =  StaffTypeSerializer(read_only=True)
    #     return super(StaffSerializer, self).to_representation(instance)



class StaffDataSerializer(serializers.ModelSerializer):
    staff_type_name = serializers.ReadOnlyField(source='staff_type.staff_type')
    staff_level_name = serializers.ReadOnlyField(source='staff_level.staff_level')
    type_of_access_name = serializers.ReadOnlyField(source='type_of_access.type_of_access')
    
    
    class Meta:
        model = models.StaffDetail
        # fields = ['id', 'name', 'mobile', 'email']
        fields = ['id', 'name', 'mobile', 'email', 'staff_type_name','staff_type','staff_level_name','staff_level','type_of_access_name', 'type_of_access' ]



class CorporateSerializer(serializers.ModelSerializer):
    parent_company_name = serializers.ReadOnlyField(source='parent_company.parent_company')
    billing_cycle_name = serializers.ReadOnlyField(source='billing_cycle.billing_cycle')
    level1_name = serializers.ReadOnlyField(source='level1.name')
    level2_name = serializers.ReadOnlyField(source='level2.name')
    industry_name = serializers.ReadOnlyField(source='industry.type_of_industry')
    
    class Meta:
        model = models.CorporateDetail
        fields = '__all__'



class CorporateDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.CorporateDetail
        fields = ['id', 'corporate_name']

    # def to_representation(self, instance):
    #     self.fields['level1'] =  StaffDataSerializer(read_only=True)
    #     self.fields['level2'] =  StaffDataSerializer(read_only=True)
    #     return super(CorporateSerializer, self).to_representation(instance)



class VendorSerializer(serializers.ModelSerializer):
    billing_cycle_name = serializers.ReadOnlyField(source='billing_cycle.billing_cycle')
    type_of_service_name = serializers.ReadOnlyField(source='type_of_service.type_of_service')
    type_of_visit_name = serializers.ReadOnlyField(source='type_of_visit.type_of_visit')

    class Meta:
        model = models.VendorDetail
        # fields = '__all__'
        fields = ['id','vendor_name','vendor_code','type_of_service','type_of_visit','billing_cycle','GST_no','start_date','end_date','mobile',\
            'email','pincode','address','state','city','login_via','stakeholder_name','stakeholder_mobile','stakeholder_email','contact_person1',\
            'contact_person_designation1','contact_person_mobile1','contact_person_email1','contact_person2','contact_person_designation2',\
            'contact_person_mobile2','contact_person_email2','contact_person3','contact_person_designation3','contact_person_mobile3',\
            'contact_person_email3','status','billing_cycle_name','type_of_service_name','type_of_visit_name', 'profile_image','billing_email']



class CorporateNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CorporateDetail
        fields = ['id', 'corporate_name', 'corporate_code']


class EmployeeDetailSerializer(serializers.ModelSerializer):
    corporate_name = serializers.ReadOnlyField(source='corporate.corporate_name')
    gender_name = serializers.ReadOnlyField(source='gender.gender')
    # dependent_relation1_name = serializers.ReadOnlyField(source='dependent_relation1.relation')
    # dependent_relation2_name = serializers.ReadOnlyField(source='dependent_relation2.relation')
    # dependent_relation3_name = serializers.ReadOnlyField(source='dependent_relation3.relation')
    # gender1_name = serializers.ReadOnlyField(source='gender1.gender')
    # gender2_name = serializers.ReadOnlyField(source='gender2.gender')
    # gender3_name = serializers.ReadOnlyField(source='gender3.gender')
    
    class Meta:
        model = models.EmployeeDetail
        # fields = '__all__'
        fields = ['id','gender_name','corporate_name','corporate','employee_name','employee_code','department','date_of_join','date_of_birth','gender',\
        'mobile','email','hr_employee','hr_corporate_code','status', 'profile_image']


class EmployeeDependentSerializer(serializers.ModelSerializer):
    dependent_relation_name = serializers.ReadOnlyField(source='dependent_relation.relation')
    gender_name = serializers.ReadOnlyField(source='gender.gender')
   
    class Meta:
        model = models.EmployeeDependent
        fields = '__all__'


class IndividualDependentSerializer(serializers.ModelSerializer):
    dependent_relation_name = serializers.ReadOnlyField(source='dependent_relation.relation')
    gender_name = serializers.ReadOnlyField(source='gender.gender')
   
    class Meta:
        model = models.IndividualDependent
        fields = '__all__'

class EmployeeDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.EmployeeDetail
        fields = ['id', 'employee_name']

class PackageDetailSerializer(serializers.ModelSerializer):
    type_of_service_name = serializers.ReadOnlyField(source='type_of_service.type_of_service')
    type_of_visit_name = serializers.ReadOnlyField(source='type_of_visit.type_of_visit')
    age_category_name = serializers.ReadOnlyField(source='age_category.age_category')
    gender_name = serializers.ReadOnlyField(source='gender.gender')
    # corporate_name = serializers.ReadOnlyField(source='corporate.corporate_name')
    billing_cycle_name = serializers.ReadOnlyField(source='billing_cycle.billing_cycle')
    tags_name = serializers.ReadOnlyField(source='tags.payment_tags')
    package_applicable_name = serializers.ReadOnlyField(source='package_applicable.employee_name')
    relation_with_employee_name = serializers.ReadOnlyField(source='relation_with_employee.relation')
    relation_age_category_name = serializers.ReadOnlyField(source='relation_age_category.age_category')
    relation_gender_name = serializers.ReadOnlyField(source='relation_gender.gender')
    vendor_name = serializers.ReadOnlyField(source='vendor.vendor_name')

    corporate_name = serializers.SerializerMethodField()


    class Meta:
        model = models.PackageDetail
        fields = ['id','package_type', 'package_name', 'package_code', 'vendor', 'MRP', 'vendor_name',
                  'base_amount', 'profit', 'tax', 'tax_amount', 'igst', 'igst_amount', 
                  'sgst', 'sgst_amount', 'cgst', 'cgst_amount', 'discount_price', 
                  'offer_price', 'corporate_selection', 'type_of_service', 'type_of_visit', 
                  'corporate', 'age_category', 'gender', 'start_date', 'end_date', 
                  'billing_cycle', 'tags', 'description', 'relation_with_employee', 
                  'status', 'created_at','type_of_service_name','corporate_name',
                  'type_of_visit_name','age_category_name','gender_name','billing_cycle_name',
                  'tags_name','package_applicable_name','relation_with_employee_name','preparation_description', 'detail_description',
                  'relation_age_category_name','relation_gender_name', 'total_test_number', 'test_list', 'slug']
    

    def get_corporate_name(self, obj):
        return [corp.corporate_name for corp in obj.corporate.all()]


    # def to_representation(self, instance):
    #     self.fields['corporate'] =  CorporateDataSerializer(read_only=True)
    #     return super(PackageDetailSerializer, self).to_representation(instance)


class VendorNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.VendorDetail
        fields = ['id', 'vendor_name', 'vendor_code']

class PackageNameSerializer(serializers.ModelSerializer):
    type_of_service = serializers.ReadOnlyField(source='type_of_service.type_of_service')

    class Meta:
        model = models.PackageDetail
        fields = ['id', 'package_name', 'type_of_service_id', 'type_of_service', 'slug']



class CenterDetailSerializer(serializers.ModelSerializer):
    type_of_service_name = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()
    package_name = serializers.SerializerMethodField()
    

    class Meta:
        model = models.CenterDetail
        fields = ['id','center_name','address','pincode','state','city','location','vendor','package','map_link',
                  'type_of_service','latitude','longitude','type_of_service_name','vendor_name','package_name','status']
        
    def get_type_of_service_name(self, obj):
        return [tos.type_of_service for tos in obj.type_of_service.all()]

    def get_vendor_name(self, obj):
        return [vendor.vendor_name for vendor in obj.vendor.all()]

    def get_package_name(self, obj):
        return [package.package_name for package in obj.package.all()]
    
    # def to_representation(self, instance):
    #     self.fields['vendor'] =  VendorNameSerializer(read_only=True, many=True)
    #     self.fields['package'] =  PackageNameSerializer(read_only=True, many=True)
    #     return super(CenterDetailSerializer, self).to_representation(instance)


class CenterDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.CenterDetail
        fields = '__all__'



class CenterTestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.CenterDetail
        exclude = ['vendor','package','type_of_service']


class PackageVendorSerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.vendor_name')
    package_vendor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = models.PackageDetail
        fields = ['id', 'package_name', 'vendor', 'vendor_name', 'package_vendor_name']

    def get_package_vendor_name(self, obj):
        return f"{obj.package_name} - {obj.vendor.vendor_name}" if obj.vendor else obj.package_name


class HolidayDetailSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    # center = serializers.SerializerMethodField()

    class Meta:
        model = models.HolidayDetail
        fields = '__all__'

    def get_state(self, obj):

        print("obj=====>",obj)
        state_detail = models.HolidayDetail.objects.get(id=obj.id)
        get_state = state_detail.state
        if not isinstance(get_state, str) or not get_state.strip():
            return []

        try:
            parsed = ast.literal_eval(get_state)
            print("parsed===>",type(parsed))
            if isinstance(parsed, list):
                print("parsed===>",type(parsed))
                return parsed
            elif isinstance(parsed, str):
                print("parsed===>",type(parsed.strip()))
                return [parsed.strip()]
        except (ValueError, SyntaxError):
            print("parsed===>",type([get_state.strip()]))
            
            return [get_state.strip()]
        
        return []


    def get_city(self, obj):

        print("obj=====>",obj)
        city_detail = models.HolidayDetail.objects.get(id=obj.id)
        get_city = city_detail.city
        if not isinstance(get_city, str) or not get_city.strip():
            return []

        try:
            parsed = ast.literal_eval(get_city)
            print("parsed===>",type(parsed))
            if isinstance(parsed, list):
                print("parsed===>",type(parsed))
                return parsed
            elif isinstance(parsed, str):
                print("parsed===>",type(parsed.strip()))
                return [parsed.strip()]
        except (ValueError, SyntaxError):
            print("parsed===>",type([get_city.strip()]))
            
            return [get_city.strip()]
        
        return []


    # def get_center(self, obj):

    #     print("obj=====>",obj)
    #     state_detail = models.HolidayDetail.objects.get(id=obj.id)
    #     get_center = state_detail.center
    #     if not isinstance(get_center, str) or not get_center.strip():
    #         return []

    #     try:
    #         parsed = ast.literal_eval(get_center)
    #         print("parsed===>",type(parsed))
    #         if isinstance(parsed, list):
    #             print("parsed===>",type(parsed))
    #             return parsed
    #         elif isinstance(parsed, str):
    #             print("parsed===>",type(parsed.strip()))
    #             return [parsed.strip()]
    #     except (ValueError, SyntaxError):
    #         print("parsed===>",type([get_center.strip()]))
            
    #         return [get_center.strip()]
        
    #     return []

    # def to_representation(self, instance):
    #     self.fields['center'] =  CenterDetailSerializer(read_only=True)
    #     self.fields['type_of_service'] =  TypeOfServiceSerializer(read_only=True)
    #     return super(HolidayDetailSerializer, self).to_representation(instance)

class HealthTipsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.HealthTips
        fields = '__all__'


class IndividualUserDetailSerializer(serializers.ModelSerializer):
    gender_name = serializers.ReadOnlyField(source='gender.gender')
    
    class Meta:
        model = models.IndividualUserDetail
        fields = '__all__'


class EmployeeAddressDetailSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = models.EmployeeAddressDetail
        fields = '__all__'

class IndividualAddressDetailSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = models.IndividualAddressDetail
        fields = '__all__'


class AppointmentDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.AppointmentDetail
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['employee'] =  EmployeeDetailSerializer(read_only=True)
        self.fields['patient'] =  EmployeeDependentSerializer(read_only=True)
        self.fields['package'] =  PackageDetailSerializer(read_only=True)
        self.fields['center'] =  CenterDetailSerializer(read_only=True)
        self.fields['individual'] =  IndividualUserDetailSerializer(read_only=True)
        # self.fields['vendor'] =  VendorNameSerializer(read_only=True)
        self.fields['individual_patient'] =  IndividualDependentSerializer(read_only=True)
        self.fields['individual_address'] =  IndividualAddressDetailSerialiser(read_only=True)
        self.fields['employee_address'] =  EmployeeAddressDetailSerialiser(read_only=True)
        return super(AppointmentDetailSerializer, self).to_representation(instance)

class AppointmentDetailEBPFSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.AppointmentDetail
        exclude = ['individual', 'individual_patient', 'reason', 'remark', 'report_date', 'report']

    def to_representation(self, instance):
        self.fields['employee'] =  EmployeeDetailSerializer(read_only=True)
        self.fields['patient'] =  EmployeeDependentSerializer(read_only=True)
        self.fields['package'] =  PackageDetailSerializer(read_only=True)
        self.fields['center'] =  CenterDetailSerializer(read_only=True)
        return super(AppointmentDetailEBPFSerializer, self).to_representation(instance)

class ModuleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Module
        fields = '__all__'

class AdminModuleRightsSerializer(serializers.ModelSerializer):
    module = serializers.ReadOnlyField(source='module.module')
    module_id = serializers.ReadOnlyField(source='module.id')
    
    class Meta:
        model = models.AdminModuleRights
        fields = '__all__'

    # def to_representation(self, instance):
    #     self.fields['module'] =  ModuleSerializer(read_only=True)
    #     return super(AdminModuleRightsSerializer, self).to_representation(instance)

# class OfferDetailSerializer(serializers.ModelSerializer):
#     # duration_name = serializers.ReadOnlyField(source='duration.duration')
    
#     class Meta:
#         model = models.OfferDetail
#         fields = '__all__'

class NotificationNameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.NotificationDetail
        fields = ['id','title', 'created_date', 'created_time', 'notification_type', 'user_read']

class NotificationDetailSerializer(serializers.ModelSerializer):    
    individual_name = serializers.ReadOnlyField(source='individual.name')
    employee_name = serializers.ReadOnlyField(source='employee.employee_name')
    center_name = serializers.ReadOnlyField(source='center.center_name')
    package = serializers.ReadOnlyField(source='package.package_name')
    type_of_visit = serializers.ReadOnlyField(source='type_of_visit.type_of_visit')

    class Meta:
        model = models.NotificationDetail
        fields = '__all__'

class AppointmentTransactionData(serializers.ModelSerializer):
    
    class Meta:
        model = models.AppointmentDetail
        fields = ['id','title', 'created_date', 'created_time', 'notification_type', 'user_read']


class IndividualUserTransaction(serializers.ModelSerializer):
    
    class Meta:
        model = models.IndividualUserDetail
        fields = ['id', 'mobile', 'email', 'pincode', 'state']

class EmployeeDetailTransaction(serializers.ModelSerializer):
    
    class Meta:
        model = models.EmployeeDetail
        fields = ['id', 'mobile', 'email', 'pincode', 'state']

class PackageDetailTransaction(serializers.ModelSerializer):
    type_of_service = serializers.ReadOnlyField(source='type_of_service.type_of_service')
    type_of_visit = serializers.ReadOnlyField(source='type_of_visit.type_of_visit')
    
    class Meta:
        model = models.PackageDetail
        fields = ['id', 'base_amount', 'tax_amount', 'offer_price','type_of_service','type_of_visit','MRP', 'discount_price', 'tax', \
        'tax_amount', 'igst', 'igst_amount', 'sgst', 'sgst_amount', 'cgst', 'cgst_amount', 'profit']




class TransactionSerializer(serializers.ModelSerializer):    
    corporate_name = serializers.ReadOnlyField(source='corporate.corporate_name')
    individual_name = serializers.ReadOnlyField(source='individual.name')
    employee_name = serializers.ReadOnlyField(source='employee.employee_name')
    package_name = serializers.ReadOnlyField(source='package.package_name')
    individual_patient_name = serializers.ReadOnlyField(source='individual_patient.dependent_name')
    patient_name = serializers.ReadOnlyField(source='patient.dependent_name')
    

    class Meta:
        model = models.Transaction
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['individual'] =  IndividualUserTransaction(read_only=True)
        self.fields['employee'] =  EmployeeDetailTransaction(read_only=True)
        self.fields['package'] =  PackageDetailTransaction(read_only=True)
        return super(TransactionSerializer, self).to_representation(instance)


class DateAppointentSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    is_date_selected = serializers.SerializerMethodField()

    class Meta:
        model = models.AppointmentDetail
        fields = ['id','date','is_date_selected']

    def get_date(self, object):
        data = {}
        appointment = models.AppointmentDetail.objects.get(id=object.id)

        data={
            'appointment_date_1':appointment.appointment_date_1,
            'appointment_date_2':appointment.appointment_date_2,
            'home_sample_date_1':appointment.home_sample_date_1,
            'home_sample_date_2':appointment.home_sample_date_2,
        }
        return data
    
    def get_is_date_selected(self,object):
        appointment = models.AppointmentDetail.objects.get(id=object.id)

        if appointment.type_of_visit.type_of_visit == "At Home":
            if appointment.home_sample_date_1 not in [None,'','null'] and appointment.home_sample_date_2 not in [None,'','null']:
                return True
            
        elif appointment.type_of_visit.type_of_visit == "At Center":
            if appointment.appointment_date_1 not in [None,'','null'] and appointment.appointment_date_2 not in [None,'','null']:
                return True
            
        elif appointment.type_of_visit.type_of_visit == "Hybrid":
            if appointment.appointment_date_1 not in [None,'','null'] and appointment.appointment_date_1 not in [None,'','null'] and appointment.home_sample_date_1 not in [None,'','null'] and appointment.home_sample_date_2 not in [None,'','null']:
                return True
        
        return False
            

    
class AddToCartSerializer(serializers.ModelSerializer):    
    corporate_name = serializers.ReadOnlyField(source='corporate.corporate_name')
    individual_name = serializers.ReadOnlyField(source='individual.name')
    employee_name = serializers.ReadOnlyField(source='employee.employee_name')
    package_name = serializers.ReadOnlyField(source='package.package_name')
    individual_patient_name = serializers.ReadOnlyField(source='individual_patient.dependent_name')
    patient_name = serializers.ReadOnlyField(source='patient.dependent_name')
    

    class Meta:
        model = models.AddToCart
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['appointment'] =  DateAppointentSerializer(read_only=True)
        self.fields['individual'] =  IndividualUserTransaction(read_only=True)
        self.fields['employee'] =  EmployeeDetailTransaction(read_only=True)
        self.fields['package'] =  PackageDetailTransaction(read_only=True)
        return super(AddToCartSerializer, self).to_representation(instance)

class ActiveCenterDetailTransaction(serializers.ModelSerializer):
    
    class Meta:
        model = models.CenterDetail
        fields = ['id', 'center_name', 'state','city', 'status']



class HolidayDetailDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HolidayDetail
        fields = ['id', 'holiday_name','start_date','end_date']



class PackageExportSerialiser(serializers.ModelSerializer):
    vendor = serializers.ReadOnlyField(source='vendor.vendor_name')
    type_of_service = serializers.ReadOnlyField(source='type_of_service.type_of_service')
    type_of_visit = serializers.ReadOnlyField(source='type_of_visit.type_of_visit')
    age_category = serializers.ReadOnlyField(source='age_category.age_category')
    gender = serializers.ReadOnlyField(source='gender.gender')
    billing_cycle = serializers.ReadOnlyField(source='billing_cycle.billing_cycle')
    tags = serializers.ReadOnlyField(source='tags.payment_tags')
    corporate = serializers.SerializerMethodField()
    relation_with_employee = serializers.SerializerMethodField()
    
    
    class Meta:
        model = models.PackageDetail
        fields = '__all__'

    def get_corporate(self, obj):
        if obj.corporate.values_list('corporate_name', flat=True):
            data = str(list(obj.corporate.values_list('corporate_name', flat=True)))
        else:
            data = ''
        return data

    def get_relation_with_employee(self, obj):
        if obj.relation_with_employee.values_list('relation', flat=True):
            data = str(list(obj.relation_with_employee.values_list('relation', flat=True)))
        else:
            data = ''
        return data



class CenterExportSerialiser(serializers.ModelSerializer):
    
    type_of_service = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()
    package = serializers.SerializerMethodField()
    
    
    class Meta:
        model = models.CenterDetail
        fields = '__all__'

    def get_type_of_service(self, obj):
        if obj.type_of_service.values_list('type_of_service', flat=True):
            data = str(list(obj.type_of_service.values_list('type_of_service', flat=True)))
        else:
            data = ''
        return data

    def get_vendor(self, obj):
        if obj.vendor.values_list('vendor_name', flat=True):
            data = str(list(obj.vendor.values_list('vendor_name', flat=True)))
        else:
            data = ''
        return data

    def get_package(self, obj):
        if obj.package.values_list('package_name', flat=True):
            data = str(list(obj.package.values_list('package_name', flat=True)))
        else:
            data = ''
        return data




class AppointmentExportSerialiser(serializers.ModelSerializer):

    individual = serializers.ReadOnlyField(source='individual.name')
    individual_patient = serializers.ReadOnlyField(source='individual_patient.dependent_name')
    employee = serializers.ReadOnlyField(source='employee.employee_name')
    patient = serializers.ReadOnlyField(source='patient.dependent_name')
    package = serializers.ReadOnlyField(source='package.package_name')
    center = serializers.ReadOnlyField(source='center.center_name')
    vendor = serializers.ReadOnlyField(source='vendor.vendor_name')
    type_of_visit = serializers.ReadOnlyField(source='type_of_visit.type_of_visit')

    report = serializers.SerializerMethodField()

    class Meta:
        model = models.AppointmentDetail
        fields = '__all__'

    def get_report(self, obj):
        if not obj.report:
            return None

        base_url = getattr(settings, 'BASE_URL')
        return f"{base_url}{obj.report.url}"

class TestCategoryTransaction(serializers.ModelSerializer):
    
    class Meta:
        model = models.TestCategory
        fields = "__all__"

class TestSubCategoryTransaction(serializers.ModelSerializer):
    test_category_name = serializers.ReadOnlyField(source='test_category.test_category')
    
    class Meta:
        model = models.TestSubCategory
        fields = "__all__"

    # def to_representation(self, instance):
    #     self.fields['test_category'] =  TestCategoryTransaction(read_only=True)
    #     return super(TestSubCategoryTransaction, self).to_representation(instance)


class TestsProductDetailSerialiser(serializers.ModelSerializer):
    test_subcategory_name = serializers.ReadOnlyField(source='test_subcategory.test_subcategory')
    
    class Meta:
        model = models.TestsProductDetail
        fields = "__all__"

class ComparePackageListSerialiser(serializers.ModelSerializer):
    tags_name = serializers.ReadOnlyField(source='tags.payment_tags')
    
    class Meta:
        model = models.PackageDetail
        fields = ['id', 'package_name', 'base_amount', 'discount_price', 'offer_price', 'total_test_number', 'MRP', 'tags_name']




class CenterDetailSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = models.CenterDetail
        fields = ['id', 'city','location']


class RescheduleAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RescheduleAppointment
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['appointment'] = AppointmentDetailSerializer(read_only=True)
        return super(RescheduleAppointmentSerializer, self).to_representation(instance)


class HohEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HohEmployee
        fields = '__all__'


class DarwinboxCandidateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DarwinboxCandidateAppointment
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['hoh_employee'] = HohEmployeeSerializer(read_only=True)
        self.fields['package'] = PackageDetailSerializer(read_only=True)
        self.fields['center'] = CenterDetailSerializer(read_only=True)
        self.fields['vendor'] = VendorSerializer(read_only=True)
        self.fields['type_of_visit'] = TypeOfVisitSerializer(read_only=True)
        return super(DarwinboxCandidateAppointmentSerializer, self).to_representation(instance)


class RescheduleDarwinboxCandidateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RescheduleDarwinboxCandidateAppointment
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['appointment'] = DarwinboxCandidateAppointmentSerializer(read_only=True)
        self.fields['hoh_employee'] = HohEmployeeSerializer(read_only=True)
        return super(RescheduleDarwinboxCandidateAppointmentSerializer, self).to_representation(instance)
