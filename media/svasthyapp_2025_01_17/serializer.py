from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import authenticate
from datetime import datetime


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
    class Meta:
        model = models.StaffDetail
        fields = ['id', 'name', 'mobile', 'email']



class CorporateSerializer(serializers.ModelSerializer):
    parent_company_name = serializers.ReadOnlyField(source='parent_company.parent_company')
    billing_cycle_name = serializers.ReadOnlyField(source='billing_cycle.billing_cycle')
    level1_name = serializers.ReadOnlyField(source='level1.name')
    level2_name = serializers.ReadOnlyField(source='level2.name')
    
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
        fields = '__all__'


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
        fields = '__all__'


class EmployeeDependentSerializer(serializers.ModelSerializer):
    dependent_relation_name = serializers.ReadOnlyField(source='dependent_relation.relation')
    gender_name = serializers.ReadOnlyField(source='gender.gender')
   
    class Meta:
        model = models.EmployeeDependent
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
    corporate_name = serializers.ReadOnlyField(source='corporate.corporate_name')
    billing_cycle_name = serializers.ReadOnlyField(source='billing_cycle.billing_cycle')
    tags_name = serializers.ReadOnlyField(source='tags.payment_tags')
    package_applicable_name = serializers.ReadOnlyField(source='package_applicable.employee_name')
    relation_with_employee_name = serializers.ReadOnlyField(source='relation_with_employee.relation')
    relation_age_category_name = serializers.ReadOnlyField(source='relation_age_category.age_category')
    relation_gender_name = serializers.ReadOnlyField(source='relation_gender.gender')


    class Meta:
        model = models.PackageDetail
        fields = '__all__'


class CenterDetailSerializer(serializers.ModelSerializer):
    type_of_service_name = serializers.ReadOnlyField(source='type_of_service.type_of_service')
    vendor_name = serializers.ReadOnlyField(source='vendor.vendor_name')
    package_name = serializers.ReadOnlyField(source='package.package_name')

    class Meta:
        model = models.CenterDetail
        fields = '__all__'


class CenterDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.CenterDetail
        fields = '__all__'



class VendorNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.VendorDetail
        fields = ['id', 'vendor_name']

class PackageNameSerializer(serializers.ModelSerializer):
    type_of_service = serializers.ReadOnlyField(source='type_of_service.type_of_service')

    class Meta:
        model = models.PackageDetail
        fields = ['id', 'package_name', 'type_of_service_id', 'type_of_service']




class HolidayDetailSerializer(serializers.ModelSerializer):
    type_of_service_name = serializers.ReadOnlyField(source='type_of_service.type_of_service')
    vendor_name = serializers.ReadOnlyField(source='vendor.vendor_name')
    center_name = serializers.ReadOnlyField(source='center.center_name')

    class Meta:
        model = models.HolidayDetail
        fields = '__all__'

    # def to_representation(self, instance):
    #     self.fields['center'] =  CenterDetailSerializer(read_only=True)
    #     self.fields['type_of_service'] =  TypeOfServiceSerializer(read_only=True)
    #     return super(HolidayDetailSerializer, self).to_representation(instance)

class HealthTipsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.HealthTips
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
        return super(AppointmentDetailSerializer, self).to_representation(instance)
