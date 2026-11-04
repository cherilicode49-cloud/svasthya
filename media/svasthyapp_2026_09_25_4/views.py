import traceback
from django.shortcuts import render
from svasthyapp import models
import io
from rest_framework.parsers import JSONParser
from datetime import datetime, timedelta, date
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import base64
import math, random 
from .serializer import AdminUserSerializer, CorporateSerializer, StaffDepartmentSerializer, StaffSerializer, VendorSerializer, \
    TypeOfAccessSerializer, StaffLevelSerializer, StaffTypeSerializer, AgeCategorySerializer, GenderSerializer, RelationSerializer, TypeOfServiceSerializer, \
    TypeOfVisitSerializer, ParentCompanySerializer, BillingCycleSerializer, WeekdaysSerializer, HolidaysSerializer, PaymentTagsSerializer, EmployeeDetailSerializer, \
    CorporateDataSerializer, PackageDetailSerializer, CenterDetailSerializer, EmployeeDataSerializer, VendorNameSerializer, PackageNameSerializer, HolidayDetailSerializer, \
    StaffDataSerializer, HealthTipsSerializer, EmployeeDependentSerializer, AppointmentDetailSerializer, CenterDataSerializer, IndividualUserDetailSerializer, \
    IndividualDependentSerializer, AdminModuleRightsSerializer, TypeOfIndustrySerializer, PackageVendorSerializer, AppointmentDetailEBPFSerializer, \
    NotificationNameSerializer, NotificationDetailSerializer, TransactionSerializer, AddToCartSerializer, ActiveCenterDetailTransaction, HolidayDetailDateSerializer, CenterTestSerializer, \
    PackageExportSerialiser, CenterExportSerialiser, AppointmentExportSerialiser, TestCategoryTransaction, TestSubCategoryTransaction, TestsProductDetailSerialiser, \
    ComparePackageListSerialiser, EmployeeAddressDetailSerialiser, IndividualAddressDetailSerialiser, CenterDetailSerialiser, HohEmployeeSerializer, DarwinboxCandidateAppointmentSerializer, \
    RescheduleDarwinboxCandidateAppointmentSerializer, RescheduleAppointmentSerializer
from django.core.mail import send_mail

import time
import requests
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import xlrd as xl
import xlrd 
from django.http import JsonResponse
from openpyxl import load_workbook
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from openpyxl.styles import PatternFill
import openpyxl as op
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
from django.db.models import Q
from django.conf import settings
SITE_MEDIA_BASE_URL = settings.SITE_MEDIA_BASE_URL ## BASE URLs for media which is defind in setting.py

from django.shortcuts import render
import threading
import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re

import requests

from django.conf import settings

from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import csv
import io
from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from django.db import transaction
from django.utils.dateparse import parse_date

#### PDF
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.http import HttpResponse
from xhtml2pdf import pisa
import io
from num2words import num2words
# import datetime

import pdfkit
from django.core.files.base import ContentFile
from django.template.loader import get_template

#### Radius code 
from math import cos, radians
from django.db.models import F
from django.db.models.functions import ACos, Cos, Sin, Radians, Cast
from django.db.models import FloatField, ExpressionWrapper


AUTHKEY = "91d8de23a0144ed5"
ENTITY_ID = "1101580270000085391"
SENDER_ID = "VMCLLP"
DLT_TEMPLATE_ID = "1107175370307466562"

def custom_404(request, exception=None):
    return render(request, "404_page.html", status=404)



@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        mobile = str(python_data.get('mobile', None))
        otp = str(python_data.get('otp', None))
        check_user_email = models.AdminUser.objects.filter(email = email).count()
        if check_user_email == 1:
            check_user_otp = models.AdminUser.objects.filter(email = email, otp = otp).count()
            if check_user_otp == 1:
                admin_user = models.AdminUser.objects.filter(email = email, otp = otp).values_list('id', flat=True)[0]

                create_history = models.AdminUserLoginHistory.objects.create(
                    admin_user_id = admin_user,
                    email = email,
                    time = current_time
                ).save()

                res = {
                        'statuscode' : 200,
                        "status":"Success",
                        'message':"User Login Successfully."
                        }
                        
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')   
            else:
                res = {
                        "status":"Failed",
                        'message':"You have entered the wrong PIN."
                        }
                        
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')   
        else:
            res = {
                    "status":"Failed",
                    'message':"You have entered the wrong User."
                    }
                    
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')   



@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        get_data={}
        for i,j in request.FILES.items():
            get_data.update({i:j})

        for i,j in request.POST.items():
            get_data.update({i:j})

        base64_string = get_data.get('data')
        base64_bytes = base64_string.encode("ascii")
        string_bytes = base64.b64decode(base64_bytes)
        python_data = string_bytes.decode("ascii")
        python_data = json.loads(python_data)
        print(python_data, 'python_data')
        user_type = python_data.get('user_type')
        mobile = python_data.get('mobile', None)
        digits = "123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 9)]
        # print(python_data, 'ohrjg')
        # OTP = '111111'

        if user_type == 'admin':
            check_email = models.StaffDetail.objects.filter(mobile = mobile).count()
            if check_email == 1:
                check_status = models.StaffDetail.objects.filter(mobile = mobile, status = 'Active').count()
                if check_status == 1:
                    user = models.StaffDetail.objects.get(mobile = mobile)
                    user.OTP = OTP
                    user.save()

                    message = "Dear User, OTP for login into portal is "+OTP+" and valid till 2 minutes. Do not share this OTP to anyone for security reasons. -Vakare Management Consultants LLP"
                    RecepientMobile = mobile.replace("+91", "").strip()
                    CountryCode = "91"
                    send_sms = requests.get("https://api.authkey.io/request?authkey="+AUTHKEY+"&mobile="+RecepientMobile+"&country_code="+CountryCode+"&sms="+message+"&sender="+SENDER_ID+"&pe_id="+ENTITY_ID+"&template_id="+DLT_TEMPLATE_ID)

                    # print("SMS RESPOSNSE-=-=-=-=-=---->",send_sms)

                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':'OTP send successfully.',
                        'otp' : OTP
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "You're account is inactive, Please contact with admin."
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json')        
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Valid Mobile Number."
                    }
                data = json.dumps(res)
                encoded_dict = str(data).encode('utf-8')
                data = base64.b64encode(encoded_dict)
                json_data = JSONRenderer().render(data)
                return HttpResponse(json_data, content_type= 'application/json')       
        
        elif user_type == 'vendor':
            vendor_code = python_data.get('vendor_code')
            email = python_data.get('email', None)
            mobile = python_data.get('mobile', None)
            vendor_id = models.VendorDetail.objects.filter(vendor_code=vendor_code).values_list('id', flat=True)[0]
            
            if email != None:

                check_email = models.VendorDetail.objects.filter(id=vendor_id, email = email).count()
                if check_email == 1:
                    check_status = models.VendorDetail.objects.filter(id=vendor_id, email = email, status = 'Active').count()
                    if check_status == 1:
                        vendor = models.VendorDetail.objects.get(email = email)
                        vendor.OTP = OTP
                        vendor.save()

                        res = {
                            'statuscode' : 200,
                            'status':'Success',
                            'message':'OTP send successfully.',
                            'otp' : OTP
                            }
                        data = json.dumps(res)
                        encoded_dict = str(data).encode('utf-8')
                        data = base64.b64encode(encoded_dict)
                        json_data = JSONRenderer().render(data)
                        return HttpResponse(json_data, content_type= 'application/json')       
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "You're account is inactive, Please contact with admin."
                            }
                        data = json.dumps(res)
                        encoded_dict = str(data).encode('utf-8')
                        data = base64.b64encode(encoded_dict)
                        json_data = JSONRenderer().render(data)
                        return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Email."
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json')       
        
            elif mobile != None:
                check_email = models.VendorDetail.objects.filter(id=vendor_id, mobile = mobile).count()
                if check_email == 1:
                    check_status = models.VendorDetail.objects.filter(id=vendor_id, mobile = mobile, status = 'Active').count()
                    if check_status == 1:
                        vendor = models.VendorDetail.objects.get(mobile = mobile)
                        vendor.OTP = OTP
                        vendor.save()
 
                        message = "Dear User, OTP for login into portal is "+OTP+" and valid till 2 minutes. Do not share this OTP to anyone for security reasons. -Vakare Management Consultants LLP"
                        RecepientMobile = mobile.replace("+91", "").strip()
                        CountryCode = "91"
                        send_sms = requests.get("https://api.authkey.io/request?authkey="+AUTHKEY+"&mobile="+RecepientMobile+"&country_code="+CountryCode+"&sms="+message+"&sender="+SENDER_ID+"&pe_id="+ENTITY_ID+"&template_id="+DLT_TEMPLATE_ID)


                        res = {
                            'statuscode' : 200,
                            'status':'Success',
                            'message':'OTP send successfully.',
                            'otp' : OTP
                            }
                        data = json.dumps(res)
                        encoded_dict = str(data).encode('utf-8')
                        data = base64.b64encode(encoded_dict)
                        json_data = JSONRenderer().render(data)
                        return HttpResponse(json_data, content_type= 'application/json')     
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "You're account is inactive, Please contact with admin."
                            }
                        data = json.dumps(res)
                        encoded_dict = str(data).encode('utf-8')
                        data = base64.b64encode(encoded_dict)
                        json_data = JSONRenderer().render(data)
                        return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Mobile."
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json')       


        elif user_type == 'employee':
            corporate_code = python_data.get('corporate_code')
            email = python_data.get('email', None)
            mobile = python_data.get('mobile', None)
            corporate_id = models.CorporateDetail.objects.filter(corporate_code=corporate_code).values_list('id', flat=True)[0]
            # print(corporate_id, 'corporate_id')
            if email != None:
                # print(1)

                check_email = models.EmployeeDetail.objects.filter(corporate_id=corporate_id, email = email).count()
                if check_email == 1:
                    check_status = models.EmployeeDetail.objects.filter(corporate_id=corporate_id, email = email, status = 'Active').count()
                    if check_status == 1:
                        employee = models.EmployeeDetail.objects.get(email = email)
                        employee.OTP = OTP
                        employee.save()

                        res = {
                            'statuscode' : 200,
                            'status':'Success',
                            'message':'OTP send successfully.',
                            'otp' : OTP
                            }
                        data = json.dumps(res)
                        encoded_dict = str(data).encode('utf-8')
                        data = base64.b64encode(encoded_dict)
                        json_data = JSONRenderer().render(data)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "You're account is inactive, Please contact with admin."
                            }
                        data = json.dumps(res)
                        encoded_dict = str(data).encode('utf-8')
                        data = base64.b64encode(encoded_dict)
                        json_data = JSONRenderer().render(data)
                        return HttpResponse(json_data, content_type= 'application/json')             
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Email."
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json')       
            
            elif mobile != None:
                check_email = models.EmployeeDetail.objects.filter(corporate_id=corporate_id, mobile = mobile).count()
                # print(check_email, 'check_email')
                if check_email == 1:
                    check_status = models.EmployeeDetail.objects.filter(corporate_id=corporate_id, mobile = mobile, status = 'Active').count()
                    if check_status == 1:
                        employee = models.EmployeeDetail.objects.get(mobile = mobile)
                        employee.OTP = OTP
                        employee.save()
                        
                        message = "Dear User, OTP for login into portal is "+OTP+" and valid till 2 minutes. Do not share this OTP to anyone for security reasons. -Vakare Management Consultants LLP"
                        RecepientMobile = mobile.replace("+91", "").strip()
                        CountryCode = "91"
                        send_sms = requests.get("https://api.authkey.io/request?authkey="+AUTHKEY+"&mobile="+RecepientMobile+"&country_code="+CountryCode+"&sms="+message+"&sender="+SENDER_ID+"&pe_id="+ENTITY_ID+"&template_id="+DLT_TEMPLATE_ID)


                        res = {
                            'statuscode' : 200,
                            'status':'Success',
                            'message':'OTP send successfully.',
                            'otp' : OTP
                            }
                        data = json.dumps(res)
                        encoded_dict = str(data).encode('utf-8')
                        data = base64.b64encode(encoded_dict)
                        json_data = JSONRenderer().render(data)
                        return HttpResponse(json_data, content_type= 'application/json')    
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "You're account is inactive, Please contact with admin."
                            }
                        data = json.dumps(res)
                        encoded_dict = str(data).encode('utf-8')
                        data = base64.b64encode(encoded_dict)
                        json_data = JSONRenderer().render(data)
                        return HttpResponse(json_data, content_type= 'application/json')         
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Mobile."
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json')       
        
        elif user_type == 'individual':
            check_email = models.IndividualUserDetail.objects.filter(mobile = mobile).count()
            if check_email == 1:
                check_status = models.IndividualUserDetail.objects.filter(mobile = mobile, status = 'Active').count()
                if check_status == 1:
                    user = models.IndividualUserDetail.objects.get(mobile = mobile)
                    user.OTP = OTP
                    user.save()
                    message = "Dear User, OTP for login into portal is "+OTP+" and valid till 2 minutes. Do not share this OTP to anyone for security reasons. -Vakare Management Consultants LLP"
                    RecepientMobile = mobile.replace("+91", "").strip()
                    CountryCode = "91"
                    send_sms = requests.get("https://api.authkey.io/request?authkey="+AUTHKEY+"&mobile="+RecepientMobile+"&country_code="+CountryCode+"&sms="+message+"&sender="+SENDER_ID+"&pe_id="+ENTITY_ID+"&template_id="+DLT_TEMPLATE_ID)
                    # print(send_sms, 'send_smssend_smssend_sms')

                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':'OTP send successfully.',
                        'otp' : OTP
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "You're account is inactive, Please contact with admin."
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json')        
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Valid Mobile Number."
                    }
                data = json.dumps(res)
                encoded_dict = str(data).encode('utf-8')
                data = base64.b64encode(encoded_dict)
                json_data = JSONRenderer().render(data)
                return HttpResponse(json_data, content_type= 'application/json')       
        
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid user type."
                }
            data = json.dumps(res)
            encoded_dict = str(data).encode('utf-8')
            data = base64.b64encode(encoded_dict)
            json_data = JSONRenderer().render(data)
            return HttpResponse(json_data, content_type= 'application/json')   


@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        get_data={}
        for i,j in request.FILES.items():
            get_data.update({i:j})

        for i,j in request.POST.items():
            get_data.update({i:j})

        base64_string = get_data.get('data')
        base64_bytes = base64_string.encode("ascii")
        string_bytes = base64.b64decode(base64_bytes)
        python_data = string_bytes.decode("ascii")
        python_data = json.loads(python_data)


        user_type = python_data.get('user_type')
        mobile = python_data.get('mobile', None)
        OTP = python_data.get('OTP')
    
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        
        if user_type == 'admin':
            check_mobile = models.StaffDetail.objects.filter(mobile = mobile).count()
            if check_mobile == 1:
                get_otp = models.StaffDetail.objects.filter(mobile = mobile).values_list('OTP', flat=True)[0]
                if get_otp == OTP:
                    staff = models.StaffDetail.objects.get(mobile = mobile)
                    staff_email = staff.email
                    staff_user = staff.id
                    serialiser = StaffSerializer(staff)
                    staff_data = serialiser.data
                    staff_data.update({'user_type':user_type})

                    create_history = models.StaffLoginHistory.objects.create(
                        staff_id = staff_user,
                        email = staff_email,
                        time = current_time
                    ).save() 

                    get_all_access = models.AdminModuleRights.objects.filter(staff_id = staff_user)
                    serialiser = AdminModuleRightsSerializer(get_all_access, many=True)

                    all_data = serialiser.data
                    list_data = []
                    for data in all_data:
                        data_dict = {}
                        module = data.get('module')
                        data_dict.update({module:data})
                        list_data.append(data_dict)

                    # rights =

                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':"Login Successfully." ,
                        'data':staff_data,
                        'rights': list_data
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message':"You've Entered wrong OTP." 
                        }           
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json')       
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Valid Email."
                    }
                data = json.dumps(res)
                encoded_dict = str(data).encode('utf-8')
                data = base64.b64encode(encoded_dict)
                json_data = JSONRenderer().render(data)
                return HttpResponse(json_data, content_type= 'application/json') 
        
        elif user_type == 'vendor':
            email = python_data.get('email', None)
            mobile = python_data.get('mobile', None)
            if email != None:
                check_email = models.VendorDetail.objects.filter(email = email).count()
                if check_email == 1:
                    active_user = models.VendorDetail.objects.filter(email = email, status = 'Active').count()
                    if active_user == 1:
                        get_otp = models.VendorDetail.objects.filter(email = email).values_list('OTP', flat=True)[0]
                        if get_otp == OTP:
                            vendor = models.VendorDetail.objects.get(email = email)
                            
                            vendor_id = vendor.id
                            serialiser = VendorSerializer(vendor)
                            data = serialiser.data
                            data.update({'user_type':user_type})

                            create_history = models.VendorLoginHistory.objects.create(
                                vendor_id = vendor_id,
                                email = email,
                                time = current_time
                            ).save()
                            res = {
                                'statuscode' : 200,
                                'status':'Success',
                                'message':"Login Successfully." ,
                                'data':data
                                }
                            data = json.dumps(res)
                            encoded_dict = str(data).encode('utf-8')
                            data = base64.b64encode(encoded_dict)
                            json_data = JSONRenderer().render(data)
                            return HttpResponse(json_data, content_type= 'application/json')       
                        else:
                            res = {
                                'statuscode' : 406,
                                'status':'false',
                                'message':"You've Entered wrong OTP." 
                                }                     
                            data = json.dumps(res)
                            encoded_dict = str(data).encode('utf-8')
                            data = base64.b64encode(encoded_dict)
                            json_data = JSONRenderer().render(data)
                            return HttpResponse(json_data, content_type= 'application/json')   
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message':"You're account currently Inactive." 
                            }
                        data = json.dumps(res)
                        encoded_dict = str(data).encode('utf-8')
                        data = base64.b64encode(encoded_dict)
                        json_data = JSONRenderer().render(data)
                        return HttpResponse(json_data, content_type= 'application/json')   
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Email."
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json') 
            
            elif mobile != None:
                check_email = models.VendorDetail.objects.filter(mobile = mobile).count()
                if check_email == 1:
                    
                    active_user = models.VendorDetail.objects.filter(mobile = mobile, status = 'Active').count()
                    if active_user == 1:
                        get_otp = models.VendorDetail.objects.filter(mobile = mobile).values_list('OTP', flat=True)[0]
                        if get_otp == OTP:
                            vendor = models.VendorDetail.objects.get(mobile = mobile)
                            
                            vendor_id = vendor.id
                            serialiser = VendorSerializer(vendor)
                            data = serialiser.data
                            data.update({'user_type':user_type})

                            create_history = models.VendorLoginHistory.objects.create(
                                vendor_id = vendor_id,
                                email = mobile,
                                time = current_time
                            ).save()
                            res = {
                                'statuscode' : 200,
                                'status':'Success',
                                'message':"Login Successfully." ,
                                'data':data
                                }
                            data = json.dumps(res)
                            encoded_dict = str(data).encode('utf-8')
                            data = base64.b64encode(encoded_dict)
                            json_data = JSONRenderer().render(data) 
                            return HttpResponse(json_data, content_type= 'application/json')       
                        else:
                            res = {
                                'statuscode' : 406,
                                'status':'false',
                                'message':"You've Entered wrong OTP." 
                                }
                            data = json.dumps(res)
                            encoded_dict = str(data).encode('utf-8')
                            data = base64.b64encode(encoded_dict)
                            json_data = JSONRenderer().render(data)
                            return HttpResponse(json_data, content_type= 'application/json')   
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message':"You've account currently Inactive." 
                            }
                        data = json.dumps(res)
                        encoded_dict = str(data).encode('utf-8')
                        data = base64.b64encode(encoded_dict)
                        json_data = JSONRenderer().render(data)
                        return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Mobile."
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json') 
                    
        elif user_type == 'employee':
            email = python_data.get('email', None)
            mobile = python_data.get('mobile', None)
            if email != None:
                check_email = models.EmployeeDetail.objects.filter(email = email).count()
                if check_email == 1:
                    active_user = models.EmployeeDetail.objects.filter(email = email, status = 'Active').count()
                    if active_user == 1:

                        get_otp = models.EmployeeDetail.objects.filter(email = email).values_list('OTP', flat=True)[0]
                        if get_otp == OTP:
                            employee = models.EmployeeDetail.objects.get(email = email)
                            
                            employee_id = employee.id
                            login_via = employee.corporate.login_via
                            serialiser = EmployeeDetailSerializer(employee)
                            data = serialiser.data
                            data.update({'login_via':login_via, 'user_type':user_type})


                            create_history = models.EmployeeLoginHistory.objects.create(
                                employee_id = employee_id,
                                email = email,
                                time = current_time
                            ).save()

                            res = {
                                'statuscode' : 200,
                                'status':'Success',
                                'message':"Login Successfully." ,
                                'data':data
                                }
                            data = json.dumps(res)
                            encoded_dict = str(data).encode('utf-8')
                            data = base64.b64encode(encoded_dict)
                            json_data = JSONRenderer().render(data)
                            return HttpResponse(json_data, content_type= 'application/json')       
                        else:
                            res = {
                                'statuscode' : 406,
                                'status':'false',
                                'message':"You've Entered wrong OTP." 
                                }
                            data = json.dumps(res)
                            encoded_dict = str(data).encode('utf-8')
                            data = base64.b64encode(encoded_dict)
                            json_data = JSONRenderer().render(data)
                            return HttpResponse(json_data, content_type= 'application/json')       
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message':"You've account currently Inactive." 
                            }
                        data = json.dumps(res)
                        encoded_dict = str(data).encode('utf-8')
                        data = base64.b64encode(encoded_dict)
                        json_data = JSONRenderer().render(data)
                        return HttpResponse(json_data, content_type= 'application/json')   
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Email."
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json') 

            elif mobile != None:
                check_mobile = models.EmployeeDetail.objects.filter(mobile = mobile).count()
                if check_mobile == 1:
                    active_user = models.EmployeeDetail.objects.filter(mobile = mobile, status = 'Active').count()
                    if active_user == 1:
                        get_otp = models.EmployeeDetail.objects.filter(mobile = mobile).values_list('OTP', flat=True)[0]
                        if get_otp == OTP:
                            employee = models.EmployeeDetail.objects.get(mobile = mobile)
                            
                            employee_id = employee.id
                            login_via = employee.corporate.login_via

                            serialiser = EmployeeDetailSerializer(employee)
                            data = serialiser.data
                            data.update({'login_via':login_via, 'user_type':user_type})

                            create_history = models.EmployeeLoginHistory.objects.create(
                                employee_id = employee_id,
                                email = mobile,
                                time = current_time
                            ).save()
                            res = {
                                'statuscode' : 200,
                                'status':'Success',
                                'message':"Login Successfully." ,
                                'data':data
                                }                                                        
                            data = json.dumps(res)
                            encoded_dict = str(data).encode('utf-8')
                            data = base64.b64encode(encoded_dict)
                            json_data = JSONRenderer().render(data)
                            return HttpResponse(json_data, content_type= 'application/json')       
                        else:
                            res = {
                                'statuscode' : 406,
                                'status':'false',
                                'message':"You've Entered wrong OTP." 
                                }
                            data = json.dumps(res)
                            encoded_dict = str(data).encode('utf-8')
                            data = base64.b64encode(encoded_dict)
                            json_data = JSONRenderer().render(data)
                            return HttpResponse(json_data, content_type= 'application/json')       
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message':"You've account currently Inactive." 
                            }                       
                        data = json.dumps(res)
                        encoded_dict = str(data).encode('utf-8')
                        data = base64.b64encode(encoded_dict)
                        json_data = JSONRenderer().render(data)
                        return HttpResponse(json_data, content_type= 'application/json')   
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Mobile Number."
                        }   
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json') 
        
        elif user_type == 'individual':
            check_mobile = models.IndividualUserDetail.objects.filter(mobile = mobile).count()
            if check_mobile == 1:
                get_otp = models.IndividualUserDetail.objects.filter(mobile = mobile).values_list('OTP', flat=True)[0]
                if get_otp == OTP:
                    user_data = models.IndividualUserDetail.objects.get(mobile = mobile)
                    mobile = user_data.mobile
                    user = user_data.id
                    serialiser = IndividualUserDetailSerializer(user_data)
                    data = serialiser.data
                    data.update({'user_type':user_type})

                    create_history = models.IndividualLoginHistory.objects.create(
                        user_id = user,
                        mobile = mobile,
                        time = current_time
                    ).save() 
                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':"Login Successfully." ,
                        'data':data
                        }
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message':"You've Entered wrong OTP." 
                        }           
                    data = json.dumps(res)
                    encoded_dict = str(data).encode('utf-8')
                    data = base64.b64encode(encoded_dict)
                    json_data = JSONRenderer().render(data)
                    return HttpResponse(json_data, content_type= 'application/json')       
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Valid Email."
                    }
                data = json.dumps(res)
                encoded_dict = str(data).encode('utf-8')
                data = base64.b64encode(encoded_dict)
                json_data = JSONRenderer().render(data)
                return HttpResponse(json_data, content_type= 'application/json') 
        


        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid User Type."
                }           
            data = json.dumps(res)
            encoded_dict = str(data).encode('utf-8')
            data = base64.b64encode(encoded_dict)
            json_data = JSONRenderer().render(data)
            return HttpResponse(json_data, content_type= 'application/json') 
    


@csrf_exempt
def staff_register(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))

        mobile = python_data.get('mobile')
        email = python_data.get('email')
        staff_code = python_data.get('staff_code')
        
        # print(python_data, 'python_data')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_mobile = models.StaffDetail.objects.filter(mobile = mobile).count()
        if check_mobile == 0:
            check_email = models.StaffDetail.objects.filter(email = email).count()
            # if email == None:
            
            if check_email == 0:
                check_staff_code = models.StaffDetail.objects.filter(staff_code = staff_code).count()
                if check_staff_code == 0:
                    staff = models.StaffDetail.objects.create(
                        name = python_data.get('name'),
                        staff_code = str(python_data.get('staff_code')).upper(),
                        department_id = python_data.get('department'),
                        type_of_access_id = python_data.get('type_of_access'),
                        staff_type_id = python_data.get('staff_type'),
                        staff_level_id = python_data.get('staff_level'),
                        mobile = python_data.get('mobile'),
                        email = python_data.get('email'),
                        assign_to = python_data.get('assign_to'),
                        
                        staff_access = python_data.get('staff_access'),
                        status = 'Active',
                        created_at = current_time
                    )
                    staff.save()
                    get_staff_id = staff.id
                    # get_type_of_access = staff.type_of_access_id.type_of_access
                    get_type_of_access = models.TypeOfAccess.objects.filter(id = staff.type_of_access_id).values_list('type_of_access', flat=True)[0]

                    
                    if get_type_of_access == 'Super Admin': 
                        get_all_module = models.Module.objects.all()
                        for module in get_all_module:
                            module_id = module.id
                            
                            admin_rights = models.AdminModuleRights.objects.create(
                                module_id = module_id,
                                staff_id = get_staff_id,
                                module_access = 'active',
                                edit_access = 'active',
                                view_access = 'active',
                                delete_access = 'active',
                                created_at = current_time
                            )
                            admin_rights.save()

                    elif get_type_of_access == 'Admin':
                        get_staff_access = staff.staff_access
                        if get_staff_access == 'All Access': 
                            get_all_module = models.Module.objects.all()
                            for module in get_all_module:
                                module_id = module.id
                                module_name = module.module
                                if module_name == 'Staff' or module_name == 'Holiday':
                                    admin_rights = models.AdminModuleRights.objects.create(
                                        module_id = module_id,
                                        staff_id = get_staff_id,
                                        module_access = 'active',
                                        edit_access = 'inactive',
                                        view_access = 'active',
                                        delete_access = 'inactive',
                                        created_at = current_time
                                    )
                                    admin_rights.save()
                                else:
                                    admin_rights = models.AdminModuleRights.objects.create(
                                        module_id = module_id,
                                        staff_id = get_staff_id,
                                        module_access = 'active',
                                        edit_access = 'active',
                                        view_access = 'active',
                                        delete_access = 'active',
                                        created_at = current_time
                                    )
                                    admin_rights.save()

                        elif get_staff_access == 'Only View': 
                            get_all_module = models.Module.objects.all()
                            for module in get_all_module:
                                module_id = module.id
                                admin_rights = models.AdminModuleRights.objects.create(
                                    module_id = module_id,
                                    staff_id = get_staff_id,
                                    module_access = 'active',
                                    edit_access = 'inactive',
                                    view_access = 'active',
                                    delete_access = 'inactive',
                                    created_at = current_time
                                )
                                admin_rights.save()

                    elif get_type_of_access == 'Staff':
                        get_all_module = models.Module.objects.all()
                        for module in get_all_module:
                            module_id = module.id
                            module_name = module.module
                            if module_name == 'Corporate' or module_name == 'Appointment' or module_name == 'Employee':
                                admin_rights = models.AdminModuleRights.objects.create(
                                    module_id = module_id,
                                    staff_id = get_staff_id,
                                    module_access = 'active',
                                    edit_access = 'active',
                                    view_access = 'active',
                                    delete_access = 'active',
                                    created_at = current_time
                                )
                                admin_rights.save()
                            else:
                                admin_rights = models.AdminModuleRights.objects.create(
                                    module_id = module_id,
                                    staff_id = get_staff_id,
                                    module_access = 'inactive',
                                    edit_access = 'inactive',
                                    view_access = 'inactive',
                                    delete_access = 'inactive',
                                    created_at = current_time
                                )
                                admin_rights.save()

                    elif get_type_of_access == 'Designer':
                        get_all_module = models.Module.objects.all()
                        for module in get_all_module:
                            module_id = module.id
                            
                            admin_rights = models.AdminModuleRights.objects.create(
                                module_id = module_id,
                                staff_id = get_staff_id,
                                module_access = 'active',
                                edit_access = 'inactive',
                                view_access = 'active',
                                delete_access = 'inactive',
                                created_at = current_time
                            )
                            admin_rights.save()
                    
                    else:
                        get_all_module = models.Module.objects.all()
                        for module in get_all_module:
                            module_id = module.id
                            
                            admin_rights = models.AdminModuleRights.objects.create(
                                module_id = module_id,
                                staff_id = get_staff_id,
                                module_access = 'active',
                                edit_access = 'inactive',
                                view_access = 'active',
                                delete_access = 'inactive',
                                created_at = current_time
                            )
                            admin_rights.save()


                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Staff Added Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Staff Code Already registered, Please try with other."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Email Already registered, Please try with other."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Mobile Number Already registered, Please try with other."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def staff_status_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_staff = models.StaffDetail.objects.filter(id = id).count()
        if check_staff == 1:
            staff = models.StaffDetail.objects.get(id = id)
            staff.status = status
            staff.save()

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Status Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Staff."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def staff_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        mobile = python_data.get('mobile')
        
        check_staff = models.StaffDetail.objects.filter(id = id).count()
        if check_staff == 1:
            check_mobile = models.StaffDetail.objects.filter(id = id, mobile = mobile).count()
            if check_mobile == 1:
                staff = models.StaffDetail.objects.get(id = id)
                staff.name = python_data.get('name', staff.name)
                staff.mobile = python_data.get('mobile', staff.mobile)
                staff.email = python_data.get('email', staff.email)
                staff.assign_to = python_data.get('assign_to', staff.assign_to)
                
                staff.staff_code = str(python_data.get('staff_code', staff.staff_code)).upper()
                staff.staff_type_id = python_data.get('staff_type', staff.staff_type)
                staff.department_id = python_data.get('department', staff.department)
                staff.type_of_access_id = python_data.get('type_of_access', staff.type_of_access)
                staff.staff_level_id = python_data.get('staff_level', staff.staff_level)
                staff.staff_access = python_data.get('staff_access', staff.staff_access)
                staff.save()

                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Staff Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
            else:
                check_mobile = models.StaffDetail.objects.filter(mobile = mobile).count()
                if check_mobile == 0:
                    staff = models.StaffDetail.objects.get(id = id)
                    staff.name = python_data.get('name', staff.name)
                    staff.mobile = python_data.get('mobile', staff.mobile)
                    staff.email = python_data.get('email', staff.email)
                    staff.assign_to = python_data.get('assign_to', staff.assign_to)
                    
                    staff.staff_code = str(python_data.get('staff_code', staff.staff_code)).upper()
                    staff.staff_type_id = python_data.get('staff_type', staff.staff_type)
                    staff.department_id = python_data.get('department', staff.department)
                    staff.type_of_access_id = python_data.get('type_of_access', staff.type_of_access)
                    staff.staff_level_id = python_data.get('staff_level', staff.staff_level)
                    staff.staff_access = python_data.get('staff_access', staff.staff_access)
                    staff.save()

                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Staff Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter mobile number already register."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 


        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Staff."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def staff_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        staff = python_data.get('id')
        status = python_data.get('status')
        check_status = models.StaffDetail.objects.filter(id = staff).count()
        if check_status == 1:
            staff_details = models.StaffDetail.objects.get(id = staff)
            staff_details.status = status
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Status Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def staff_profile_image_update(request):
    if request.method == 'POST':
        python_data={}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})
        
        staff = python_data.get('staff')
        profile_image = python_data.get('profile_image')
        check_emp = models.StaffDetail.objects.filter(id = staff).count()
        if check_emp == 1:
            staff = models.StaffDetail.objects.get(id = staff)
            if type(python_data.get('profile_image', staff.profile_image)) != str: 
                staff.profile_image = python_data.get('profile_image', staff.profile_image)
            staff.save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Profile Image Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Staff."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def list_all_staff(request):
    if request.method == 'POST':
        all_staff = models.StaffDetail.objects.all().order_by('-id')
        serialiser = StaffSerializer(all_staff, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def list_only_staff(request):
    if request.method == 'POST':
        all_staff_type = models.StaffType.objects.all()
        list_type = []
        for staff_type in all_staff_type:
            if staff_type.staff_type != 'Super Admin' and staff_type.staff_type != 'Admin':  
                list_type.append(staff_type.id)

        list_data = []
        for single_type in list_type:
            all_staff = models.StaffDetail.objects.filter(staff_type = single_type)
            serialiser = StaffDataSerializer(all_staff, many=True)
            list_data.append(serialiser.data)
        
        
        merged_list = [item for sublist in list_data for item in sublist]

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : merged_list
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def active_all_staff(request):
    if request.method == 'POST':
        all_staff = models.StaffDetail.objects.filter(status='Active').order_by('-id')
        serialiser = StaffSerializer(all_staff, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def corporate_register(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        mobile = python_data.get('mobile')
        email = python_data.get('email')
        corporate_code = python_data.get('corporate_code')
        
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_corporate_code = models.CorporateDetail.objects.filter(corporate_code = corporate_code).count()
        if check_corporate_code == 0:
        
            check_mobile = models.CorporateDetail.objects.filter(mobile = mobile).count()
            if check_mobile == 0:
                check_email = models.CorporateDetail.objects.filter(email = email).count()
                if check_email == 0:
                    check_corporate_code = models.CorporateDetail.objects.filter(corporate_code = corporate_code).count()
                    if check_corporate_code == 0:
                        corporate = models.CorporateDetail.objects.create(
                            parent_company_id = python_data.get('parent_company', None),
                            corporate_name = python_data.get('corporate_name'),
                            corporate_code = str(python_data.get('corporate_code')).upper(),
                            
                            type_of_corporation = python_data.get('type_of_corporation'),
                            industry_id = python_data.get('industry'),
                            spoke_person = python_data.get('spoke_person'),
                            mobile = python_data.get('mobile'),
                            email = python_data.get('email'),
                            pan_card = python_data.get('pan_card'),
                            GST_no = python_data.get('GST_no'),
                            billing_cycle_id = python_data.get('billing_cycle'),
                            start_date = python_data.get('start_date'),
                            end_date = python_data.get('end_date'),
                            address = python_data.get('address'),
                            pincode = python_data.get('pincode'),
                            state = python_data.get('state'),
                            city = python_data.get('city'),
                            billing_email = python_data.get('billing_email'),
                            
                            # level1_id = python_data.get('level1'),
                            # level2_id = python_data.get('level2'),
                            login_via = python_data.get('login_via'),
                            status = 'Active',
                            created_at = current_time
                        )
                        corporate.save()

                        if python_data.get('level1') == '':
                            corporate.level1.set([])
                        else:
                            corporate.level1.set((python_data.get('level1', corporate.level1)))
                        
                        if python_data.get('level2') == '':
                            corporate.level2.set([])
                        else:
                            corporate.level2.set((python_data.get('level2', corporate.level2)))
                        

                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Corporate Added Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "Enter Code Already registered, Please try with other."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Email Already registered, Please try with other."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 

            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Mobile Number Already registered, Please try with other."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Corporate Code Already registered, Please try with other."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 





@csrf_exempt
def corporate_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        
        mobile = python_data.get('mobile')
        check_coporate = models.CorporateDetail.objects.filter(id = id, mobile= mobile).count()
        if check_coporate == 1:
            corporate = models.CorporateDetail.objects.get(id = id)
            corporate.parent_company_id = python_data.get('parent_company', corporate.parent_company)
            # corporate.corporate_code = python_data.get('corporate_code', corporate.corporate_code).upper()
            corporate.corporate_name = python_data.get('corporate_name', corporate.corporate_name)
            corporate.type_of_corporation = python_data.get('type_of_corporation', corporate.type_of_corporation)
            corporate.industry_id = python_data.get('industry', corporate.industry)
            corporate.spoke_person = python_data.get('spoke_person', corporate.spoke_person)
            corporate.pan_card = python_data.get('pan_card', corporate.pan_card)
            corporate.GST_no = python_data.get('GST_no', corporate.GST_no)
            corporate.billing_cycle_id = python_data.get('billing_cycle', corporate.billing_cycle)
            corporate.start_date = python_data.get('start_date', corporate.start_date)
            corporate.end_date = python_data.get('end_date', corporate.end_date)
            corporate.address = python_data.get('address', corporate.address)
            corporate.pincode = python_data.get('pincode', corporate.pincode)
            corporate.state = python_data.get('state', corporate.state)
            corporate.city = python_data.get('city', corporate.city)
            corporate.billing_email = python_data.get('billing_email', corporate.billing_email)
            # corporate.level1_id = python_data.get('level1', corporate.level1)
            # corporate.level2_id = python_data.get('level2', corporate.level2)
            corporate.login_via = python_data.get('login_via', corporate.login_via)
            corporate.save()

            if python_data.get('level1') == '':
                corporate.level1.set([])
            else:
                corporate.level1.set((python_data.get('level1', corporate.level1)))
            
            if python_data.get('level2') == '':
                corporate.level2.set([])
            else:
                corporate.level2.set((python_data.get('level2', corporate.level2)))
                    

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Corporate Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            check_mobile = models.CorporateDetail.objects.filter(mobile = mobile).count()
            if check_mobile == 0:
                corporate = models.CorporateDetail.objects.get(id = id)
                corporate.parent_company_id = python_data.get('parent_company', corporate.parent_company)
                # corporate.corporate_code = python_data.get('corporate_code', corporate.corporate_code).upper()
                corporate.mobile = python_data.get('mobile', corporate.mobile)
                corporate.corporate_name = python_data.get('corporate_name', corporate.corporate_name)
                corporate.type_of_corporation = python_data.get('type_of_corporation', corporate.type_of_corporation)
                corporate.industry_id = python_data.get('industry', corporate.industry)
                corporate.spoke_person = python_data.get('spoke_person', corporate.spoke_person)
                corporate.pan_card = python_data.get('pan_card', corporate.pan_card)
                corporate.GST_no = python_data.get('GST_no', corporate.GST_no)
                corporate.billing_cycle_id = python_data.get('billing_cycle', corporate.billing_cycle)
                corporate.start_date = python_data.get('start_date', corporate.start_date)
                corporate.end_date = python_data.get('end_date', corporate.end_date)
                corporate.address = python_data.get('address', corporate.address)
                corporate.pincode = python_data.get('pincode', corporate.pincode)
                corporate.state = python_data.get('state', corporate.state)
                corporate.city = python_data.get('city', corporate.city)
                corporate.billing_email = python_data.get('billing_email', corporate.billing_email)
                # corporate.level1_id = python_data.get('level1', corporate.level1)
                # corporate.level2_id = python_data.get('level2', corporate.level2)
                corporate.login_via = python_data.get('login_via', corporate.login_via)
                corporate.save()

                if python_data.get('level1') == '':
                    corporate.level1.set([])
                else:
                    corporate.level1.set((python_data.get('level1', corporate.level1)))
                
                if python_data.get('level2') == '':
                    corporate.level2.set([])
                else:
                    corporate.level2.set((python_data.get('level2', corporate.level2)))
                
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Corporate Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Mobile is already Registered."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def corporate_status_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_corporate = models.CorporateDetail.objects.filter(id = id).count()
        if check_corporate == 1:
            corporate = models.CorporateDetail.objects.get(id = id)
            corporate.status = status
            corporate.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : 'Corporate status update Successfully.'
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 






# @csrf_exempt
# def list_all_corporate(request):
#     if request.method == 'POST':
#         all_corporate = models.CorporateDetail.objects.all().order_by('-id')
#         serialiser = CorporateSerializer(all_corporate, many=True)
        
#         res = {
#             'statuscode' : 200,
#             'status':'true',
#             'data' : serialiser.data
#             }
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type= 'application/json') 





@csrf_exempt
def list_all_corporate(request):
    if request.method == 'POST':
        # json_data = request.body
        # stream = io.BytesIO(json_data)
        # python_data = JSONParser().parse(stream)
        get_data={}
        for i,j in request.FILES.items():
            get_data.update({i:j})
        
        for i,j in request.POST.items():
            get_data.update({i:j})

        base64_string = get_data.get('data')
        base64_bytes = base64_string.encode("ascii")
        string_bytes = base64.b64decode(base64_bytes)
        python_data = string_bytes.decode("ascii")
        python_data = json.loads(python_data)


        id = python_data.get('id')

        page_number = int(python_data.get('page_number',1))
        row_size = int(python_data.get('row_size',10))
        last_row = row_size * page_number
        first_row = last_row - row_size

        
        corporate_code = python_data.get('corporate_code',None)
        parent_company_name = python_data.get('parent_company_name',None)
        corporate_name = python_data.get('corporate_name',None)
        start_date = python_data.get('start_date',None)
        billing_cycle_name = python_data.get('billing_cycle_name',None)
        spoke_person = python_data.get('spoke_person',None)
        mobile = python_data.get('mobile',None)
        status = python_data.get('status',None)

        filter_condition = {}

        if corporate_code not in [None,'','null']:
            filter_condition['corporate_code__icontains'] = corporate_code
        if parent_company_name not in [None,'','null']:
            filter_condition['parent_company__parent_company__icontains'] = parent_company_name
        if corporate_name not in [None,'','null']:
            filter_condition['corporate_name__icontains'] = corporate_name
        if start_date not in [None,'','null']:
            filter_condition['start_date__gte'] = start_date
        
        if billing_cycle_name not in [None,'','null']:
            filter_condition['billing_cycle__billing_cycle__icontains'] = billing_cycle_name
        if spoke_person not in [None,'','null']:
            filter_condition['spoke_person__icontains'] = spoke_person
        if mobile not in [None,'','null']:
            filter_condition['mobile__icontains'] = mobile
        if status not in [None,'','null']:
            if status != 'All':
                filter_condition['status'] = status



        check_staff = models.StaffDetail.objects.filter(id = id).count()
        if check_staff == 1:
            staff_id = models.StaffDetail.objects.get(id = id)
            get_type_access = staff_id.type_of_access.type_of_access
            if get_type_access == 'Super Admin' or get_type_access == 'Admin': 
                total_records = models.CorporateDetail.objects.filter(**filter_condition).order_by('-id').count()
                all_corporate = models.CorporateDetail.objects.filter(**filter_condition).order_by('-id')[first_row:last_row]
                serialiser = CorporateSerializer(all_corporate, many=True)
            else:
                total_records = models.CorporateDetail.objects.filter(Q(level1 =staff_id) | Q(level2 =staff_id ), **filter_condition).distinct().count()
                all_corporate = models.CorporateDetail.objects.filter(Q(level1 =staff_id) | Q(level2 =staff_id ), **filter_condition).distinct()[first_row:last_row]

                serialiser = CorporateSerializer(all_corporate, many=True)

            res = {
                'statuscode' : 200,
                'status':'true',
                'data' : serialiser.data,
                'total_records':total_records
                }

            data = json.dumps(res)
            encoded_dict = str(data).encode('utf-8')
            data = base64.b64encode(encoded_dict)
            json_data = JSONRenderer().render(data)
            return HttpResponse(json_data, content_type= 'application/json') 
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'message' : 'Staff not found',
            }

        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 
        


@csrf_exempt
def active_all_corporate(request):
    if request.method == 'POST':
 
        get_data={}
        for i,j in request.FILES.items():
            get_data.update({i:j})

        for i,j in request.POST.items():
            get_data.update({i:j})

        base64_string = get_data.get('data')
        base64_bytes = base64_string.encode("ascii")
        string_bytes = base64.b64decode(base64_bytes)
        python_data = string_bytes.decode("ascii")
        python_data = json.loads(python_data)

        id = python_data.get('id')
        check_staff = models.StaffDetail.objects.filter(id = id).count()
        if check_staff == 1:
            staff_id = models.StaffDetail.objects.get(id = id)
            get_type_access = staff_id.type_of_access.type_of_access
            if get_type_access == 'Super Admin' or get_type_access == 'Admin': 
                all_corporate = models.CorporateDetail.objects.all().order_by('-id')
                serialiser = CorporateDataSerializer(all_corporate, many=True)
            else:
                all_corporate = models.CorporateDetail.objects.filter(Q(level1 =staff_id) | Q(level2 =staff_id )).distinct()
                serialiser = CorporateDataSerializer(all_corporate, many=True)
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
    
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def vendor_register(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        mobile = python_data.get('mobile')
        email = python_data.get('email')
        vendor_code = python_data.get('vendor_code')
        
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_mobile = models.VendorDetail.objects.filter(mobile = mobile).count()
        if check_mobile == 0:
            check_email = models.VendorDetail.objects.filter(email = email).count()
            if check_email == 0:
                check_vendor_code = models.VendorDetail.objects.filter(vendor_code = vendor_code).count()
                if check_vendor_code == 0:
                    vendor = models.VendorDetail.objects.create(
                        vendor_name = python_data.get('vendor_name', None),
                        vendor_code = str(python_data.get('vendor_code')).upper(),
                        # type_of_service_id = python_data.get('type_of_service'),
                        type_of_visit_id = python_data.get('type_of_visit'),
                        GST_no = python_data.get('GST_no'),
                        billing_cycle_id = python_data.get('billing_cycle'),
                        start_date = python_data.get('start_date'),
                        end_date = python_data.get('end_date'),
                        mobile = python_data.get('mobile'),
                        email = python_data.get('email'),
                        pincode = python_data.get('pincode'),
                        address = python_data.get('address'),
                        state = python_data.get('state'),
                        city = python_data.get('city'),
                        login_via = python_data.get('login_via'),
                        billing_email = python_data.get('billing_email'),
                        stakeholder_name = python_data.get('stakeholder_name'),
                        stakeholder_mobile = python_data.get('stakeholder_mobile'),
                        stakeholder_email = python_data.get('stakeholder_email'),
                        contact_person1 = python_data.get('contact_person1', None),
                        contact_person_designation1 = python_data.get('contact_person_designation1', None),
                        contact_person_mobile1 = python_data.get('contact_person_mobile1', None),
                        contact_person_email1 = python_data.get('contact_person_email1', None),
                        contact_person2 = python_data.get('contact_person2', None),
                        contact_person_designation2 = python_data.get('contact_person_designation2', None),
                        contact_person_mobile2 = python_data.get('contact_person_mobile2', None),
                        contact_person_email2 = python_data.get('contact_person_email2', None),
                        contact_person3 = python_data.get('contact_person3', None),
                        contact_person_designation3 = python_data.get('contact_person_designation3', None),
                        contact_person_mobile3 = python_data.get('contact_person_mobile3', None),
                        contact_person_email3 = python_data.get('contact_person_email3', None),
                        status = 'Active',
                        created_at = current_time
                    )
                    vendor.save()
                    if python_data.get('type_of_service') == '':
                        vendor.type_of_service.set([])
                    else:
                        vendor.type_of_service.set((python_data.get('type_of_service', vendor.type_of_service)))
                    
                    
                        

                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Vendor Added Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Vendor Code Already registered, Please try with other."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Email Already registered, Please try with other."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Mobile Number Already registered, Please try with other."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def vendor_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        mobile = python_data.get('mobile')
        check_vendor = models.VendorDetail.objects.filter(id = id, mobile=mobile).count()
        if check_vendor == 1:
            vendor = models.VendorDetail.objects.get(id = id)
            vendor.vendor_name = python_data.get('vendor_name', vendor.vendor_name)
            vendor.vendor_code = python_data.get('vendor_code', vendor.vendor_code)
            vendor.type_of_service_id = python_data.get('type_of_service', vendor.type_of_service)
            vendor.type_of_visit_id = python_data.get('type_of_visit', vendor.type_of_visit)
            vendor.GST_no = python_data.get('GST_no', vendor.GST_no)
            vendor.billing_cycle_id = python_data.get('billing_cycle', vendor.billing_cycle)
            vendor.start_date = python_data.get('start_date', vendor.start_date)
            vendor.end_date = python_data.get('end_date', vendor.end_date)
            vendor.pincode = python_data.get('pincode', vendor.pincode)
            vendor.address = python_data.get('address', vendor.address)
            vendor.billing_email = python_data.get('billing_email', vendor.billing_email)
            vendor.email = python_data.get('email', vendor.email)
            vendor.mobile = python_data.get('mobile', vendor.mobile)
            
            vendor.state = python_data.get('state', vendor.state)
            vendor.city = python_data.get('city', vendor.city)
            vendor.login_via = python_data.get('login_via', vendor.login_via)
            vendor.stakeholder_name = python_data.get('stakeholder_name', vendor.stakeholder_name)
            vendor.stakeholder_mobile = python_data.get('stakeholder_mobile', vendor.stakeholder_mobile)
            vendor.stakeholder_email = python_data.get('stakeholder_email', vendor.stakeholder_email)
            vendor.contact_person1 = python_data.get('contact_person1', vendor.contact_person1)
            vendor.contact_person_designation1 = python_data.get('contact_person_designation1', vendor.contact_person_designation1)
            vendor.contact_person_mobile1 = python_data.get('contact_person_mobile1', vendor.contact_person_mobile1)
            vendor.contact_person_email1 = python_data.get('contact_person_email1', vendor.contact_person_email1)
            vendor.contact_person2 = python_data.get('contact_person2', vendor.contact_person2)
            vendor.contact_person_designation2 = python_data.get('contact_person_designation2', vendor.contact_person_designation2)
            vendor.contact_person_mobile2 = python_data.get('contact_person_mobile2', vendor.contact_person_mobile2)
            vendor.contact_person_email2 = python_data.get('contact_person_email2', vendor.contact_person_email2)
            vendor.contact_person3 = python_data.get('contact_person3', vendor.contact_person3)
            vendor.contact_person_designation3 = python_data.get('contact_person_designation3', vendor.contact_person_designation3)
            vendor.contact_person_mobile3 = python_data.get('contact_person_mobile3', vendor.contact_person_mobile3)
            vendor.contact_person_email3 = python_data.get('contact_person_email3', vendor.contact_person_email3)
            
            vendor.save()
            if python_data.get('type_of_service') == '':
                vendor.type_of_service.set([])
            else:
                vendor.type_of_service.set((python_data.get('type_of_service', vendor.type_of_service)))
                    
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Vendor Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        
        else:
            check_mobile = models.VendorDetail.objects.filter(mobile = mobile).count()
            if check_mobile == 0:
                vendor = models.VendorDetail.objects.get(id = id)
                vendor.vendor_name = python_data.get('vendor_name', vendor.vendor_name)
                vendor.vendor_code = python_data.get('vendor_code', vendor.vendor_code)
                vendor.type_of_service_id = python_data.get('type_of_service', vendor.type_of_service)
                vendor.type_of_visit_id = python_data.get('type_of_visit', vendor.type_of_visit)
                vendor.GST_no = python_data.get('GST_no', vendor.GST_no)
                vendor.billing_cycle_id = python_data.get('billing_cycle', vendor.billing_cycle)
                vendor.start_date = python_data.get('start_date', vendor.start_date)
                vendor.end_date = python_data.get('end_date', vendor.end_date)
                vendor.pincode = python_data.get('pincode', vendor.pincode)
                vendor.address = python_data.get('address', vendor.address)
                vendor.billing_email = python_data.get('billing_email', vendor.billing_email)
                vendor.email = python_data.get('email', vendor.email)
                vendor.mobile = python_data.get('mobile', vendor.mobile)
                
                vendor.state = python_data.get('state', vendor.state)
                vendor.city = python_data.get('city', vendor.city)
                vendor.login_via = python_data.get('login_via', vendor.login_via)
                vendor.stakeholder_name = python_data.get('stakeholder_name', vendor.stakeholder_name)
                vendor.stakeholder_mobile = python_data.get('stakeholder_mobile', vendor.stakeholder_mobile)
                vendor.stakeholder_email = python_data.get('stakeholder_email', vendor.stakeholder_email)
                vendor.contact_person1 = python_data.get('contact_person1', vendor.contact_person1)
                vendor.contact_person_designation1 = python_data.get('contact_person_designation1', vendor.contact_person_designation1)
                vendor.contact_person_mobile1 = python_data.get('contact_person_mobile1', vendor.contact_person_mobile1)
                vendor.contact_person_email1 = python_data.get('contact_person_email1', vendor.contact_person_email1)
                vendor.contact_person2 = python_data.get('contact_person2', vendor.contact_person2)
                vendor.contact_person_designation2 = python_data.get('contact_person_designation2', vendor.contact_person_designation2)
                vendor.contact_person_mobile2 = python_data.get('contact_person_mobile2', vendor.contact_person_mobile2)
                vendor.contact_person_email2 = python_data.get('contact_person_email2', vendor.contact_person_email2)
                vendor.contact_person3 = python_data.get('contact_person3', vendor.contact_person3)
                vendor.contact_person_designation3 = python_data.get('contact_person_designation3', vendor.contact_person_designation3)
                vendor.contact_person_mobile3 = python_data.get('contact_person_mobile3', vendor.contact_person_mobile3)
                vendor.contact_person_email3 = python_data.get('contact_person_email3', vendor.contact_person_email3)
                
                vendor.save()
                if python_data.get('type_of_service') == '':
                    vendor.type_of_service.set([])
                else:
                    vendor.type_of_service.set((python_data.get('type_of_service', vendor.type_of_service)))
                        
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Vendor Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
            
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Mobile number already Registerd."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def vendor_profile_image_update(request):
    if request.method == 'POST':
        python_data={}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})
        
        vendor = python_data.get('vendor')
        profile_image = python_data.get('profile_image')
        check_emp = models.VendorDetail.objects.filter(id = vendor).count()
        if check_emp == 1:
            vendor = models.VendorDetail.objects.get(id = vendor)
            if type(python_data.get('profile_image', vendor.profile_image)) != str: 
                vendor.profile_image = python_data.get('profile_image', vendor.profile_image)
            vendor.save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Profile Image Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Vendor."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def vendor_code_check(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        vendor_code = python_data.get('vendor_code')

        check_vendor_code = models.VendorDetail.objects.filter(vendor_code__exact = vendor_code).count()
        if check_vendor_code == 1:
            vendor_code = models.VendorDetail.objects.get(vendor_code = vendor_code)
            login_via = vendor_code.login_via
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'login_via':login_via
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message':"You've Enter wrong Vendor Code."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def list_all_vendor(request):
    if request.method == 'POST':
        python_data = {}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})

        data = python_data.get('data')

        try:
            decoded_bytes = base64.b64decode(data)
            decoded_python_data = json.loads(decoded_bytes.decode('utf-8'))
        except:
            decoded_python_data = {}

        page_number = int(decoded_python_data.get('page_number',1))
        row_size = int(decoded_python_data.get('row_size',10))
        last_row = row_size * page_number
        first_row = last_row - row_size

        filter_condition = {}

        vendor_code = decoded_python_data.get('vendor_code')
        vendor_name = decoded_python_data.get('vendor_name')
        type_of_visit_name = decoded_python_data.get('type_of_visit_name')
        start_date = decoded_python_data.get('start_date')
        end_date = decoded_python_data.get('end_date')
        billing_cycle_name = decoded_python_data.get('billing_cycle_name')
        mobile = decoded_python_data.get('mobile')
        email = decoded_python_data.get('email')
        status = decoded_python_data.get('status')

        if vendor_code not in [None,'','null']:
            filter_condition['vendor_code__icontains'] = vendor_code
        if vendor_name not in [None,'','null']:
            filter_condition['vendor_name__icontains'] = vendor_name
        if type_of_visit_name not in [None,'','null']:
            filter_condition['type_of_visit__type_of_visit__icontains'] = type_of_visit_name
        if start_date not in [None,'','null']:
            filter_condition['start_date__gte'] = start_date
        if end_date not in [None,'','null']:
            filter_condition['end_date__lte'] = end_date
        if billing_cycle_name not in [None,'','null']:
            filter_condition['billing_cycle__billing_cycle__icontains'] = billing_cycle_name
        if mobile not in [None,'','null']:
            filter_condition['mobile__icontains'] = mobile
        if email not in [None,'','null']:
            filter_condition['email__icontains'] = email
        if status not in [None,'','null']:
            if status != 'All':
                filter_condition['status'] = status
        

        total_records = models.VendorDetail.objects.filter(**filter_condition).count()
        all_vendor = models.VendorDetail.objects.filter(**filter_condition).order_by('-id')[first_row:last_row]
        serialiser = VendorSerializer(all_vendor, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data,
            'total_records':total_records
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def service_visit_wise_vendor_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        type_of_service = python_data.get('type_of_service')
        type_of_visit = python_data.get('type_of_visit', None)
        if type_of_visit == None:
            all_vendor = models.VendorDetail.objects.filter(type_of_service = type_of_service).order_by('-id')
            serialiser = VendorNameSerializer(all_vendor, many=True)
        else: 
            check_type_of_visit = models.TypeOfVisit.objects.filter(id = type_of_visit).values_list('type_of_visit', flat=True)[0]  
            if check_type_of_visit == 'Hybrid':
                all_vendor = models.VendorDetail.objects.filter(type_of_service = type_of_service, type_of_visit= type_of_visit).order_by('-id')
            else:
                get_hybrid_id = models.TypeOfVisit.objects.filter(type_of_visit = 'Hybrid').values_list('id', flat=True)[0]
                type_of_visit = [type_of_visit,get_hybrid_id ]
                all_vendor = models.VendorDetail.objects.filter(type_of_service = type_of_service, type_of_visit__in= type_of_visit).order_by('-id')
            
            serialiser = VendorNameSerializer(all_vendor, many=True)
            
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        # data = json.dumps(res)
        # encoded_dict = str(data).encode('utf-8')
        # data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def service_wise_vendor_list(request):
    if request.method == 'POST':
        all_service = request.POST['service']
        if all_service.isdigit():
            check_service = models.TypeOfService.objects.filter(id = all_service).count()
            if check_service == 1:
                get_all_vendor = models.VendorDetail.objects.filter(type_of_service = all_service)
                serialiser = VendorNameSerializer(get_all_vendor, many=True)
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'data':serialiser.data
                }                                                        
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
        else:
            list_service = all_service.split(',')
            list_data = []
            for service in list_service:
                check_service = models.TypeOfService.objects.filter(id = service).count()
                if check_service == 1:
                    get_all_vendor = models.VendorDetail.objects.filter(type_of_service = service)
                    for vendor in get_all_vendor:
                        serialiser = VendorNameSerializer(vendor)
                        list_data.append(serialiser.data)

            data = [dict(t) for t in {tuple(d.items()) for d in list_data}]
            
            res = {
                'statuscode' : 200,
                'status':'true',
                'data':data
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def all_active_vendor(request):
    if request.method == 'POST':
        all_vendor = models.VendorDetail.objects.filter(status='Active').order_by('-id')
        serialiser = VendorNameSerializer(all_vendor, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def vendor_status_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_vendor = models.VendorDetail.objects.filter(id = id).count()
        if check_vendor == 1:
            vendor = models.VendorDetail.objects.get(id = id)
            vendor.status = status
            vendor.save()

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Status Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Vendor."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def staff_department_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        staff_department = python_data.get('staff_department')
        check_staff_department = models.StaffDepartment.objects.filter(staff_department = staff_department).count()
        if check_staff_department == 0:
            staff = models.StaffDepartment.objects.create(
                staff_department = staff_department,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Staff Department Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Staff Department already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def staff_department_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.StaffDepartment.objects.filter(id = id).count()
        if check_department == 1:
            staff_department = python_data.get('staff_department')
            status = python_data.get('status')
            if staff_department:
                check_staff_department = models.StaffDepartment.objects.filter(id = id, staff_department = staff_department).count()
                if check_staff_department == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Staff Department Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_staff_department = models.StaffDepartment.objects.filter(staff_department = staff_department).count()
                    if check_staff_department == 0:
                        staff = models.StaffDepartment.objects.get(id = id)
                        staff.staff_department = staff_department
                        staff.status = python_data.get('status', staff.status)
                        staff.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Staff Department Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Staff Department already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                staff = models.StaffDepartment.objects.get(id = id)
                staff.status = python_data.get('status', staff.status)
                staff.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Staff Department Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_staff_department_list(request):
    if request.method == 'POST':
        all_staff_department = models.StaffDepartment.objects.all().order_by('-id')
        serialiser = StaffDepartmentSerializer(all_staff_department, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def staff_department_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        staff = python_data.get('id')
        check_staff = models.StaffDepartment.objects.filter(id = staff).count()
        if check_staff == 1:
            
            staff_details = models.StaffDepartment.objects.get(id = staff)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Staff Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def type_of_access_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        type_of_access = python_data.get('type_of_access')
        check_type_of_access = models.TypeOfAccess.objects.filter(type_of_access = type_of_access).count()
        if check_type_of_access == 0:
            toa = models.TypeOfAccess.objects.create(
                type_of_access = type_of_access,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Type Of Access Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Type Of Access already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def type_of_access_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.TypeOfAccess.objects.filter(id = id).count()
        if check_department == 1:
            type_of_access = python_data.get('type_of_access')
            status = python_data.get('status')
            if type_of_access:
                check_type_of_access = models.TypeOfAccess.objects.filter(id = id, type_of_access = type_of_access).count()
                if check_type_of_access == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Type Of Access Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_type_of_access = models.TypeOfAccess.objects.filter(type_of_access = type_of_access).count()
                    if check_type_of_access == 0:
                        toa = models.TypeOfAccess.objects.get(id = id)
                        toa.type_of_access = type_of_access
                        toa.status = python_data.get('status', toa.status)
                        toa.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Type Of Access Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Type Of Access already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                toa = models.TypeOfAccess.objects.get(id = id)
                toa.status = python_data.get('status', toa.status)
                toa.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Type Of Access Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_type_of_access_list(request):
    if request.method == 'POST':
        all_type_of_access = models.TypeOfAccess.objects.all().order_by('-id')
        serialiser = TypeOfAccessSerializer(all_type_of_access, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def type_of_access_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        staff = python_data.get('id')
        check_staff = models.TypeOfAccess.objects.filter(id = staff).count()
        if check_staff == 1:
            
            staff_details = models.TypeOfAccess.objects.get(id = staff)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Type of Access Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def staff_level_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        staff_level = python_data.get('staff_level')
        check_staff_level = models.StaffLevel.objects.filter(staff_level = staff_level).count()
        if check_staff_level == 0:
            level = models.StaffLevel.objects.create(
                staff_level = staff_level,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Staff Level Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Staff Level already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def staff_level_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.StaffLevel.objects.filter(id = id).count()
        if check_department == 1:
            staff_level = python_data.get('staff_level')
            status = python_data.get('status')
            if staff_level:
                check_staff_level = models.StaffLevel.objects.filter(id = id, staff_level = staff_level).count()
                if check_staff_level == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Staff Level Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_staff_level = models.StaffLevel.objects.filter(staff_level = staff_level).count()
                    if check_staff_level == 0:
                        level = models.StaffLevel.objects.get(id = id)
                        level.staff_level = staff_level
                        level.status = python_data.get('status', level.status)
                        level.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Staff Level Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Staff Level already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                level = models.StaffLevel.objects.get(id = id)
                level.status = python_data.get('status', level.status)
                level.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Staff Level Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_staff_level_list(request):
    if request.method == 'POST':
        all_staff_level = models.StaffLevel.objects.all().order_by('-id')
        serialiser = StaffLevelSerializer(all_staff_level, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def staff_level_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        staff = python_data.get('id')
        check_staff = models.StaffLevel.objects.filter(id = staff).count()
        if check_staff == 1:
            
            staff_details = models.StaffLevel.objects.get(id = staff)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Staff Level Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')



@csrf_exempt
def staff_type_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        staff_type = python_data.get('staff_type')
        check_staff_type = models.StaffType.objects.filter(staff_type = staff_type).count()
        if check_staff_type == 0:
            level = models.StaffType.objects.create(
                staff_type = staff_type,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Staff Type Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Staff Type already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def staff_type_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.StaffType.objects.filter(id = id).count()
        if check_department == 1:
            staff_type = python_data.get('staff_type')
            status = python_data.get('status')
            if staff_type:
                check_staff_type = models.StaffType.objects.filter(id = id, staff_type = staff_type).count()
                if check_staff_type == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Staff Type Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_staff_type = models.StaffType.objects.filter(staff_type = staff_type).count()
                    if check_staff_type == 0:
                        level = models.StaffType.objects.get(id = id)
                        level.staff_type = staff_type
                        level.status = python_data.get('status', level.status)
                        level.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Staff Type Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Staff Type already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                level = models.StaffType.objects.get(id = id)
                level.status = python_data.get('status', level.status)
                level.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Staff Type Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_staff_type_list(request):
    if request.method == 'POST':
        all_staff_type = models.StaffType.objects.all().order_by('-id')
        serialiser = StaffTypeSerializer(all_staff_type, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def staff_type_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        staff = python_data.get('id')
        check_staff = models.StaffType.objects.filter(id = staff).count()
        if check_staff == 1:
            
            staff_details = models.StaffType.objects.get(id = staff)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Staff Type Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')



@csrf_exempt
def type_of_industry_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        type_of_industry = python_data.get('type_of_industry')
        check_type_of_industry = models.TypeOfIndustry.objects.filter(type_of_industry = type_of_industry).count()
        if check_type_of_industry == 0:
            level = models.TypeOfIndustry.objects.create(
                type_of_industry = type_of_industry,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Type of Industry Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Type of Industry already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def type_of_industry_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.TypeOfIndustry.objects.filter(id = id).count()
        if check_department == 1:
            type_of_industry = python_data.get('type_of_industry')
            status = python_data.get('status')
            if type_of_industry:
                check_type_of_industry = models.TypeOfIndustry.objects.filter(id = id, type_of_industry = type_of_industry).count()
                if check_type_of_industry == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Type of Industry Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_type_of_industry = models.TypeOfIndustry.objects.filter(type_of_industry = type_of_industry).count()
                    if check_type_of_industry == 0:
                        level = models.TypeOfIndustry.objects.get(id = id)
                        level.type_of_industry = type_of_industry
                        level.status = python_data.get('status', level.status)
                        level.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Type of Industry Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Type of Industry already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                level = models.TypeOfIndustry.objects.get(id = id)
                level.status = python_data.get('status', level.status)
                level.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Type of Industry Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_type_of_industry_list(request):
    if request.method == 'POST':
        all_type_of_industry = models.TypeOfIndustry.objects.all().order_by('-id')
        serialiser = TypeOfIndustrySerializer(all_type_of_industry, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def type_of_industry_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        industry = python_data.get('id')
        check_staff = models.TypeOfIndustry.objects.filter(id = industry).count()
        if check_staff == 1:
            
            staff_details = models.TypeOfIndustry.objects.get(id = industry)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Type of Industry Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def all_active_type_of_industry_list(request):
    if request.method == 'POST':
        type_of_industry = models.TypeOfIndustry.objects.filter(status='Active').order_by('-id')
        serialiser = TypeOfIndustrySerializer(type_of_industry, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def duration_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        duration = python_data.get('duration')
        check_duration = models.Duration.objects.filter(duration = duration).count()
        if check_duration == 0:
            duration = models.Duration.objects.create(
                duration = duration,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Duration Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Duration already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def duration_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_duration = models.Duration.objects.filter(id = id).count()
        if check_duration == 1:
            duration = python_data.get('duration')
            status = python_data.get('status')
            if duration:
                check_duration = models.Duration.objects.filter(id = id, duration = duration).count()
                if check_duration == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Duration Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_duration = models.Duration.objects.filter(duration = duration).count()
                    if check_duration == 0:
                        level = models.Duration.objects.get(id = id)
                        level.duration = duration
                        level.status = python_data.get('status', level.status)
                        level.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Duration Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Duration already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                level = models.Duration.objects.get(id = id)
                level.status = python_data.get('status', level.status)
                level.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Duration Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_duration_list(request):
    if request.method == 'POST':
        all_duration = models.Duration.objects.all().order_by('-id')
        serialiser = DurationSerializer(all_duration, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def duration_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        duration = python_data.get('id')
        check_duration = models.Duration.objects.filter(id = duration).count()
        if check_duration == 1:
            
            duration_details = models.Duration.objects.get(id = duration)
            duration_details.status = 'Inactive'
            duration_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Duration Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def all_active_duration_list(request):
    if request.method == 'POST':
        duration = models.Duration.objects.filter(status='Active').order_by('-id')
        serialiser = DurationSerializer(duration, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def platform_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        platform = python_data.get('platform')
        check_platform = models.Platform.objects.filter(platform = platform).count()
        if check_platform == 0:
            platform = models.Platform.objects.create(
                platform = platform,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Platform Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Platform already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        
@csrf_exempt
def platform_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_platform = models.Platform.objects.filter(id = id).count()
        if check_platform == 1:
            platform = python_data.get('platform')
            status = python_data.get('status')
            if platform:
                check_platform = models.Platform.objects.filter(id = id, platform = platform).count()
                if check_platform == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Platform Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_platform = models.Platform.objects.filter(platform = platform).count()
                    if check_platform == 0:
                        level = models.Platform.objects.get(id = id)
                        level.platform = platform
                        level.status = python_data.get('status', level.status)
                        level.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Platform Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Platform already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                level = models.Platform.objects.get(id = id)
                level.status = python_data.get('status', level.status)
                level.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Platform Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_platform_list(request):
    if request.method == 'POST':
        all_platform = models.Platform.objects.all().order_by('-id')
        serialiser = PlatformSerializer(all_platform, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def platform_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        platform = python_data.get('id')
        check_platform = models.Platform.objects.filter(id = platform).count()
        if check_platform == 1:
            
            platform_details = models.Platform.objects.get(id = platform)
            platform_details.status = 'Inactive'
            platform_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Platform Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def all_active_platform_list(request):
    if request.method == 'POST':
        platform = models.Platform.objects.filter(status='Active').order_by('-id')
        serialiser = PlatformSerializer(platform, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def age_category_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        age_category = python_data.get('age_category')
        check_age_category = models.AgeCategory.objects.filter(age_category = age_category).count()
        if check_age_category == 0:
            age = models.AgeCategory.objects.create(
                age_category = age_category,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Age Category Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Age Category already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def age_category_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.AgeCategory.objects.filter(id = id).count()
        if check_department == 1:
            age_category = python_data.get('age_category')
            status = python_data.get('status')
            if age_category:
                check_age_category = models.AgeCategory.objects.filter(id = id, age_category = age_category).count()
                if check_age_category == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Age Category Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_age_category = models.AgeCategory.objects.filter(age_category = age_category).count()
                    if check_age_category == 0:
                        age = models.AgeCategory.objects.get(id = id)
                        age.age_category = age_category
                        age.status = python_data.get('status', age.status)
                        age.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Age Category Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Age Category already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                age = models.AgeCategory.objects.get(id = id)
                age.status = python_data.get('status', age.status)
                age.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Age Category Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_age_category_list(request):
    if request.method == 'POST':
        all_age_category = models.AgeCategory.objects.all().order_by('-id')
        serialiser = AgeCategorySerializer(all_age_category, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def age_category_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        age = python_data.get('id')
        check_staff = models.AgeCategory.objects.filter(id = age).count()
        if check_staff == 1:
            
            staff_details = models.AgeCategory.objects.get(id = age)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Age Category Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')



@csrf_exempt
def gender_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        gender = python_data.get('gender')
        check_gender = models.Gender.objects.filter(gender = gender).count()
        if check_gender == 0:
            age = models.Gender.objects.create(
                gender = gender,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Gender Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Gender already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def gender_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.Gender.objects.filter(id = id).count()
        if check_department == 1:
            gender = python_data.get('gender')
            status = python_data.get('status')
            if gender:
                check_gender = models.Gender.objects.filter(id = id, gender = gender).count()
                if check_gender == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Gender Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_gender = models.Gender.objects.filter(gender = gender).count()
                    if check_gender == 0:
                        age = models.Gender.objects.get(id = id)
                        age.gender = gender
                        age.status = python_data.get('status', age.status)
                        age.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Gender Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Gender already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                age = models.Gender.objects.get(id = id)
                age.status = python_data.get('status', age.status)
                age.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Gender Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_gender_list(request):
    if request.method == 'POST':
        all_gender = models.Gender.objects.all().order_by('-id')
        serialiser = GenderSerializer(all_gender, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def gender_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        gender = python_data.get('id')
        check_staff = models.Gender.objects.filter(id = gender).count()
        if check_staff == 1:
            
            staff_details = models.Gender.objects.get(id = gender)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Gender Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def relation_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        relation = python_data.get('relation')
        check_relation = models.Relation.objects.filter(relation = relation).count()
        if check_relation == 0:
            relate = models.Relation.objects.create(
                relation = relation,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Relation Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Relation already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def relation_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.Relation.objects.filter(id = id).count()
        if check_department == 1:
            relation = python_data.get('relation')
            status = python_data.get('status')
            if relation:
                check_relation = models.Relation.objects.filter(id = id, relation = relation).count()
                if check_relation == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Relation Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_relation = models.Relation.objects.filter(relation = relation).count()
                    if check_relation == 0:
                        relate = models.Relation.objects.get(id = id)
                        relate.relation = relation
                        relate.status = python_data.get('status', relate.status)
                        relate.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Relation Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Relation already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                relate = models.Relation.objects.get(id = id)
                relate.status = python_data.get('status', relate.status)
                relate.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Relation Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_relation_list(request):
    if request.method == 'POST':
        all_relation = models.Relation.objects.all().order_by('-id')
        serialiser = RelationSerializer(all_relation, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def relation_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        relation = python_data.get('id')
        check_staff = models.Relation.objects.filter(id = relation).count()
        if check_staff == 1:
            
            staff_details = models.Relation.objects.get(id = relation)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Relation Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def type_of_service_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        type_of_service = python_data.get('type_of_service')
        check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
        if check_type_of_service == 0:
            relate = models.TypeOfService.objects.create(
                type_of_service = type_of_service,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "TypeOfService Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This TypeOfService already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def type_of_service_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.TypeOfService.objects.filter(id = id).count()
        if check_department == 1:
            type_of_service = python_data.get('type_of_service')
            status = python_data.get('status')
            if type_of_service:
                check_type_of_service = models.TypeOfService.objects.filter(id = id, type_of_service = type_of_service).count()
                if check_type_of_service == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "TypeOfService Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                    if check_type_of_service == 0:
                        service = models.TypeOfService.objects.get(id = id)
                        service.type_of_service = type_of_service
                        service.status = python_data.get('status', service.status)
                        service.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "TypeOfService Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This TypeOfService already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                service = models.TypeOfService.objects.get(id = id)
                service.status = python_data.get('status', service.status)
                service.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "TypeOfService Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_type_of_service_list(request):
    if request.method == 'POST':
        all_type_of_service = models.TypeOfService.objects.all().order_by('-id')
        serialiser = TypeOfServiceSerializer(all_type_of_service, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def type_of_service_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        service = python_data.get('id')
        check_staff = models.TypeOfService.objects.filter(id = service).count()
        if check_staff == 1:
            
            staff_details = models.TypeOfService.objects.get(id = service)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Type of Service Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')



@csrf_exempt
def type_of_visit_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        type_of_visit = python_data.get('type_of_visit')
        check_type_of_visit = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).count()
        if check_type_of_visit == 0:
            relate = models.TypeOfVisit.objects.create(
                type_of_visit = type_of_visit,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "TypeOfVisit Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This TypeOfVisit already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def type_of_visit_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.TypeOfVisit.objects.filter(id = id).count()
        if check_department == 1:
            type_of_visit = python_data.get('type_of_visit')
            status = python_data.get('status')
            if type_of_visit:
                check_type_of_visit = models.TypeOfVisit.objects.filter(id = id, type_of_visit = type_of_visit).count()
                if check_type_of_visit == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "TypeOfVisit Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_type_of_visit = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).count()
                    if check_type_of_visit == 0:
                        visit = models.TypeOfVisit.objects.get(id = id)
                        visit.type_of_visit = type_of_visit
                        visit.status = python_data.get('status', visit.status)
                        visit.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "TypeOfVisit Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This TypeOfVisit already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                visit = models.TypeOfVisit.objects.get(id = id)
                visit.status = python_data.get('status', visit.status)
                visit.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "TypeOfVisit Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_type_of_visit_list(request):
    if request.method == 'POST':
        all_type_of_visit = models.TypeOfVisit.objects.all().order_by('-id')
        serialiser = TypeOfVisitSerializer(all_type_of_visit, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def type_of_visit_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        visit = python_data.get('id')
        check_staff = models.TypeOfVisit.objects.filter(id = visit).count()
        if check_staff == 1:
            
            staff_details = models.TypeOfVisit.objects.get(id = visit)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Type of Visit Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def parent_company_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        parent_company = python_data.get('parent_company')
        check_parent_company = models.ParentCompany.objects.filter(parent_company = parent_company).count()
        if check_parent_company == 0:
            relate = models.ParentCompany.objects.create(
                parent_company = parent_company,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "ParentCompany Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This ParentCompany already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def parent_company_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.ParentCompany.objects.filter(id = id).count()
        if check_department == 1:
            parent_company = python_data.get('parent_company')
            status = python_data.get('status')
            if parent_company:
                check_parent_company = models.ParentCompany.objects.filter(id = id, parent_company = parent_company).count()
                if check_parent_company == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "ParentCompany Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_parent_company = models.ParentCompany.objects.filter(parent_company = parent_company).count()
                    if check_parent_company == 0:
                        parent = models.ParentCompany.objects.get(id = id)
                        parent.parent_company = parent_company
                        parent.status = python_data.get('status', parent.status)
                        parent.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "ParentCompany Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This ParentCompany already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                parent = models.ParentCompany.objects.get(id = id)
                parent.status = python_data.get('status', parent.status)
                parent.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "ParentCompany Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_parent_company_list(request):
    if request.method == 'POST':
        all_parent_company = models.ParentCompany.objects.all().order_by('-id')
        serialiser = ParentCompanySerializer(all_parent_company, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def parent_company_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        visit = python_data.get('id')
        check_staff = models.ParentCompany.objects.filter(id = visit).count()
        if check_staff == 1:
            
            staff_details = models.ParentCompany.objects.get(id = visit)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Parent Company Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')



@csrf_exempt
def billing_cycle_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        billing_cycle = python_data.get('billing_cycle')
        check_billing_cycle = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).count()
        if check_billing_cycle == 0:
            relate = models.BillingCycle.objects.create(
                billing_cycle = billing_cycle,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "BillingCycle Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This BillingCycle already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def billing_cycle_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.BillingCycle.objects.filter(id = id).count()
        if check_department == 1:
            billing_cycle = python_data.get('billing_cycle')
            status = python_data.get('status')
            if billing_cycle:
                check_billing_cycle = models.BillingCycle.objects.filter(id = id, billing_cycle = billing_cycle).count()
                if check_billing_cycle == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "BillingCycle Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_billing_cycle = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).count()
                    if check_billing_cycle == 0:
                        billing = models.BillingCycle.objects.get(id = id)
                        billing.billing_cycle = billing_cycle
                        billing.status = python_data.get('status', billing.status)
                        billing.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "BillingCycle Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This BillingCycle already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                billing = models.BillingCycle.objects.get(id = id)
                billing.status = python_data.get('status', billing.status)
                billing.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "BillingCycle Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_billing_cycle_list(request):
    if request.method == 'POST':
        all_billing_cycle = models.BillingCycle.objects.all().order_by('-id')
        serialiser = BillingCycleSerializer(all_billing_cycle, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def billing_cycle_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        cycle = python_data.get('id')
        check_staff = models.BillingCycle.objects.filter(id = cycle).count()
        if check_staff == 1:
            
            staff_details = models.BillingCycle.objects.get(id = cycle)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Billing Cycle Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def weekdays_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        weekdays = python_data.get('weekdays')
        check_weekdays = models.Weekdays.objects.filter(weekdays = weekdays).count()
        if check_weekdays == 0:
            relate = models.Weekdays.objects.create(
                weekdays = weekdays,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Weekdays Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Weekdays already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def weekdays_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.Weekdays.objects.filter(id = id).count()
        if check_department == 1:
            weekdays = python_data.get('weekdays')
            status = python_data.get('status')
            if weekdays:
                check_weekdays = models.Weekdays.objects.filter(id = id, weekdays = weekdays).count()
                if check_weekdays == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Weekdays Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_weekdays = models.Weekdays.objects.filter(weekdays = weekdays).count()
                    if check_weekdays == 0:
                        week = models.Weekdays.objects.get(id = id)
                        week.weekdays = weekdays
                        week.status = python_data.get('status', week.status)
                        week.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Weekdays Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Weekdays already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                week = models.Weekdays.objects.get(id = id)
                week.status = python_data.get('status', week.status)
                week.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Weekdays Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_weekdays_list(request):
    if request.method == 'POST':
        all_weekdays = models.Weekdays.objects.all().order_by('-id')
        serialiser = WeekdaysSerializer(all_weekdays, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def weekdays_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        week = python_data.get('id')
        check_staff = models.Weekdays.objects.filter(id = week).count()
        if check_staff == 1:
            
            staff_details = models.Weekdays.objects.get(id = week)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Weekedays Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')




@csrf_exempt
def holidays_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        holidays = python_data.get('holidays')
        check_holidays = models.Holidays.objects.filter(holidays = holidays).count()
        if check_holidays == 0:
            relate = models.Holidays.objects.create(
                holidays = holidays,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Holidays Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Holidays already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def holidays_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.Holidays.objects.filter(id = id).count()
        if check_department == 1:
            holidays = python_data.get('holidays')
            status = python_data.get('status')
            if holidays:
                check_holidays = models.Holidays.objects.filter(id = id, holidays = holidays).count()
                if check_holidays == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Holidays Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_holidays = models.Holidays.objects.filter(holidays = holidays).count()
                    if check_holidays == 0:
                        days = models.Holidays.objects.get(id = id)
                        days.holidays = holidays
                        days.status = python_data.get('status', days.status)
                        days.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Holidays Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Holidays already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                days = models.Holidays.objects.get(id = id)
                days.status = python_data.get('status', days.status)
                days.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Holidays Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_holidays_list(request):
    if request.method == 'POST':
        all_holidays = models.Holidays.objects.all().order_by('-id')
        serialiser = HolidaysSerializer(all_holidays, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def holidays_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        holiday = python_data.get('id')
        check_staff = models.Holidays.objects.filter(id = holiday).count()
        if check_staff == 1:
            
            staff_details = models.Holidays.objects.get(id = holiday)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Holidays Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')



@csrf_exempt
def payment_tags_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        payment_tags = python_data.get('payment_tags')
        check_payment_tags = models.PaymentTags.objects.filter(payment_tags = payment_tags).count()
        if check_payment_tags == 0:
            relate = models.PaymentTags.objects.create(
                payment_tags = payment_tags,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "PaymentTags Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This PaymentTags already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def payment_tags_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.PaymentTags.objects.filter(id = id).count()
        if check_department == 1:
            payment_tags = python_data.get('payment_tags')
            status = python_data.get('status')
            if payment_tags:
                check_payment_tags = models.PaymentTags.objects.filter(id = id, payment_tags = payment_tags).count()
                if check_payment_tags == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "PaymentTags Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_payment_tags = models.PaymentTags.objects.filter(payment_tags = payment_tags).count()
                    if check_payment_tags == 0:
                        payment = models.PaymentTags.objects.get(id = id)
                        payment.payment_tags = payment_tags
                        payment.status = python_data.get('status', payment.status)
                        payment.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "PaymentTags Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This PaymentTags already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                payment = models.PaymentTags.objects.get(id = id)
                payment.status = python_data.get('status', payment.status)
                payment.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "PaymentTags Status Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_payment_tags_list(request):
    if request.method == 'POST':
        all_payment_tags = models.PaymentTags.objects.all().order_by('-id')
        serialiser = PaymentTagsSerializer(all_payment_tags, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def payment_tags_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        tags = python_data.get('id')
        check_staff = models.PaymentTags.objects.filter(id = tags).count()
        if check_staff == 1:
            
            staff_details = models.PaymentTags.objects.get(id = tags)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Payment Tags Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')




@csrf_exempt
def all_active_staff_department_list(request):
    if request.method == 'POST':
        all_staff_department = models.StaffDepartment.objects.filter(status='Active').order_by('-id')
        serialiser = StaffDepartmentSerializer(all_staff_department, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
       
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_active_type_of_access_list(request):
    if request.method == 'POST':
        all_type_of_access = models.TypeOfAccess.objects.filter(status='Active').order_by('-id')
        serialiser = TypeOfAccessSerializer(all_type_of_access, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_staff_level_list(request):
    if request.method == 'POST':
        staff_level = models.StaffLevel.objects.filter(status='Active').order_by('-id')
        serialiser = StaffLevelSerializer(staff_level, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_active_staff_type_list(request):
    if request.method == 'POST':
        all_staff_type = models.StaffType.objects.filter(status='Active').order_by('-id')
        serialiser = StaffTypeSerializer(all_staff_type, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_age_category_list(request):
    if request.method == 'POST':
        all_age_category = models.AgeCategory.objects.filter(status='Active').order_by('-id')
        serialiser = AgeCategorySerializer(all_age_category, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_gender_list(request):
    if request.method == 'POST':
        all_gender = models.Gender.objects.filter(status='Active').order_by('-id')
        serialiser = GenderSerializer(all_gender, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_relation_list(request):
    if request.method == 'POST':
        all_relation = models.Relation.objects.filter(status='Active').order_by('-id')
        serialiser = RelationSerializer(all_relation, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_type_of_service_list(request):
    if request.method == 'POST':
        all_type_of_service = models.TypeOfService.objects.filter(status='Active').order_by('-id')
        serialiser = TypeOfServiceSerializer(all_type_of_service, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_type_of_visit_list(request):
    if request.method == 'POST':
        all_type_of_visit = models.TypeOfVisit.objects.filter(status='Active').order_by('-id')
        serialiser = TypeOfVisitSerializer(all_type_of_visit, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_parent_company_list(request):
    if request.method == 'POST':
        all_parent_company = models.ParentCompany.objects.filter(status='Active').order_by('-id')
        serialiser = ParentCompanySerializer(all_parent_company, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_billing_cycle_list(request):
    if request.method == 'POST':
        all_billing_cycle = models.BillingCycle.objects.filter(status='Active').order_by('-id')
        serialiser = BillingCycleSerializer(all_billing_cycle, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_weekdays_list(request):
    if request.method == 'POST':
        all_weekdays = models.Weekdays.objects.filter(status='Active').order_by('-id')
        serialiser = WeekdaysSerializer(all_weekdays, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_holidays_list(request):
    if request.method == 'POST':
        all_holidays = models.Holidays.objects.filter(status='Active').order_by('-id')
        serialiser = HolidaysSerializer(all_holidays, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_payment_tags_list(request):
    if request.method == 'POST':
        all_payment_tags = models.PaymentTags.objects.filter(status='Active').order_by('-id')
        serialiser = PaymentTagsSerializer(all_payment_tags, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def employee_register(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        mobile = python_data.get('mobile')
        email = python_data.get('email')
        employee_code = python_data.get('employee_code')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_mobile = models.EmployeeDetail.objects.filter(mobile = mobile).count()
        if check_mobile == 0:
            check_email = models.EmployeeDetail.objects.filter(email = email).count()
            if check_email == 0:
                check_employee_code = models.EmployeeDetail.objects.filter(employee_code = employee_code).count()
                if check_employee_code == 0:
                    emp = models.EmployeeDetail.objects.create(
                        corporate_id = python_data.get('corporate'),
                        employee_name = python_data.get('employee_name'),
                        employee_code = str(python_data.get('employee_code')).upper(),
                        department = python_data.get('department'),
                        date_of_join = python_data.get('date_of_join'),
                        date_of_birth = python_data.get('date_of_birth'),
                        gender_id = python_data.get('gender'),
                        mobile = python_data.get('mobile'),
                        email = python_data.get('email'),
                        hr_employee = python_data.get('hr_employee'),
                        hr_corporate_code = python_data.get('hr_corporate_code'),
                        address = python_data.get('address'),
                        pincode = python_data.get('pincode'),
                        state = python_data.get('state'),
                        city = python_data.get('city'),
                        employee_from = 'Svasthya',
                        status = 'Active',
                        created_at = current_time
                    )
                    emp.save()
                    employee_id = emp.id


                    add_address = models.EmployeeAddressDetail.objects.create(
                        employee_id = employee_id,
                        address_type = "Home",
                        address = python_data.get('address'),
                        latitude = python_data.get('latitude'),
                        longitude = python_data.get('longitude'),
                        pincode = python_data.get('pincode'),
                        state = python_data.get('state'),
                        city = python_data.get('city'),
                        mobile = python_data.get('mobile'),
                        created_at = current_time
                    ).save()
                                    

                    self_id = models.Relation.objects.filter(relation = 'Self').values_list('id', flat=True)[0]

                    self_create = models.EmployeeDependent.objects.create(
                        employee_id = employee_id,
                        dependent_name = emp.employee_name,
                        dependent_relation_id = self_id, 
                        date_of_birth = emp.date_of_birth,
                        gender_id = emp.gender.id,
                        created_at = current_time
                    ).save()
                
                    
                    for count in range(1, 20):
                        dependent_relation = 'dependent_relation' + str(count)
                        date_of_birth = 'date_of_birth' + str(count)
                        gender = 'gender' + str(count)
                        dependent_name = 'dependent_name' + str(count)

                        child_id = models.Relation.objects.filter(relation = 'Child').values_list('id', flat=True)[0]

                        if python_data.get(dependent_relation) and python_data.get(date_of_birth) and python_data.get(gender) and python_data.get(dependent_name):
                            dependent_relation_data = python_data.get(dependent_relation)
                            date_of_birth_data = python_data.get(date_of_birth)
                            gender_data = python_data.get(gender)
                            dependent_name_data = python_data.get(dependent_name)
        
                            child_count = models.EmployeeDependent.objects.filter(dependent_relation_id = child_id, employee_id = employee_id).count()
                            if dependent_relation_data != child_id:
                                dependent_create = models.EmployeeDependent.objects.create(
                                    employee_id = employee_id,
                                    dependent_name = dependent_name_data,
                                    dependent_relation_id = dependent_relation_data, 
                                    date_of_birth = date_of_birth_data,
                                    gender_id = gender_data,
                                    created_at = current_time
                                ).save()
                            
                            elif dependent_relation_data == child_id:
                                if child_count < 3:
                                    dependent_create = models.EmployeeDependent.objects.create(
                                        employee_id = employee_id,
                                        dependent_name = dependent_name_data,
                                        dependent_relation_id = dependent_relation_data, 
                                        date_of_birth = date_of_birth_data,
                                        gender_id = gender_data,
                                        created_at = current_time
                                    ).save()
                                
                                else:
                                    pass
                            else:
                                pass
                        else:
                            break

                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Employee Added Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Employee Code Already registered, Please try with other."
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                    
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Email Already registered, Please try with other."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Mobile Number Already registered, Please try with other."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def employee_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        id = python_data.get('id')
        mobile = python_data.get('mobile')
        check_emp = models.EmployeeDetail.objects.filter(id = id, mobile=mobile).count()
        if check_emp == 1:
            employee = models.EmployeeDetail.objects.get(id = id)
            employee.corporate_id = python_data.get('corporate', employee.corporate)
            employee.employee_name = python_data.get('employee_name', employee.employee_name)
            employee.employee_code = str(python_data.get('employee_code', employee.employee_code)).upper()
            employee.department = python_data.get('department', employee.department)
            employee.date_of_join = python_data.get('date_of_join', employee.date_of_join)
            employee.date_of_birth = python_data.get('date_of_birth', employee.date_of_birth)
            employee.gender_id = python_data.get('gender', employee.gender)
            employee.mobile = python_data.get('mobile', employee.mobile)
            employee.email = python_data.get('email', employee.email)

            employee.hr_employee = python_data.get('hr_employee', employee.hr_employee)
            employee.hr_corporate_code = python_data.get('hr_corporate_code', employee.hr_corporate_code)
            employee.address = python_data.get('address', employee.address)
            employee.pincode = python_data.get('pincode', employee.pincode)
            employee.state = python_data.get('state', employee.state)
            employee.city = python_data.get('city', employee.city)
            
            employee.save()

            self_data_id = models.EmployeeDependent.objects.filter(employee = employee.id, dependent_relation__relation= 'Self').values_list('id', flat=True)[0]
            self_data_update = models.EmployeeDependent.objects.get(id = self_data_id)
            self_data_update.date_of_birth = python_data.get('date_of_birth', employee.date_of_birth)
            self_data_update.save()


            for count in range(1, 20):
                dependent_relation = 'dependent_relation' + str(count)
                date_of_birth = 'date_of_birth' + str(count)
                gender = 'gender' + str(count)
                dependent_name = 'dependent_name' + str(count)

                if python_data.get(dependent_relation) and python_data.get(date_of_birth) and python_data.get(gender) and python_data.get(dependent_name):
                    dependent_relation_data = python_data.get(dependent_relation)
                    date_of_birth_data = python_data.get(date_of_birth)
                    gender_data = python_data.get(gender)
                    dependent_name_data = python_data.get(dependent_name)

                    dependent_check = models.EmployeeDependent.objects.filter(employee = employee.id, dependent_relation_id= dependent_relation_data).count()
                    if dependent_check == 0:
                        dependent_create = models.EmployeeDependent.objects.create(
                            employee_id = employee.id,
                            dependent_name = dependent_name_data,
                            dependent_relation_id = dependent_relation_data, 
                            date_of_birth = date_of_birth_data,
                            gender_id = gender_data,
                            created_at = current_time
                        ).save()
                    elif dependent_check == 0:
                        get_dependent_id = models.EmployeeDependent.objects.filter(employee = employee.id, dependent_relation_id= dependent_relation_data).values_list('id', flat=True)[0]
                        dependent = models.EmployeeDependent.objects.get(id = get_dependent_id)
                        dependent.dependent_name = dependent_name_data
                        dependent.date_of_birth = date_of_birth_data
                        dependent.gender_id = gender_data
                        dependent.save()
                    else:
                        pass
                else:
                    break

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Employee Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        
        else:
            check_mobile = models.EmployeeDetail.objects.filter(mobile = mobile).count()
            if check_mobile == 0:
                employee = models.EmployeeDetail.objects.get(id = id)
                employee.corporate_id = python_data.get('corporate', employee.corporate)
                employee.employee_name = python_data.get('employee_name', employee.employee_name)
                employee.employee_code = str(python_data.get('employee_code', employee.employee_code)).upper()
                employee.department = python_data.get('department', employee.department)
                employee.date_of_join = python_data.get('date_of_join', employee.date_of_join)
                employee.date_of_birth = python_data.get('date_of_birth', employee.date_of_birth)
                employee.gender_id = python_data.get('gender', employee.gender)
                employee.mobile = python_data.get('mobile', employee.mobile)
                employee.email = python_data.get('email', employee.email)

                employee.hr_employee = python_data.get('hr_employee', employee.hr_employee)
                employee.hr_corporate_code = python_data.get('hr_corporate_code', employee.hr_corporate_code)
                employee.address = python_data.get('address', employee.address)
                employee.pincode = python_data.get('pincode', employee.pincode)
                employee.state = python_data.get('state', employee.state)
                employee.city = python_data.get('city', employee.city)
                
                employee.save()
                self_data_id = models.EmployeeDependent.objects.filter(employee = employee.id, dependent_relation__relation= 'Self').values_list('id', flat=True)[0]
                self_data_update = models.EmployeeDependent.objects.get(id = self_data_id)
                self_data_update.date_of_birth = python_data.get('date_of_birth', employee.date_of_birth)
                self_data_update.save()

                for count in range(1, 20):
                    dependent_relation = 'dependent_relation' + str(count)
                    date_of_birth = 'date_of_birth' + str(count)
                    gender = 'gender' + str(count)
                    dependent_name = 'dependent_name' + str(count)

                    if python_data.get(dependent_relation) and python_data.get(date_of_birth) and python_data.get(gender) and python_data.get(dependent_name):
                        dependent_relation_data = python_data.get(dependent_relation)
                        date_of_birth_data = python_data.get(date_of_birth)
                        gender_data = python_data.get(gender)
                        dependent_name_data = python_data.get(dependent_name)

                        dependent_check = models.EmployeeDependent.objects.filter(employee = employee.id, dependent_relation_id= dependent_relation_data).count()
                        if dependent_check == 0:
                            dependent_create = models.EmployeeDependent.objects.create(
                                employee_id = employee.id,
                                dependent_name = dependent_name_data,
                                dependent_relation_id = dependent_relation_data, 
                                date_of_birth = date_of_birth_data,
                                gender_id = gender_data,
                                created_at = current_time
                            ).save()
                        elif dependent_check == 0:
                            get_dependent_id = models.EmployeeDependent.objects.filter(employee = employee.id, dependent_relation_id= dependent_relation_data).values_list('id', flat=True)[0]
                            dependent = models.EmployeeDependent.objects.get(id = get_dependent_id)
                            dependent.dependent_name = dependent_name_data
                            dependent.date_of_birth = date_of_birth_data
                            dependent.gender_id = gender_data
                            dependent.save()
                        else:
                            pass
                    else:
                        break

                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Employee Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')     
        
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter mobile number already Registered."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def employee_profile_image_update(request):
    if request.method == 'POST':
        python_data={}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})
        
        employee = python_data.get('employee')
        profile_image = python_data.get('profile_image')
        check_emp = models.EmployeeDetail.objects.filter(id = employee).count()
        if check_emp == 1:
            employee = models.EmployeeDetail.objects.get(id = employee)
            if type(python_data.get('profile_image', employee.profile_image)) != str: 
                employee.profile_image = python_data.get('profile_image', employee.profile_image)
            employee.save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Profile Image Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Employee."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')



@csrf_exempt
def employee_data_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')
        employee_name = python_data.get('employee_name')
        date_of_birth = python_data.get('date_of_birth')
        gender = python_data.get('gender')
        mobile = python_data.get('mobile')
        email = python_data.get('email')
        address = python_data.get('address')
        pincode = python_data.get('pincode')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")

        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        if check_employee == 1:
            employee_data = models.EmployeeDetail.objects.get(id = employee)
            get_employee_name = employee_data.employee_name
            get_date_of_birth = employee_data.date_of_birth
            get_gender = employee_data.gender
            get_mobile = employee_data.mobile
            get_email = employee_data.email
            get_address = employee_data.address
            get_pincode = employee_data.pincode

            if get_employee_name != employee_name or get_date_of_birth != date_of_birth or get_gender != gender or \
                get_mobile != mobile or get_email != email or get_address != address or get_pincode != pincode:

                data = models.EmployeeUpdateHistory.objects.create(
                    employee_id = employee,
                    employee_name = employee_name,
                    date_of_birth =date_of_birth,
                    gender_id =gender,
                    mobile =mobile,
                    email =email,
                    address =address,
                    pincode =pincode,
                    status = 'Pending',
                    created_at = current_time
                ).save()

                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your Data Submit Successfully, HR will check and update your data."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your Didn't Change any data."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Employee."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def new_employee_dependent_request(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')
        dependent_name = python_data.get('dependent_name')
        dependent_relation = python_data.get('dependent_relation')
        date_of_birth = python_data.get('date_of_birth')
        gender = python_data.get('gender')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")


        add_dependent = models.NewEmployeeDependentRequest.objects.create(
            employee_id = employee, 
            dependent_name = dependent_name,
            dependent_relation_id = dependent_relation,
            date_of_birth = date_of_birth,
            gender_id = gender,
            created_at = current_time
        ).save()
        res = {
            'statuscode' : 200,
            'status':'true',
            'message' : "HR will respond you as soon as possible."
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def employee_status_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_emp = models.EmployeeDetail.objects.filter(id = id).count()
        if check_emp == 1:
            employee = models.EmployeeDetail.objects.get(id = id)
            employee.status = status
            employee.save()

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Status Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Staff."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def list_all_employee(request):
    if request.method == 'POST':
        get_data={}
        for i,j in request.FILES.items():
            get_data.update({i:j})

        for i,j in request.POST.items():
            get_data.update({i:j})

        base64_string = get_data.get('data')
        base64_bytes = base64_string.encode("ascii")
        string_bytes = base64.b64decode(base64_bytes)
        python_data = string_bytes.decode("ascii")
        python_data = json.loads(python_data)

        page_number = int(python_data.get('page_number',1))
        row_size = int(python_data.get('row_size',10))
        last_row = row_size * page_number
        first_row = last_row - row_size

        filter_condition = {}

        employee_code = python_data.get('employee_code',None)
        employee_name = python_data.get('employee_name',None)
        corporate_name = python_data.get('corporate_name',None)
        department = python_data.get('department',None)
        date_of_join = python_data.get('date_of_join',None)
        date_of_birth = python_data.get('date_of_birth',None)
        gender_name = python_data.get('gender_name',None)
        mobile = python_data.get('mobile',None)
        email = python_data.get('email',None)
        hr_employee = python_data.get('hr_employee',None)
        city = python_data.get('city',None)
        status = python_data.get('status',None)

        if employee_code not in [None,'','null']:
            filter_condition['employee_code__icontains']=employee_code
        if employee_name not in [None,'','null']:
            filter_condition['employee_name__icontains']=employee_name
        if corporate_name not in [None,'','null']:
            filter_condition['corporate__corporate_name__icontains']=corporate_name
        if department not in [None,'','null']:
            filter_condition['department__icontains']=department
        if date_of_join not in [None,'','null']:
            filter_condition['date_of_join__icontains']=date_of_join
        if date_of_birth not in [None,'','null']:
            filter_condition['date_of_birth__icontains']=date_of_birth
        if gender_name not in [None,'','null']:
            gender_name = gender_name.lower()
            if gender_name in ['f','e','fe','fem','fema','femal','female']:
                filter_condition['gender__gender__icontains']="Female"
            elif gender_name in ['m','ma','mal','male']:
                filter_condition['gender__gender__iexact']="Male"

        if mobile not in [None,'','null']:
            filter_condition['mobile__icontains']=mobile
        if email not in [None,'','null']:
            filter_condition['email__icontains']=email
        if hr_employee not in [None,'','null']:
            filter_condition['hr_employee__icontains']=hr_employee
        if city not in [None,'','null']:
            filter_condition['city__icontains']=city
        if status not in [None,'','null']:
            if status != 'All':
                filter_condition['status'] = status



        id = python_data.get('id')
        check_staff = models.StaffDetail.objects.filter(id = id).count()

        if check_staff == 1:
            staff_id = models.StaffDetail.objects.get(id = id)
            get_type_access = staff_id.type_of_access.type_of_access
            if get_type_access == 'Super Admin' or get_type_access == 'Admin': 
                total_records = models.EmployeeDetail.objects.filter(**filter_condition).count()
                all_emp = models.EmployeeDetail.objects.filter(**filter_condition).order_by('-id')[first_row:last_row]
                list_data = []
                for emp in all_emp:
                    emp = models.EmployeeDetail.objects.get(id = emp.id)
                    serialiser = EmployeeDetailSerializer(emp)
                    data = serialiser.data

                    address = models.EmployeeAddressDetail.objects.filter(employee = emp.id)
                    address_data = EmployeeAddressDetailSerialiser(address, many=True).data
                    
                    all_dependent = models.EmployeeDependent.objects.filter(employee = emp).order_by('id')
                    
                    list_dependent = []
                    for dependent in all_dependent:
                        self_id = models.Relation.objects.filter(relation = 'Self').values_list('id', flat=True)[0]
                        relation = dependent.dependent_relation.id
                        if self_id != relation:
                            dependent_serialiser = EmployeeDependentSerializer(dependent)
                            list_dependent.append(dependent_serialiser.data)
                        
                    data.update({'user_address': address_data, 'dependent_data':list_dependent})
                    list_data.append(data)
                
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'data' : list_data,
                    'total_records': total_records
                    }
                
                data = json.dumps(res)
                encoded_dict = str(data).encode('utf-8')
                data = base64.b64encode(encoded_dict)
                json_data = JSONRenderer().render(data)
                return HttpResponse(json_data, content_type= 'application/json') 
                
            else:
                all_corporate = models.CorporateDetail.objects.filter(Q(level1 =staff_id) | Q(level2 =staff_id )).distinct()
                serialiser = CorporateDataSerializer(all_corporate, many=True)
                for corporate in all_corporate:

                    total_records = models.EmployeeDetail.objects.filter(**filter_condition, corporate = corporate).count()
                    all_emp = models.EmployeeDetail.objects.filter(**filter_condition, corporate = corporate).order_by('-id')[first_row:last_row]
                    list_data = []
                    for emp in all_emp:
                        emp = models.EmployeeDetail.objects.get(id = emp.id)
                        serialiser = EmployeeDetailSerializer(emp)
                        data = serialiser.data

                        address = models.EmployeeAddressDetail.objects.filter(employee = emp.id)
                        address_data = EmployeeAddressDetailSerialiser(address, many=True).data
                        
                        all_dependent = models.EmployeeDependent.objects.filter(employee = emp).order_by('id')
                        
                        list_dependent = []
                        for dependent in all_dependent:
                            self_id = models.Relation.objects.filter(relation = 'Self').values_list('id', flat=True)[0]
                            relation = dependent.dependent_relation.id
                            if self_id != relation:
                                dependent_serialiser = EmployeeDependentSerializer(dependent)
                                list_dependent.append(dependent_serialiser.data)
                            
                        data.update({'user_address': address_data,'dependent_data':list_dependent})
                        list_data.append(data)
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'data' : list_data,
                    'total_records': total_records
                    }
                
                data = json.dumps(res)
                encoded_dict = str(data).encode('utf-8')
                data = base64.b64encode(encoded_dict)
                json_data = JSONRenderer().render(data)
                return HttpResponse(json_data, content_type= 'application/json')     

@csrf_exempt
def employee_address_list(request):
    if request.method == 'POST':
        get_data={}
        for i,j in request.FILES.items():
            get_data.update({i:j})

        for i,j in request.POST.items():
            get_data.update({i:j})
            
        base64_string = get_data.get('data')
        base64_bytes = base64_string.encode("ascii")
        string_bytes = base64.b64decode(base64_bytes)
        python_data = string_bytes.decode("ascii")
        python_data = json.loads(python_data)

        id = python_data.get('id')
        address = models.EmployeeAddressDetail.objects.filter(employee = id)
        address_data = EmployeeAddressDetailSerialiser(address, many=True).data            

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : address_data
            }
        
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def individual_address_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        individual_address = models.IndividualAddressDetail.objects.filter(individual = id)
        address_data = IndividualAddressDetailSerialiser(individual_address, many=True).data

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : address_data
            }
        
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



# @csrf_exempt
# def list_all_employee(request):
#     if request.method == 'POST':
        

#         all_emp = models.EmployeeDetail.objects.all().order_by('-id')
#         list_data = []
#         for emp in all_emp:
#             emp = models.EmployeeDetail.objects.get(id = emp.id)
#             serialiser = EmployeeDetailSerializer(emp)
#             data = serialiser.data
#             all_dependent = models.EmployeeDependent.objects.filter(employee = emp).order_by('id')
            
#             list_dependent = []
#             for dependent in all_dependent:
#                 self_id = models.Relation.objects.filter(relation = 'Self').values_list('id', flat=True)[0]
#                 relation = dependent.dependent_relation.id
#                 if self_id != relation:
#                     dependent_serialiser = EmployeeDependentSerializer(dependent)
#                     list_dependent.append(dependent_serialiser.data)
                
#             data.update({'dependent_data':list_dependent})
#             list_data.append(data)
                

#         res = {
#             'statuscode' : 200,
#             'status':'true',
#             'data' : list_data
#             }
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def active_employee_list(request):
    if request.method == 'POST':
        all_emp = models.EmployeeDetail.objects.filter(status='Active').order_by('-id')
        list_dependent = []
        for emp in all_emp:
            emp = models.EmployeeDetail.objects.get(id = emp.id)
            serialiser = EmployeeDetailSerializer(emp)
            data = serialiser.data
            dependent = models.EmployeeDependent.objects.filter(employee = emp).order_by('id')
            dependent_serialiser = EmployeeDependentSerializer(dependent, many=True)
            data.update({'dependent_data':dependent_serialiser.data})
            list_dependent.append(data)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_dependent
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def employee_dependent_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')
        all_dependent = models.EmployeeDependent.objects.filter(employee = employee).order_by('id')
        serialiser = EmployeeDependentSerializer(all_dependent, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def update_dependent_employee(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))        
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        employee = python_data.get('employee')
        id = python_data.get('id')
        dependent_relation = python_data.get('dependent_relation')
        date_of_birth = python_data.get('date_of_birth')
        gender = python_data.get('gender')
        dependent_name = python_data.get('dependent_name')
        
        child_id = models.Relation.objects.filter(relation = 'Child').values_list('id', flat=True)[0]


        check_dependent = models.EmployeeDependent.objects.filter(id = id, employee=employee).count()
        if check_dependent == 1:
            if dependent_relation != child_id:
                dependent_relation_check = models.EmployeeDependent.objects.filter(id = id, employee=employee, dependent_relation= dependent_relation).count()
                if dependent_relation_check == 1:
                    dependent = models.EmployeeDependent.objects.get(id = id)
                    dependent.dependent_name = python_data.get('dependent_name', dependent.dependent_name)
                    dependent.dependent_relation_id = python_data.get('dependent_relation', dependent.dependent_relation)
                    dependent.date_of_birth = python_data.get('date_of_birth', dependent.date_of_birth)
                    dependent.gender_id = python_data.get('gender', dependent.gender)
                    dependent.save()
                    
                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':"Dependent Update Successfully." ,
                        }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')  
                else:
                    dependent_relation_check = models.EmployeeDependent.objects.filter(employee=employee, dependent_relation= dependent_relation).count()
                    if dependent_relation_check == 0:
                        dependent = models.EmployeeDependent.objects.get(id = id)
                        dependent.dependent_name = python_data.get('dependent_name', dependent.dependent_name)
                        dependent.dependent_relation_id = python_data.get('dependent_relation', dependent.dependent_relation)
                        dependent.date_of_birth = python_data.get('date_of_birth', dependent.date_of_birth)
                        dependent.gender_id = python_data.get('gender', dependent.gender)
                        dependent.save()
                        
                        res = {
                            'statuscode' : 200,
                            'status':'Success',
                            'message':"Dependent Update Successfully." ,
                            }                                                        
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')  
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message':"Dependent Relation already exists." ,
                            }                                                        
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')

            elif dependent_relation == child_id:
                child_count = models.EmployeeDependent.objects.filter(dependent_relation_id = child_id).count()

                if child_count <= 3:
                    dependent = models.EmployeeDependent.objects.get(id = id)
                    dependent.dependent_name = python_data.get('dependent_name', dependent.dependent_name)
                    dependent.dependent_relation_id = python_data.get('dependent_relation', dependent.dependent_relation)
                    dependent.date_of_birth = python_data.get('date_of_birth', dependent.date_of_birth)
                    dependent.gender_id = python_data.get('gender', dependent.gender)
                    dependent.save()
                    
                    
                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':"Dependent Update Successfully." ,
                        }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')  
                
                
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "You already added 3 child."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def individual_dependent_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        individual = python_data.get('individual')
        
        all_dependent = models.IndividualDependent.objects.filter(individual = individual).order_by('id')
        
        serialiser = IndividualDependentSerializer(all_dependent, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def package_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        corporate_selection = python_data.get('corporate_selection', None)
        test_category = python_data.get('test_category', None)
        test_subcategory = python_data.get('test_subcategory', None)
        package = models.PackageDetail.objects.create(
            package_type = python_data.get('package_type'),
            package_name = python_data.get('package_name'),
            vendor_id = python_data.get('vendor'),
            package_code = str(python_data.get('package_code')).upper(),
            
            MRP = python_data.get('MRP'),
            base_amount = python_data.get('base_amount'),
            profit = python_data.get('profit'),
            tax = python_data.get('tax'),
            tax_amount = python_data.get('tax_amount'),
            igst = python_data.get('igst'),
            igst_amount = python_data.get('igst_amount'),
            sgst = python_data.get('sgst'),
            sgst_amount = python_data.get('sgst_amount'),
            cgst = python_data.get('cgst'),
            cgst_amount = python_data.get('cgst_amount'),
            discount_price = python_data.get('discount_price'),
            offer_price = python_data.get('offer_price'),
            
            total_test_number = python_data.get('total_test_number'),
            test_list = python_data.get('test_list'),


            corporate_selection = python_data.get('corporate_selection', None),
            type_of_service_id = python_data.get('type_of_service'),
            type_of_visit_id = python_data.get('type_of_visit'),

            start_date = python_data.get('start_date'),
            end_date = python_data.get('end_date'),
            billing_cycle_id = python_data.get('billing_cycle', None),
            tags_id = python_data.get('tags'),
            description = python_data.get('description'),
            preparation_description = python_data.get('preparation_description'),
            detail_description = python_data.get('detail_description'),
            


            gender_id = python_data.get('gender'),
            age_category_id = python_data.get('age_category'),
            # relation_gender_id = python_data.get('relation_gender'),
            status = 'Active',
            created_at = current_time
        )
        package.save()

        if corporate_selection != None:
            if corporate_selection == 'All':
                all_corporate = models.CorporateDetail.objects.filter(status = 'Active').values_list('id',flat=True)
                package.corporate.set(all_corporate)
            else:
                if python_data.get('corporate') == '':
                    package.corporate.set([])
                else:
                    package.corporate.set((python_data.get('corporate', package.corporate)))
        # try:
        #     for category in test_category:
        #         key_data = category.get('key')
        #         value_data = category.get('value')
                
        #         category_data = models.TestsProductDetail.objects.create(
        #             test_category_id = key_data,
        #             package_id = package.id,
        #             value = value_data,
        #             created_at = current_time,
        #         ).save()

        #     for subcategory in test_subcategory:
        #         key_data = subcategory.get('key')
        #         value_data = subcategory.get('value')
        #         get_subcategory = models.TestSubCategory.objects.get(id = key_data)
        #         get_category = get_subcategory.test_category.id

        #         category_data = models.TestsProductDetail.objects.create(
        #             test_category_id = get_category,
        #             test_subcategory_id = get_subcategory.id,
        #             package_id = package.id,
        #             value = value_data,
        #             created_at = current_time,
        #         ).save()
        # except:
        #     pass
        
        if python_data.get('relation_with_employee') == '':
            package.relation_with_employee.set([])
        else:
            package.relation_with_employee.set((python_data.get('relation_with_employee', package.relation_with_employee)))
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'message' : "Package Added Successfully."
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 
        


@csrf_exempt
def package_tests(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        test_category = python_data.get('test_category')
        test_subcategory = python_data.get('test_subcategory')
        package = python_data.get('package')
        print(python_data, 'python_data')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        for category in test_category:
            key_data = category.get('key')
            value_data = category.get('value')
            id_data = category.get('id')
            if id_data:
                category_data = models.TestsProductDetail.objects.get(id = id_data)
                category_data.test_category_id = key_data
                category_data.package_id = package
                category_data.value = value_data
                category_data.save()
            else:
                category_data = models.TestsProductDetail.objects.create(
                    test_category_id = key_data,
                    package_id = package,
                    value = value_data,
                    created_at = current_time,
                ).save()

        for subcategory in test_subcategory:
            key_data = subcategory.get('key')
            value_data = subcategory.get('value')
            get_subcategory = models.TestSubCategory.objects.get(id = key_data)
            get_category = get_subcategory.test_category.id
            id_data = subcategory.get('id')
            if id_data:
                subcategory_data = models.TestsProductDetail.objects.get(id = id_data)
                subcategory_data.test_category_id = get_category
                subcategory_data.test_subcategory_id = get_subcategory.id
                subcategory_data.package_id = package
                subcategory_data.value = value_data
                subcategory_data.save()
            else:
                subcategory_data = models.TestsProductDetail.objects.create(
                    test_category_id = get_category,
                    test_subcategory_id = key_data,
                    package_id = package,
                    value = value_data,
                    created_at = current_time,
                ).save()

        res = {
            'statuscode' : 200,
            'status':'true',
            'message' : "Tests Added Successfully."
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def package_tests_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        test_category = python_data.get('test_category')
        test_subcategory = python_data.get('test_subcategory')
        package = python_data.get('package')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")

        get_all_category = list(models.TestsProductDetail.objects.filter(package = package, test_subcategory = None).values_list('test_category', flat=True).distinct())

        # for category in test_category:
        #     key_data = category.get('key')
        #     value_data = category.get('value')
            
        #     category_data = models.TestsProductDetail.objects.create(
        #         test_category_id = key_data,
        #         package_id = package,
        #         value = value_data,
        #         created_at = current_time,
        #     ).save()

        # for subcategory in test_subcategory:
        #     key_data = subcategory.get('key')
        #     value_data = subcategory.get('value')
        #     get_subcategory = models.TestSubCategory.objects.get(id = key_data)
        #     get_category = get_subcategory.test_category.id

        #     category_data = models.TestsProductDetail.objects.create(
        #         test_category_id = get_category,
        #         test_subcategory_id = get_subcategory.id,
        #         package_id = package,
        #         value = value_data,
        #         created_at = current_time,
        #     ).save()

        res = {
            'statuscode' : 200,
            'status':'true',
            'message' : "Tests Added Successfully."
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def package_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        corporate_selection = python_data.get('corporate_selection', None)

        check_package = models.PackageDetail.objects.filter(id = id).count()
        if check_package == 1:
            package = models.PackageDetail.objects.get(id = id)
            package.package_type = python_data.get('package_type', package.package_type)
            package.package_name = python_data.get('package_name', package.package_name)
            package.package_code = str(python_data.get('package_code', package.package_code)).upper()
            package.vendor_id = python_data.get('vendor', package.vendor)
            package.MRP = python_data.get('MRP', package.MRP)
            package.base_amount = python_data.get('base_amount', package.base_amount)
            package.profit = python_data.get('profit', package.profit)
            package.tax = python_data.get('tax', package.tax)
            package.tax_amount = python_data.get('tax_amount', package.tax_amount)
            package.igst = python_data.get('igst', package.igst)
            package.igst_amount = python_data.get('igst_amount', package.igst_amount)
            package.sgst = python_data.get('sgst', package.sgst)
            package.sgst_amount = python_data.get('sgst_amount', package.sgst_amount)
            package.cgst = python_data.get('cgst', package.cgst)
            package.cgst_amount = python_data.get('cgst_amount', package.cgst_amount)
            package.discount_price = python_data.get('discount_price', package.discount_price)
            package.offer_price = python_data.get('offer_price', package.offer_price)
            package.type_of_service_id = python_data.get('type_of_service', package.type_of_service)
            package.type_of_visit_id = python_data.get('type_of_visit', package.type_of_visit)
            package.corporate_id = python_data.get('corporate', package.corporate)
            package.start_date = python_data.get('start_date', package.start_date)
            package.total_test_number = python_data.get('total_test_number', package.total_test_number)
            package.test_list = python_data.get('test_list', package.test_list)

            package.end_date = python_data.get('end_date', package.end_date)
            package.billing_cycle_id = python_data.get('billing_cycle', package.billing_cycle)
            package.tags_id = python_data.get('tags', package.tags)
            package.description = python_data.get('description', package.description)
            package.preparation_description = python_data.get('preparation_description', package.preparation_description)
            package.detail_description = python_data.get('detail_description', package.detail_description)
            

            # package.package_applicable = python_data.get('package_applicable', package.package_applicable)
            package.age_category_id = python_data.get('age_category', package.age_category)
            package.gender_id = python_data.get('gender', package.gender) 
            package.corporate_selection = python_data.get('corporate_selection', package.corporate_selection) 
            package.save()

            if corporate_selection != None:
                if corporate_selection == 'All':
                    all_corporate = models.CorporateDetail.objects.filter(status = 'Active').values_list('id',flat=True)
                    package.corporate.set(all_corporate)
                else:
                    if python_data.get('corporate') == '':
                        package.corporate.set([])
                    else:
                        package.corporate.set((python_data.get('corporate', package.corporate)))


            try:
                if python_data.get('relation_with_employee') == '':
                    package.relation_with_employee.set([])
                else:
                    package.relation_with_employee.set((python_data.get('relation_with_employee', package.relation_with_employee)))
            except:
                pass

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "package Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid package."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def package_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        package = python_data.get('id')
        check_package = models.PackageDetail.objects.filter(id = package).count()
        if check_package == 1:
            
            package_details = models.PackageDetail.objects.get(id = package)
            package_details.status = 'Inactive'
            package_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Package Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Package ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def package_status_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_package = models.PackageDetail.objects.filter(id = id).count()
        if check_package == 1:
            package = models.PackageDetail.objects.get(id = id)
            package.status = status
            package.save()

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Status Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid package."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def list_all_package(request):
    if request.method == 'POST':
        python_data = {}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})

        data = python_data.get('data')

        try:
            decoded_bytes = base64.b64decode(data)
            decoded_python_data = json.loads(decoded_bytes.decode('utf-8'))
        except:
            decoded_python_data = {}

        page_number = int(decoded_python_data.get('page_number',1))
        row_size = int(decoded_python_data.get('row_size',10))
        last_row = row_size * page_number
        first_row = last_row - row_size

        package_code = decoded_python_data.get('package_code',None)
        package_name = decoded_python_data.get('package_name',None)
        package_type = decoded_python_data.get('package_type',None)
        MRP = decoded_python_data.get('MRP',None)
        discount_price = decoded_python_data.get('discount_price',None)
        offer_price = decoded_python_data.get('offer_price',None)
        type_of_service_name = decoded_python_data.get('type_of_service_name',None)
        type_of_visit_name = decoded_python_data.get('type_of_visit_name',None)
        age_category_name = decoded_python_data.get('age_category_name',None)
        gender_name = decoded_python_data.get('gender_name',None)
        corporate_list = decoded_python_data.get('corporate_list',None)
        start_date = decoded_python_data.get('start_date',None)
        end_date = decoded_python_data.get('end_date',None)
        billing_cycle_name = decoded_python_data.get('billing_cycle_name',None)
        tags_name = decoded_python_data.get('tags_name',None)
        status = decoded_python_data.get('status',None)

        filter_condition = {}

        if package_code not in [None,'','null']:
            filter_condition['package_code__icontains'] = package_code
        if package_name not in [None,'','null']:
            filter_condition['package_name__icontains'] = package_name
        if package_type not in [None,'','null']:
            filter_condition['package_type__icontains'] = package_type
        if MRP not in [None,'','null']:
            filter_condition['MRP__icontains'] = MRP
        if discount_price not in [None,'','null']:
            filter_condition['discount_price__icontains'] = discount_price
        if offer_price not in [None,'','null']:
            filter_condition['offer_price__icontains'] = offer_price
        if type_of_service_name not in [None,'','null']:
            filter_condition['type_of_service__type_of_service__icontains'] = type_of_service_name
        if type_of_visit_name not in [None,'','null']:
            filter_condition['type_of_visit__type_of_visit__icontains'] = type_of_visit_name
        if age_category_name not in [None,'','null']:
            filter_condition['age_category__age_category__icontains'] = age_category_name
        if gender_name not in [None,'','null']:
            filter_condition['gender__gender__icontains'] = gender_name
        if corporate_list not in [None,'','null']:
            filter_condition['corporate__corporate_name__icontains'] = corporate_list
        if start_date not in [None,'','null']:
            filter_condition['start_date__gte'] = start_date
        if end_date not in [None,'','null']:
            filter_condition['end_date__lte'] = end_date
        if billing_cycle_name not in [None,'','null']:
            filter_condition['billing_cycle__billing_cycle__icontains'] = billing_cycle_name
        if tags_name not in [None,'','null']:
            filter_condition['tags__payment_tags__icontains'] = tags_name
        if status not in [None,'','null']:
            if status != 'All':
                filter_condition['status'] = status




        # total_records = models.PackageDetail.objects.filter(**filter_condition).order_by('-id').count()
        # print("total_records----->",total_records)
        # all_emp = models.PackageDetail.objects.filter(**filter_condition).order_by('-id')[first_row:last_row]
        # serialiser = PackageDetailSerializer(all_emp, many=True)
        
        total_records = models.PackageDetail.objects.filter(**filter_condition).order_by('-id').count()
        list_data = []
        all_emp = models.PackageDetail.objects.filter(**filter_condition).order_by('-id')[first_row:last_row]
        for emp in all_emp:
            emp = models.PackageDetail.objects.get(id = emp.id)
            serialiser = PackageDetailSerializer(emp).data
            all_test_category = models.TestsProductDetail.objects.filter(package = emp.id, test_subcategory = None)
            test_category = []
            for category in all_test_category:
                category_data = models.TestsProductDetail.objects.filter(id = category.id).values_list('test_category', 'value', 'id')[0]
                key = category_data[0]
                value = category_data[1]
                id = category_data[2]
                test_category.append({'id':id, 'key':key, 'value':value})

            all_test_subcategory = models.TestsProductDetail.objects.filter(package = emp.id).exclude(test_subcategory = None)
            test_subcategory = []
            for subcategory in all_test_subcategory:
                subcategory_data = models.TestsProductDetail.objects.filter(id = subcategory.id).values_list('test_subcategory', 'value', 'id')[0]
                key = subcategory_data[0]
                value = subcategory_data[1]
                id = subcategory_data[2]
                test_subcategory.append({'id':id, 'key':key, 'value':value})

            serialiser.update({'test_category':test_category})
            serialiser.update({'test_subcategory':test_subcategory})
            list_data.append(serialiser)

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data,
            'total_records':total_records
            }
                
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_package(request):
    if request.method == 'POST':
        all_package = models.PackageDetail.objects.filter(status='Active').order_by('-id')
        serialiser = PackageNameSerializer(all_package, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def employee_list_by_corporate(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        corporate_id = python_data.get('corporate_id')
        check_corporate = models.CorporateDetail.objects.filter(id = corporate_id).count()
        if check_corporate == 1:
            employee_list = models.EmployeeDetail.objects.filter(corporate = corporate_id, status='Active').order_by('-id')
            serialiser = EmployeeDataSerializer(employee_list, many=True)
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'data' : serialiser.data
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Corporate."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def center_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")

        center = models.CenterDetail.objects.create(
            center_name = python_data.get('center_name'),
            address = python_data.get('address'),
            pincode = python_data.get('pincode'),
            state = python_data.get('state'),
            city = python_data.get('city'),
            location = python_data.get('location'),
            # vendor_id = python_data.get('vendor'),
            # package_id = python_data.get('package'),
            # type_of_service_id = python_data.get('type_of_service'),
            latitude = python_data.get('latitude'),
            longitude = python_data.get('longitude'),
            map_link = python_data.get('map_link'),
            status = 'Active',
            created_at = current_time
        )
        center.save()
        if python_data.get('type_of_service') == '':
            center.type_of_service.set([])
        else:
            center.type_of_service.set(python_data.get('type_of_service', center.type_of_service))

        if python_data.get('vendor') == '':
            center.vendor.set([])
        else:
            center.vendor.set(python_data.get('vendor', center.vendor))
    
        if python_data.get('package') == '':
            center.package.set([])
        else:
            center.package.set(python_data.get('package', center.package))
    


        res = {
            'statuscode' : 200,
            'status':'true',
            'message' : "Center Added Successfully."
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 
        
@csrf_exempt
def center_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_center = models.CenterDetail.objects.filter(id = id).count()
        if check_center == 1:
            center = models.CenterDetail.objects.get(id = id)
            center.center_name = python_data.get('center_name', center.center_name)
            center.address = python_data.get('address', center.address)
            center.pincode = python_data.get('pincode', center.pincode)
            center.state = python_data.get('state', center.state)
            center.city = python_data.get('city', center.city)
            center.location = python_data.get('location', center.location)
            # center.vendor_id = python_data.get('vendor', center.vendor)
            # center.package_id = python_data.get('package', center.package)
            center.type_of_service_id = python_data.get('type_of_service', center.type_of_service)
            center.latitude = python_data.get('latitude', center.latitude)
            center.longitude = python_data.get('longitude', center.longitude)
            center.map_link = python_data.get('map_link', center.map_link)
            
            center.save()
            if python_data.get('type_of_service') == '':
                center.type_of_service.set([])
            else:
                center.type_of_service.set(python_data.get('type_of_service', center.type_of_service))
                
            if python_data.get('vendor') == '':
                center.vendor.set([])
            else:
                center.vendor.set(python_data.get('vendor', center.vendor))
        
            if python_data.get('package') == '':
                center.package.set([])
            else:
                center.package.set(python_data.get('package', center.package))
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "center Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid center."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def center_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        center = python_data.get('id')
        check_center = models.CenterDetail.objects.filter(id = center).count()
        if check_center == 1:
            
            center_details = models.CenterDetail.objects.get(id = center)
            center_details.status = 'Inactive'
            center_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Center Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Center ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def active_center_list(request):
    if request.method == 'POST':
        active_center_list = models.CenterDetail.objects.filter(status = 'Active').order_by('-id')
        serialiser = ActiveCenterDetailTransaction(active_center_list, many=True)
            
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 
    


@csrf_exempt
def package_wise_center(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        package = python_data.get('package')
        # package = request.POST['package']
        check_package = models.PackageDetail.objects.filter(id = package).count()
        if check_package == 1:
            get_all_center = models.CenterDetail.objects.filter(package = package)
            serialiser = CenterDetailSerializer(get_all_center, many=True)
            res = {
                'statuscode' : 200,
                'status':'true',
                'data':serialiser.data
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        

@csrf_exempt
def center_status_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_center = models.CenterDetail.objects.filter(id = id).count()
        if check_center == 1:
            center = models.CenterDetail.objects.get(id = id)
            center.status = status
            center.save()

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Status Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid package."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def list_all_center(request):
    if request.method == 'POST':
        python_data = {}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})

        data = python_data.get('data')

        try:
            decoded_bytes = base64.b64decode(data)
            decoded_python_data = json.loads(decoded_bytes.decode('utf-8'))
        except:
            decoded_python_data = {}
        page_number = int(decoded_python_data.get('page_number',1))
        row_size = int(decoded_python_data.get('row_size',10))
        last_row = row_size * page_number
        first_row = last_row - row_size

        center_name = decoded_python_data.get('center_name',None)
        state = decoded_python_data.get('state',None)
        city = decoded_python_data.get('city',None)
        location = decoded_python_data.get('location',None)
        pincode = decoded_python_data.get('pincode',None)
        address_short = decoded_python_data.get('address_short',None)
        vendor_name = decoded_python_data.get('vendor_name',None)
        package_name_list = decoded_python_data.get('package_name_list',None)
        type_of_service_name = decoded_python_data.get('type_of_service_name',None)
        latitude = decoded_python_data.get('latitude',None)
        longitude = decoded_python_data.get('longitude',None)

        status = decoded_python_data.get('status',None)

        filter_condition = {}

        if center_name not in [None,'','null']:
            filter_condition['center_name__icontains'] = center_name
        if state not in [None,'','null']:
            filter_condition['state__icontains'] = state
        if city not in [None,'','null']:
            filter_condition['city__icontains'] = city
        if location not in [None,'','null']:
            filter_condition['location__icontains'] = location
        if pincode not in [None,'','null']:
            filter_condition['pincode__icontains'] = pincode
        if address_short not in [None,'','null']:
            filter_condition['address_short__icontains'] = address_short
        if vendor_name not in [None,'','null']:
            filter_condition['vendor__vendor_name__icontains'] = vendor_name
        if package_name_list not in [None,'','null']:
            filter_condition['package__package_name__icontains'] = package_name_list
        if type_of_service_name not in [None,'','null']:
            filter_condition['type_of_service__type_of_service__icontains'] = type_of_service_name
        if latitude not in [None,'','null']:
            filter_condition['latitude__icontains'] = latitude
        if longitude not in [None,'','null']:
            filter_condition['longitude__icontains'] = longitude
        if status not in [None,'','null']:
            if status != 'All':
                filter_condition['status'] = status
        
        

        total_records = models.CenterDetail.objects.filter(**filter_condition).order_by('-id').count()
        all_center = models.CenterDetail.objects.filter(**filter_condition).order_by('-id')[first_row:last_row]
        serialiser = CenterDetailSerializer(all_center, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data,
            'total_records':total_records
            }

        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def center_serivce_list_by_vendor(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        vendor = python_data.get('vendor')
        get_center_count = models.CenterDetail.objects.filter(vendor = vendor).count()
        if get_center_count != 0:
            
            all_center = models.CenterDetail.objects.filter(vendor = vendor)
            list_center = []
            for center in all_center:
                center_name = center.center_name
                list_center.append(center_name)
            filter_center_data = list(set(list_center))
            
            list_data = []
            for center_data in filter_center_data:
                center_dict = {}

                center_service = models.CenterDetail.objects.filter(center_name = center_data)
                serialiser = CenterDetailSerializer(center_service, many=True)
                data = serialiser.data

                center_dict.update({'center_name':center_data, 'service_data':data})
                list_data.append(center_dict)
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def holiday_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        state_selection = python_data.get('state_selection')
        holiday_name = python_data.get('holiday_name')
        start_date = python_data.get('start_date')
        end_date = python_data.get('end_date')
        if state_selection == 'All State':
            holiday = models.HolidayDetail.objects.create(
                state_selection = state_selection,
                state = None,
                city_selection = None,
                city = None,
                center_selection = None,
                holiday_name = python_data.get('holiday_name'),
                start_date = python_data.get('start_date'),
                end_date = python_data.get('end_date'),
                status = 'Active'
            )
            holiday.save()
        
            get_all_center = models.CenterDetail.objects.all().values_list('id', flat=True)
            center_list = list(get_all_center)
            
            if center_list == '':
                holiday.center.set([])
            elif type(center_list) == int:
                holiday.center.set([eval(str(center_list))])
            else:                        
                holiday.center.set(center_list)
            

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Holiday Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

        elif state_selection == 'Select State':
            state = python_data.get('state')
            city_selection = python_data.get('city_selection')
            if city_selection == 'All City':
                holiday = models.HolidayDetail.objects.create(
                    state_selection = state_selection,
                    state = state,
                    city_selection = city_selection,
                    city = None,
                    center_selection = None,
                    holiday_name = python_data.get('holiday_name'),
                    start_date = python_data.get('start_date'),
                    end_date = python_data.get('end_date'),
                    status = 'Active'
                )
                holiday.save()

                center_list = []
                for get_state in state:
                    get_center = models.CenterDetail.objects.filter(state = get_state).values_list('id', flat=True)
                    list_center = list(get_center)
                    center_list.extend(list_center)

                
                if center_list == '':
                    holiday.center.set([])
                elif type(center_list) == int:
                    holiday.center.set([eval(str(center_list))])
                else:                        
                    holiday.center.set(center_list)
                

                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Holiday Create Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
            elif city_selection == 'Select City':
                city = python_data.get('city')
                center_selection = python_data.get('center_selection')
                if center_selection == 'All Center':
                    holiday = models.HolidayDetail.objects.create(
                        state_selection = state_selection,
                        state = state,
                        city_selection = city_selection,
                        city = city,
                        center_selection = center_selection,
                        holiday_name = python_data.get('holiday_name'),
                        start_date = python_data.get('start_date'),
                        end_date = python_data.get('end_date'),
                        status = 'Active'
                    )
                    holiday.save()
                
                    center_list = []
                    for get_city in city:
                        get_center = models.CenterDetail.objects.filter(city = get_city).values_list('id', flat=True)
                        list_center = list(get_center)
                        center_list.extend(list_center)
                        
                    if center_list == '':
                        holiday.center.set([])
                    elif type(center_list) == int:
                        holiday.center.set([eval(str(center_list))])
                    else:                        
                        holiday.center.set(center_list)
                    

                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Holiday Create Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                elif center_selection == 'Select Center':
                    center_list = python_data.get('center')
                    holiday = models.HolidayDetail.objects.create(
                        state_selection = state_selection,
                        state = state,
                        city_selection = city_selection,
                        city = city,
                        center_selection = center_selection,
                        holiday_name = python_data.get('holiday_name'),
                        start_date = python_data.get('start_date'),
                        end_date = python_data.get('end_date'),
                        status = 'Active'
                    )
                    holiday.save()
                
                    # center_list = []
                    # for get_city in city:
                    #     get_center = models.CenterDetail.objects.filter(city = get_city).values_list('id', flat=True)
                    #     list_center = list(get_center)
                    #     center_list.extend(list_center)
                        
                    if center_list == '':
                        holiday.center.set([])
                    elif type(center_list) == int:
                        holiday.center.set([eval(str(center_list))])
                    else:                        
                        holiday.center.set(center_list)
                    

                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Holiday Create Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
        
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Something Went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 





        
        

@csrf_exempt
def holiday_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        state_selection = python_data.get('state_selection')
        check_holiday = models.HolidayDetail.objects.filter(id = id).count()
        if check_holiday == 1:
            if state_selection == 'All State':
                holiday = models.HolidayDetail.objects.get(id = id)
                holiday.state_selection = state_selection
                holiday.state = None
                holiday.city_selection = None
                holiday.city = None
                holiday.center_selection = None
                holiday.holiday_name = python_data.get('holiday_name', holiday.holiday_name)
                holiday.start_date = python_data.get('start_date', holiday.start_date)
                holiday.end_date = python_data.get('end_date', holiday.end_date)
                holiday.status = python_data.get('status', holiday.status)
                holiday.save()
            
                get_all_center = models.CenterDetail.objects.all().values_list('id', flat=True)
                center_list = list(get_all_center)
                
                if center_list == '':
                    holiday.center.set([])
                elif type(center_list) == int:
                    holiday.center.set([eval(str(center_list))])
                else:                        
                    holiday.center.set(center_list)
                

                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Holiday Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

            elif state_selection == 'Select State':
                state = python_data.get('state')
                city_selection = python_data.get('city_selection')
                if city_selection == 'All City':
                    holiday = models.HolidayDetail.objects.get(id = id)
                    holiday.state_selection = state_selection
                    holiday.state = state
                    holiday.city_selection = city_selection
                    holiday.city = None
                    holiday.center_selection = None
                    holiday.holiday_name = python_data.get('holiday_name', holiday.holiday_name)
                    holiday.start_date = python_data.get('start_date', holiday.start_date)
                    holiday.end_date = python_data.get('end_date', holiday.end_date)
                    holiday.status = python_data.get('status', holiday.status)
                    holiday.save()

                    center_list = []
                    for get_state in state:
                        get_center = models.CenterDetail.objects.filter(state = get_state).values_list('id', flat=True)
                        list_center = list(get_center)
                        center_list.extend(list_center)

                    
                    if center_list == '':
                        holiday.center.set([])
                    elif type(center_list) == int:
                        holiday.center.set([eval(str(center_list))])
                    else:                        
                        holiday.center.set(center_list)
                    

                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Holiday Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                
                elif city_selection == 'Select City':
                    city = python_data.get('city')
                    center_selection = python_data.get('center_selection')
                    if center_selection == 'All Center':
                        holiday = models.HolidayDetail.objects.get(id = id)
                        holiday.state_selection = state_selection
                        holiday.state = state
                        holiday.city_selection = city_selection
                        holiday.city = city
                        holiday.center_selection = center_selection
                        holiday.holiday_name = python_data.get('holiday_name', holiday.holiday_name)
                        holiday.start_date = python_data.get('start_date', holiday.start_date)
                        holiday.end_date = python_data.get('end_date', holiday.end_date)
                        holiday.status = python_data.get('status', holiday.status)
                        holiday.save()
                    
                        center_list = []
                        for get_city in city:
                            get_center = models.CenterDetail.objects.filter(city = get_city).values_list('id', flat=True)
                            list_center = list(get_center)
                            center_list.extend(list_center)
                            
                        if center_list == '':
                            holiday.center.set([])
                        elif type(center_list) == int:
                            holiday.center.set([eval(str(center_list))])
                        else:                        
                            holiday.center.set(center_list)
                        

                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Holiday Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    elif center_selection == 'Select Center':
                        center_list = python_data.get('center')
                        holiday = models.HolidayDetail.objects.get(id = id)
                        holiday.state_selection = state_selection,
                        holiday.state = state
                        holiday.city_selection = city_selection
                        holiday.city = city
                        holiday.center_selection = center_selection
                        holiday.holiday_name = python_data.get('holiday_name', holiday.holiday_name)
                        holiday.start_date = python_data.get('start_date', holiday.start_date)
                        holiday.end_date = python_data.get('end_date', holiday.end_date)
                        holiday.status = python_data.get('status', holiday.status)
                        holiday.save()
                            
                        if center_list == '':
                            holiday.center.set([])
                        elif type(center_list) == int:
                            holiday.center.set([eval(str(center_list))])
                        else:                        
                            holiday.center.set(center_list)
                        

                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Holiday Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Holiday."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def holiday_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        holiday = python_data.get('id')
        check_holiday = models.HolidayDetail.objects.filter(id = holiday).count()
        if check_holiday == 1:
            
            holiday_details = models.HolidayDetail.objects.get(id = holiday)
            holiday_details.status = 'Inactive'
            holiday_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Holiday Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Holiday ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def holiday_status_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_holiday = models.HolidayDetail.objects.filter(id = id).count()
        if check_holiday == 1:
            holiday = models.HolidayDetail.objects.get(id = id)
            holiday.status = status
            holiday.save()

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Holiday Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Holiday."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def list_all_holiday(request):
    if request.method == 'POST':
        all_holiday = models.HolidayDetail.objects.all().order_by('-id')
        serialiser = HolidayDetailSerializer(all_holiday, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
                
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def corporate_code_check(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        corporate_code = python_data.get('corporate_code')

        check_corporate_code = models.CorporateDetail.objects.filter(corporate_code = corporate_code).count()
        if check_corporate_code == 1:
            check_status_corporate_code = models.CorporateDetail.objects.filter(corporate_code = corporate_code, status = 'Active').count()
            if check_status_corporate_code == 1:
                corporate_code = models.CorporateDetail.objects.get(corporate_code = corporate_code)
                login_via = corporate_code.login_via
            
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'login_via':login_via
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 401,
                    'status':'false',
                    'message':"Currently your corporate is Inactive."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message':"You've Enter wrong Corporate Code."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def corporate_package_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')

        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        if check_employee == 1:
            employee = models.EmployeeDetail.objects.get(id = employee)
            corporate = employee.corporate.id
            all_emp = models.PackageDetail.objects.filter(corporate = corporate, status='Active').order_by('-id')
            serialiser = PackageDetailSerializer(all_emp, many=True)
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'data' : serialiser.data
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "You've Enter wrong employee ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
            


@csrf_exempt
def health_tips_create(request):
    if request.method == 'POST':
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        python_data={}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})
        
        
        health = models.HealthTips.objects.create(
            title = python_data.get('title'),
            start_date = python_data.get('start_date'),
            end_date = python_data.get('end_date'),
            redirection_url = python_data.get('redirection_url'),
            media = python_data.get('media'),
            status = 'Active',
            created_at = 
            current_time
        )
        health.save()

        res = {
            'statuscode' : 200,
            'status':'true',
            'message' : "Health Tip Added Successfully."
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def health_tips_update(request):
    if request.method == 'POST':
        python_data={}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})
        
        id = python_data.get('id')
        check_health = models.HealthTips.objects.filter(id = id).count()
        if check_health == 1:
            health = models.HealthTips.objects.get(id = id)
            health.title = python_data.get('title', health.title)
            health.start_date = python_data.get('start_date', health.start_date)
            health.end_date = python_data.get('end_date', health.end_date)
            health.redirection_url = python_data.get('redirection_url', health.redirection_url)
            if type(python_data.get('media', health.media)) != str: 
                health.media = python_data.get('media', health.media)
            health.status = python_data.get('status', health.status)
            
            health.save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Health Tip Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Health Tip."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def health_tips_status_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_health = models.HealthTips.objects.filter(id = id).count()
        if check_health == 1:
            health = models.HealthTips.objects.get(id = id)
            health.status = status
            health.save()

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Status Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def list_all_health_tips(request):
    if request.method == 'POST':
        all_health = models.HealthTips.objects.all().order_by('-id')
        serialiser = HealthTipsSerializer(all_health, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def list_active_health_tips(request):
    if request.method == 'POST':
        all_health = models.HealthTips.objects.filter(status = 'Active').order_by('-id')
        serialiser = HealthTipsSerializer(all_health, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def active_inactive_health_tips(request):
    if request.method == 'POST':
        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()

        list_data = []
        all_health = models.HealthTips.objects.all().order_by('-id')
        for health in all_health:
            health_tips_id = models.HealthTips.objects.get(id = health.id)
            start_date = health_tips_id.start_date
            health_tips_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = health_tips_id.end_date
            health_tips_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if current_date >= health_tips_start_date and current_date <= health_tips_end_date:
                health_tips_id.status = 'Active'
                health_tips_id.save()

            else:
                health_tips_id.status = 'Inactive'
                health_tips_id.save()

        res = {
            'statuscode' : 200,
            'status':'true',
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def health_tips_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        health = python_data.get('id')
        check_staff = models.HealthTips.objects.filter(id = health).count()
        if check_staff == 1:
            
            staff_details = models.HealthTips.objects.get(id = health)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Health Tips Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Staff ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


# @csrf_exempt
# def service_wise_package_list_employee(request):
#     if request.method == 'POST':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         python_data = JSONParser().parse(stream)
#         employee = python_data.get('employee')
#         check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
#         list_data = []
#         if check_employee == 1:
#             employee = models.EmployeeDetail.objects.get(id = employee)
#             corporate = employee.corporate_id
#             all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
#             for service in all_service:
#                 package_count = models.PackageDetail.objects.filter(type_of_service = service.id, corporate = corporate, status='Active').count()
#                 if package_count >= 1:
#                     service_dictionary = {}
#                     get_all_package = models.PackageDetail.objects.filter(type_of_service = service.id, corporate = corporate).order_by('-id')
#                     serialiser = PackageDetailSerializer(get_all_package, many=True)
#                     service_dictionary.update({'service':service.type_of_service, 'data':serialiser.data})
#                     list_data.append(service_dictionary)

        
#         res = {
#             'statuscode' : 200,
#             'status':'true',
#             'data' : list_data
#             }
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type= 'application/json') 


# @csrf_exempt
# def service_wise_package_list_employee(request):
#     if request.method == 'POST':
#         python_data = JSONParser().parse(io.BytesIO(request.body))
#         employee = python_data.get('employee')
#         check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
#         list_data = []
#         if check_employee == 1:
#             employee = models.EmployeeDetail.objects.get(id = employee)
#             employee_gender = employee.gender.gender
#             # employee_gender = 'All'
#             get_dependent = models.EmployeeDependent.objects.filter(employee = employee.id).count()
#             print(get_dependent, 'get_dependent', True, 'Check true')
            
#             if get_dependent > 0:
#                 all_genders = list(models.EmployeeDependent.objects.filter(employee=employee.id).values_list('gender__gender', flat=True).distinct())
#                 if not employee_gender in all_genders:
#                     all_genders.append(employee_gender)
            
#             if 'Male' in all_genders or 'Female' in all_genders and 'All' not in all_genders:
#                 all_genders.append('All')

#             print(all_genders, 'all_genders')
#             gender_ids = list(models.Gender.objects.filter(gender__in=all_genders).values_list('id', flat=True))
            
#             corporate = employee.corporate_id

#             all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
#             for service in all_service:

#                 service_dictionary = {}
#                 get_all_individual_package = models.PackageDetail.objects.filter(type_of_service = service.id,gender_id__in=gender_ids, package_type = 'Individual').order_by('-id')
#                 list_package_data = []
#                 for package_individual in get_all_individual_package:
#                     print(models.CenterDetail.objects.filter(package = package_individual.id).count(), 'check count')
#                     if models.CenterDetail.objects.filter(package = package_individual.id).count() > 0:
#                         serialiser = PackageDetailSerializer(package_individual)
#                         list_package_data.append(serialiser.data)
                
#                 get_all_package = models.PackageDetail.objects.filter(type_of_service = service.id,gender_id__in=gender_ids, corporate = corporate).order_by('-id')
#                 print(get_all_package, 'get_all_package')
#                 for package_data in get_all_package:
#                     if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
#                         package_serialiser = PackageDetailSerializer(package_data)
#                         list_package_data.append(package_serialiser.data)
    
#                 if list_package_data != []:
#                     service_dictionary.update({'service':service.type_of_service, 'data':list_package_data})
#                     list_data.append(service_dictionary)

        
#         res = {
#             'statuscode' : 200,
#             'status':'true',
#             'data' : list_data
#             }
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type= 'application/json') 


#### Date : 2025-07-03
# @csrf_exempt
# def service_wise_package_list_employee(request):
#     if request.method == 'POST':
#         python_data = JSONParser().parse(io.BytesIO(request.body))
#         employee = python_data.get('employee')
#         check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
#         list_data = []
#         if check_employee == 1:
#             employee = models.EmployeeDetail.objects.get(id = employee)
#             employee_gender = employee.gender.gender
#             get_dependent = models.EmployeeDependent.objects.filter(employee = employee.id).count()            
#             if get_dependent > 0:
#                 data_data = list(models.EmployeeDependent.objects.filter(employee=employee.id))
#                 data_update = []
#                 all_gender = []
#                 for single_data in data_data:
#                     gender = single_data.gender.gender
#                     all_gender.append(gender)
#                     birth_date = single_data.date_of_birth

#                     try:
#                         dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
#                         dob =  dt.strftime('%Y-%m-%d')
#                     except ValueError:
#                         try:
#                             dt = datetime.strptime(birth_date, '%Y-%m-%d')
#                             dob = dt.strftime('%Y-%m-%d')
#                         except ValueError:
#                             pass


#                     dob = datetime.strptime(dob, '%Y-%m-%d').date()
#                     today = date.today()
#                     age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
#                     if age < 40:
#                         age = 'Below 40'
#                     else:
#                         age = 'Above 40'

#                     data_update.append((single_data.gender.gender, age))
                
#                 data_update = list(set(data_update))

#                 genders = [item[0] for item in data_update]
                
#                 all_gender = list(set(all_gender))
#                 data_update.append(('All', 'All'))
#                 data_update.append(('All', 'Above 40'))
#                 data_update.append(('All', 'Below 40'))
#                 if 'Male' in all_gender:
#                     data_update.append(('Male', 'All'))
#                 if 'Female' in all_gender:
#                     data_update.append(('Female', 'All'))
            
#             print(data_update, 'data_update')
#             data_update = list(set(data_update))
#             list_id = [] 
#             for gender, age_group in data_update:
#                 gender_id = models.Gender.objects.filter(gender=gender).values_list('id', flat=True)[0]
#                 age_category_id = models.AgeCategory.objects.filter(age_category=age_group).values_list('id', flat=True)[0]
#                 list_id.append((gender_id, age_category_id))
            
#             corporate = employee.corporate_id

#             all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
#             for service in all_service:

#                 service_dictionary = {}
#                 filters = Q()
#                 for gender_id, age_category_id in list_id:
#                     filters |= Q(gender_id=gender_id, age_category_id=age_category_id)

#                 list_package_data = []
                
#                 get_all_package = models.PackageDetail.objects.filter(type_of_service=service.id,corporate = corporate).filter(filters).order_by('-id')
#                 for package_data in get_all_package:
#                     if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
#                         package_serialiser = PackageDetailSerializer(package_data)
#                         list_package_data.append(package_serialiser.data)
    
#                 get_all_individual_package = models.PackageDetail.objects.filter(type_of_service=service.id,package_type='Individual').filter(filters).order_by('-id')
#                 for package_individual in get_all_individual_package:
#                     if models.CenterDetail.objects.filter(package = package_individual.id).count() > 0:
#                         serialiser = PackageDetailSerializer(package_individual)
#                         list_package_data.append(serialiser.data)
                
#                 if list_package_data != []:
#                     service_dictionary.update({'service':service.type_of_service, 'data':list_package_data})
#                     list_data.append(service_dictionary)

        
#         res = {
#             'statuscode' : 200,
#             'status':'true',
#             'data' : list_data
#             }
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def service_wise_package_list_employee(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')
        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        list_data = []
        if check_employee == 1:
            employee = models.EmployeeDetail.objects.get(id = employee)
            corporate = employee.corporate_id

            all_service = models.TypeOfService.objects.filter(status = 'Active')
            for service in all_service:   
                service_dictionary = {}
                list_package_data = []
                package_list = []
                get_all_package = models.PackageDetail.objects.filter(type_of_service=service.id,corporate = corporate, status='Active')
                for package_data in get_all_package:
                    if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                        package = models.PackageDetail.objects.get(id = package_data.id)
                        age_category = package.age_category.age_category
                        package_gender = package.gender.gender

                        relation_data = list(package_data.relation_with_employee.values_list('relation', flat=True))
                        for relation in relation_data:
                            check_relation = models.EmployeeDependent.objects.filter(employee = employee, dependent_relation__relation = relation).count()
                            if check_relation == 1:
                                single_data = models.EmployeeDependent.objects.get(employee = employee, dependent_relation__relation = relation)
                                gender = single_data.gender.gender
                                birth_date = single_data.date_of_birth
                                
                                try:
                                    dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                                    dob =  dt.strftime('%Y-%m-%d')
                                except ValueError:
                                    try:
                                        dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                        dob = dt.strftime('%Y-%m-%d')
                                    except ValueError:
                                        pass


                                dob = datetime.strptime(dob, '%Y-%m-%d').date()
                                today = date.today()
                                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

                                if age < 40:
                                    age = 'Below 40'
                                else:
                                    age = 'Above 40'

                                if (age_category == age or age_category == "All") and (package_gender == gender or package_gender == 'All'):
                                    package_list.append(package_data)

                        # package_list = list(set(package_list))
                        package_list = list(dict.fromkeys(package_list))
                        package_serialiser = PackageDetailSerializer(package_list, many=True)
                        
                get_all_individual_package = models.PackageDetail.objects.filter(type_of_service=service.id,package_type='Individual', status='Active')
                for package_data in get_all_individual_package:
                    if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                        package = models.PackageDetail.objects.get(id = package_data.id)
                        age_category = package.age_category.age_category
                        package_gender = package.gender.gender

                        relation_data = list(package_data.relation_with_employee.values_list('relation', flat=True))
                        for relation in relation_data:
                            check_relation = models.EmployeeDependent.objects.filter(employee = employee, dependent_relation__relation = relation).count()
                            if check_relation == 1:
                                single_data = models.EmployeeDependent.objects.get(employee = employee, dependent_relation__relation = relation)
                                gender = single_data.gender.gender
                                birth_date = single_data.date_of_birth
                                
                                try:
                                    dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                                    dob =  dt.strftime('%Y-%m-%d')
                                except ValueError:
                                    try:
                                        dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                        dob = dt.strftime('%Y-%m-%d')
                                    except ValueError:
                                        pass


                                dob = datetime.strptime(dob, '%Y-%m-%d').date()
                                today = date.today()
                                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                                if age < 40:
                                    age = 'Below 40'
                                else:
                                    age = 'Above 40'

                                if (age_category == age or age_category == "All") and (package_gender == gender or package_gender == 'All'):
                                    package_list.append(package_data)
                                    
                        # package_list = list(set(package_list))
                        package_list = list(dict.fromkeys(package_list))
                        package_serialiser = PackageDetailSerializer(package_list, many=True)
                
                if package_list != []:
                    service_dictionary.update({'service':service.type_of_service, 'data':package_serialiser.data})
                    list_data.append(service_dictionary)

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 





# @csrf_exempt
# def service_wise_package_list_individual(request):
#     if request.method == 'POST':
#         python_data = JSONParser().parse(io.BytesIO(request.body))
#         individual = python_data.get('individual')
            
#         individual = models.IndividualUserDetail.objects.get(id = individual)
#         individual_gender = individual.gender.gender

#         get_dependent = models.IndividualDependent.objects.filter(individual = individual.id).count()
#         print(get_dependent, 'get_dependent', True, 'Check true')
            
#         if get_dependent > 0:
#             all_genders = list(models.IndividualDependent.objects.filter(individual=individual.id).values_list('gender__gender', flat=True).distinct())
#             if not individual_gender in all_genders:
#                 all_genders.append(individual_gender)
        
#         if 'Male' in all_genders or 'Female' in all_genders and 'All' not in all_genders:
#             all_genders.append('All')

#         print(all_genders, 'all_genders')
#         gender_ids = list(models.Gender.objects.filter(gender__in=all_genders).values_list('id', flat=True))
        
        
#         list_data = []
#         all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
#         for service in all_service:

#             service_dictionary = {}
#             get_all_package = models.PackageDetail.objects.filter(type_of_service = service.id, gender_id__in=gender_ids, package_type = 'Individual').order_by('-id')
#             list_package_data = []
#             for package_data in get_all_package:
#                 if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
#                     serialiser = PackageDetailSerializer(package_data)
#                     list_package_data.append(serialiser.data)
            
#             if list_package_data != []:
#                 service_dictionary.update({'service':service.type_of_service, 'data':list_package_data})
#                 list_data.append(service_dictionary)

        
#         res = {
#             'statuscode' : 200,
#             'status':'true',
#             'data' : list_data
#             }
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type= 'application/json') 

## Date : 2025-07-04
# @csrf_exempt 
# def service_wise_package_list_individual(request):
#     if request.method == 'POST':
#         python_data = JSONParser().parse(io.BytesIO(request.body))
#         individual = python_data.get('individual')
#         check_individual = models.IndividualUserDetail.objects.filter(id = individual).count()
#         list_data = []
#         if check_individual == 1:
#             individual = models.IndividualUserDetail.objects.get(id = individual)
#             individual_gender = individual.gender.gender
#             get_dependent = models.IndividualDependent.objects.filter(individual = individual.id).count()            
#             if get_dependent > 0:
#                 data_data = list(models.IndividualDependent.objects.filter(individual=individual.id))
#                 data_update = []
#                 all_gender = []
#                 for single_data in data_data:
#                     gender = single_data.gender.gender
#                     all_gender.append(gender)
#                     birth_date = single_data.date_of_birth

#                     try:
#                         dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
#                         dob =  dt.strftime('%Y-%m-%d')
#                     except ValueError:
#                         try:
#                             dt = datetime.strptime(birth_date, '%Y-%m-%d')
#                             dob = dt.strftime('%Y-%m-%d')
#                         except ValueError:
#                             pass


#                     dob = datetime.strptime(dob, '%Y-%m-%d').date()
#                     today = date.today()
#                     age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
#                     if age < 40:
#                         age = 'Below 40'
#                     else:
#                         age = 'Above 40'

#                     data_update.append((single_data.gender.gender, age))
                
#                 data_update = list(set(data_update))

#                 genders = [item[0] for item in data_update]
                
#                 all_gender = list(set(all_gender))
#                 data_update.append(('All', 'All'))
#                 data_update.append(('All', 'Above 40'))
#                 data_update.append(('All', 'Below 40'))
#                 if 'Male' in all_gender:
#                     data_update.append(('Male', 'All'))
#                 if 'Female' in all_gender:
#                     data_update.append(('Female', 'All'))
            
#             print(data_update, 'data_update')
#             data_update = list(set(data_update))
#             list_id = [] 
#             for gender, age_group in data_update:
#                 gender_id = models.Gender.objects.filter(gender=gender).values_list('id', flat=True)[0]
#                 age_category_id = models.AgeCategory.objects.filter(age_category=age_group).values_list('id', flat=True)[0]
#                 list_id.append((gender_id, age_category_id))


#             all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
#             for service in all_service:

#                 # service_dictionary = {}
#                 # filters = Q()
#                 # for gender_id, age_category_id in list_id:
#                 #     filters |= Q(gender_id=gender_id, age_category_id=age_category_id)

#                 # get_all_individual_package = models.PackageDetail.objects.filter(type_of_service=service.id,package_type='Individual').filter(filters).order_by('-id')

#                 # list_package_data = []
#                 # for package_individual in get_all_individual_package:
#                 #     if models.CenterDetail.objects.filter(package = package_individual.id).count() > 0:
#                 #         serialiser = PackageDetailSerializer(package_individual)
#                 #         list_package_data.append(serialiser.data)
                
#                 # get_all_package = models.PackageDetail.objects.filter(type_of_service=service.id,corporate = corporate).filter(filters).order_by('-id')
#                 # for package_data in get_all_package:
#                 #     if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
#                 #         package_serialiser = PackageDetailSerializer(package_data)
#                 #         list_package_data.append(package_serialiser.data)
    
#                 # if list_package_data != []:
#                 #     service_dictionary.update({'service':service.type_of_service, 'data':list_package_data})
#                 #     list_data.append(service_dictionary)

#                 service_dictionary = {}
#                 filters = Q()
#                 for gender_id, age_category_id in list_id:
#                     filters |= Q(gender_id=gender_id, age_category_id=age_category_id)
                
#                 get_all_package = models.PackageDetail.objects.filter(type_of_service = service.id, package_type = 'Individual').order_by('-id')
#                 list_package_data = []
#                 for package_data in get_all_package:
#                     if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
#                         serialiser = PackageDetailSerializer(package_data)
#                         list_package_data.append(serialiser.data)
                
#                 if list_package_data != []:
#                     service_dictionary.update({'service':service.type_of_service, 'data':list_package_data})
#                     list_data.append(service_dictionary)

        
#         res = {
#             'statuscode' : 200,
#             'status':'true',
#             'data' : list_data
#             }
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def service_wise_package_list_individual(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        individual = python_data.get('individual')
        
        check_individual = models.IndividualUserDetail.objects.filter(id = individual).count()
        list_data = []

        if check_individual == 1:
            individual = models.IndividualUserDetail.objects.get(id = individual)
            individual_gender = individual.gender.gender

            all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
            for service in all_service:   
                service_dictionary = {}
                list_package_data = []
                package_list = []

                get_all_individual_package = models.PackageDetail.objects.filter(type_of_service=service.id,package_type='Individual', status='Active')
                for package_data in get_all_individual_package:
                    if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                        package = models.PackageDetail.objects.get(id = package_data.id)
                        age_category = package.age_category.age_category
                        package_gender = package.gender.gender

                        relation_data = list(package_data.relation_with_employee.values_list('relation', flat=True))
                        for relation in relation_data:
                            check_relation = models.IndividualDependent.objects.filter(individual = individual, dependent_relation__relation = relation).count()
                            if check_relation == 1:
                                single_data = models.IndividualDependent.objects.get(individual = individual, dependent_relation__relation = relation)
                                gender = single_data.gender.gender
                                birth_date = single_data.date_of_birth
                                
                                try:
                                    dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                                    dob =  dt.strftime('%Y-%m-%d')
                                except ValueError:
                                    try:
                                        dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                        dob = dt.strftime('%Y-%m-%d')
                                    except ValueError:
                                        pass


                                dob = datetime.strptime(dob, '%Y-%m-%d').date()
                                today = date.today()
                                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                                if age < 40:
                                    age = 'Below 40'
                                else:
                                    age = 'Above 40'

                                if (age_category == age or age_category == "All") and (package_gender == gender or package_gender == 'All'):
                                    package_list.append(package_data)
                                    
                        package_list = list(set(package_list))
                        package_serialiser = PackageDetailSerializer(package_list, many=True)
                
                if package_list != []:
                    service_dictionary.update({'service':service.type_of_service, 'data':package_serialiser.data})
                    list_data.append(service_dictionary)

        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def service_wise_package_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_service = models.TypeOfService.objects.filter(id = id).count()
        if check_service == 1:
            get_all_package = models.PackageDetail.objects.filter(type_of_service = id).order_by('-id')
            serialiser = PackageNameSerializer(get_all_package, many=True)
            res = {
                'statuscode' : 200,
                'status':'true',
                'data' : serialiser.data
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Smoething Went Wrong"
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def search_package(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        user_type = python_data.get('user_type')
        search_by = python_data.get('search_by')
        search = python_data.get('search')

        list_data=[]
        search_list_data = []

        if user_type == 'employee':
            employee = python_data.get('employee')
            check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
            if check_employee == 1:
                employee = models.EmployeeDetail.objects.get(id = employee)
                corporate = employee.corporate_id
                if search_by == 'Location':
                    all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
                    for service in all_service: 

                        get_center_details = models.CenterDetail.objects.filter(city = search, type_of_service = service.id,package__corporate=corporate).distinct()
                        get_distinct_package = list(models.CenterDetail.objects.filter(city = search, package__type_of_service = service.id,package__corporate=corporate).values_list('package', flat=True).distinct())
                        service_dictionary = {}
                        loc_list_data = []
                        if get_distinct_package != []:
                            for package_id in get_distinct_package:
                                get_package_detail = models.PackageDetail.objects.get(id=package_id)
                                get_package_detail_serializer = PackageDetailSerializer(get_package_detail).data
                                loc_list_data.append(get_package_detail_serializer)

                            service_dictionary.update({'service':service.type_of_service, 'data':loc_list_data})
                            
                            search_list_data.append(service_dictionary)


                elif search_by == 'Pincode':

                    all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
                    for service in all_service: 
                        get_center_details = models.CenterDetail.objects.filter(pincode = search, type_of_service = service.id,package__corporate=corporate).distinct()
                        get_distinct_package = list(models.CenterDetail.objects.filter(pincode = search, package__type_of_service = service.id,package__corporate=corporate).values_list('package', flat=True).distinct())
                        service_dictionary = {}
                        pin_list_data = []
                        if get_distinct_package != []:
                            for package_id in get_distinct_package:
                                get_package_detail = models.PackageDetail.objects.get(id=package_id)
                                get_package_detail_serializer = PackageDetailSerializer(get_package_detail).data
                                pin_list_data.append(get_package_detail_serializer)

                            service_dictionary.update({'service':service.type_of_service, 'data':pin_list_data})
                            
                            search_list_data.append(service_dictionary)


                elif search_by == 'Services':
                    check_service = models.TypeOfService.objects.filter(id = search).count()
                    if check_service == 1:
                        service = models.TypeOfService.objects.get(id = search)
                        get_all_package = models.PackageDetail.objects.filter(type_of_service = service.id,corporate = corporate).order_by('-id')
                        service_dictionary = {}
                        serialiser = PackageDetailSerializer(get_all_package, many=True)
                        service_dictionary.update({'service':service.type_of_service, 'data':serialiser.data})
                        search_list_data.append(service_dictionary)
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'data' : search_list_data
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
            
        elif user_type == 'individual':
            if search_by == 'Location':
                all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
                for service in all_service: 
                    get_center_details = models.CenterDetail.objects.filter(city = search, type_of_service = service.id).distinct()
                    get_distinct_package = list(models.CenterDetail.objects.filter(city = search, package__type_of_service = service.id).values_list('package', flat=True).distinct())
                    service_dictionary = {}
                    loc_list_data = []
                    if get_distinct_package != []:
                        for package_id in get_distinct_package:
                            check_package = models.PackageDetail.objects.filter(id=package_id,package_type = 'Individual').count()
                            if check_package == 1:
                                get_package_detail = models.PackageDetail.objects.get(id=package_id)

                                get_package_detail_serializer = PackageDetailSerializer(get_package_detail).data
                                loc_list_data.append(get_package_detail_serializer)
                    
                        if len(loc_list_data) > 0:
                            service_dictionary.update({'service':service.type_of_service, 'data':loc_list_data})
                        
                        search_list_data.append(service_dictionary)


            elif search_by == 'Pincode':

                all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
                for service in all_service: 
                    get_center_details = models.CenterDetail.objects.filter(pincode = search, type_of_service = service.id).distinct()

                    get_distinct_package = list(models.CenterDetail.objects.filter(pincode = search, package__type_of_service = service.id).values_list('package', flat=True).distinct())

                    service_dictionary = {}
                    pin_list_data = []
                    if get_distinct_package != []:
                        for package_id in get_distinct_package:
                            check_package = models.PackageDetail.objects.filter(id=package_id,package_type = 'Individual').count()
                            if check_package == 1:
                                get_package_detail = models.PackageDetail.objects.get(id=package_id)

                                get_package_detail_serializer = PackageDetailSerializer(get_package_detail).data
                                pin_list_data.append(get_package_detail_serializer)
                    
                        if len(pin_list_data) > 0:
                            service_dictionary.update({'service':service.type_of_service, 'data':pin_list_data})
                        
                        search_list_data.append(service_dictionary)


            elif search_by == 'Services':
                check_service = models.TypeOfService.objects.filter(id = search).count()
                if check_service == 1:
                    service = models.TypeOfService.objects.get(id = search)
                    get_all_package = models.PackageDetail.objects.filter(type_of_service = service.id, package_type = 'Individual').order_by('-id')
                    service_dictionary = {}
                    serialiser = PackageDetailSerializer(get_all_package, many=True)
                    service_dictionary.update({'service':service.type_of_service, 'data':serialiser.data})
                    search_list_data.append(service_dictionary)
            res = {
                'statuscode' : 200,
                'status':'true',
                'data' : search_list_data
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
            
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "You've Enter wrong user ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 



# @csrf_exempt
# def package_list_employee(request):
#     if request.method == 'POST':
#         python_data = JSONParser().parse(io.BytesIO(request.body))
#         employee = python_data.get('employee')
#         check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        
#         if check_employee == 1:
#             employee = models.EmployeeDetail.objects.get(id = employee)
#             corporate = employee.corporate_id
#             list_data = []
#             get_all_package = models.PackageDetail.objects.filter(corporate = corporate).order_by('-id')
#             for package in get_all_package:
#                 package_data = models.PackageDetail.objects.get(id = package.id)
#                 serialiser = PackageDetailSerializer(package_data)
#                 data = serialiser.data
#                 center_count = models.CenterDetail.objects.filter(package = package_data).count()
#                 if center_count == 1:
#                     center_data = models.CenterDetail.objects.get(package = package_data)
#                     center_serialiser = CenterDataSerializer(center_data)
#                     data.update({'center':center_serialiser.data})
#                 list_data.append(data)
        
#         res = {
#             'statuscode' : 200,
#             'status':'true',
#             'data' : list_data
#             }
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type= 'application/json') 


### Date : 2025-07-07
# @csrf_exempt
# def package_list_employee(request):
#     if request.method == 'POST':
#         python_data = JSONParser().parse(io.BytesIO(request.body))
#         employee = python_data.get('employee')
#         check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        
#         if check_employee == 1:
#             employee = models.EmployeeDetail.objects.get(id = employee)
#             corporate = employee.corporate_id
#             list_data = []
#             get_all_individual_package = models.PackageDetail.objects.filter(package_type = 'Individual').order_by('-id')
#             for package_indi in get_all_individual_package:
#                 package_data = models.PackageDetail.objects.get(id = package_indi.id)
#                 serialiser = PackageDetailSerializer(package_data)
#                 data = serialiser.data
#                 center_count = models.CenterDetail.objects.filter(package = package_data).count()
#                 if center_count == 1:
#                     center_data = models.CenterDetail.objects.get(package = package_data)
#                     center_serialiser = CenterDataSerializer(center_data)
#                     data.update({'center':center_serialiser.data})
#                 list_data.append(data)
        
            
#             get_all_package = models.PackageDetail.objects.filter(corporate = corporate).order_by('-id')
#             for package in get_all_package:
#                 package_data = models.PackageDetail.objects.get(id = package.id)
#                 serialiser = PackageDetailSerializer(package_data)
#                 data = serialiser.data
#                 center_count = models.CenterDetail.objects.filter(package = package_data).count()
#                 if center_count == 1:
#                     center_data = models.CenterDetail.objects.get(package = package_data)
#                     center_serialiser = CenterDataSerializer(center_data)
#                     data.update({'center':center_serialiser.data})
#                 list_data.append(data)
        
#         res = {
#             'statuscode' : 200,
#             'status':'true',
#             'data' : list_data
#             }
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def package_list_employee(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')
        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        
        if check_employee == 1:
            employee = models.EmployeeDetail.objects.get(id = employee)
            corporate = employee.corporate_id
            list_data = []
            service_dictionary = {}
            list_package_data = []
            package_list = []
            get_all_package = models.PackageDetail.objects.filter(corporate = corporate, status = "Active")
            for package_data in get_all_package:
                if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                    package = models.PackageDetail.objects.get(id = package_data.id)
                    age_category = package.age_category.age_category
                    package_gender = package.gender.gender

                    relation_data = list(package_data.relation_with_employee.values_list('relation', flat=True))
                    for relation in relation_data:
                        check_relation = models.EmployeeDependent.objects.filter(employee = employee, dependent_relation__relation = relation).count()
                        if check_relation == 1:
                            single_data = models.EmployeeDependent.objects.get(employee = employee, dependent_relation__relation = relation)
                            gender = single_data.gender.gender
                            birth_date = single_data.date_of_birth
                            
                            try:
                                dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                                dob =  dt.strftime('%Y-%m-%d')
                            except ValueError:
                                try:
                                    dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                    dob = dt.strftime('%Y-%m-%d')
                                except ValueError:
                                    pass


                            dob = datetime.strptime(dob, '%Y-%m-%d').date()
                            today = date.today()
                            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                            if age < 40:
                                age = 'Below 40'
                            else:
                                age = 'Above 40'

                            if (age_category == age or age_category == "All") and (package_gender == gender or package_gender == 'All'):

                                package_list.append(package_data)

                    package_list = list(dict.fromkeys(package_list))

            get_all_individual_package = models.PackageDetail.objects.filter(package_type = 'Individual', status='Active').order_by('-id')
            for package_data in get_all_individual_package:
                if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                    package = models.PackageDetail.objects.get(id = package_data.id)
                    age_category = package.age_category.age_category
                    package_gender = package.gender.gender

                    relation_data = list(package_data.relation_with_employee.values_list('relation', flat=True))
                    for relation in relation_data:
                        check_relation = models.EmployeeDependent.objects.filter(employee = employee, dependent_relation__relation = relation).count()
                        if check_relation == 1:
                            single_data = models.EmployeeDependent.objects.get(employee = employee, dependent_relation__relation = relation)
                            gender = single_data.gender.gender
                            birth_date = single_data.date_of_birth
                            
                            try:
                                dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                                dob =  dt.strftime('%Y-%m-%d')
                            except ValueError:
                                try:
                                    dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                    dob = dt.strftime('%Y-%m-%d')
                                except ValueError:
                                    pass


                            dob = datetime.strptime(dob, '%Y-%m-%d').date()
                            today = date.today()
                            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                            if age < 40:
                                age = 'Below 40'
                            else:
                                age = 'Above 40'

                            if (age_category == age or age_category == "All") and (package_gender == gender or package_gender == 'All'):

                                package_list.append(package_data)
                    package_list = list(dict.fromkeys(package_list))

            package_serialiser = PackageDetailSerializer(package_list, many=True)


        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : package_serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



### Date : 2025-07-07
# @csrf_exempt
# def package_list_individual(request):
#     if request.method == 'POST':

#         list_data = []
#         get_all_package = models.PackageDetail.objects.filter(package_type = 'Individual').order_by('-id')
#         for package in get_all_package:
#             package_data = models.PackageDetail.objects.get(id = package.id)
#             serialiser = PackageDetailSerializer(package_data)
#             data = serialiser.data
#             center_count = models.CenterDetail.objects.filter(package = package_data).count()
#             if center_count == 1:
#                 center_data = models.CenterDetail.objects.get(package = package_data)
#                 center_serialiser = CenterDataSerializer(center_data)
#                 data.update({'center':center_serialiser.data})
#             list_data.append(data)
        
#         res = {
#             'statuscode' : 200,
#             'status':'true',
#             'data' : list_data
#             }
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def package_list_individual(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        individual = python_data.get('individual')
        check_individual = models.IndividualUserDetail.objects.filter(id = individual).count()

        if check_individual == 1:
            get_all_individual_package = models.PackageDetail.objects.filter(package_type = 'Individual').order_by('-id')
            package_list = []
            for package_data in get_all_individual_package:
                if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                    package = models.PackageDetail.objects.get(id = package_data.id)
                    age_category = package.age_category.age_category
                    package_gender = package.gender.gender

                    relation_data = list(package_data.relation_with_employee.values_list('relation', flat=True))
                    for relation in relation_data:
                        check_relation = models.IndividualDependent.objects.filter(individual = individual, dependent_relation__relation = relation).count()
                        if check_relation == 1:
                            single_data = models.IndividualDependent.objects.get(individual = individual, dependent_relation__relation = relation)
                            gender = single_data.gender.gender
                            birth_date = single_data.date_of_birth
                            
                            try:
                                dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                                dob =  dt.strftime('%Y-%m-%d')
                            except ValueError:
                                try:
                                    dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                    dob = dt.strftime('%Y-%m-%d')
                                except ValueError:
                                    pass


                            dob = datetime.strptime(dob, '%Y-%m-%d').date()
                            today = date.today()
                            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                            if age < 40:
                                age = 'Below 40'
                            else:
                                age = 'Above 40'

                            if (age_category == age or age_category == "All") and (package_gender == gender or package_gender == 'All'):

                                package_list.append(package_data)
                    package_list = list(dict.fromkeys(package_list))

            package_serialiser = PackageDetailSerializer(package_list, many=True)
            
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : package_serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def appointment_data_check(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')
        patient = python_data.get('patient')
        package = python_data.get('package')
        
        get_package_payment_tags = models.PackageDetail.objects.filter(id = package).values_list('tags', flat=True)[0]
        package_payment_tags = models.PaymentTags.objects.filter(id = get_package_payment_tags).values_list('payment_tags', flat=True)[0]
        
        if package_payment_tags == 'Corporate pay':
            check_appointment = models.AppointmentDetail.objects.filter(package =package, employee =employee, patient= patient).exclude(status='add_to_cart').count()
            if check_appointment != 0:
                check_booking = models.AppointmentDetail.objects.filter(package =package, employee =employee, patient= patient).exclude(status='Cancel').count()
                if check_booking == 1:
                    check_booking = models.AppointmentDetail.objects.filter(package =package, employee =employee, patient= patient).values_list('report', flat=True)[0]
                    if check_booking != None and check_booking != 'null' and check_booking != '':
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'first_time':False,
                            'package_book':True,
                            'is_self_pay':False,
                            'message' : "Health checkup benefit already utilised. Kindly explore other available packages"
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'package_book':True,
                            'is_self_pay':False,
                            'first_time':False,
                            'message' : "Appointment already booked and is currently under process"
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')
                else:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'package_book':False,
                        'is_self_pay':False,
                        'first_time':True,
                        'message' : "You're eligible for book this appointment."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
            elif check_appointment == 0:
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'package_book':False,
                    'is_self_pay':False,
                    'first_time':True,
                    'message' : "You're eligible for book this appointment."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

        elif package_payment_tags == 'Self Pay':                            
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'first_time':False,
                    'is_self_pay':True,
                    'package_book':True,
                    'message' : "You need to pay by your self."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

        else:

            res = {
                'statuscode' : 406,
                'status':False,
                'message' : "Something went Wrong."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


def createPDF(context):
    def generate_pdf():
        now = datetime.now()
        formatted_date = now.strftime("%B %d, %Y")
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = now.strftime("%H:%M:%S")
        date_time = str(current_date) + str(curr_time)

        recipient_name = context.get('recipient_name')
        appointment_id = context.get('appointment_id')

        invoice_template = get_template("invoice_template.html")
        html_content = invoice_template.render(context)

        options = {
            'page-size': 'A4',
            'no-outline': None,
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            'viewport-size': '1280x1024'
        }
        
        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        
        pdf = pdfkit.from_string(html_content, False, options=options, configuration=config)
        # pdf = pdfkit.from_string(html_content, False, options=options)
        
        pdf_name = f'invoice_{recipient_name +"_"+ date_time}.pdf'
        pdf_file = ContentFile(pdf, name=pdf_name)

        transaction = models.Transaction.objects.get(appointment=appointment_id)
        transaction.invoice.save(pdf_file.name, pdf_file)
        transaction.save()

    pdf_thread = threading.Thread(target=generate_pdf)
    pdf_thread.start()


@csrf_exempt
def appointment_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        individual = python_data.get('individual')
        employee = python_data.get('employee')
        patient = python_data.get('patient')
        package = python_data.get('package')
        center = python_data.get('center')
        appointment_date_1 = python_data.get('appointment_date_1', None)
        appointment_date_2 = python_data.get('appointment_date_2', None)
        home_sample_date_1 = python_data.get('home_sample_date_1', None)
        home_sample_date_2 = python_data.get('home_sample_date_2', None)
        flag = python_data.get('flag', 'employee')
        cart_flag = python_data.get('cart_flag')
        is_payment = python_data.get('is_payment')
        method = python_data.get('method')
        transaction_id = python_data.get('transaction_id')
        address = python_data.get('address')


        type_of_visit = models.PackageDetail.objects.filter(id = package).values_list('type_of_visit', flat=True)[0]

        now = datetime.now()
        formatted_date = now.strftime("%B %d, %Y")
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        current_time = now.strftime("%Y%m%d%H%M%S")
        current_date_booking = now.strftime("%Y%m%d")
        if cart_flag == True:
            status = 'add_to_cart'
        else: 
            status = 'Request Received'

        if flag == 'employee':
            check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
            list_data = []
            if check_employee == 1:
                vendor_id = models.PackageDetail.objects.filter(id = package).values_list('vendor', flat=True)[0]
                appointment_check = models.AppointmentDetail.objects.filter(employee_id = employee, patient_id = patient,package_id = package, status= 'add_to_cart').count()

                if appointment_check == 0 or appointment_check == 0:

                    appointment_create = models.AppointmentDetail.objects.create(
                        employee_id = employee,  
                        appointment_type = 'Employee',
                        patient_id = patient,
                        employee_address_id = address,
                        package_id = package,
                        center_id = center,
                        vendor_id = vendor_id,
                        type_of_visit_id = type_of_visit,
                        appointment_date_1 = appointment_date_1, 
                        appointment_date_2 = appointment_date_2,
                        home_sample_date_1 = home_sample_date_1,
                        home_sample_date_2 = home_sample_date_2,
                        status = status,
                        created_at = current_date
                    )
                    appointment_create.save()
                    appointment_id = appointment_create.id

                    if cart_flag != True:
                        package_data = models.PackageDetail.objects.get(id = package)
                        package_type = package_data.package_type
                        amount = package_data.offer_price
                        corporate_id = models.EmployeeDetail.objects.filter(id = employee).values_list('corporate', flat=True)[0]

                        if is_payment == False:
                            amount = 0
                        ### Invoice Data
                        total_today_appointment = models.AppointmentDetail.objects.filter(created_at =current_date).count()
                        formatted_num = format(total_today_appointment, '03d')
                        all_appointment = models.AppointmentDetail.objects.all().count()
                        all_formatted_num = format(all_appointment, '05d')
                        
                        booking_id = 'BKG-' + str(current_date_booking) + '-' +str(formatted_num)
                        
                        invoice_id = f'25-26/{formatted_num}/IN-{all_formatted_num}'
                        # 25-26/0001/IN-00001
                        transaction_create = models.Transaction.objects.create(
                            transaction_type = package_type,
                            appointment_id = appointment_create.id,
                            is_payment = is_payment,
                            booking_id = booking_id,
                            method = method,
                            transaction_id = transaction_id,
                            invoice_id = invoice_id,
                            individual_id=None,
                            corporate_id=corporate_id,
                            employee_id=employee,
                            package_id=package,
                            amount=amount,
                            patient_id = patient,
                            status='Paid',
                            reason = 'Paid but Appointment/Report is pending.',
                            created_at=current_date
                        ).save()

                        notification = models.NotificationDetail.objects.create(
                            title = 'Health Checkup Request Received',
                            notification_type = 'Acknowledgment',
                            preferred_appointment_date1 = appointment_date_1,
                            preferred_appointment_date2 = appointment_date_2,
                            user_type = 'employee',
                            employee_id = employee,
                            center_id = center,
                            package_id = package,
                            type_of_visit_id = type_of_visit,
                            created_date = current_date,
                            created_time = curr_time,
                            user_read = 'false'
                        ).save()


                        name = appointment_create.employee.employee_name
                        recipient_name = appointment_create.patient.dependent_name
                        recipient_number = appointment_create.employee.mobile
                        recipient_email = appointment_create.employee.email
                        recipient_address = appointment_create.employee.address + ', ' + appointment_create.employee.city + ' - ' + appointment_create.employee.pincode
                        recipient_date_of_birth = appointment_create.patient.date_of_birth
                        recipient_dependent_relation = appointment_create.patient.dependent_relation.relation
                        center_name = appointment_create.center.center_name
                        center_address = appointment_create.center.address + ', ' + appointment_create.center.city + ' - ' + appointment_create.center.pincode
                        appointment_date_1 =appointment_create.appointment_date_1
                        appointment_date_2 = appointment_create.appointment_date_2
                        gender = appointment_create.patient.gender.gender
                        

                        invoice_date = formatted_date

                        package_name = appointment_create.package.package_name
                        package_service = appointment_create.package.type_of_service.type_of_service
                        visit_type = appointment_create.package.type_of_visit.type_of_visit
                        
                        package_amount = appointment_create.package.MRP
                        package_discount_price = appointment_create.package.discount_price
                        package_offer_price = appointment_create.package.offer_price
                    
                        amount_in_words = num2words(package_offer_price, lang='en').capitalize() + " only"
                        
                        center_state = appointment_create.center.state
                        appointment_id = appointment_create.id

                        if center_state == 'Maharashtra':
                            package_SGST = appointment_create.package.sgst
                            package_SGST_amount = appointment_create.package.sgst_amount
                            package_CGST = appointment_create.package.cgst
                            package_CGST_amount = appointment_create.package.cgst_amount

                            context= {
                                "name":name,
                                "recipient_name":recipient_name,
                                "recipient_number":recipient_number,
                                "recipient_email":recipient_email,
                                "recipient_address":recipient_address,
                                "recipient_date_of_birth":recipient_date_of_birth,
                                "recipient_dependent_relation":recipient_dependent_relation,
                                "appointment_date_1": appointment_date_1,
                                "appointment_date_2": appointment_date_2,
                                "gender":gender,

                                "center_name":center_name,
                                "center_address":center_address,
                                "invoice_id":invoice_id,
                                "invoice_date":invoice_date,
                                "booking_id":booking_id,

                                "package_name":package_name,
                                "package_service":package_service,
                                "visit_type":visit_type,
                                "package_amount":package_amount,
                                "package_discount_price":package_discount_price,
                                "amount_in_words":amount_in_words,
                                "package_offer_price":package_offer_price,
                                "method":method,
                                'amount':amount,

                                "flag":True,
                                "package_SGST":package_SGST,
                                "package_SGST_amount":package_SGST_amount,
                                "package_CGST":package_CGST,
                                "package_CGST_amount":package_CGST_amount,
                                "appointment_id":appointment_id
                            }    
                        else:
                            package_IGST = appointment_create.package.igst
                            package_IGST_amount = appointment_create.package.igst_amount
                            
                            context= {
                                "name":name,
                                "recipient_name":recipient_name,
                                "recipient_email":recipient_email,
                                "recipient_number":recipient_number,
                                "recipient_address":recipient_address,
                                "recipient_date_of_birth":recipient_date_of_birth,
                                "recipient_dependent_relation":recipient_dependent_relation,
                                "appointment_date_1": appointment_date_1,
                                "appointment_date_2": appointment_date_2,
                                "gender":gender,
                                
                                "center_name":center_name,
                                "center_address":center_address,
                                "invoice_id":invoice_id,
                                "invoice_date":invoice_date,
                                "booking_id":booking_id,
                                "method":method,
                                'amount':amount,
                                

                                "package_name":package_name,
                                "package_service":package_service,
                                "visit_type":visit_type,
                                "package_amount":package_amount,
                                "package_discount_price":package_discount_price,
                                "amount_in_words":amount_in_words,
                                "package_offer_price":package_offer_price,

                                "flag":False,
                                "package_IGST":package_IGST,
                                "package_IGST_amount":package_IGST_amount,
                                "appointment_id":appointment_id
                            }
                        
                        data = createPDF(context)
                        if recipient_email != None and recipient_email != 'null' and recipient_email != '':        
                            htmlgen = get_template("health_checkup.html").render(context)
                            send_mail('Acknowledgment of Your Health Checkup Request',"password",settings.EMAIL_HOST_USER,[recipient_email], fail_silently=False, html_message=htmlgen)
                
                        
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "You're appointment book successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "You're appointment book successfully.",
                            'appointment_id':appointment_id
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    res = {
                                'statuscode' : 406,
                                'status':'false',
                                'message':'Package with this dependent already in cart.'
                            }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')

        elif flag == 'individual':
            check_individual = models.IndividualUserDetail.objects.filter(id = individual).count()
            list_data = []
            if check_individual == 1:
                vendor_id = models.PackageDetail.objects.filter(id = package).values_list('vendor', flat=True)[0]
                appointment_check = models.AppointmentDetail.objects.filter(individual_id = individual,individual_patient_id = patient,package_id = package, status= 'add_to_cart').count()
                if appointment_check == 0 or appointment_check == 1:
                    appointment_create = models.AppointmentDetail.objects.create(
                        individual_id = individual,  
                        appointment_type = 'Individual',
                        individual_patient_id = patient,
                        individual_address_id = address,
                        package_id = package,
                        center_id = center,
                        vendor_id = vendor_id,
                        type_of_visit_id = type_of_visit,
                        appointment_date_1 = appointment_date_1, 
                        appointment_date_2 = appointment_date_2,
                        home_sample_date_1 = home_sample_date_1,
                        home_sample_date_2 = home_sample_date_2,
                        status = status,
                        created_at = current_date
                    )
                    appointment_create.save()
                    appointment_id = appointment_create.id

                    if cart_flag != True:
                        package_data = models.PackageDetail.objects.get(id = package)
                        package_type = package_data.package_type
                        amount = package_data.offer_price
                        # corporate_id = models.EmployeeDetail.objects.filter(id = employee).values_list('corporate', flat=True)[0]

                        if is_payment == False:
                            amount = 0
                        ### Invoice Data
                        total_today_appointment = models.AppointmentDetail.objects.filter(created_at =current_date).count()
                        formatted_num = format(total_today_appointment, '03d')
                        all_appointment = models.AppointmentDetail.objects.all().count()
                        all_formatted_num = format(all_appointment, '05d')

                        booking_id = 'BKG-' + str(current_date_booking) + '-' +str(formatted_num)
                        
                        invoice_id = f'25-26/{formatted_num}/IN-{all_formatted_num}'

                        package_data = models.PackageDetail.objects.get(id = package)
                        package_type = package_data.package_type
                        amount = package_data.offer_price

                        transaction_create = models.Transaction.objects.create(
                            transaction_type = package_type,
                            appointment_id = appointment_create.id,
                            is_payment = is_payment,
                            booking_id = booking_id,
                            invoice_id = invoice_id,
                            individual_id=individual,
                            method = method,
                            transaction_id = transaction_id,
                            corporate_id=None,
                            employee_id=None,
                            package_id=package,
                            amount=amount,
                            individual_patient_id = patient,
                            status='Paid',
                            reason = 'Paid but Appointment/Report is pending.',
                            created_at=current_date
                        ).save()

                        notification = models.NotificationDetail.objects.create(
                            title = 'Health Checkup Request Received',
                            notification_type = 'Acknowledgment',
                            preferred_appointment_date1 = appointment_date_1,
                            preferred_appointment_date2 = appointment_date_2,
                            user_type = 'individual',
                            individual_id = individual,
                            center_id = center,
                            package_id = package,
                            type_of_visit_id = type_of_visit,
                            created_date = current_date,
                            created_time = curr_time,
                            user_read = 'false'
                        ).save()

                        
                        recipient_name = appointment_create.individual_patient.dependent_name
                        recipient_number = appointment_create.individual.mobile
                        recipient_email = appointment_create.individual.email
                        recipient_address = appointment_create.individual.address + ', ' + appointment_create.individual.city + ' - ' + appointment_create.individual.pincode

                        center_name = appointment_create.center.center_name
                        center_address = appointment_create.center.address + ', ' + appointment_create.center.city + ' - ' + appointment_create.center.pincode


                        invoice_date = formatted_date

                        package_name = appointment_create.package.package_name
                        package_service = appointment_create.package.type_of_service.type_of_service
                        
                        package_amount = appointment_create.package.MRP
                        package_discount_price = appointment_create.package.discount_price
                        package_offer_price = appointment_create.package.offer_price
                    
                        amount_in_words = num2words(package_offer_price, lang='en').capitalize() + " only"
                        
                        center_state = appointment_create.center.state
                        appointment_id = appointment_create.id


                        if center_state == 'Maharashtra':
                            package_SGST = appointment_create.package.sgst
                            package_SGST_amount = appointment_create.package.sgst_amount
                            package_CGST = appointment_create.package.cgst
                            package_CGST_amount = appointment_create.package.cgst_amount

                            context= {
                                "recipient_name":recipient_name,
                                "recipient_number":recipient_number,
                                "recipient_email":recipient_email,
                                "recipient_address":recipient_address,
                                
                                "center_name":center_name,
                                "center_address":center_address,
                                "invoice_id":invoice_id,
                                "invoice_date":invoice_date,
                                "booking_id":booking_id,
                                "method":method,

                                "package_name":package_name,
                                "package_service":package_service,
                                "package_amount":package_amount,
                                "package_discount_price":package_discount_price,
                                "amount_in_words":amount_in_words,
                                "package_offer_price":package_offer_price,

                                "flag":True,
                                "package_SGST":package_SGST,
                                "package_SGST_amount":package_SGST_amount,
                                "package_CGST":package_CGST,
                                "package_CGST_amount":package_CGST_amount,
                                "appointment_id":appointment_id
                            }    
                        else:
                            package_IGST = appointment_create.package.igst
                            package_IGST_amount = appointment_create.package.igst_amount
                            
                            context= {
                                "recipient_name":recipient_name,
                                "recipient_number":recipient_number,
                                "recipient_address":recipient_address,
                                "center_name":center_name,
                                "center_address":center_address,
                                "invoice_id":invoice_id,
                                "invoice_date":invoice_date,
                                "booking_id":booking_id,
                                "method":method,

                                "package_name":package_name,
                                "package_service":package_service,
                                "package_amount":package_amount,
                                "package_discount_price":package_discount_price,
                                "amount_in_words":amount_in_words,
                                "package_offer_price":package_offer_price,

                                "flag":False,
                                "package_IGST":package_IGST,
                                "package_IGST_amount":package_IGST_amount,
                                "appointment_id":appointment_id

                            }

                        data = createPDF(context)

                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "You're appointment book successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            
                    else:
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "You're appointment book successfully.",
                            'appointment_id':appointment_id
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    res = {
                                'statuscode' : 406,
                                'status':'false',
                                'message':'Package with this dependent already in cart.'
                            }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Please Enter Individual."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        else:

            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Employee."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

# @csrf_exempt
# def createPDF(context):
#     now = datetime.now()
#     print(now, 'nownow')
#     formatted_date = now.strftime("%B %d, %Y")
#     current_date_data = now.strftime('%Y-%m-%d')
#     current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
#     curr_time = time.strftime("%H:%M:%S", time.localtime())
#     current_time = now.strftime("%Y%m%d%H%M%S")
#     current_date_booking = now.strftime("%Y%m%d")


#     date_time = str(current_date) + str(curr_time)
#     print(context, 'vadvdvkjdgvh')
#     recipient_name = context.get('recipient_name')
#     appointment_id = context.get('appointment_id')

#     invoice_template = get_template("invoice_template.html")
#     html_content = invoice_template.render(context)
#     options = {
            
#             'page-size': 'A4',
#             'no-outline': None,
#             'margin-top': '0mm',
#             'margin-right': '0mm',
#             'margin-bottom': '0mm',
#             'margin-left': '0mm',
#             'viewport-size': '1280x1024'
#         }
#     pdf = pdfkit.from_string(html_content, False, options=options)
#     pdf_name = f'invoice_{recipient_name +"_"+ date_time}.pdf'
#     pdf_file = ContentFile(pdf, name=pdf_name)
#     transaction = models.Transaction.objects.get(appointment = appointment_id)
#     transaction.invoice.save(pdf_file.name, pdf_file) 
#     transaction.save()

#     return None



@csrf_exempt
def appointment_booking_reschedule(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        appointment = python_data.get('appointment')
        status = python_data.get('status')

        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        check_appointment = models.AppointmentDetail.objects.filter(id = appointment).count()
        if check_appointment == 1:
            if status == 'Confirmed':
                appointment = models.AppointmentDetail.objects.get(id = appointment)
                appointment.remark = python_data.get('remark', appointment.remark)
                appointment.confirm_appointment_date = python_data.get('confirm_appointment_date', appointment.confirm_appointment_date)
                appointment.confirm_home_sample_date = python_data.get('confirm_home_sample_date', appointment.confirm_home_sample_date)
                appointment.status = 'Confirmed'
                appointment.save()
                
                type_of_visit = models.PackageDetail.objects.filter(id = appointment.package.id).values_list('type_of_visit', flat=True)[0]
                
                if appointment.appointment_type == "Employee":
                    individual = None
                    employee = appointment.employee.id
                    patient_name = appointment.patient.dependent_name
                    recipient_email = appointment.employee.email
                
                if appointment.appointment_type == "Individual":
                    employee = None
                    individual = appointment.individual.id
                    patient_name = appointment.patient.dependent_name
                    recipient_email = appointment.individual.email



                notification = models.NotificationDetail.objects.create(
                    title = 'Health Check-up Appointment Confirmed',
                    notification_type = 'Confirmation Appointment',
                    preferred_appointment_date1 = appointment.confirm_appointment_date,
                    preferred_appointment_date2 = appointment.confirm_home_sample_date,
                    user_type = (appointment.appointment_type).lower(),
                    individual_id = individual,
                    employee_id = employee,
                    center_id = appointment.center.id,
                    package_id = appointment.package.id,
                    type_of_visit_id = type_of_visit,
                    created_date = current_date,
                    created_time = curr_time,
                    user_read = 'false'
                )
                notification.save()

                context ={
                    "patient_name":patient_name,
                    "appointment_date":appointment.confirm_appointment_date,
                    "center_name":appointment.center.center_name,
                    "center_address":appointment.center.address,
                    "package_name":appointment.package.package_name

                }

                if recipient_email != None and recipient_email != 'null' and recipient_email != '':        
                    htmlgen = get_template("appointment_confirmation.html").render(context)
                    send_mail('Your Upcoming Health Check-up – Appointment Confirmation',"password",'setting.EMAIL_HOST_USER',[recipient_email], fail_silently=False, html_message=htmlgen)
            

                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your appointment Booked successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
            
            elif status == 'Rescheduled':
                appointment = models.AppointmentDetail.objects.get(id = appointment)
                old_appointment_date = appointment.confirm_appointment_date or appointment.appointment_date_1
                old_home_sample_date = appointment.confirm_home_sample_date or appointment.home_sample_date_1
                new_appointment_date = python_data.get('confirm_appointment_date', appointment.confirm_appointment_date)
                new_home_sample_date = python_data.get('confirm_home_sample_date', appointment.confirm_home_sample_date)
                rescheduled_by = python_data.get('rescheduled_by', appointment.appointment_type)
                reason = python_data.get('reason', appointment.reason)
                remark = python_data.get('remark', appointment.remark)

                reschedule_record = models.RescheduleAppointment.objects.create(
                    appointment=appointment,
                    rescheduled_by=rescheduled_by,
                    old_appointment_date=old_appointment_date,
                    new_appointment_date=new_appointment_date,
                    old_home_sample_date=old_home_sample_date,
                    new_home_sample_date=new_home_sample_date,
                    reason=reason,
                    remark=remark,
                    status='Rescheduled',
                    created_at=current_date
                )

                appointment.remark = remark
                appointment.reason = reason
                appointment.confirm_appointment_date = new_appointment_date
                appointment.confirm_home_sample_date = new_home_sample_date
                appointment.status = 'Rescheduled'
                appointment.save()

                reschedule_serializer = RescheduleAppointmentSerializer(reschedule_record)
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your appointment Rescheduled successfully.",
                    'data': reschedule_serializer.data
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter valid Status."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')   

        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid appointment."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def reschedule_appointment_list(request):
    if request.method in ['POST', 'GET']:
        if request.method == 'POST':
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('appointment_id') or python_data.get('appointment')
        else:
            appointment_id = request.GET.get('appointment_id') or request.GET.get('appointment')

        if appointment_id:
            records = models.RescheduleAppointment.objects.filter(appointment_id=appointment_id).order_by('-id')
        else:
            records = models.RescheduleAppointment.objects.all().order_by('-id')

        serializer = RescheduleAppointmentSerializer(records, many=True)
        res = {
            'statuscode': 200,
            'status': 'true',
            'data': serializer.data
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')




@csrf_exempt
def appointment_cancel_done(request):
    if request.method == 'POST':
        python_data={}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})

        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = time.strftime("%H:%M:%S", time.localtime())

        appointment = python_data.get('appointment')
        status = python_data.get('status')
        check_appointment = models.AppointmentDetail.objects.filter(id = appointment).count()
        if check_appointment == 1:
            if status == 'Cancel':
                appointment = models.AppointmentDetail.objects.get(id = appointment)
                appointment.reason = python_data.get('reason', appointment.reason)
                appointment.status = 'Cancel'
                appointment.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your appointment Cancel successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
            
            elif status == 'Reports Uploaded':
                appointment = models.AppointmentDetail.objects.get(id = appointment)
                
                if type(python_data.get('report', appointment.report)) != str:         
                    appointment.report = python_data.get('report', appointment.report)
                    appointment.report_date = current_date
                    # appointment.report_date = python_data.get('report_date', appointment.report_date)

                appointment.status = 'Reports Uploaded'
                appointment.save()
                transaction = models.Transaction.objects.get(appointment = appointment)
                transaction.reason = 'Appointment done and Report Uploaded.'
                transaction.status = 'Complete'
                transaction.save()
                
                appointment_type = appointment.appointment_type
                if (appointment_type).lower() == 'employee':
                    recipient_name = appointment.patient.dependent_name
                    employee = appointment.employee.id
                    individual = None
                    recipient_email =appointment.employee.email
                else:
                    recipient_name = appointment.individual_patient.dependent_name
                    individual = appointment.individual.id
                    employee = None
                    recipient_email =appointment.individual.email

                notification = models.NotificationDetail.objects.create(
                    title = 'Your Health Check-Up Report is Ready!',
                    notification_type = 'Report Ready',
                    user_type = appointment_type,
                    employee_id = employee,
                    individual_id = individual,
                    recipient_name = recipient_name,
                    created_date = current_date,
                    created_time = curr_time,
                    user_read = 'false'
                ).save()

                context={
                    "recipient_name":recipient_name
                }
                if recipient_email != None and recipient_email != 'null' and recipient_email != '':        
                    htmlgen = get_template("report_upload.html").render(context)
                    send_mail('Your Health Check-Up Report – We Value Your Feedback 💙',"password",'setting.EMAIL_HOST_USER',[recipient_email], fail_silently=False, html_message=htmlgen)
                    
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your appointment Done successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
            
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter valid Status."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')   

        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid appointment."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def appointment_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        appointment = python_data.get('id')
        check_appointment = models.AppointmentDetail.objects.filter(id = appointment).count()
        if check_appointment == 1:
            
            appointment_details = models.AppointmentDetail.objects.get(id = appointment)
            appointment_details.status = 'Pending'
            appointment_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "appointment Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid appointment ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def all_appointment_list(request):
    if request.method == 'POST':
        get_data={}
        for i,j in request.FILES.items():
            get_data.update({i:j})
        
        for i,j in request.POST.items():
            get_data.update({i:j})

        base64_string = get_data.get('data')
        base64_bytes = base64_string.encode("ascii")
        string_bytes = base64.b64decode(base64_bytes)
        python_data = string_bytes.decode("ascii")
        python_data = json.loads(python_data)
        
        employee_total_records = 0
        individual_totals_records = 0

        page_number = int(python_data.get('page_number',1))
        row_size = int(python_data.get('row_size',10))
        last_row = row_size * page_number
        first_row = last_row - row_size

        id = python_data.get('id')
        # id = request.POST['id']
        check_staff = models.StaffDetail.objects.filter(id = id).count()
        if check_staff == 1:
            staff_id = models.StaffDetail.objects.get(id = id)
            get_type_access = staff_id.type_of_access.type_of_access
            if get_type_access == 'Super Admin' or get_type_access == 'Admin': 

                corporate_name = python_data.get('corporate_name', None)
                employee_name = python_data.get('employee_name', None)
                individual_name = python_data.get('individual_name', None)
                patient_name = python_data.get('patient_name', None)
                address_short = python_data.get('address_short', None)
                package_name = python_data.get('package_name', None)
                package_price = python_data.get('package_price', None)
                type_of_service = python_data.get('type_of_service', None)
                type_of_visit = python_data.get('type_of_visit', None)
                center_name = python_data.get('center_name', None)
                vendor_name = python_data.get('vendor_name', None)
                created_at = python_data.get('created_at', None)
                appointment_date_1 = python_data.get('appointment_date_1', None)
                appointment_date_2 = python_data.get('appointment_date_2', None)
                home_sample_date_1 = python_data.get('home_sample_date_1', None)
                home_sample_date_2 = python_data.get('home_sample_date_2', None)
                confirm_appointment_date = python_data.get('confirm_appointment_date', None)
                confirm_home_sample_date = python_data.get('confirm_home_sample_date', None)
                report_date = python_data.get('report_date', None)
                status = python_data.get('status', None)


                filter_condition = {}

                # Corporate & Individual
                if corporate_name not in [None, '', 'null']:
                    filter_condition['corporate_name__icontains'] = corporate_name

                if employee_name not in [None, '', 'null']:
                    filter_condition['employee__employee_name__icontains'] = employee_name

                if individual_name not in [None, '', 'null']:
                    filter_condition['individual__name__icontains'] = individual_name

                # Patient & Address
                if patient_name not in [None, '', 'null']:
                    filter_condition['individual_patient__dependent_name__icontains'] = patient_name

                if address_short not in [None, '', 'null']:
                    filter_condition['individual__address__icontains'] = address_short

                # Package details
                if package_name not in [None, '', 'null']:
                    filter_condition['package__package_name__icontains'] = package_name

                if package_price not in [None, '', 'null']:
                    filter_condition['package__offer_price__icontains'] = package_price

                # Service & Visit details
                if type_of_service not in [None, '', 'null']:
                    filter_condition['package__type_of_service__type_of_service__icontains'] = type_of_service

                if type_of_visit not in [None, '', 'null']:
                    filter_condition['type_of_visit__type_of_visit__icontains'] = type_of_visit

                # Center & Vendor
                if center_name not in [None, '', 'null']:
                    filter_condition['center__center_name__icontains'] = center_name

                if vendor_name not in [None, '', 'null']:
                    filter_condition['vendor__vendor_name__icontains'] = vendor_name

                # Dates
                if created_at not in [None, '', 'null']:
                    filter_condition['created_at__icontains'] = created_at

                if appointment_date_1 not in [None, '', 'null']:
                    filter_condition['appointment_date_1__icontains'] = appointment_date_1

                if appointment_date_2 not in [None, '', 'null']:
                    filter_condition['appointment_date_2__icontains'] = appointment_date_2

                if home_sample_date_1 not in [None, '', 'null']:
                    filter_condition['home_sample_date_1__icontains'] = home_sample_date_1

                if home_sample_date_2 not in [None, '', 'null']:
                    filter_condition['home_sample_date_2__icontains'] = home_sample_date_2

                if confirm_appointment_date not in [None, '', 'null']:
                    filter_condition['confirm_appointment_date__icontains'] = confirm_appointment_date

                if confirm_home_sample_date not in [None, '', 'null']:
                    filter_condition['confirm_home_sample_date__icontains'] = confirm_home_sample_date

                if report_date not in [None, '', 'null']:
                    filter_condition['report_date__icontains'] = report_date
                
                if status not in [None, '', 'null']:
                    if status != 'All':
                        filter_condition['status__icontains'] = status


                all_appointment = models.AppointmentDetail.objects.filter(**filter_condition).exclude(status='add_to_cart').order_by('-id')
                serialiser = AppointmentDetailSerializer(all_appointment, many=True)

                employee_total_records = models.AppointmentDetail.objects.filter(**filter_condition, appointment_type = 'Employee').exclude(status='add_to_cart').count()
                all_appointment_employee = models.AppointmentDetail.objects.filter(**filter_condition, appointment_type = 'Employee').exclude(status='add_to_cart').order_by('-id')[first_row:last_row]
                employee_serialiser = AppointmentDetailSerializer(all_appointment_employee, many=True)
                list_employee_data = employee_serialiser.data
                
                individual_totals_records = models.AppointmentDetail.objects.filter(**filter_condition, appointment_type = 'Individual').exclude(status='add_to_cart').count()
                all_appointment_individual = models.AppointmentDetail.objects.filter(**filter_condition, appointment_type = 'Individual').exclude(status='add_to_cart').order_by('-id')[first_row:last_row]
                individual_serialiser = AppointmentDetailSerializer(all_appointment_individual, many=True)
                list_individual_data = individual_serialiser.data
            
            else:
                list_employee_data = []

                staff_assign_to = models.StaffDetail.objects.filter(id = id).values_list('assign_to', flat=True)[0]
                if staff_assign_to == 'Corporate':
                    corporate_name = python_data.get('corporate_name',None)
                    employee_name = python_data.get('employee_name',None)
                    patient_name = python_data.get('patient_name',None)
                    address_short = python_data.get('address_short',None)
                    package_name = python_data.get('package_name',None)
                    package_price = python_data.get('package_price',None)
                    type_of_service = python_data.get('type_of_service',None)
                    type_of_visit = python_data.get('type_of_visit',None)
                    center_name = python_data.get('center_name',None)
                    vendor_name = python_data.get('vendor_name',None)
                    created_at = python_data.get('created_at',None)
                    appointment_date_1 = python_data.get('appointment_date_1',None)
                    appointment_date_2 = python_data.get('appointment_date_2',None)
                    home_sample_date_1 = python_data.get('home_sample_date_1',None)
                    home_sample_date_2 = python_data.get('home_sample_date_2',None)
                    confirm_appointment_date = python_data.get('confirm_appointment_date',None)
                    confirm_home_sample_date = python_data.get('confirm_home_sample_date',None)
                    report_date = python_data.get('report_date',None)

                    filter_condition = {}

                    if corporate_name not in [None,'','null']:
                        filter_condition['corporate_name__icontains'] = corporate_name
                    if employee_name not in [None,'','null']:
                        filter_condition['employee__employee_name__icontains'] = employee_name
                    if patient_name not in [None,'','null']:
                        filter_condition['patient__dependent_name__icontains'] = patient_name
                    if address_short not in [None,'','null']:
                        filter_condition['address_short__icontains'] = address_short
                    if package_name not in [None,'','null']:
                        filter_condition['package__package_name__icontains'] = package_name
                    if package_price not in [None,'','null']:
                        filter_condition['package__package_price__icontains'] = package_price
                    if type_of_service not in [None,'','null']:
                        filter_condition['type_of_service__icontains'] = type_of_service
                    if type_of_visit not in [None,'','null']:
                        filter_condition['type_of_visit__type_of_visit__icontains'] = type_of_visit
                    if center_name not in [None,'','null']:
                        filter_condition['center__center_name__icontains'] = center_name
                    if vendor_name not in [None,'','null']:
                        filter_condition['vendor__vendor_name__icontains'] = vendor_name
                    if created_at not in [None,'','null']:
                        filter_condition['created_at__icontains'] = created_at
                    if appointment_date_1 not in [None,'','null']:
                        filter_condition['appointment_date_1__icontains'] = appointment_date_1
                    if appointment_date_2 not in [None,'','null']:
                        filter_condition['appointment_date_2__icontains'] = appointment_date_2
                    if home_sample_date_1 not in [None,'','null']:
                        filter_condition['home_sample_date_1__icontains'] = home_sample_date_1
                    if home_sample_date_2 not in [None,'','null']:
                        filter_condition['home_sample_date_2__icontains'] = home_sample_date_2
                    if confirm_appointment_date not in [None,'','null']:
                        filter_condition['confirm_appointment_date__icontains'] = confirm_appointment_date
                    if confirm_home_sample_date not in [None,'','null']:
                        filter_condition['confirm_home_sample_date__icontains'] = confirm_home_sample_date
                    if report_date not in [None,'','null']:
                        filter_condition['report_date__icontains'] = report_date


                    
                    all_corporate = models.CorporateDetail.objects.filter(Q(level1 =staff_id) | Q(level2 =staff_id )).distinct()
                    serialiser = CorporateSerializer(all_corporate, many=True)
                    for corporate in all_corporate:
                        get_all_employee = models.EmployeeDetail.objects.filter(corporate = corporate.id)
                        list_individual_data = []
                        for employee in get_all_employee:
                            employee_total_records = models.AppointmentDetail.objects.filter(**filter_condition,employee= employee, appointment_type = 'Employee').exclude(status='add_to_cart').count()
                            all_appointment_employee = models.AppointmentDetail.objects.filter(**filter_condition,employee= employee, appointment_type = 'Employee').exclude(status='add_to_cart').order_by('-id')[first_row:last_row]
                            employee_serialiser = AppointmentDetailSerializer(all_appointment_employee, many=True)
                            list_employee_data.append(employee_serialiser.data)

                    list_employee_data = sum(list_employee_data, [])
                
                elif staff_assign_to == 'Individual':
                    individual_name = python_data.get('individual_name',None)
                    patient_name = python_data.get('patient_name',None)
                    address_short = python_data.get('address_short',None)
                    package_name = python_data.get('package_name',None)
                    package_price = python_data.get('package_price',None)
                    type_of_service = python_data.get('type_of_service',None)
                    type_of_visit = python_data.get('type_of_visit',None)
                    center_name = python_data.get('center_name',None)
                    vendor_name = python_data.get('vendor_name',None)
                    created_at = python_data.get('created_at',None)
                    appointment_date_1 = python_data.get('appointment_date_1',None)
                    appointment_date_2 = python_data.get('appointment_date_2',None)
                    home_sample_date_1 = python_data.get('home_sample_date_1',None)
                    home_sample_date_2 = python_data.get('home_sample_date_2',None)
                    confirm_appointment_date = python_data.get('confirm_appointment_date',None)
                    confirm_home_sample_date = python_data.get('confirm_home_sample_date',None)
                    report_date = python_data.get('report_date',None)

                    filter_condition = {}

                    if individual_name not in [None, '', 'null']:
                        filter_condition['individual__individual_name__icontains'] = individual_name

                    if patient_name not in [None, '', 'null']:
                        filter_condition['patient__patient_name__icontains'] = patient_name

                    if address_short not in [None, '', 'null']:
                        filter_condition['address_short__icontains'] = address_short

                    if package_name not in [None, '', 'null']:
                        filter_condition['package__package_name__icontains'] = package_name

                    if package_price not in [None, '', 'null']:
                        filter_condition['package__package_price__icontains'] = package_price

                    if type_of_service not in [None, '', 'null']:
                        filter_condition['type_of_service__icontains'] = type_of_service

                    if type_of_visit not in [None, '', 'null']:
                        filter_condition['type_of_visit__type_of_visit__icontains'] = type_of_visit

                    if center_name not in [None, '', 'null']:
                        filter_condition['center__center_name__icontains'] = center_name

                    if vendor_name not in [None, '', 'null']:
                        filter_condition['vendor__vendor_name__icontains'] = vendor_name

                    if created_at not in [None, '', 'null']:
                        filter_condition['created_at__icontains'] = created_at

                    if appointment_date_1 not in [None, '', 'null']:
                        filter_condition['appointment_date_1__icontains'] = appointment_date_1

                    if appointment_date_2 not in [None, '', 'null']:
                        filter_condition['appointment_date_2__icontains'] = appointment_date_2

                    if home_sample_date_1 not in [None, '', 'null']:
                        filter_condition['home_sample_date_1__icontains'] = home_sample_date_1

                    if home_sample_date_2 not in [None, '', 'null']:
                        filter_condition['home_sample_date_2__icontains'] = home_sample_date_2

                    if confirm_appointment_date not in [None, '', 'null']:
                        filter_condition['confirm_appointment_date__icontains'] = confirm_appointment_date

                    if confirm_home_sample_date not in [None, '', 'null']:
                        filter_condition['confirm_home_sample_date__icontains'] = confirm_home_sample_date

                    if report_date not in [None, '', 'null']:
                        filter_condition['report_date__icontains'] = report_date


                    list_employee_data = []
                    list_individual_data = []

                    individual_totals_records = models.AppointmentDetail.objects.filter(**filter_condition, appointment_type = 'Individual').exclude(status='add_to_cart').count()
                    all_appointment_individual = models.AppointmentDetail.objects.filter(**filter_condition, appointment_type = 'Individual').exclude(status='add_to_cart').order_by('-id')[first_row:last_row]
                    individual_serialiser = AppointmentDetailSerializer(all_appointment_individual, many=True)
                    list_individual_data.append(individual_serialiser.data)

        res = {
            'statuscode' : 200,
            'status':'true',
            # 'data' : serialiser.data,
            'employee_data':list_employee_data,
            'employee_total_records':employee_total_records,
            'individual_data':list_individual_data,
            'individual_totals_records':individual_totals_records
        }
        
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



# @csrf_exempt
# def all_appointment_list_corporate(request):
#     if request.method == 'POST':
#         get_data={}
#         for i,j in request.FILES.items():
#             get_data.update({i:j})
        
#         for i,j in request.POST.items():
#             get_data.update({i:j})

#         base64_string = get_data.get('data')
#         base64_bytes = base64_string.encode("ascii")
#         string_bytes = base64.b64decode(base64_bytes)
#         python_data = string_bytes.decode("ascii")
#         python_data = json.loads(python_data)

#         print("python_data--=-=-->",python_data)
        
#         id = python_data.get('id',None)

#         corporate_name = python_data.get('corporate_name',None)
#         employee_name = python_data.get('employee_name',None)
#         patient_name = python_data.get('patient_name',None)
#         address_short = python_data.get('address_short',None)
#         package_name = python_data.get('package_name',None)
#         package_price = python_data.get('package_price',None)
#         type_of_service = python_data.get('type_of_service',None)
#         type_of_visit = python_data.get('type_of_visit',None)
#         center_name = python_data.get('center_name',None)
#         vendor_name = python_data.get('vendor_name',None)
#         created_at = python_data.get('created_at',None)
#         appointment_date_1 = python_data.get('appointment_date_1',None)
#         appointment_date_2 = python_data.get('appointment_date_2',None)
#         home_sample_date_1 = python_data.get('home_sample_date_1',None)
#         home_sample_date_2 = python_data.get('home_sample_date_2',None)
#         confirm_appointment_date = python_data.get('confirm_appointment_date',None)
#         confirm_home_sample_date = python_data.get('confirm_home_sample_date',None)
#         report_date = python_data.get('report_date',None)




@csrf_exempt
def appointment_list_for_vendor(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        vendor = python_data.get('vendor')
        check_vendor = models.VendorDetail.objects.filter(id = vendor).count()
        if check_vendor == 1:
            all_appointment = models.AppointmentDetail.objects.filter(vendor = vendor).exclude(status='add_to_cart').order_by('-id')
            serialiser = AppointmentDetailSerializer(all_appointment, many=True)

            done_appointment_count = models.AppointmentDetail.objects.filter(vendor = vendor, status = 'Reports Uploaded').count()
            cancel_appointment_count = models.AppointmentDetail.objects.filter(vendor = vendor, status = 'Cancel').count()
            booking_appointment_count = models.AppointmentDetail.objects.filter(vendor = vendor, status = 'Confirmed').count()
            reschedule_appointment_count = models.AppointmentDetail.objects.filter(vendor = vendor, status = 'Rescheduled').count()

            res = {
                'statuscode' : 200,
                'status':'true',
                'data' : serialiser.data,
                'done_appointment_count':done_appointment_count,
                'cancel_appointment_count':cancel_appointment_count,
                'booking_appointment_count':booking_appointment_count,
                'reschedule_appointment_count':reschedule_appointment_count
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Vendor ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def employee_appointment_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')
        all_appointment = models.AppointmentDetail.objects.filter(employee = employee).exclude(status='add_to_cart').order_by('-id')
        
        serialiser = AppointmentDetailSerializer(all_appointment, many=True)
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def individual_appointment_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        individual = python_data.get('individual')
        all_appointment = models.AppointmentDetail.objects.filter(individual = individual).exclude(status='add_to_cart').order_by('-id')
        
        serialiser = AppointmentDetailSerializer(all_appointment, many=True)
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def bulk_import(request):
    if (request.method == "POST"):
        python_data={}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})
        
        excel_file = python_data.get('excel_file')
        flag = python_data.get('flag')

        
        letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',\
                'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ', \
                'BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM','BN','BO','BP','BQ','BR','BS','BT','BU','BV','BW','BX','BY','BZ']
            
        
        if flag == 'Staff':
            try:
                fs = FileSystemStorage()
                fs.delete('staff_details.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('staff_details.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0

            new_filename = 'staff_details_data.xlsx'
            new_file_url = fs.url(new_filename)
            new_file_path = fs.path(new_filename)  

            wb = load_workbook(new_file_path)
            ws = wb.active
            ws.delete_rows(2, ws.max_row) 
            wb.save(new_file_path)
            
            new_workbook = load_workbook(new_file_path)
            new_sheet = new_workbook.active

            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue
                
                if row[0] == None:
                    break
                
                # print(row, 'row')
                
                name = row[1]
                mobile = '+91 ' + str(row[2])
                email = row[3]
                staff_code = (str(row[4])).upper()
                staff_type = row[5]
                staff_level = row[6]
                type_of_access = row[7]
                department = row[8]
                assign_to = row[9]
                
                get_new_cell = str(letters[0]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[0]  
                new_workbook.save(new_file_path)
        
                get_new_cell = str(letters[1]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[1]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[2]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = mobile
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[3]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[3]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[4]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[4]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[5]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[5]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[6]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[6]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[7]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[7]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[8]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[8]  
                new_workbook.save(new_file_path)

                get_new_cell = str(letters[9]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[9]  
                new_workbook.save(new_file_path)


                name_reason = None
                name_count = 0 
                for char in name:
                    if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                        name_count += 1
                
                if name_count != 0:
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    name_reason = 'Enter alphanumeric character only'
                    invalid_count += 1
                
                mobile_reason = None
                if len(mobile) == 14:
                    check_mobile = models.StaffDetail.objects.filter(mobile = mobile).count()
                    if check_mobile != 0:
                        get_cell = str(letters[2]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        mobile_reason = 'Enter Mobile Number already Registerd'
                        invalid_count += 1
                else:
                    get_cell = str(letters[2]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    mobile_reason = 'Enter 10-digit Mobile Number'
                    invalid_count += 1


                email_reason = None
                if "@" in email and "." in email.split("@")[-1]:
                
                    check_email = models.StaffDetail.objects.filter(email = email).count()
                    if check_email != 0:
                        get_cell = str(letters[3]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        email_reason = 'Enter Email already Registerd'
                        invalid_count += 1
                else:
                    get_cell = str(letters[3]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    email_reason = 'Enter Valid Email'
                    invalid_count += 1


                staff_code_reason = None
                check_staff_code = models.StaffDetail.objects.filter(staff_code = staff_code).count()
                if check_staff_code != 0:
                    get_cell = str(letters[4]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    staff_code_reason = 'Enter Staff Code already Registerd'
                    invalid_count += 1
                
                staff_type_reason = None
                check_staff_type = models.StaffType.objects.filter(staff_type = staff_type).count()
                if check_staff_type == 0:
                    get_cell = str(letters[5]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    staff_type_reason = "You've Entered wrong Staff Type"
                    invalid_count += 1

                staff_level_reason = None
                check_staff_level = models.StaffLevel.objects.filter(staff_level = staff_level).count()
                if check_staff_level == 0:
                    get_cell = str(letters[6]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    staff_level_reason = "You've Entered wrong Staff Level"
                    invalid_count += 1
                
                type_of_access_reason = None
                check_type_of_access = models.TypeOfAccess.objects.filter(type_of_access = type_of_access).count()
                if check_type_of_access == 0:
                    get_cell = str(letters[7]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    type_of_access_reason = "You've Entered wrong Type of Access"
                    invalid_count += 1

                department_reason = None
                check_department = models.StaffDepartment.objects.filter(staff_department = department).count()
                if check_department == 0:
                    get_cell = str(letters[8]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    department_reason = "You've Entered wrong Staff Department"
                    invalid_count += 1

                list_reason = []

                
                if name_reason != None:
                    list_reason.append(name_reason)
                
                if mobile_reason != None:
                    list_reason.append(mobile_reason)
                
                if email_reason != None:
                    list_reason.append(email_reason)
                
                if staff_code_reason != None:
                    list_reason.append(staff_code_reason)

                if staff_type_reason != None:
                    list_reason.append(staff_type_reason)

                if staff_level_reason != None:
                    list_reason.append(staff_level_reason)

                if type_of_access_reason != None:
                    list_reason.append(type_of_access_reason)

                if department_reason != None:
                    list_reason.append(department_reason)

                final_reason = ', '.join(map(str, list_reason)) 

                # print(final_reason, 'fdinal reason check ')
                if final_reason == '':
                    row_status = 'Valid'
                    start_color="3d7d13" 
                    end_color="3d7d13"
                else:
                    row_status = 'Invalid'
                    start_color="e39830"
                    end_color="e39830"


                get_new_cell = str(letters[10]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(row_status)
                cell_new_bg.fill = PatternFill(start_color=start_color, end_color=end_color,fill_type = "solid")
                new_workbook.save(new_file_path)


                get_new_cell = str(letters[11]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(final_reason)  
                new_workbook.save(new_file_path)

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'
            link = SITE_MEDIA_BASE_URL + new_filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Corporate':
            try:
                fs = FileSystemStorage()
                fs.delete('corporate_details.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('corporate_details.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0

            new_filename = 'corporate_details_data.xlsx'
            new_file_url = fs.url(new_filename)
            new_file_path = fs.path(new_filename)  

            wb = load_workbook(new_file_path)
            ws = wb.active
            ws.delete_rows(2, ws.max_row) 
            wb.save(new_file_path)
            
            new_workbook = load_workbook(new_file_path)
            new_sheet = new_workbook.active



            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue																		
                

                if row[0] == None:
                    break

                mobile = '+91 ' + str(row[1])
                email = row[2]
                corporate_name = row[3]
                corporate_code = (str(row[4])).upper()
                parent_company = row[5]
                type_of_corporation = row[6]
                industry = row[7]
                spoke_person = row[8]
                billing_email = row[9]
                billing_cycle = row[10]
                level1 = row[11]
                level2 = row[12]
                pan_card = row[13]
                GST_no = row[14]
                start_date = row[15]
                end_date = row[16]
                address = row[17]
                pincode = str(row[18])
                state = row[19]
                city = row[20]
                login_via = (row[21]).lower()
        
                get_new_cell = str(letters[0]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[0]  
                new_workbook.save(new_file_path)
        
                get_new_cell = str(letters[1]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = mobile
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[2]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[2]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[3]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[3]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[4]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[4]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[5]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[5]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[6]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[6]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[7]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[7]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[8]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[8]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[9]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[9]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[10]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[10]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[11]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[11]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[12]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[12]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[13]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[13]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[14]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[14]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[15]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[15]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[16]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[16]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[17]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[17]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[18]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[18]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[19]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[19]  
                new_workbook.save(new_file_path)

                            
                get_new_cell = str(letters[20]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = (row[20]).lower()  
                new_workbook.save(new_file_path)

                get_new_cell = str(letters[21]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = (row[21]).lower()  
                new_workbook.save(new_file_path)
                
                mobile_reason = None
                if len(mobile) == 14:
                    check_mobile = models.StaffDetail.objects.filter(mobile = mobile).count()
                    if check_mobile != 0:
                        get_cell = str(letters[1]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        mobile_reason = 'Enter Mobile Number already Registerd'
                        invalid_count += 1
                else:
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    mobile_reason = 'Enter 10-digit Mobile Number'
                    invalid_count += 1

                

                email_reason = None
                if "@" in email and "." in email.split("@")[-1]:
                
                    check_email = models.CorporateDetail.objects.filter(email = email).count()
                    if check_email != 0:
                        get_cell = str(letters[2]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        email_reason = 'Enter Email already Registerd'
                        invalid_count += 1
                else:
                    get_cell = str(letters[2]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    email_reason = 'Enter Valid Email'
                    invalid_count += 1

                corporate_name_reason = None
                corporate_name_count = 0 
                for char in corporate_name:
                    if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                        # print(char, 'chr')
                        corporate_name_count += 1
                
                if corporate_name_count != 0:
                    get_cell = str(letters[3]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    corporate_name_reason = 'Enter alphanumeric character only'
                    invalid_count += 1


                corporate_code_reason = None
                if len(corporate_code) <= 5:
                    check_corporate_code = models.CorporateDetail.objects.filter(corporate_code = corporate_code).count()
                    if check_corporate_code != 0:
                        get_cell = str(letters[4]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        corporate_code_reason = 'Enter Corporate Code already Registerd'
                        invalid_count += 1
                else:
                    get_cell = str(letters[4]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    corporate_code_reason = 'Corporate Code must be at most 5 characters.'
                    invalid_count += 1

                parent_company_reason = None
                if parent_company != None:
                    check_parent_company = models.ParentCompany.objects.filter(parent_company = parent_company).count()
                    if check_parent_company == 0:
                        get_cell = str(letters[5]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        parent_company_reason = 'Enter valid Parent Company'
                        invalid_count += 1
                
                industry_reason = None
                check_industry = models.TypeOfIndustry.objects.filter(type_of_industry = industry).count()
                if check_industry == 0:
                    get_cell = str(letters[7]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    industry_reason = 'Enter valid Type of Industry'
                    invalid_count += 1

                spoke_person_reason = None
                spoke_person_count = 0 
                for char in spoke_person:
                    if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                        spoke_person_count += 1
                
                if spoke_person_count != 0:
                    get_cell = str(letters[8]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    spoke_person_reason = 'Enter alphanumeric character only'
                    invalid_count += 1
                
                billing_reason = None
                check_billing_cycle = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).count()
                if check_billing_cycle == 0:
                    get_cell = str(letters[10]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    billing_reason = 'Enter valid Billing Cycle'
                    invalid_count += 1
                
                level1_reason = None
                if level1 != None:
                    list_level1 = level1.split(',')
                    list_data = []
                    for data in list_level1:
                        list_data.append(data.strip()) 
                    
                    level1_count = 0
                    for level in list_data:
                        get_level_1 = models.StaffLevel.objects.filter(staff_level = 'Level 1').values_list('id', flat=True)[0]
                        get_type_of_access = models.TypeOfAccess.objects.filter(type_of_access = 'Staff').values_list('id', flat=True)[0]
                        check_level1 = models.StaffDetail.objects.filter(staff_code = level, staff_level = get_level_1, type_of_access = get_type_of_access).count()
                        if check_level1 != 1:
                            level1_count += 1

                    if level1_count != 0:
                        get_cell = str(letters[11]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        level1_reason = 'Enter valid staff Level 1 code'
                        invalid_count += 1
                
                level2_reason = None
                if level2 != None:
                    list_level2 = level2.split(',')
                    list_data = []
                    for data in list_level2:
                        list_data.append(data.strip()) 
                    
                    level2_count = 0
                    for level in list_data:
                        get_level_2 = models.StaffLevel.objects.filter(staff_level = 'Level 2').values_list('id', flat=True)[0]
                        get_type_of_access = models.TypeOfAccess.objects.filter(type_of_access = 'Staff').values_list('id', flat=True)[0]

                        check_level2 = models.StaffDetail.objects.filter(staff_code = level, staff_level = get_level_2, type_of_access = get_type_of_access).count()
                        
                        if check_level2 != 1:
                            level2_count += 1

                    if level2_count != 0:
                        get_cell = str(letters[12]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        level2_reason = 'Enter valid staff Level 2 code'
                        invalid_count += 1


                pan_card_reason = None
                # print(pan_card, 'pancard')
                if pan_card == None:
                    # print('elif pan')
                    get_cell = str(letters[13]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    pan_card_reason = 'Enter Pan Card'
                    invalid_count += 1
                elif not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_card):
                    # print('if pan')
                    get_cell = str(letters[13]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    pan_card_reason = 'Enter Valid Pan Card'
                    invalid_count += 1
                
                GST_no_reason = None
                if GST_no == None:
                    get_cell = str(letters[14]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    GST_no_reason = 'Enter GST No'
                    invalid_count += 1
                elif not re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$', GST_no):
                    get_cell = str(letters[14]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    GST_no_reason = 'Enter Valid GST No'
                    invalid_count += 1

                
                billing_email_reason = None
                if billing_email == None:
                    get_cell = str(letters[9]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    billing_email_reason = 'Enter Billing Email'
                    invalid_count += 1
                else:
                    if not "@" in billing_email and "." in billing_email.split("@")[-1]:
                        get_cell = str(letters[9]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        billing_email_reason = 'Enter Valid Email'
                        invalid_count += 1
                
                pincode_reason = None
                pincode_count = 0 
                if len(pincode) == 6:
                    for char in pincode:
                        if char not in "0123456789":
                            pincode_count += 1
                    
                    if pincode_count != 0:
                        get_cell = str(letters[18]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        pincode_reason = 'Enter Numeric Code only'
                        invalid_count += 1
                else:
                    get_cell = str(letters[18]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    pincode_reason = 'Enter Valid Pin Code'
                    invalid_count += 1

                list_reason = []
                if mobile_reason != None:
                    list_reason.append(mobile_reason)
                
                if email_reason != None:
                    list_reason.append(email_reason)
                
                if corporate_name_reason != None:
                    list_reason.append(corporate_name_reason)

                if corporate_code_reason != None:
                    list_reason.append(corporate_code_reason)

                if parent_company_reason != None:
                    list_reason.append(parent_company_reason)

                if spoke_person_reason != None:
                    list_reason.append(spoke_person_reason)
                
                if industry_reason != None:
                    list_reason.append(industry_reason)

                if billing_reason != None:
                    list_reason.append(billing_reason)

                if level1_reason != None:
                    list_reason.append(level1_reason)
                
                if level2_reason != None:
                    list_reason.append(level2_reason)
                
                if pan_card_reason != None:
                    list_reason.append(pan_card_reason)
                
                if GST_no_reason != None:
                    list_reason.append(GST_no_reason)
                
                if billing_email_reason != None:
                    list_reason.append(billing_email_reason)

                if pincode_reason != None:
                    list_reason.append(pincode_reason)

                
                
                final_reason = ', '.join(map(str, list_reason)) 

                # print(final_reason, 'fdinal reason check ')
                if final_reason == '':
                    row_status = 'Valid'
                    start_color="3d7d13" 
                    end_color="3d7d13"
                else:
                    row_status = 'Invalid'
                    start_color="e39830"
                    end_color="e39830"


                get_new_cell = str(letters[22]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(row_status)
                cell_new_bg.fill = PatternFill(start_color=start_color, end_color=end_color,fill_type = "solid")
                new_workbook.save(new_file_path)


                get_new_cell = str(letters[23]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(final_reason)  
                new_workbook.save(new_file_path)


            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'
            link = SITE_MEDIA_BASE_URL + new_filename

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
              
        elif flag == 'Vendor':
            try:
                fs = FileSystemStorage()
                fs.delete('vendor_details.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('vendor_details.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0

            new_filename = 'vendor_details_data.xlsx'
            new_file_url = fs.url(new_filename)
            new_file_path = fs.path(new_filename)  

            wb = load_workbook(new_file_path)
            ws = wb.active
            ws.delete_rows(2, ws.max_row) 
            wb.save(new_file_path)
            
            new_workbook = load_workbook(new_file_path)
            new_sheet = new_workbook.active

            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                if row[0] == None:
                    break
                mobile = None
                if row[1] != None:
                    mobile = '+91 ' + str(row[1])
                
                email = row[2]
                vendor_name = row[3]
                vendor_code = (str(row[4])).upper()
                type_of_service = row[5]
                type_of_visit = row[6]
                billing_cycle = row[7]
                start_date = row[8]
                end_date = row[9]
                GST_no = row[10]
                billing_email = row[11]
                pincode = str(row[12])
                address = row[13]
                state = row[14]
                city = row[15]
                stakeholder_name = row[16]
                stakeholder_mobile = None
                if row[17] != None :
                    stakeholder_mobile =  '+91 ' + str(row[17])
                
                stakeholder_email = row[18]
                contact_person1 = row[19]
                contact_person_designation1 = row[20]
                
                contact_person_mobile1 = None
                if row[21] != None:
                    contact_person_mobile1 = '+91 ' + str(row[21])
                
                contact_person_email1 = row[22]
                contact_person2 = row[23]
                contact_person_designation2 = row[24]
                
                contact_person_mobile2= None
                if row[25] != None:
                    contact_person_mobile2 = '+91 ' + str(row[25])
                
                contact_person_email2 = row[26]
                contact_person3 = row[27]
                contact_person_designation3 = row[28]
                
                contact_person_mobile3= None
                if row[29] != None:
                    contact_person_mobile3 = '+91 ' + str(row[29])
                
                
                contact_person_email3 = row[30]
                login_via = row[31]

                get_new_cell = str(letters[0]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[0]  
                new_workbook.save(new_file_path)
        
                get_new_cell = str(letters[1]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = mobile
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[2]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[2]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[3]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[3]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[4]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[4]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[5]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[5]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[6]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[6]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[7]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[7]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[8]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[8]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[9]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[9]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[10]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[10]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[11]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[11]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[12]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[12]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[13]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[13]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[14]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[14]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[15]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[15]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[16]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[16]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[17]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = stakeholder_mobile
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[18]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[18]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[19]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[19]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[20]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[20]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[21]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = contact_person_mobile1
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[22]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[22]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[23]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[23]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[24]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[24]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[25]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = contact_person_mobile2 
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[26]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[26]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[27]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[27]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[28]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[28]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[29]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = contact_person_mobile3
                new_workbook.save(new_file_path)

                get_new_cell = str(letters[30]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[30]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[31]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[31]  
                new_workbook.save(new_file_path)

                mobile_reason = None
                if len(mobile) == 14:
                    check_mobile = models.VendorDetail.objects.filter(mobile = mobile).count()
                    if check_mobile != 0:
                        get_cell = str(letters[1]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        mobile_reason = 'Enter Mobile Number already Registerd'
                        invalid_count += 1
                else:
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    mobile_reason = 'Enter 10-digit Mobile Number'
                    invalid_count += 1

                

                email_reason = None
                if "@" in email and "." in email.split("@")[-1]:
                
                    check_email = models.VendorDetail.objects.filter(email = email).count()
                    if check_email != 0:
                        get_cell = str(letters[2]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        email_reason = 'Enter Email already Registerd'
                        invalid_count += 1
                else:
                    get_cell = str(letters[2]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    email_reason = 'Enter Valid Email'
                    invalid_count += 1

                vendor_name_reason = None
                vendor_name_count = 0 
                for char in vendor_name:
                    if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                        # print(char, 'chr')
                        vendor_name_count += 1
                
                if vendor_name_count != 0:
                    get_cell = str(letters[3]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    vendor_name_reason = 'Enter alphanumeric character only'
                    invalid_count += 1

                billing_email_reason = None
                if billing_email == None:
                    get_cell = str(letters[11]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    billing_email_reason = 'Enter Billing Email'
                    invalid_count += 1
                else:
                    if not "@" in billing_email and "." in billing_email.split("@")[-1]:
                        get_cell = str(letters[11]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        billing_email_reason = 'Enter Valid Email'
                        invalid_count += 1

                vendor_code_reason = None
                check_vendor_code = models.VendorDetail.objects.filter(vendor_code = vendor_code).count()
                if check_vendor_code != 0:
                    get_cell = str(letters[4]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    vendor_code_reason = 'Enter Vendor Code already registerd'
                    invalid_count += 1
                
                type_service_reason = None
                if type_of_service != None:
                    list_type_of_service = type_of_service.split(',')
                    list_data = []
                    for data in list_type_of_service:
                        list_data.append(data.strip()) 

                    service_count = 0
                    for service in list_data:
                        check_service = models.TypeOfService.objects.filter(type_of_service = service).count()
                        if check_service != 1:
                            service_count += 1

                    if service_count != 0:
                        get_cell = str(letters[5]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        type_service_reason = 'Enter Valid Type of Service'
                        invalid_count += 1

                type_visit_reason = None
                check_type_of_visit = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).count()
                if check_type_of_visit == 0:
                    get_cell = str(letters[6]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    type_visit_reason = 'Enter Valid Type of Visit'
                    invalid_count += 1
                
                billing_reason = None
                check_billing_cycle = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).count()
                if check_billing_cycle == 0:
                    get_cell = str(letters[7]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    billing_reason = 'Enter Valid Billing Cycle'
                    invalid_count += 1

                pincode_reason = None
                pincode_count = 0 
                if len(pincode) == 6:
                    for char in pincode:
                        if char not in "0123456789":
                            pincode_count += 1
                    
                    if pincode_count != 0:
                        get_cell = str(letters[12]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        pincode_reason = 'Enter Numeric Code only'
                        invalid_count += 1
                else:
                    get_cell = str(letters[12]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    pincode_reason = 'Enter Valid Pin Code'
                    invalid_count += 1

                                
                GST_no_reason = None
                if not re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$', GST_no):
                    get_cell = str(letters[10]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    GST_no_reason = 'Enter Valid GST No'
                    invalid_count += 1
                
                stakeholder_name_reason = None
                stakeholder_name_count = 0 
                for char in stakeholder_name:
                    if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                        # print(char, 'chr')
                        stakeholder_name_count += 1
                
                if stakeholder_name_count != 0:
                    get_cell = str(letters[16]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    stakeholder_name_reason = 'Enter alphanumeric character only'
                    invalid_count += 1

                stakeholder_mobile_reason = None
                if len(stakeholder_mobile) != 14:
                    get_cell = str(letters[17]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    stakeholder_mobile_reason = 'Enter 10-digit Mobile Number'
                    invalid_count += 1

                stakeholder_email_reason = None
                if not "@" in stakeholder_email and "." in stakeholder_email.split("@")[-1]:
                    get_cell = str(letters[18]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    stakeholder_email_reason = 'Enter Valid Stakeholder Email'
                    invalid_count += 1
            
                
                contact_person1_reason = None
                contact_person1_count = 0 
                # print(contact_person1, 'contact_person1')
                if contact_person1 != None:
                    for char in contact_person1:
                        if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                            # print(char, 'chr')
                            contact_person1_count += 1
                    
                    if contact_person1_count != 0:
                        get_cell = str(letters[19]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        contact_person1_reason = 'Enter alphanumeric character only in first contact person'
                        invalid_count += 1
                else:
                    get_cell = str(letters[19]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    contact_person1_reason = 'Enter first contact person Name'
                    invalid_count += 1

                    
                contact_person_mobile1_reason = None
                if contact_person_mobile1 != None:
                    if len(contact_person_mobile1) != 14:
                        get_cell = str(letters[21]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        contact_person_mobile1_reason = 'Enter First contact person 10-digit Mobile Number'
                        invalid_count += 1
                else:
                    get_cell = str(letters[21]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    contact_person_mobile1_reason = 'Enter First contact person Mobile Number'
                    invalid_count += 1


                contact_person_email1_reason = None
                if contact_person_email1 != None:
                    if not "@" in contact_person_email1 and "." in contact_person_email1.split("@")[-1]:
                        get_cell = str(letters[22]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        contact_person_email1_reason = 'Enter Valid First Contact Person Email'
                        invalid_count += 1
                else:
                    get_cell = str(letters[22]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    contact_person_email1_reason = 'Enter First Contact Person Email'
                    invalid_count += 1


                
                contact_person2_reason = None
                if contact_person2 != None:
                    contact_person2_count = 0 
                    for char in contact_person2:
                        if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                            # print(char, 'chr')
                            contact_person2_count += 1
                    
                    if contact_person2_count != 0:
                        get_cell = str(letters[23]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        contact_person2_reason = 'Enter alphanumeric character only in Second contact person'
                        invalid_count += 1

                contact_person_mobile2_reason = None
                if contact_person_mobile2 != None:
                    if len(contact_person_mobile2) != 14:
                        get_cell = str(letters[25]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        contact_person_mobile2_reason = 'Enter Second contact person 10-digit Mobile Number'
                        invalid_count += 1

                contact_person_email2_reason = None
                # print(contact_person_email2, 'contact_person_email2')
                if contact_person_email2 != None:
                    if not "@" in contact_person_email2 and "." in contact_person_email2.split("@")[-1]:
                        get_cell = str(letters[26]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        contact_person_email2_reason = 'Enter Valid Second Contact Person Email'
                        invalid_count += 1

                 
                contact_person3_reason = None
                if contact_person3 != None:
                    contact_person3_count = 0 
                    for char in contact_person3:
                        if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                            # print(char, 'chr')
                            contact_person3_count += 1
                    
                    if contact_person3_count != 0:
                        get_cell = str(letters[27]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        contact_person3_reason = 'Enter alphanumeric character only in Third contact person'
                        invalid_count += 1

                contact_person_mobile3_reason = None
                if contact_person_mobile3 != None:
                    if len(contact_person_mobile3) != 14:
                        get_cell = str(letters[29]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        contact_person_mobile3_reason = 'Enter Third contact person 10-digit Mobile Number'
                        invalid_count += 1

                contact_person_email3_reason = None
                # print(contact_person_email3, 'contact_person_email3')
                if contact_person_email3 != None:
                    if not "@" in contact_person_email3 and "." in contact_person_email3.split("@")[-1]:
                        get_cell = str(letters[30]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        contact_person_email3_reason = 'Enter Valid Third Contact Person Email'
                        invalid_count += 1


                list_reason = []
                if mobile_reason != None:
                    list_reason.append(mobile_reason)
                
                if email_reason != None:
                    list_reason.append(email_reason)

                if vendor_name_reason != None:
                    list_reason.append(vendor_name_reason) 
                
                if vendor_code_reason != None:
                    list_reason.append(vendor_code_reason)

                if type_service_reason != None:
                    list_reason.append(type_service_reason)

                if type_visit_reason != None:
                    list_reason.append(type_visit_reason)

                if billing_reason != None:
                    list_reason.append(billing_reason)
                
                if billing_email_reason != None:
                    list_reason.append(billing_email_reason)
                    
                if pincode_reason != None:
                    list_reason.append(pincode_reason)

                if GST_no_reason != None:
                    list_reason.append(GST_no_reason)

                if stakeholder_name_reason != None:
                    list_reason.append(stakeholder_name_reason)
                    
                if stakeholder_mobile_reason != None:
                    list_reason.append(stakeholder_mobile_reason)

                if stakeholder_email_reason != None:
                    list_reason.append(stakeholder_email_reason)

                if contact_person1_reason != None:
                    list_reason.append(contact_person1_reason)
                    
                if contact_person_mobile1_reason != None:
                    list_reason.append(contact_person_mobile1_reason)

                if contact_person_email1_reason != None:
                    list_reason.append(contact_person_email1_reason)

                if contact_person2_reason != None:
                    list_reason.append(contact_person2_reason)
                    
                if contact_person_mobile2_reason != None:
                    list_reason.append(contact_person_mobile2_reason)

                if contact_person_email2_reason != None:
                    list_reason.append(contact_person_email2_reason)

                if contact_person3_reason != None:
                    list_reason.append(contact_person3_reason)
                    
                if contact_person_mobile3_reason != None:
                    list_reason.append(contact_person_mobile3_reason)

                if contact_person_email3_reason != None:
                    list_reason.append(contact_person_email3_reason)







                
                final_reason = ', '.join(map(str, list_reason)) 

                # print(final_reason, 'fdinal reason check ')
                if final_reason == '':
                    row_status = 'Valid'
                    start_color="3d7d13" 
                    end_color="3d7d13"
                else:
                    row_status = 'Invalid'
                    start_color="e39830"
                    end_color="e39830"


                get_new_cell = str(letters[32]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(row_status)
                cell_new_bg.fill = PatternFill(start_color=start_color, end_color=end_color,fill_type = "solid")
                new_workbook.save(new_file_path)


                get_new_cell = str(letters[33]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(final_reason)  
                new_workbook.save(new_file_path)


            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'
            
            # print(invalid_count, 'invalid_count')
            link = SITE_MEDIA_BASE_URL + new_filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Package':
            try:
                fs = FileSystemStorage()
                fs.delete('package_details.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('package_details.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0

            new_filename = 'package_details_data.xlsx'
            new_file_url = fs.url(new_filename)
            new_file_path = fs.path(new_filename)  

            wb = load_workbook(new_file_path)
            ws = wb.active
            ws.delete_rows(2, ws.max_row) 
            wb.save(new_file_path)
            
            new_workbook = load_workbook(new_file_path)
            new_sheet = new_workbook.active

            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                # print(row_index,'-->', row)
                if row_index == 1:
                    continue

                if row[0] == None:
                    break
                
                
                # print(row_index, row, 'data')
                package_type = row[1]
                package_name = row[2]
                package_code = (str(row[3])).upper()
                description = row[4]
                type_of_service = row[5]
                vendor = row[6]

                relation_with_employee = row[7]
                age_category = row[8]
                gender = row[9]
                corporate = row[10]
                type_of_visit = row[11]
                billing_cycle = row[12]
                tags = row[13]

                MRP = row[14]
                base_amount = row[15]
                profit = row[16]
                tax = row[17]
                discount_price = row[18]
                offer_price = row[19]
                start_date = (str(row[20])).replace(" 00:00:00","")
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                
                
                end_date = (str(row[21])).replace(" 00:00:00","")
                end_date =  datetime.strptime(end_date, "%Y-%m-%d").date()
                
                

                get_new_cell = str(letters[0]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[0]  
                new_workbook.save(new_file_path)
        
                get_new_cell = str(letters[1]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[1]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[2]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[2]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[3]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[3]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[4]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[4]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[5]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[5]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[6]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[6]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[7]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[7]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[8]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[8]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[9]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[9]  
                new_workbook.save(new_file_path)
                
                if package_type == 'Corporate':
                    get_new_cell = str(letters[10]) + str(row_index)
                    cell_new_bg = new_sheet[get_new_cell]
                    new_sheet[get_new_cell].value = row[10]  
                    new_workbook.save(new_file_path)
                    
                get_new_cell = str(letters[11]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[11]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[12]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[12]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[13]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[13]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[14]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[14]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[15]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[15]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[16]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[16]  
                new_workbook.save(new_file_path)

                get_new_cell = str(letters[17]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(row[17])  
                new_workbook.save(new_file_path)

                if discount_price == None:
                    get_new_cell = str(letters[18]) + str(row_index)
                    cell_new_bg = new_sheet[get_new_cell]
                    new_sheet[get_new_cell].value = '-'
                    new_workbook.save(new_file_path)
                else:
                    get_new_cell = str(letters[18]) + str(row_index)
                    cell_new_bg = new_sheet[get_new_cell]
                    new_sheet[get_new_cell].value = row[18]  
                    new_workbook.save(new_file_path)
                
                if offer_price == None:
                    get_new_cell = str(letters[19]) + str(row_index)
                    cell_new_bg = new_sheet[get_new_cell]
                    new_sheet[get_new_cell].value = '-'
                    new_workbook.save(new_file_path)
                else:
                    get_new_cell = str(letters[19]) + str(row_index)
                    cell_new_bg = new_sheet[get_new_cell]
                    new_sheet[get_new_cell].value = row[19]  
                    new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[20]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = start_date
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[21]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = end_date  
                new_workbook.save(new_file_path)
                
                package_type_reason = None
                if package_type not in ['Corporate', 'Individual']:
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    package_type_reason = 'Package Type only accept Individual or Corporate'
                    invalid_count += 1
                
                
                package_code_reason = None
                check_package_code = models.PackageDetail.objects.filter(package_code = package_code).count()
                if check_package_code != 0:
                    get_cell = str(letters[3]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    package_code_reason = 'Enter Package Code already Registerd'
                    invalid_count += 1

                type_service_reason = None
                check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                if check_type_of_service != 1:
                    get_cell = str(letters[5]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    type_service_reason = 'Enter Valid Type of Service'
                    invalid_count += 1
                
                vendor_reason = None
                check_vendor = models.VendorDetail.objects.filter(vendor_code = vendor).count()
                if check_vendor != 1:
                    get_cell = str(letters[6]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    vendor_reason = 'Enter Valid Vendor Code'
                    invalid_count += 1
                else:
                    check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                    if check_type_of_service == 1:
                        check_type_of_visit = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).count()
                        if check_type_of_visit == 1:
                            get_id = models.TypeOfService.objects.filter(type_of_service = type_of_service).values_list('id', flat=True)[0]
                            get_type_of_visit = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).values_list('id', flat=True)[0]    
                            check_vendor_service = models.VendorDetail.objects.filter((Q(type_of_visit= get_type_of_visit) | Q(type_of_visit__type_of_visit ='Hybrid')), vendor_code = vendor, type_of_service= get_id).count()
                            # check_vendor_service = models.VendorDetail.objects.filter(
                            #     Q(vendor_code=vendor) &
                            #     (Q(type_of_visit=get_type_of_visit) | Q(type_of_visit__type_of_visit='Hybrid')) &
                            #     Q(type_of_service=get_id)
                            # ).count()
                            # print(check_vendor, 'adfas')
                            if check_vendor_service != 1:
                                get_cell = str(letters[6]) + str(row_index)
                                cell_bg = new_sheet[get_cell]
                                cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                                new_workbook.save(new_file_path)
                                vendor_reason = 'Enter type of service/type of visit is not assign to vendor'

                                invalid_count += 1
                        else:
                            get_cell = str(letters[6]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            vendor_reason = 'Enter Valid type of Visit'
                            invalid_count += 1

                    else:
                        get_cell = str(letters[6]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        vendor_reason = 'Enter Valid type of service'
                        invalid_count += 1

                relation_reason = None
                if relation_with_employee != None:
                    list_relation = relation_with_employee.split(',')
                    list_data = []
                    for data in list_relation:
                        list_data.append(data.strip()) 

                    relation_count = 0
                    for relation in list_data:
                        check_relation = models.Relation.objects.filter(relation = relation).count()
                        if check_relation != 1:
                            relation_count += 1

                    if relation_count != 0:
                        get_cell = str(letters[7]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        relation_reason = 'Enter Valid Relation'
                        invalid_count += 1

                corporate_reason = None
                if package_type == 'Corporate':
                    if corporate != None:
                        list_corporate = corporate.split(',')
                        list_corporate_data = []
                        for data in list_corporate:
                            list_corporate_data.append(data.strip()) 

                        corporate_count = 0
                        # print(list_corporate_data, 'list_corporate_data')
                        for corporate in list_corporate_data:
                            check_corporate = models.CorporateDetail.objects.filter(corporate_code = corporate).count()
                            # print(check_corporate, 'check_corporate')
                            if check_corporate != 1:
                                corporate_count += 1

                        if corporate_count != 0:
                            get_cell = str(letters[10]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            corporate_reason = 'Enter Valid Corporate'
                            invalid_count += 1

                type_visit_reason = None
                check_type_of_visit = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).count()
                if check_type_of_visit == 0:
                    get_cell = str(letters[11]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    type_visit_reason = 'Enter Valid Type of Visit'
                    invalid_count += 1
            
                age_category_reason = None
                check_age_category = models.AgeCategory.objects.filter(age_category = age_category).count()
                if check_age_category == 0:
                    get_cell = str(letters[8]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    age_category_reason = 'Enter Valid Age Category'
                    invalid_count += 1
                
                gender_reason = None
                check_gender = models.Gender.objects.filter(gender = gender).count()
                if check_gender == 0:
                    get_cell = str(letters[9]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    gender_reason = 'Enter Valid Gender'
                    invalid_count += 1

                billing_reason = None
                check_billing_cycle = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).count()
                if check_billing_cycle == 0:
                    get_cell = str(letters[12]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    billing_reason = 'Enter Valid Billing Cycle'
                    invalid_count += 1
                
                tag_reason = None
                check_tags = models.PaymentTags.objects.filter(payment_tags = tags, status = 'Active').count()
                if check_tags == 0:
                    get_cell = str(letters[13]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    tag_reason = 'Enter Valid Payment Tags'
                    invalid_count += 1
                else:
                    if package_type == 'Individual':
                        if tags != 'Self Pay':
                            get_cell = str(letters[13]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            tag_reason = 'Individual package type only support Self Pay'
                            invalid_count += 1
                
                MRP_reason = None
                if MRP == None:
                    invalid_count += 1
                    MRP_reason = 'Enter MRP'
                elif MRP == int(0):
                    get_cell = str(letters[14]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    invalid_count += 1        
                    MRP_reason = 'Enter more than 0 MRP'
                else:
                    s = str(MRP)
                    if not (s.lstrip('-').isdigit()) and not(s.count('.') == 1 and s.replace('.', '', 1).lstrip('-').isdigit()):
                        get_cell = str(letters[14]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        
                        MRP_reason = 'MRP should be in numeric only'
                        invalid_count += 1
                    else:
                        print("Valid number")
                
                base_amount_reason = None
                if base_amount == None:
                    invalid_count += 1
                    base_amount_reason = 'Enter Base Amount'
                elif base_amount == int(0):
                    get_cell = str(letters[15]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    invalid_count += 1
                    base_amount_reason = 'Enter more than 0 Base amount'
                else:
                    s = str(base_amount)
                    if not (s.lstrip('-').isdigit()) and not(s.count('.') == 1 and s.replace('.', '', 1).lstrip('-').isdigit()):
                        get_cell = str(letters[15]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        invalid_count += 1
                        base_amount_reason = 'Base Amount should be in numeric only'


                profit_reason = None
                if profit == None:
                    invalid_count += 1
                    profit_reason = 'Enter Profit Amount'
                else:
                    s = str(profit)
                    if not (s.lstrip('-').isdigit()) and not(s.count('.') == 1 and s.replace('.', '', 1).lstrip('-').isdigit()):
                        get_cell = str(letters[16]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        invalid_count += 1
                        profit_reason = 'Profit Amount should be in numeric only'
                

                list_reason = []
                if package_type_reason != None:
                    list_reason.append(package_type_reason)
                
                if package_code_reason != None:
                    list_reason.append(package_code_reason)
                
                if type_service_reason != None:
                    list_reason.append(type_service_reason)
                
                if vendor_reason != None:
                    list_reason.append(vendor_reason)

                if relation_reason != None:
                    list_reason.append(relation_reason)

                if corporate_reason != None:
                    list_reason.append(corporate_reason)

                if type_visit_reason != None:
                    list_reason.append(type_visit_reason)
                
                if age_category_reason != None:
                    list_reason.append(age_category_reason)

                if gender_reason != None:
                    list_reason.append(gender_reason)

                if billing_reason != None:
                    list_reason.append(billing_reason)

                if tag_reason != None:
                    list_reason.append(tag_reason)

                if MRP_reason != None:
                    list_reason.append(MRP_reason)

                if base_amount_reason != None:
                    list_reason.append(base_amount_reason)
                
                if profit_reason != None:
                    list_reason.append(profit_reason)
                

                
                final_reason = ', '.join(map(str, list_reason)) 
                if final_reason == '':
                    row_status = 'Valid'
                    start_color="3d7d13" 
                    end_color="3d7d13"
                else:
                    row_status = 'Invalid'
                    start_color="e39830"
                    end_color="e39830"

                get_new_cell = str(letters[22]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(row_status)
                cell_new_bg.fill = PatternFill(start_color=start_color, end_color=end_color,fill_type = "solid")
                new_workbook.save(new_file_path)


                get_new_cell = str(letters[23]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(final_reason)  
                new_workbook.save(new_file_path)


            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + new_filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Employee':
            try:
                fs = FileSystemStorage()
                fs.delete('employee_details.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('employee_details.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0

            new_filename = 'employee_details_data.xlsx'
            new_file_url = fs.url(new_filename)
            new_file_path = fs.path(new_filename)  

            wb = load_workbook(new_file_path)
            ws = wb.active
            ws.delete_rows(2, ws.max_row) 
            wb.save(new_file_path)
            
            new_workbook = load_workbook(new_file_path)
            new_sheet = new_workbook.active

            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                if row[0] == None:
                    break

                mobile = '+91 ' + str(row[1])
                email = row[2]
                employee_name = row[3]
                employee_code = (str(row[4])).upper()
                relation = row[5]
                corporate = row[6]
                department = row[7]
                gender = row[8]
                date_of_join = (str(row[9])).replace(" 00:00:00","")
                date_of_birth = (str(row[10])).replace(" 00:00:00","")
                # print(date_of_birth, date_of_join)
                hr_employee = row[11]
                hr_corporate_code = row[12]
                address = row[13]
                pincode = str(row[14])
                state = row[15]
                city = row[16]

                get_new_cell = str(letters[0]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[0]  
                new_workbook.save(new_file_path)
        
                get_new_cell = str(letters[1]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = '+91 ' + str(row[1])  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[2]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[2]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[3]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[3]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[4]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[4]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[5]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[5]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[6]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[6]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[7]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[7]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[8]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[8]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[9]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[9]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[10]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[10]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[11]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[11]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[12]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[12]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[13]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[13]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[14]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[14]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[15]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[15]  
                new_workbook.save(new_file_path)

                get_new_cell = str(letters[16]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[16]  
                new_workbook.save(new_file_path)

                relation_reason = None
                check_relation = models.Relation.objects.filter(relation = relation).count()
                # print(check_relation, 'check_relation')
                if check_relation == 0:
                    get_cell = str(letters[5]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    relation_reason = 'Enter Valid Relation'
                    invalid_count += 1
                    
                    mobile_reason = None
                    email_reason = None
                    employee_code_reason = None
                    gender_reason = None
                    corporate_code_reason = None
                    employee_name_reason = None
                    hr_employee_reason = None
                    birthday_reason = None



                if check_relation == 1:
                    relation = models.Relation.objects.filter(relation = relation).values_list('relation', flat=True)[0]
                    if relation == 'Self':
                        
                        mobile_reason = None
                        if len(mobile) == 14:
                            check_mobile = models.EmployeeDetail.objects.filter(mobile = mobile).count()
                            if check_mobile != 0:
                                get_cell = str(letters[1]) + str(row_index)
                                cell_bg = new_sheet[get_cell]
                                cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                                new_workbook.save(new_file_path)
                                mobile_reason = 'Enter Mobile Number already Registerd'
                                invalid_count += 1
                        else:
                            get_cell = str(letters[1]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            mobile_reason = 'Enter 10-digit Mobile Number'
                            invalid_count += 1


                        email_reason = None
                        if "@" in email and "." in email.split("@")[-1]:
                            check_email = models.EmployeeDetail.objects.filter(email = email).count()
                            if check_email != 0:
                                get_cell = str(letters[2]) + str(row_index)
                                cell_bg = new_sheet[get_cell]
                                cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                                new_workbook.save(new_file_path)
                                email_reason = 'Enter Email already Registerd'
                                invalid_count += 1
                        else:
                            get_cell = str(letters[2]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            email_reason = 'Enter Valid Email'
                            invalid_count += 1

                        employee_name_reason = None
                    
                        employee_name_count = 0 
                        for char in employee_name:
                            if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                                employee_name_count += 1
                        
                        if employee_name_count != 0:
                            get_cell = str(letters[3]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            employee_name_reason = 'Enter alphanumeric character only'
                            invalid_count += 1

                        employee_code_reason = None
                        check_employee_code = models.EmployeeDetail.objects.filter(employee_code = employee_code).count()
                        if check_employee_code != 0:
                            get_cell = str(letters[4]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            employee_code_reason = 'Enter Employee Code already Registerd'
                            invalid_count += 1

                        gender_reason = None
                        check_gender = models.Gender.objects.filter(gender = gender).count()
                        if check_gender == 0:
                            get_cell = str(letters[8]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            gender_reason = 'Enter Valid Gender'
                            invalid_count += 1
                        
                        corporate_code_reason = None
                        check_corporate = models.CorporateDetail.objects.filter(corporate_code = corporate).count()
                        if check_corporate == 0:
                            get_cell = str(letters[6]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            corporate_code_reason = 'Enter Valid Corporate Code'
                            invalid_count += 1

                        birthday_reason = None
                        today = date.today()
                        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
                        year_difference = today.year - date_of_birth.year
                        if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
                            year_difference -= 1
                        if year_difference < 18:
                            get_cell = str(letters[10]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            invalid_count += 1
                            birthday_reason = 'Employee Age Should be above 18'
                        
                        hr_employee_reason = None
                        hr_employee_count = 0 
                        for char in hr_employee:
                            if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
                                hr_employee_count += 1
                        
                        if hr_employee_count != 0:
                            get_cell = str(letters[11]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            name_reason = 'Enter alphanumeric character only'
                            invalid_count += 1

                        pincode_reason = None
                        pincode_count = 0 
                        if len(pincode) == 6:
                            for char in pincode:
                                if char not in "0123456789":
                                    pincode_count += 1
                            
                            if pincode_count != 0:
                                get_cell = str(letters[14]) + str(row_index)
                                cell_bg = new_sheet[get_cell]
                                cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                                new_workbook.save(new_file_path)
                                pincode_reason = 'Enter Numeric Code only'
                                invalid_count += 1
                        else:
                            get_cell = str(letters[14]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            pincode_reason = 'Enter Valid Pin Code'
                            invalid_count += 1
                            
                    elif relation == 'Child':

                        employee_code_reason = None
                        # print(employee_code, 'employee_code')
                        if employee_code == 'NONE':
                            get_cell = str(letters[4]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            employee_code_reason = 'You need to add Employee Code'
                            invalid_count += 1

                        birthday_reason = None
                        today = date.today()
                        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
                        year_difference = today.year - date_of_birth.year
                        if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
                            year_difference -= 1

                        # print(year_difference, 'year_difference')
                        if year_difference > 0 and year_difference > 25:
                            get_cell = str(letters[10]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            invalid_count += 1
                            birthday_reason = relation +' Age Should be Between 0 to 25'

                        mobile_reason = None
                        email_reason = None
                        relation_reason = None
                        gender_reason = None
                        corporate_code_reason = None
                        # birthday_reason = None
                        employee_name_reason = None
                        pincode_reason = None
                        hr_employee_reason = None
                    
                    elif relation == 'Mother' or relation == 'Mother-In-Law':

                        employee_code_reason = None
                        # print(employee_code, 'employee_code')
                        if employee_code == 'NONE':
                            get_cell = str(letters[4]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            employee_code_reason = 'You need to add Employee Code'
                            invalid_count += 1

                        birthday_reason = None
                        today = date.today()
                        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
                        year_difference = today.year - date_of_birth.year
                        if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
                            year_difference -= 1

                        # print(year_difference, 'year_difference')
                        if year_difference <= 40:
                            get_cell = str(letters[10]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            invalid_count += 1
                            birthday_reason = relation +' Age Should be above 40'


                        mobile_reason = None
                        email_reason = None
                        relation_reason = None
                        gender_reason = None
                        corporate_code_reason = None
                        # birthday_reason = None
                        employee_name_reason = None
                        pincode_reason = None
                        hr_employee_reason = None

                    elif relation == 'Father' or relation == 'Father-In-Law':

                        employee_code_reason = None
                        # print(employee_code, 'employee_code')
                        if employee_code == 'NONE':
                            get_cell = str(letters[4]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            employee_code_reason = 'You need to add Employee Code'
                            invalid_count += 1

                        birthday_reason = None
                        today = date.today()
                        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
                        year_difference = today.year - date_of_birth.year
                        if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
                            year_difference -= 1
                        if year_difference <= 45:
                            get_cell = str(letters[10]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            invalid_count += 1
                            birthday_reason = relation +' Age Should be above 45'


                        mobile_reason = None
                        email_reason = None
                        relation_reason = None
                        gender_reason = None
                        corporate_code_reason = None
                        # birthday_reason = None
                        employee_name_reason = None
                        pincode_reason = None
                        hr_employee_reason = None
                    
                    elif relation == 'Spouse' or relation == 'Partner':

                        employee_code_reason = None
                        # print(employee_code, 'employee_code')
                        if employee_code == 'NONE':
                            get_cell = str(letters[4]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            employee_code_reason = 'You need to add Employee Code'
                            invalid_count += 1

                        birthday_reason = None
                        today = date.today()
                        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
                        year_difference = today.year - date_of_birth.year
                        if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
                            year_difference -= 1
                        if year_difference <= 18:
                            get_cell = str(letters[10]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            invalid_count += 1
                            birthday_reason = relation +' Age Should be above 18'


                        mobile_reason = None
                        email_reason = None
                        relation_reason = None
                        gender_reason = None
                        corporate_code_reason = None
                        # birthday_reason = None
                        employee_name_reason = None
                        pincode_reason = None
                        hr_employee_reason = None

                    else:
                        employee_code_reason = None
                        # print(employee_code, 'employee_code')
                        if employee_code == 'NONE':
                            get_cell = str(letters[4]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            employee_code_reason = 'You need to add Employee Code'
                            invalid_count += 1

                        
                        mobile_reason = None
                        email_reason = None
                        relation_reason = None
                        gender_reason = None
                        corporate_code_reason = None
                        birthday_reason = None
                        employee_name_reason = None
                        pincode_reason = None
                        hr_employee_reason = None
            
                
                list_reason = []
                if relation_reason != None:
                    list_reason.append(relation_reason)

                if mobile_reason != None:
                    list_reason.append(mobile_reason)
                
                if employee_name_reason != None:
                    list_reason.append(employee_name_reason)

                if email_reason != None:
                    list_reason.append(email_reason)
                
                if employee_code_reason != None:
                    list_reason.append(employee_code_reason)
                
                if gender_reason != None:
                    list_reason.append(gender_reason)
                
                if corporate_code_reason != None:
                    list_reason.append(corporate_code_reason)

                if hr_employee_reason != None:
                    list_reason.append(hr_employee_reason)

                if birthday_reason != None:
                    list_reason.append(birthday_reason)

                
                final_reason = ', '.join(map(str, list_reason)) 
                if final_reason == '':
                    row_status = 'Valid'
                    start_color="3d7d13" 
                    end_color="3d7d13"
                else:
                    row_status = 'Invalid'
                    start_color="e39830"
                    end_color="e39830"

                get_new_cell = str(letters[17]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(row_status)
                cell_new_bg.fill = PatternFill(start_color=start_color, end_color=end_color,fill_type = "solid")
                new_workbook.save(new_file_path)


                get_new_cell = str(letters[18]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(final_reason)  
                new_workbook.save(new_file_path)


            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + new_filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
          
        elif flag == 'Center':
            try:
                fs = FileSystemStorage()
                fs.delete('center_details.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('center_details.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0

            new_filename = 'center_details_data.xlsx'
            new_file_url = fs.url(new_filename)
            new_file_path = fs.path(new_filename)  

            wb = load_workbook(new_file_path)
            ws = wb.active
            ws.delete_rows(2, ws.max_row) 
            wb.save(new_file_path)
            
            new_workbook = load_workbook(new_file_path)
            new_sheet = new_workbook.active


            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue
                
                if row[0] == None:
                    break
                print(row_index, 'row_index')
                center_name = row[1]
                vendor = str(row[2])
                vendor_for_package = str(row[2]) 
                package = str(row[3])
                type_of_service = str(row[4])
                type_of_service_for_package = str(row[4])
                address = row[5]
                pincode = str(row[6])
                state = row[7]
                city = row[8]
                location = row[9]
                latitude = row[10]
                longitude = row[11]
                

                get_new_cell = str(letters[0]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[0]  
                new_workbook.save(new_file_path)
        
                get_new_cell = str(letters[1]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[1]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[2]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[2]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[3]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[3]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[4]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[4]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[5]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[5]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[6]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[6]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[7]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[7]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[8]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[8]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[9]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[9]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[10]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[10]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[11]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[11]  
                new_workbook.save(new_file_path)

                check_center_data = models.CenterDetail.objects.filter(center_name= center_name, pincode = pincode).count()
                # print(check_center_data, 'check_center_data')
                if check_center_data == 0 :
                    vendor_reason = None
                    if vendor != None:
                        list_vendor = vendor.split(',')
                        list_data = []
                        for data in list_vendor:
                            list_data.append(data.strip()) 

                        vendor_count = 0
                        for vendor in list_data:
                            check_vendor = models.VendorDetail.objects.filter(vendor_code = vendor).count()
                            if check_vendor != 1:
                                vendor_count += 1

                        if vendor_count != 0:
                            get_cell = str(letters[2]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            vendor_reason = "Enter Valid vendor"
                            invalid_count += 1
                    
                    package_reason = None
                    if package != None:
                        list_package = package.split(',')
                        list_data = []
                        for data in list_package:
                            list_data.append(data.strip()) 

                        # print(vendor_for_package, 'gdsd')
                        list_vendor = vendor_for_package.split(',')
                        list_vendor_data = []
                        for data in list_vendor:
                            list_vendor_data.append(data.strip()) 
                        
                        list_type_of_service = type_of_service_for_package.split(',')
                        list_type_of_service_data = []
                        for data in list_type_of_service:
                            list_type_of_service_data.append(data.strip()) 

                        # print(list_vendor_data, 'fasfas', list_type_of_service_data)
                        package_count = 0
                        list_reason = []
                        for package in list_data:
                            check_package = models.PackageDetail.objects.filter(package_code = package).count()
                            if check_package != 1:
                                package_count += 1
                                package_reason = str(package) + ' package not available.'
                                list_reason.append(package_reason)

                            collect_vendor_code = ""
                            vendor_count = 0
                            if check_package == 1:
                                for vendor in list_vendor_data:
                                    check_vendor = models.PackageDetail.objects.filter(package_code = package, vendor__vendor_code = vendor).count()
                                    collect_vendor_code = vendor
                                    if check_vendor == 1:
                                        vendor_count += 1
                                    
    
                                service_count = 0
                                if vendor_count == 0:
                                    package_reason = str(package) + ' package is not associated with the mentioned vendor.'
                                    list_reason.append(package_reason)

                                elif vendor_count == 1:

                                    for type_of_service in list_type_of_service_data:
                                        check_vendor = models.VendorDetail.objects.filter(vendor_code = collect_vendor_code, type_of_service__type_of_service = type_of_service).count()
                                        # print(check_vendor, 'vendor Coutn')
                                        if check_vendor == 1:
                                            service_count += 1
                        
                                    if service_count == 0:
                                        package_reason = str(collect_vendor_code) + ' vendor is not associated with the mentioned Service.'
                                        list_reason.append(package_reason)
                                
                        
                        if list_reason != []:
                            get_cell = str(letters[3]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            package_reason = list_reason
                            invalid_count += 1
                    
                    type_service_reason = None
                    if type_of_service != None:
                        list_type_of_service = type_of_service.split(',')
                        list_data = []
                        for data in list_type_of_service:
                            list_data.append(data.strip()) 

                        service_count = 0
                        for service in list_data:
                            check_service = models.TypeOfService.objects.filter(type_of_service = service).count()
                            if check_service != 1:
                                service_count += 1

                        if service_count != 0:
                            get_cell = str(letters[4]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            type_service_reason = "Enter Valid Type of Service"
                            invalid_count += 1
                    
                    pincode_reason = None
                    pincode_count = 0 
                    if len(pincode) == 6:
                        for char in pincode:
                            if char not in "0123456789":
                                pincode_count += 1
                        
                        if pincode_count != 0:
                            get_cell = str(letters[6]) + str(row_index)
                            cell_bg = new_sheet[get_cell]
                            cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                            new_workbook.save(new_file_path)
                            pincode_reason = 'Enter Numeric Code only'
                            invalid_count += 1
                    else:
                        get_cell = str(letters[6]) + str(row_index)
                        cell_bg = new_sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        new_workbook.save(new_file_path)
                        pincode_reason = 'Enter Valid Pin Code'
                        invalid_count += 1

                    list_reason = []
                    if vendor_reason != None:
                        list_reason.append(vendor_reason)
                    
                    if package_reason != None:
                        list_reason.append(package_reason)
                    
                    if type_service_reason != None:
                        list_reason.append(type_service_reason)

                    if pincode_reason != None:
                        list_reason.append(pincode_reason)

                else:
                    list_reason = []
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    center_vendor = "This Center with pincode is already registerd."
                    invalid_count += 1
                    list_reason = [center_vendor]

                # print(list_reason, 'list_reason')
                final_reason = ', '.join(map(str, list_reason)) 
                if final_reason == '':
                    row_status = 'Valid'
                    start_color="3d7d13" 
                    end_color="3d7d13"
                else:
                    row_status = 'Invalid'
                    start_color="e39830"
                    end_color="e39830"

                get_new_cell = str(letters[12]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(row_status)
                cell_new_bg.fill = PatternFill(start_color=start_color, end_color=end_color,fill_type = "solid")
                new_workbook.save(new_file_path)


                get_new_cell = str(letters[13]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = str(final_reason)  
                new_workbook.save(new_file_path)


            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + new_filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Holiday':
            try:
                fs = FileSystemStorage()
                fs.delete('holiday_details.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('holiday_details.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0

            new_filename = 'holiday_details_data.xlsx'
            new_file_url = fs.url(new_filename)
            new_file_path = fs.path(new_filename)  

            wb = load_workbook(new_file_path)
            ws = wb.active
            ws.delete_rows(2, ws.max_row) 
            wb.save(new_file_path)
            
            new_workbook = load_workbook(new_file_path)
            new_sheet = new_workbook.active

            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue
                                
                if row[0] == None:
                    break

                center = row[1]
                vendor = row[2]
                type_of_service = row[3]
                holiday = row[4]
                weekly_off = row[5]
                state = row[6]
                city = row[7]
                location = row[8]

                get_new_cell = str(letters[0]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[0]  
                new_workbook.save(new_file_path)
        
                get_new_cell = str(letters[1]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[1]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[2]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[2]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[3]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[3]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[4]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[4]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[5]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[5]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[6]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[6]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[7]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[7]  
                new_workbook.save(new_file_path)
                
                get_new_cell = str(letters[8]) + str(row_index)
                cell_new_bg = new_sheet[get_new_cell]
                new_sheet[get_new_cell].value = row[8]  
                new_workbook.save(new_file_path)
                
                check_center = models.CenterDetail.objects.filter(center_name = center).count()
                if check_center != 1:
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    invalid_count += 1

                check_vendor = models.VendorDetail.objects.filter(vendor_code = vendor).count()
                if check_vendor != 1:
                    get_cell = str(letters[2]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    invalid_count += 1

                check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                if check_type_of_service != 1:
                    get_cell = str(letters[3]) + str(row_index)
                    cell_bg = new_sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    new_workbook.save(new_file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + new_filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')   
        
        elif flag == 'Staff Department':
            try:
                fs = FileSystemStorage()
                fs.delete('staff_department.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('staff_department.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                staff_department = row[0]
                check_staff = models.StaffDepartment.objects.filter(staff_department = staff_department).count()
                if check_staff != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Type Of Access':
            try:
                fs = FileSystemStorage()
                fs.delete('type_of_access.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('type_of_access.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                type_of_access = row[0]
                check_type = models.TypeOfAccess.objects.filter(type_of_access = type_of_access).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Staff Level':
            try:
                fs = FileSystemStorage()
                fs.delete('staff_level.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('staff_level.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                staff_level = row[0]
                check_type = models.StaffLevel.objects.filter(staff_level = staff_level).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Staff Type':
            try:
                fs = FileSystemStorage()
                fs.delete('staff_type.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('staff_type.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                staff_type = row[0]
                check_type = models.StaffType.objects.filter(staff_type = staff_type).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Age Category':
            try:
                fs = FileSystemStorage()
                fs.delete('age_category.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('age_category.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                age_category = row[0]
                check_type = models.AgeCategory.objects.filter(age_category = age_category).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Gender':
            try:
                fs = FileSystemStorage()
                fs.delete('gender.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('gender.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                gender = row[0]
                check_type = models.Gender.objects.filter(gender = gender).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Relation':
            try:
                fs = FileSystemStorage()
                fs.delete('relation.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('relation.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                relation = row[0]
                check_type = models.Relation.objects.filter(relation = relation).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Type of Service':
            try:
                fs = FileSystemStorage()
                fs.delete('type_of_service.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('type_of_service.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                type_of_service = row[0]
                check_type = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Type of Visit':
            try:
                fs = FileSystemStorage()
                fs.delete('type_of_visit.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('type_of_visit.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                type_of_visit = row[0]
                check_type = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Parent Company':
            try:
                fs = FileSystemStorage()
                fs.delete('parent_company.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('parent_company.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                parent_company = row[0]
                check_type = models.ParentCompany.objects.filter(parent_company = parent_company).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Billing Cycle':
            try:
                fs = FileSystemStorage()
                fs.delete('billing_cycle.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('billing_cycle.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                billing_cycle = row[0]
                check_type = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Weekdays':
            try:
                fs = FileSystemStorage()
                fs.delete('weekdays.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('weekdays.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                weekdays = row[0]
                check_type = models.Weekdays.objects.filter(weekdays = weekdays).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Holidays':
            try:
                fs = FileSystemStorage()
                fs.delete('holidays.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('holidays.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                holidays = row[0]
                check_type = models.Holidays.objects.filter(holidays = holidays).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif flag == 'Payment Tags':
            try:
                fs = FileSystemStorage()
                fs.delete('payment_tags.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('payment_tags.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                payment_tags = row[0]
                check_type = models.PaymentTags.objects.filter(payment_tags = payment_tags).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Type of Industry':
            try:
                fs = FileSystemStorage()
                fs.delete('type_of_industries.xlsx')
            except:
                pass
                
            fs = FileSystemStorage()
            filename = fs.save('type_of_industries.xlsx', excel_file)
            file_url = fs.url(filename)
            file_path = fs.path(filename)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                type_of_industry = row[0]
                check_type = models.TypeOfIndustry.objects.filter(type_of_industry = type_of_industry).count()
                if check_type != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'

            link = SITE_MEDIA_BASE_URL + filename
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'File Upload successulfully.',
                "invalid_count":invalid_count,
                "flag":flag,
                "link":link
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
   
        else:
            response_data = {
                "statuscode":406,
                "status":"false",
                'message':"You've Enter wrong flag.",
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def corporate_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        corporate = python_data.get('id')
        check_corporate = models.CorporateDetail.objects.filter(id = corporate).count()
        if check_corporate == 1:
            get_all_employee = models.EmployeeDetail.objects.filter(corporate = corporate)
            for emp in get_all_employee:
                employee = models.EmployeeDetail.objects.get(id = emp.id)
                employee.status = 'Inactive'
                employee.save()
            
            corporate_details = models.CorporateDetail.objects.get(id = corporate)
            corporate_details.status = 'Inactive'
            corporate_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Corporate Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Corporate ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def vendor_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        vendor = python_data.get('id')
        check_vendor = models.VendorDetail.objects.filter(id = vendor).count()
        if check_vendor == 1:
            
            vendor_details = models.VendorDetail.objects.get(id = vendor)
            vendor_details.status = 'Inactive'
            vendor_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Vendor Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Vendor ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def employee_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('id')
        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        if check_employee == 1:
            
            employee_details = models.EmployeeDetail.objects.get(id = employee)
            employee_details.status = 'Inactive'
            employee_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Employee Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Employee ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def bulk_import_submit(request):
    if (request.method == "POST"):
        # python_data={}
        # for i,j in request.FILES.items():
        #     python_data.update({i:j})
        
        # for i,j in request.POST.items():
        #     python_data.update({i:j})
        
        python_data = JSONParser().parse(io.BytesIO(request.body))

        flag = python_data.get('flag')
        link = python_data.get('link')

        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        
        letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',\
                'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ']
            
        
        if flag == 'Staff':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                name = row[1]
                mobile = row[2]
                email = row[3]
                staff_code = (str(row[4])).upper()
                staff_type = row[5]
                staff_level = row[6]
                type_of_access = row[7]
                department = row[8]
                assign_to = row[9]
                
                check_mobile = models.StaffDetail.objects.filter(mobile = mobile).count()
                if check_mobile == 0:
                    mobile_flag = 0
                else:
                    mobile_flag = 1

                
                check_email = models.StaffDetail.objects.filter(email = email).count()
                if check_email == 0:
                    email_flag = 0
                else:
                    email_flag = 1


                check_staff_code = models.StaffDetail.objects.filter(staff_code = staff_code).count()
                if check_staff_code == 0:
                    staff_code_flag = 0
                else:
                    staff_code_flag = 1

                check_staff_type = models.StaffType.objects.filter(staff_type = staff_type).count()
                if check_staff_type == 1:
                    staff_type_id = models.StaffType.objects.filter(staff_type = staff_type).values_list('id', flat=True)[0]
                    staff_type_flag = 1
                else:
                    staff_type_flag = 0

                
                check_staff_level = models.StaffLevel.objects.filter(staff_level = staff_level).count()
                if check_staff_level == 1:
                    staff_level_id = models.StaffLevel.objects.filter(staff_level = staff_level).values_list('id', flat=True)[0]
                    staff_level_flag = 1
                else:
                    staff_level_flag = 0

                staff_access = None
                check_type_of_access = models.TypeOfAccess.objects.filter(type_of_access = type_of_access).count()
                if check_type_of_access == 1:
                    type_of_access_id = models.TypeOfAccess.objects.filter(type_of_access = type_of_access).values_list('id', flat=True)[0]
                    type_of_access_flag = 1
                    if type_of_access == 'Admin':
                        staff_access = 'All Access'
                else:
                    type_of_access_flag = 0

                check_department = models.StaffDepartment.objects.filter(staff_department = department).count()
                if check_department == 1:
                    department_id = models.StaffDepartment.objects.filter(staff_department = department).values_list('id', flat=True)
                    department_flag = 1
                else:
                    department_flag = 0

                if mobile_flag == 0 and email_flag == 0 and staff_code_flag == 0 and staff_type_flag == 1 \
                    and staff_level_flag == 1 and type_of_access_flag == 1 and department_flag == 1:
                    staff_create = models.StaffDetail.objects.create(
                        name = name, 
                        staff_code = staff_code,
                        type_of_access_id = type_of_access_id,
                        staff_type_id = staff_type_id,
                        staff_level_id = staff_level_id,
                        department_id = department_id,
                        staff_access = staff_access,
                        mobile = mobile,
                        assign_to = assign_to,
                        email = email,
                        status = 'Active',
                        created_at = current_time     
                    )
                    staff_create.save()
                    get_staff_id = staff_create.id
                    
                    if type_of_access == 'Super Admin': 
                        get_all_module = models.Module.objects.all()
                        for module in get_all_module:
                            module_id = module.id
                            
                            admin_rights = models.AdminModuleRights.objects.create(
                                module_id = module_id,
                                staff_id = get_staff_id,
                                module_access = 'active',
                                edit_access = 'active',
                                view_access = 'active',
                                delete_access = 'active',
                                created_at = current_time
                            )
                            admin_rights.save()

                    elif type_of_access == 'Admin':
                        get_all_module = models.Module.objects.all()
                        for module in get_all_module:
                            module_id = module.id
                            module_name = module.module
                            if module_name == 'Staff' or module_name == 'Holiday':
                                admin_rights = models.AdminModuleRights.objects.create(
                                    module_id = module_id,
                                    staff_id = get_staff_id,
                                    module_access = 'active',
                                    edit_access = 'inactive',
                                    view_access = 'active',
                                    delete_access = 'inactive',
                                    created_at = current_time
                                )
                                admin_rights.save()
                            else:
                                admin_rights = models.AdminModuleRights.objects.create(
                                    module_id = module_id,
                                    staff_id = get_staff_id,
                                    module_access = 'active',
                                    edit_access = 'active',
                                    view_access = 'active',
                                    delete_access = 'active',
                                    created_at = current_time
                                )
                                admin_rights.save()

                    elif type_of_access == 'Staff':
                        get_all_module = models.Module.objects.all()
                        for module in get_all_module:
                            module_id = module.id
                            module_name = module.module
                            if module_name == 'Corporate' or module_name == 'Appointment' or module_name == 'Employee':
                                admin_rights = models.AdminModuleRights.objects.create(
                                    module_id = module_id,
                                    staff_id = get_staff_id,
                                    module_access = 'active',
                                    edit_access = 'active',
                                    view_access = 'active',
                                    delete_access = 'active',
                                    created_at = current_time
                                )
                                admin_rights.save()
                            else:
                                admin_rights = models.AdminModuleRights.objects.create(
                                    module_id = module_id,
                                    staff_id = get_staff_id,
                                    module_access = 'inactive',
                                    edit_access = 'inactive',
                                    view_access = 'inactive',
                                    delete_access = 'inactive',
                                    created_at = current_time
                                )
                                admin_rights.save()

                else:
                    pass

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Staff Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Corporate':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue
                																		
                mobile = row[1]
                email = row[2]
                corporate_name = row[3]
                corporate_code = (str(row[4])).upper()
                parent_company = row[5]
                type_of_corporation = row[6]
                industry = row[7]
                spoke_person = row[8]
                billing_email = row[9]
                billing_cycle = row[10]
                level1 = row[11]
                level2 = row[12]
                pan_card = row[13]
                GST_no = row[14]
                start_date = row[15]
                end_date = row[16]
                address = row[17]
                pincode = str(row[18])
                state = row[19]
                city = row[20]
                login_via = row[21]
                
                check_mobile = models.CorporateDetail.objects.filter(mobile = mobile).count()
                if check_mobile == 0:
                    mobile_flag = 0
                else:
                    mobile_flag = 1

                
                check_email = models.CorporateDetail.objects.filter(email = email).count()
                
                if check_email == 0:
                    mail_flag = 0
                else:
                    mail_flag = 1

                check_corporate_code = models.CorporateDetail.objects.filter(corporate_code = corporate_code).count()
                if check_corporate_code == 0:
                    corporate_code_flag = 0
                else:
                    corporate_code_flag = 1

                if parent_company != None:
                    check_parent_company = models.ParentCompany.objects.filter(parent_company = parent_company).count()
                    if check_parent_company == 1:
                        parent_company_id = models.ParentCompany.objects.filter(parent_company = parent_company).values_list('id', flat=True)[0]
                        parent_company_flag = 1
                    else:
                        parent_company_flag = 0
                else:
                    parent_company_id = None
                    parent_company_flag = 1

                    
                check_type_of_industry = models.TypeOfIndustry.objects.filter(type_of_industry = industry).count()
                if check_type_of_industry == 1:
                    type_of_industry_id = models.TypeOfIndustry.objects.filter(type_of_industry = industry).values_list('id', flat=True)[0]
                    type_of_industry_flag = 1
                else:
                    type_of_industry_flag = 0
                    
                
                check_billing_cycle = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).count()
                if check_billing_cycle == 1:
                    billing_cycle_id = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).values_list('id', flat=True)[0]
                    billing_cycle_flag = 1
                else:
                    billing_cycle_flag = 0

                  
                # if level1 != None:
                #     check_level1 = models.StaffDetail.objects.filter(staff_code = level1).count()
                #     if check_level1 == 1:
                #         level1_id = models.StaffDetail.objects.filter(staff_code = level1).values_list('id', flat=True)[0]
                #         level1_flag = 1
                #     else:
                #         level1_flag = 0
                # else:
                #     level1_id = None
                #     level1_flag = 0

    
                if level1 != None:
                    list_level1 = level1.split(',')
                    level1_count = 0
                    all_level1_list = []
                
                    list_data = []
                    for data in list_level1:
                        list_data.append(data.strip()) 

                    for level in list_data:
                        get_level_1 = models.StaffLevel.objects.filter(staff_level = 'Level 1').values_list('id', flat=True)[0]
                        check_level1 = models.StaffDetail.objects.filter(staff_code = level, staff_level = get_level_1).count()
                        if check_level1 != 1:
                            level1_count += 1
                        
                        if check_level1 == 1:
                            staff_id = models.StaffDetail.objects.filter(staff_code = level, staff_level = get_level_1).values_list('id', flat=True)[0]
                            all_level1_list.append(staff_id)
                        
                        
                # if level2 != None:
                #     check_level2 = models.StaffDetail.objects.filter(staff_code = level2).count()
                #     if check_level2 == 1:
                #         level2_id = models.StaffDetail.objects.filter(staff_code = level2).values_list('id', flat=True)[0]
                #         level2_flag = 1
                #     else:
                #         level2_flag = 0
                # else:
                #     level2_id = None
                #     level2_flag = 0

                if level2 != None:
                    list_level2 = level2.split(',')
                    level2_count = 0
                    all_level2_list = []

                    list_data = []
                    for data in list_level2:
                        list_data.append(data.strip()) 

                    for level in list_data:
                        get_level_2 = models.StaffLevel.objects.filter(staff_level = 'Level 2').values_list('id', flat=True)[0]
                        check_level2 = models.StaffDetail.objects.filter(staff_code = level, staff_level = get_level_2).count()
                        if check_level2 != 1:
                            level2_count += 1
                        
                        if check_level2 == 1:
                            staff_id = models.StaffDetail.objects.filter(staff_code = level, staff_level = get_level_2).values_list('id', flat=True)[0]
                            all_level2_list.append(staff_id)

                # print(mobile_flag, mail_flag, corporate_code_flag, parent_company_flag, billing_cycle_flag, type_of_industry_flag)
                
                if mobile_flag == 0 and mail_flag == 0 and corporate_code_flag == 0 and parent_company_flag == 1 and \
                    billing_cycle_flag == 1 and type_of_industry_flag == 1 :
                    corporate_create= models.CorporateDetail.objects.create(
                        parent_company_id = parent_company_id,
                        corporate_code = corporate_code,
                        corporate_name = corporate_name,
                        type_of_corporation = type_of_corporation,
                        industry_id = type_of_industry_id,
                        spoke_person = spoke_person,
                        mobile = mobile,
                        email = email,
                        billing_email = billing_email,
                        pan_card = pan_card,
                        GST_no = GST_no,
                        billing_cycle_id =billing_cycle_id,
                        start_date = start_date,
                        end_date = end_date,
                        address = address,
                        pincode = pincode,
                        state = state,
                        city = city,
                        # level1_id = level1_id,
                        # level2_id = level2_id,
                        status = 'Active',
                        login_via = login_via,
                        created_at = current_time
                    )
                    corporate_create.save()

                    
                    if all_level1_list == '':
                        corporate_create.level1.set([])
                    elif type(all_level1_list) == int:
                        corporate_create.level1.set([eval(str(all_level1_list))])
                    else:                        
                        corporate_create.level1.set(all_level1_list)
                    
                    if all_level2_list == '':
                        corporate_create.level2.set([])
                    elif type(all_level2_list) == int:
                        corporate_create.level2.set([eval(str(all_level2_list))])
                    else:
                        corporate_create.level2.set(all_level2_list)
                else:
                    pass
                        
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Corporate Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Vendor':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue
                
                mobile = row[1]
                email = row[2]
                vendor_name = row[3]
                vendor_code = (str(row[4])).upper()
                type_of_service = row[5]
                type_of_visit = row[6]
                billing_cycle = row[7]
                start_date = row[8]
                end_date = row[9]
                GST_no = row[10]
                billing_email = row[11]
                pincode = row[12]
                address = row[13]
                state = row[14]
                city = row[15]
                stakeholder_name = row[16]
                stakeholder_mobile = row[17]
                stakeholder_email = row[18]
                contact_person1 = row[19]
                contact_person_designation1 = row[20]
                contact_person_mobile1 = row[21]
                contact_person_email1 = row[22]
                contact_person2 = row[23]
                contact_person_designation2 = row[24]
                contact_person_mobile2 = row[25]
                contact_person_email2 = row[26]
                contact_person3 = row[27]
                contact_person_designation3 = row[28]
                contact_person_mobile3 = row[29]
                contact_person_email3 = row[30]
                login_via = row[31]
                
                check_mobile = models.VendorDetail.objects.filter(mobile = mobile).count()
                if check_mobile == 0:
                    mobile_flag = 0
                else:
                    mobile_flag = 1

                check_email = models.VendorDetail.objects.filter(email = email).count()
                if check_email == 0:
                    mail_flag = 0
                else:
                    mail_flag = 1

                check_vendor_code = models.VendorDetail.objects.filter(vendor_code = vendor_code).count()
                if check_vendor_code == 0:
                    vendor_flag = 0
                else:
                    vendor_flag = 1


                if type_of_service != None:
                    list_type_of_service = type_of_service.split(',')
                    type_of_service_count = 0
                    all_type_of_service_list = []

                    list_data = []
                    for data in list_type_of_service:
                        list_data.append(data.strip()) 

                    for type_of_service in list_data:
                        check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                        if check_type_of_service != 1:
                            type_of_service_count += 1
                        
                        if check_type_of_service == 1:
                            type_of_service_id = models.TypeOfService.objects.filter(type_of_service = type_of_service).values_list('id', flat=True)[0]

                            all_type_of_service_list.append(type_of_service_id)


                check_type_of_visit = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).count()
                if check_type_of_visit == 1:
                    type_of_visit_id = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).values_list('id', flat=True)[0]
                    type_of_visit_flag = 1
                else:
                    type_of_visit_flag = 0

            
                check_billing_cycle = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).count()
                if check_billing_cycle == 1:
                    billing_cycle_id = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).values_list('id', flat=True)[0]
                    billing_cycle_flag = 1
                else:
                    billing_cycle_flag = 0


                if mobile_flag == 0 and mail_flag == 0 and vendor_flag == 0 and \
                    type_of_visit_flag == 1 and billing_cycle_flag == 1:
                    
                    vendor_create = models.VendorDetail.objects.create(
                        vendor_name = vendor_name,
                        vendor_code = vendor_code,
                        # type_of_service_id = type_of_service_id,
                        type_of_visit_id = type_of_visit_id,
                        billing_cycle_id = billing_cycle_id,
                        GST_no = GST_no,
                        start_date = start_date,
                        end_date = end_date,
                        mobile = mobile,
                        email = email,
                        pincode = pincode,
                        address = address,
                        state = state,
                        city = city,
                        billing_email = billing_email,
                        login_via = login_via,
                        stakeholder_name = stakeholder_name,
                        stakeholder_mobile = stakeholder_mobile,
                        stakeholder_email = stakeholder_email,
                        contact_person1 = contact_person1,
                        contact_person_designation1 = contact_person_designation1,
                        contact_person_mobile1 = contact_person_mobile1,
                        contact_person_email1 = contact_person_email1,
                        contact_person2 = contact_person2,
                        contact_person_designation2 = contact_person_designation2,
                        contact_person_mobile2 = contact_person_mobile2,
                        contact_person_email2 = contact_person_email2,
                        contact_person3 = contact_person3,
                        contact_person_designation3 = contact_person_designation3,
                        contact_person_mobile3 = contact_person_mobile3,
                        contact_person_email3 = contact_person_email3,
                        status = 'Active',
                        created_at = current_time
                    )
                    vendor_create.save()

                    if all_type_of_service_list == '':
                        vendor_create.type_of_service.set([])
                    elif type(all_type_of_service_list) == int:
                        vendor_create.type_of_service.set([eval(str(all_type_of_service_list))])
                    else:                        
                        vendor_create.type_of_service.set(all_type_of_service_list)
                    
                else:
                    print('fad')
                    pass

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Vendor Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Package':

            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue
                										
                        
                package_type = row[1]
                package_name = row[2]
                package_code = (str(row[3])).upper()
                description = row[4]
                type_of_service = row[5]
                vendor = row[6]

                relation_with_employee = row[7]
                age_category = row[8]
                gender = row[9]
                corporate = row[10]
                type_of_visit = row[11]
                billing_cycle = row[12]
                tags = row[13]

                MRP = row[14]
                base_amount = row[15]
                profit = row[16]
                tax = row[17]
                discount_price = row[18]
                offer_price = row[19]
                start_date = row[20]
                end_date = row[21]
                # print(tax, 'adgadg')
                # tax = int(float(tax)/100)
                # # tax = int(tax.replace("%", ""))
                # print(tax, 'fadfad')

                tax_amount = ((base_amount + profit) * float(tax)) / 100

                # print(type(tax_amount), 'tax_amount', tax_amount)
                
                tax_amount = round(float(tax_amount), 2)
                IGST = int(tax)
                IGST_amount = tax_amount
                CGST = int(tax) / 2
                CGST_amount = int(tax_amount) / 2
                SGST = int(tax) / 2
                SGST_amount = int(tax_amount) / 2

                offer_price = base_amount + profit + tax_amount
                # offer_price = format(offer_price, '02d')
                offer_price = round(float(offer_price), 2)

                discount_price =  (MRP - offer_price)
                discount_price = round(discount_price, 2)
                # print(type(offer_price), 'offer_price', type(discount_price))
                # print((offer_price), 'Data check have ', (discount_price))
                
                check_package_code = models.PackageDetail.objects.filter(package_code = package_code).count()
                if check_package_code == 0:
                    package_code_flag = 1
                else:
                    package_code_flag = 0

                relation_data = ''
                if relation_with_employee != None:
                    list_relation = relation_with_employee.split(',')
                    list_data = []
                    for data in list_relation:
                        list_data.append(data.strip()) 

                    relation_data = []
                    relation_count = 0
                    for relation in list_data:
                        relation_id = models.Relation.objects.filter(relation = relation).values_list('id', flat=True)[0]
                        relation_data.append(relation_id)

                corporate_data = ''
                if corporate != None:
                    list_corporate = corporate.split(',')
                    list_data = []
                    for data in list_corporate:
                        list_data.append(data.strip()) 

                    corporate_data = []
                    corporate_count = 0
                    for corporate in list_data:
                        corporate_id = models.CorporateDetail.objects.filter(corporate_code = corporate).values_list('id', flat=True)[0]
                        corporate_data.append(corporate_id)


                vendor_id = models.VendorDetail.objects.filter(vendor_code = vendor).values_list('id', flat=True)[0]
                type_of_service_id = models.TypeOfService.objects.filter(type_of_service = type_of_service).values_list('id', flat=True)[0]
                age_category_id = models.AgeCategory.objects.filter(age_category = age_category).values_list('id', flat=True)[0]
                gender_id = models.Gender.objects.filter(gender = gender).values_list('id', flat=True)[0]
                type_of_visit_id = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).values_list('id', flat=True)[0]
                billing_cycle_id = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).values_list('id', flat=True)[0]
                tags_id = models.PaymentTags.objects.filter(payment_tags = tags).values_list('id', flat=True)[0]

                if package_type == 'Corporate':
                    corporate_selection = 'Select Corporate'
                else:
                    corporate_selection = None

                if package_code_flag == 1: 
                    package_create = models.PackageDetail.objects.create(
                        package_type = package_type,
                        package_name = package_name,
                        package_code = package_code,
                        description = description,
                        type_of_service_id = type_of_service_id,
                        vendor_id = vendor_id,
                        age_category_id = age_category_id,
                        gender_id = gender_id,
                        type_of_visit_id = type_of_visit_id,
                        billing_cycle_id = billing_cycle_id,
                        tags_id = tags_id,
                        corporate_selection = corporate_selection,
                        
                        MRP = MRP,
                        base_amount = base_amount,
                        profit = profit,
                        tax = tax,
                        igst = IGST, 
                        igst_amount = IGST_amount, 
                        sgst = SGST, 
                        sgst_amount = SGST_amount, 
                        cgst = CGST, 
                        cgst_amount = CGST_amount, 
                        tax_amount = tax_amount,
                        discount_price = discount_price,
                        offer_price = offer_price,
                        start_date = start_date,
                        end_date = end_date,
                        status = 'Active',
                        created_at = current_time
                    )
                    package_create.save()
                    
                    if relation_data == '':
                        package_create.relation_with_employee.set([])
                    else:                        
                        package_create.relation_with_employee.set(relation_data)

                    if corporate_data == '':
                        package_create.corporate.set([])
                    else:                        
                        package_create.corporate.set(corporate_data)

                   
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Package Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')

        elif flag == 'Employee':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                mobile = row[1]
                email = row[2]
                employee_name = row[3]
                employee_code = (str(row[4])).upper()
                relation = row[5]
                corporate = row[6]
                department = row[7]
                gender = row[8]
                date_of_join = row[9]
                date_of_birth = row[10]
                hr_employee = row[11]
                hr_corporate_code = row[12]
                address = row[13]
                pincode = row[14]
                state = row[15]
                city = row[16]
                
                if relation == 'Self':
                    check_mobile = models.EmployeeDetail.objects.filter(mobile = mobile).count()
                    if check_mobile == 0:
                        mobile_flag = 0
                    else:
                        mobile_flag = 1

                    
                    check_email = models.EmployeeDetail.objects.filter(email = email).count()
                    if check_email == 0:
                        email_flag = 0
                    else:
                        email_flag = 1


                    check_employee_code = models.EmployeeDetail.objects.filter(employee_code = employee_code).count()
                    if check_employee_code == 0:
                        employee_code_flag = 0
                    else:
                        employee_code_flag = 1

                    check_gender = models.Gender.objects.filter(gender = gender).count()
                    if check_gender == 1:
                        gender_id = models.Gender.objects.filter(gender = gender).values_list('id', flat=True)[0]
                        gender_flag = 1
                    else:
                        gender_flag = 0


                    check_corporate = models.CorporateDetail.objects.filter(corporate_code = corporate).count()
                    if check_corporate == 1:
                        corporate_id = models.CorporateDetail.objects.filter(corporate_code = corporate).values_list('id', flat=True)[0]
                        corporate_flag = 1
                    else:
                        corporate_flag = 0

                    if mobile_flag == 0 and email_flag == 0 and employee_code_flag == 0 and \
                        gender_flag == 1 and corporate_flag == 1:

                        emp = models.EmployeeDetail.objects.create(  
                            corporate_id = corporate_id,
                            employee_name = employee_name,
                            employee_code = employee_code,
                            department = department,
                            date_of_join = date_of_join,
                            date_of_birth = date_of_birth,
                            gender_id = gender_id,
                            mobile = mobile,
                            email = email,
                            hr_employee = hr_employee,
                            hr_corporate_code = hr_corporate_code,
                            address = address,
                            pincode = pincode,
                            state = state,
                            city = city,
                            employee_from = 'Svasthya',
                            status = 'Active',
                            created_at = current_time
                        )
                        emp.save()
                        employee_id = emp.id

                        self_id = models.Relation.objects.filter(relation = 'Self').values_list('id', flat=True)[0]

                        self_create = models.EmployeeDependent.objects.create(
                            employee_id = employee_id,
                            dependent_name = emp.employee_name,
                            dependent_relation_id = self_id, 
                            date_of_birth = emp.date_of_birth,
                            gender_id = emp.gender.id,
                            created_at = current_time
                        ).save()
                else:
                    check_employee_code = models.EmployeeDetail.objects.filter(employee_code =employee_code).count()
                    if check_employee_code == 1:
                        emp = models.EmployeeDetail.objects.get(employee_code = employee_code)
                        employee_id = emp.id
                        relation_id = models.Relation.objects.filter(relation = relation).values_list('id', flat=True)[0]
                        gender_id = models.Gender.objects.filter(gender = gender).values_list('id', flat=True)[0]

                        relation_create = models.EmployeeDependent.objects.create(
                            employee_id = employee_id,
                            dependent_name = employee_name,
                            dependent_relation_id = relation_id, 
                            date_of_birth = date_of_birth,
                            gender_id = gender_id,
                            created_at = current_time
                        ).save()


                    
            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Employee Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')

        elif flag == 'Center':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                center_name = row[1]
                vendor = row[2]
                package = row[3]
                type_of_service = row[4]
                address = row[5]
                pincode = row[6]
                state = row[7]
                city = row[8]
                location = row[9]
                latitude = row[10]
                longitude = row[11]
                
                # check_vendor = models.VendorDetail.objects.filter(vendor_code = vendor).count()
                # if check_vendor == 1:
                #     vendor_id = models.VendorDetail.objects.filter(vendor_code = vendor).values_list('id', flat = True)[0]
                #     vendor_flag = 1
                # else:
                #     vendor_flag = 0

                if vendor != None:
                    list_vendor = vendor.split(',')
                    vendor_count = 0
                    all_vendor_list = []

                    list_data = []
                    for data in list_vendor:
                        list_data.append(data.strip()) 

                    for vendor in list_data:
                        check_vendor = models.VendorDetail.objects.filter(vendor_code = vendor).count()
                        if check_vendor != 1:
                            vendor_count += 1
                        
                        if check_vendor == 1:
                            vendor_id = models.VendorDetail.objects.filter(vendor_code = vendor).values_list('id', flat=True)[0]

                            all_vendor_list.append(vendor_id)
                
                # check_package = models.PackageDetail.objects.filter(package_code = package).count()
                # if check_package == 1:
                #     package_id = models.PackageDetail.objects.filter(package_code = package).values_list('id', flat=True)[0]
                #     package_flag = 1
                # else:
                #     package_flag = 0

                
                if package != None:
                    list_package = package.split(',')
                    package_count = 0
                    all_package_list = []

                    list_data = []
                    for data in list_package:
                        list_data.append(data.strip()) 

                    for package in list_data:
                        check_package = models.PackageDetail.objects.filter(package_code = package).count()
                        if check_package != 1:
                            package_count += 1
                        
                        if check_package == 1:
                            package_id = models.PackageDetail.objects.filter(package_code = package).values_list('id', flat=True)[0]

                            all_package_list.append(package_id)
                

                if type_of_service != None:
                    list_type_of_service = type_of_service.split(',')
                    type_of_service_count = 0
                    all_type_of_service_list = []

                    list_data = []
                    for data in list_type_of_service:
                        list_data.append(data.strip()) 

                    for type_of_service in list_data:
                        check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                        if check_type_of_service != 1:
                            type_of_service_count += 1
                        
                        if check_type_of_service == 1:
                            type_of_service_id = models.TypeOfService.objects.filter(type_of_service = type_of_service).values_list('id', flat=True)[0]

                            all_type_of_service_list.append(type_of_service_id)
                

                # check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                # if check_type_of_service == 1:
                #     type_of_service_id = models.TypeOfService.objects.filter(type_of_service = type_of_service).values_list('id', flat=True)[0]
                #     type_of_service_flag = 1
                # else:
                #     type_of_service_flag = 0

                # print(all_vendor_list, all_package_list, all_type_of_service_list)
                center_create = models.CenterDetail.objects.create(

                    center_name = center_name,
                    address = address,
                    pincode = pincode,
                    state = state,
                    city = city,
                    location = location,
                    # vendor_id = vendor_id,
                    # package_id = package_id,
                    # type_of_service_id = type_of_service_id,
                    latitude = latitude,
                    longitude = longitude,
                    status = 'Active',
                    created_at = current_time
                )
                center_create.save()
                if all_type_of_service_list == '':
                    center_create.type_of_service.set([])
                elif type(all_type_of_service_list) == int:
                    center_create.type_of_service.set([eval(str(all_type_of_service_list))])
                else:                        
                    center_create.type_of_service.set(all_type_of_service_list)

                if all_package_list == '':
                    center_create.package.set([])
                elif type(all_package_list) == int:
                    center_create.package.set([eval(str(all_package_list))])
                else:                        
                    center_create.package.set(all_package_list)
                    
                if all_vendor_list == '':
                    center_create.vendor.set([])
                elif type(all_vendor_list) == int:
                    center_create.vendor.set([eval(str(all_vendor_list))])
                else:                        
                    center_create.vendor.set(all_vendor_list)


            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Center Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Holiday':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                center = row[0]
                vendor = row[1]
                type_of_service = row[2]
                holiday = row[3]
                weekly_off = row[4]
                state = row[5]
                city = row[6]
                location = row[7]
                
                check_center = models.CenterDetail.objects.filter(center_name = center).count()
                if check_center == 1:
                    center_id = models.CenterDetail.objects.filter(center_name = center).values_list('id', flat=True)[0]
                    center_flag = 1
                else:
                    center_flag = 0

                    
                check_vendor = models.VendorDetail.objects.filter(vendor_code = vendor).count()
                if check_vendor == 1:
                    vendor_id = models.VendorDetail.objects.filter(vendor_code = vendor).values_list('id', flat=True)[0]
                    vendor_flag = 1
                else:
                    vendor_flag = 0

                    
                check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                if check_type_of_service == 1:
                    type_of_service_id = models.TypeOfService.objects.filter(type_of_service = type_of_service).values_list('id', flat=True)[0]
                    type_of_service_flag = 1
                else:
                    type_of_service_flag = 0

                if center_flag == 1 and vendor_flag == 1 and type_of_service_flag == 1:
                    holiday_create = models.HolidayDetail.objects.create(
                        vendor_id = vendor_id,
                        center_id = center_id,
                        type_of_service_id = type_of_service_id,
                        state = state,
                        city = city,
                        location = location,
                        weekly_off = weekly_off,
                        holiday = holiday,
                        status = 'Active',
                        created_at = current_time
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Holiday Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Staff Department':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                staff_department = row[0]
                
                
                check_department = models.StaffDepartment.objects.filter(staff_department = staff_department).count()
                if check_department == 1:
                    staff_flag = 1
                else:
                    staff_flag = 0

                    
                if staff_flag == 0:
                    staff_create = models.StaffDepartment.objects.create(
                        staff_department = staff_department,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Staff Department Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Type Of Access':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                type_of_access = row[0]
                
                
                check_department = models.TypeOfAccess.objects.filter(type_of_access = type_of_access).count()
                if check_department == 1:
                    type_of_access_flag = 1
                else:
                    type_of_access_flag = 0

                    
                if type_of_access_flag == 0:
                    type_of_access_create = models.TypeOfAccess.objects.create(
                        type_of_access = type_of_access,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Type Of Access Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Staff Level':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                staff_level = row[0]
                check_department = models.StaffLevel.objects.filter(staff_level = staff_level).count()
                if check_department == 1:
                    staff_level_flag = 1
                else:
                    staff_level_flag = 0

                    
                if staff_level_flag == 0:
                    staff_level_create = models.StaffLevel.objects.create(
                        staff_level = staff_level,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Staff Level Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Staff Type':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                staff_type = row[0]
                check_department = models.StaffType.objects.filter(staff_type = staff_type).count()
                if check_department == 1:
                    staff_type_flag = 1
                else:
                    staff_type_flag = 0

                    
                if staff_type_flag == 0:
                    staff_type_create = models.StaffType.objects.create(
                        staff_type = staff_type,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Staff Type Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Age Category':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                age_category = row[0]
                check_department = models.AgeCategory.objects.filter(age_category = age_category).count()
                if check_department == 1:
                    age_category_flag = 1
                else:
                    age_category_flag = 0

                    
                if age_category_flag == 0:
                    age_category_create = models.AgeCategory.objects.create(
                        age_category = age_category,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Age Category Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Gender':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                gender = row[0]
                check_department = models.Gender.objects.filter(gender = gender).count()
                if check_department == 1:
                    gender_flag = 1
                else:
                    gender_flag = 0

                    
                if gender_flag == 0:
                    gender_create = models.Gender.objects.create(
                        gender = gender,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Gender Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Relation':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                relation = row[0]
                check_department = models.Relation.objects.filter(relation = relation).count()
                if check_department == 1:
                    relation_flag = 1
                else:
                    relation_flag = 0

                    
                if relation_flag == 0:
                    relation_create = models.Relation.objects.create(
                        relation = relation,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Relation Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Type of Service':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                type_of_service = row[0]
                check_department = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                if check_department == 1:
                    type_of_service_flag = 1
                else:
                    type_of_service_flag = 0

                    
                if type_of_service_flag == 0:
                    type_of_service_create = models.TypeOfService.objects.create(
                        type_of_service = type_of_service,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Type of Service Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Type of Visit':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                type_of_visit = row[0]
                
                
                check_department = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).count()
                if check_department == 1:
                    type_of_visit_flag = 1
                else:
                    type_of_visit_flag = 0

                    
                if type_of_visit_flag == 0:
                    type_of_visit_create = models.TypeOfVisit.objects.create(
                        type_of_visit = type_of_visit,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Type Of Visit Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Parent Company':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                parent_company = row[0]
                check_department = models.ParentCompany.objects.filter(parent_company = parent_company).count()
                if check_department == 1:
                    parent_company_flag = 1
                else:
                    parent_company_flag = 0

                    
                if parent_company_flag == 0:
                    parent_company_create = models.ParentCompany.objects.create(
                        parent_company = parent_company,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Parent Company Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Billing Cycle':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                billing_cycle = row[0]
                check_department = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).count()
                if check_department == 1:
                    billing_cycle_flag = 1
                else:
                    billing_cycle_flag = 0

                    
                if billing_cycle_flag == 0:
                    billing_cycle_create = models.BillingCycle.objects.create(
                        billing_cycle = billing_cycle,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Billing Cycle Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Weekdays':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                weekdays = row[0]
                check_department = models.Weekdays.objects.filter(weekdays = weekdays).count()
                if check_department == 1:
                    weekdays_flag = 1
                else:
                    weekdays_flag = 0

                    
                if weekdays_flag == 0:
                    weekdays_create = models.Weekdays.objects.create(
                        weekdays = weekdays,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Weekdays Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Holidays':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                holidays = row[0]   
                check_department = models.Holidays.objects.filter(holidays = holidays).count()
                if check_department == 1:
                    holidays_flag = 1
                else:
                    holidays_flag = 0

                    
                if holidays_flag == 0:
                    holidays_create = models.Holidays.objects.create(
                        holidays = holidays,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Holidays Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Payment Tags':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                payment_tags = row[0]
                check_department = models.PaymentTags.objects.filter(payment_tags = payment_tags).count()
                if check_department == 1:
                    payment_tags_flag = 1
                else:
                    payment_tags_flag = 0

                    
                if payment_tags_flag == 0:
                    payment_tags_create = models.PaymentTags.objects.create(
                        payment_tags = payment_tags,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Payment Tags Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'Type of Industry':
            fs = FileSystemStorage()
            file_path = fs.path(link)  
            workbook = load_workbook(file_path)
            sheet = workbook.active
            invalid_count = 0
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                type_of_industry = row[0]
                check_department = models.TypeOfIndustry.objects.filter(type_of_industry = type_of_industry).count()
                if check_department == 1:
                    type_of_industry_flag = 1
                else:
                    type_of_industry_flag = 0

                    
                if type_of_industry_flag == 0:
                    payment_tags_create = models.TypeOfIndustry.objects.create(
                        type_of_industry = type_of_industry,
                        status = 'Active'
                    ).save()

            response_data = {
                "statuscode":200,
                "status":"Success",
                'message':'Type of Industry Data submitted successfully.',
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        
        else:
            response_data = {
                "statuscode":406,
                "status":"false",
                'message':"You've Enter wrong flag.",
            }
            json_data = JSONRenderer().render(response_data)
            return HttpResponse(json_data, content_type= 'application/json')




@csrf_exempt
def admin_staff_data_update_request(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        name = python_data.get('name')
        email = python_data.get('email')
        mobile = python_data.get('mobile')
        
        check_user = models.StaffDetail.objects.filter(id = id).count()
        if check_user == 1:
            
            user_details = models.NewStaffDetailsRequestData.objects.create(
                staff_id = id,
                name = name,
                email = email,
                mobile = mobile,
                status = 'Inactive',
            ).save()
            
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Data Update Request Send Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def individual_register(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        mobile = python_data.get('mobile_number')
        email = python_data.get('email', None)
        
        digits = "123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 9)]

        # OTP = '111111'
        # print(python_data, 'python_data')
        now = datetime.now()
        current_date_data = now.strftime("%Y-%m-%d")
        current_time = datetime.strptime(current_date_data, '%Y-%m-%d').date()

        if email != None and email != '':
            check_email = models.IndividualUserDetail.objects.filter(email = email).count()
            if check_email == 1:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Email Already registered, Please try with other.",
                    'is_email_register':"true"
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
            else:
                email = email

        check_mobile = models.IndividualUserDetail.objects.filter(mobile = mobile).count()
        if check_mobile == 0:
            

            user = models.IndividualUserDetail.objects.create(
                first_name = python_data.get('first_name'),
                last_name = python_data.get('last_name'),
                name = python_data.get('name'),
                date_of_birth = python_data.get('date_of_birth'),
                gender_id = python_data.get('gender'),
                mobile = mobile,
                email = python_data.get('email', None),
                
                status = 'Active',
                created_at = current_time,
                OTP = OTP
            )
            user.save()
            individual_id = user.id

            self_id = models.Relation.objects.filter(relation = 'Self').values_list('id', flat=True)[0]

            self_create = models.IndividualDependent.objects.create(
                individual_id = individual_id,
                dependent_name = user.name,
                dependent_relation_id = self_id, 
                date_of_birth = user.date_of_birth,
                gender_id = user.gender.id,
                created_at = current_time
            ).save()
        
            
            message = "Dear User, OTP for login into portal is "+OTP+" and valid till 2 minutes. Do not share this OTP to anyone for security reasons. -Vakare Management Consultants LLP"
            RecepientMobile = mobile.replace("+91", "").strip()
            CountryCode = "91"
            send_sms = requests.get("https://api.authkey.io/request?authkey="+AUTHKEY+"&mobile="+RecepientMobile+"&country_code="+CountryCode+"&sms="+message+"&sender="+SENDER_ID+"&pe_id="+ENTITY_ID+"&template_id="+DLT_TEMPLATE_ID)

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Individual Added Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Mobile Number Already registered, Please try with other.",
                'is_mobile_register':"true"

                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def individual_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        # print(python_data, 'python_data')
        id = python_data.get('id')
        mobile = python_data.get('mobile')
        check_individual = models.IndividualUserDetail.objects.filter(id = id, mobile=mobile).count()
        if check_individual == 1:
            individual = models.IndividualUserDetail.objects.get(id = id)
            individual.name = python_data.get('name', individual.name)
            individual.individual_code = python_data.get('individual_code', individual.individual_code)
            individual.date_of_birth = str(python_data.get('date_of_birth', individual.date_of_birth)).upper()
            individual.gender_id = python_data.get('gender', individual.gender)
            individual.mobile = python_data.get('mobile', individual.mobile)
            individual.email = python_data.get('email', individual.email)
            individual.address = python_data.get('address', individual.address)
            individual.pincode = python_data.get('pincode', individual.pincode)
            individual.state = python_data.get('state', individual.state)
            individual.city = python_data.get('city', individual.city)

            individual.save()

            self_check = models.IndividualDependent.objects.filter(individual_id = individual.id, dependent_relation__relation= 'Self').count()
            if self_check == 1:
                individual_self = models.IndividualDependent.objects.get(individual_id = individual.id, dependent_relation__relation= 'Self')
                individual_self.dependent_name = python_data.get('name', individual_self.dependent_name)
                individual_self.gender_id = python_data.get('gender', individual_self.gender)
                individual_self.date_of_birth = str(python_data.get('date_of_birth', individual.date_of_birth)).upper()
                individual_self.save()
                

                    



            for count in range(1, 20):
                dependent_relation = 'dependent_relation' + str(count)
                date_of_birth = 'date_of_birth' + str(count)
                gender = 'gender' + str(count)
                dependent_name = 'dependent_name' + str(count)

                if python_data.get(dependent_relation) and python_data.get(date_of_birth) and python_data.get(gender) and python_data.get(dependent_name):
                    dependent_relation_data = python_data.get(dependent_relation)
                    date_of_birth_data = python_data.get(date_of_birth)
                    gender_data = python_data.get(gender)
                    dependent_name_data = python_data.get(dependent_name)

                    dependent_check = models.IndividualDependent.objects.filter(individual_id = individual.id, dependent_relation_id= dependent_relation_data).count()
                    # print(dependent_check, 'dependent_checkdependent_check')
                    if dependent_check == 0:
                        dependent_create = models.IndividualDependent.objects.create(
                            individual_id = individual.id,
                            dependent_name = dependent_name_data,
                            dependent_relation_id = dependent_relation_data, 
                            date_of_birth = date_of_birth_data,
                            gender_id = gender_data,
                            created_at = current_time
                        ).save()
                    elif dependent_check == 1:
                        get_dependent_id = models.IndividualDependent.objects.filter(individual_id = individual.id, dependent_relation_id= dependent_relation_data).values_list('id', flat=True)[0]
                        # print(get_dependent_id, 'get_dependent_id')
                        dependent = models.IndividualDependent.objects.get(id = get_dependent_id)
                        dependent.dependent_name = dependent_name_data
                        dependent.date_of_birth = date_of_birth_data
                        dependent.gender_id = gender_data
                        dependent.save()
                    else:
                        pass
                else:
                    break

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Individual user Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        
        else:
            check_mobile = models.IndividualUserDetail.objects.filter(mobile = mobile).count()
            if check_mobile == 0:
                individual = models.IndividualUserDetail.objects.get(id = id)
                individual.name = python_data.get('name', individual.name)
                individual.individual_code = python_data.get('individual_code', individual.individual_code)
                individual.date_of_birth = str(python_data.get('date_of_birth', individual.date_of_birth)).upper()
                individual.gender_id = python_data.get('gender', individual.gender)
                individual.mobile = python_data.get('mobile', individual.mobile)
                individual.email = python_data.get('email', individual.email)
                individual.address = python_data.get('address', individual.address)
                individual.pincode = python_data.get('pincode', individual.pincode)
                individual.state = python_data.get('state', individual.state)
                individual.city = python_data.get('city', individual.city)

                individual.save()
                    
                self_check = models.IndividualDependent.objects.filter(individual_id = individual.id, dependent_relation__relation= 'Self').count()
                if self_check == 1:
                    individual_self = models.IndividualDependent.objects.get(individual_id = individual.id, dependent_relation__relation= 'Self')
                    individual_self.dependent_name = python_data.get('name', individual_self.dependent_name)
                    individual_self.gender_id = python_data.get('gender', individual_self.gender)
                    individual_self.date_of_birth = str(python_data.get('date_of_birth', individual.date_of_birth)).upper()
                    individual_self.save()
                    

                for count in range(1, 20):
                    dependent_relation = 'dependent_relation' + str(count)
                    date_of_birth = 'date_of_birth' + str(count)
                    gender = 'gender' + str(count)
                    dependent_name = 'dependent_name' + str(count)

                    if python_data.get(dependent_relation) and python_data.get(date_of_birth) and python_data.get(gender) and python_data.get(dependent_name):
                        dependent_relation_data = python_data.get(dependent_relation)
                        date_of_birth_data = python_data.get(date_of_birth)
                        gender_data = python_data.get(gender)
                        dependent_name_data = python_data.get(dependent_name)

                        dependent_check = models.IndividualDependent.objects.filter(individual_id = individual.id, dependent_relation_id= dependent_relation_data).count()
                        # print(dependent_check, 'dependent_checkdependent_check')
                        if dependent_check == 0:
                            dependent_create = models.IndividualDependent.objects.create(
                                individual_id = individual.id,
                                dependent_name = dependent_name_data,
                                dependent_relation_id = dependent_relation_data, 
                                date_of_birth = date_of_birth_data,
                                gender_id = gender_data,
                                created_at = current_time
                            ).save()
                        elif dependent_check == 1:
                            get_dependent_id = models.IndividualDependent.objects.filter(individual_id = individual.id, dependent_relation_id= dependent_relation_data).values_list('id', flat=True)[0]
                            # print(get_dependent_id, 'get_dependent_id')
                            dependent = models.IndividualDependent.objects.get(id = get_dependent_id)
                            dependent.dependent_name = dependent_name_data
                            dependent.date_of_birth = date_of_birth_data
                            dependent.gender_id = gender_data
                            dependent.save()
                        else:
                            pass
                    else:
                        break

                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Individual user Update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter mobile number is already registered."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def individual_profile_image_update(request):
    if request.method == 'POST':
        python_data={}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})
        
        individual = python_data.get('individual')
        profile_image = python_data.get('profile_image')
        check_emp = models.IndividualUserDetail.objects.filter(id = individual).count()
        if check_emp == 1:
            individual = models.IndividualUserDetail.objects.get(id = individual)
            if type(python_data.get('profile_image', individual.profile_image)) != str: 
                individual.profile_image = python_data.get('profile_image', individual.profile_image)
            individual.save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Profile Image Update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter valid Individual."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def all_individual_list(request):
    if request.method == 'POST':
        python_data = {}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})

        data = python_data.get('data')

        try:
            decoded_bytes = base64.b64decode(data)
            decoded_python_data = json.loads(decoded_bytes.decode('utf-8'))
        except:
            decoded_python_data = {}



        page_number = int(decoded_python_data.get('page_number',1))
        row_size = int(decoded_python_data.get('row_size',10))
        last_row = row_size * page_number
        first_row = last_row - row_size

        filter_condition = {}

        status = decoded_python_data.get('status',None)
        city = decoded_python_data.get('city',None)
        created_at = decoded_python_data.get('created_at',None)
        date_of_birth = decoded_python_data.get('date_of_birth',None)
        dependentShowInTable = decoded_python_data.get('dependentShowInTable',None)
        email = decoded_python_data.get('email',None)
        gender_name = decoded_python_data.get('gender_name',None)
        mobile = decoded_python_data.get('mobile',None)
        name = decoded_python_data.get('name',None)
    
        if name not in [None,'','null']:
            filter_condition['name__icontains'] = name
        if city not in [None,'','null']:
            filter_condition['city__icontains'] = city
        if created_at not in [None,'','null']:
            filter_condition['created_at__icontains'] = created_at
        if date_of_birth not in [None,'','null']:
            filter_condition['date_of_birth__icontains'] = date_of_birth
        # if dependentShowInTable not in [None,'','null']:
        #     filter_condition['dependentShowInTable__icontains'] = dependentShowInTable
        if email not in [None,'','null']:
            filter_condition['email__icontains'] = email
        if gender_name not in [None,'','null']:
            gender_name = gender_name.lower()
            if gender_name in ['f','e','fe','fem','fema','femal','female']:
                filter_condition['gender__gender__icontains']="Female"
            elif gender_name in ['m','ma','mal','male']:
                filter_condition['gender__gender__iexact']="Male"

        if mobile not in [None,'','null']:
            filter_condition['mobile__icontains'] = mobile
        if status not in [None,'','null']:
            if status != 'All':
                filter_condition['status'] = status


        total_records = models.IndividualUserDetail.objects.filter(**filter_condition).count()
        all_individual = models.IndividualUserDetail.objects.filter(**filter_condition).order_by('-id')[first_row:last_row]

        list_data = []
        for individual in all_individual:
            
            individual = models.IndividualUserDetail.objects.get(id = individual.id)
            serialiser = IndividualUserDetailSerializer(individual)
            data = serialiser.data


            individual_address = models.IndividualAddressDetail.objects.filter(individual = individual.id)
            address_data = IndividualAddressDetailSerialiser(individual_address, many=True).data

            all_dependent = models.IndividualDependent.objects.filter(individual = individual).order_by('id')
            # dependent_serialiser = IndividualDependentSerializer(dependent, many=True)
            # data.update({'dependent_data':dependent_serialiser.data})
            # list_dependent.append(data)
            list_dependent = []
            for dependent in all_dependent:
                self_id = models.Relation.objects.filter(relation = 'Self').values_list('id', flat=True)[0]
                relation = dependent.dependent_relation.id
                if self_id != relation:
                    dependent_serialiser = IndividualDependentSerializer(dependent)
                    list_dependent.append(dependent_serialiser.data)
                
            data.update({'user_address':address_data, 'dependent_data':list_dependent})
            list_data.append(data)
    
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data,
            'total_records':total_records
            }

        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def encrypt_data(encrypted_text):
    encrypted_text = encrypted_text
    secret_key = "1njanrhdkCnsahrebfdMvbjo32hqnd31"
    iv = "jsKidmshatyb4jdu" 
    key = secret_key.encode('utf-8') if isinstance(secret_key, str) else secret_key
    iv = iv.encode('utf-8') if isinstance(iv, str) else iv
    if len(key) != 32:
        raise ValueError("Secret key must be 32 bytes for AES-256 encryption.")
    if len(iv) != 16:
        raise ValueError("Initialization vector (IV) must be 16 bytes for CBC mode.")
    # encrypted_data = base64.b64decode(encrypted_text)
    # cipher = AES.new(key, AES.MODE_CBC, iv)
    # decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    # data = json.loads(decrypted_data.decode('utf-8'))
    # result = data.get('ErrorMessage')

    result = encrypted_text.split('/')
    first_encrypt = result[-1]
    first_encrypt = first_encrypt[3:]
    find_data = first_encrypt.find('%2F')

    if find_data != -1:
        first_encrypt = first_encrypt.replace("%2F", "/")

    encrypted_data = base64.b64decode(first_encrypt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    final_decrypt = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    final_data_get = str(final_decrypt.decode('utf-8'))
    final_data = final_data_get.split('&')
    data_dict = {}
    for convert_data in final_data:
        data_split = convert_data.split('=')
        data_dict.update({data_split[0]:data_split[1]})
    return data_dict


@csrf_exempt
def redirect_login_wellness(request):
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            encrypted_text = python_data.get('encrypted_text')
            data_get = encrypt_data(encrypted_text)
           
            corporate_code = data_get.get('corporate_code')
            employee_code = data_get.get('employee_code')

            # Fetch corporate object first
            corporate = models.CorporateDetail.objects.filter(corporate_code=corporate_code).first()
            if not corporate:
                res = {
                    'statuscode': 406,
                    'status': 'false',
                    'message': 'Enter Valid Corporate.'
                }
                return HttpResponse(JSONRenderer().render(res), content_type='application/json')

            # Try to find employee
            employee_count = models.EmployeeDetail.objects.filter(employee_code=employee_code,corporate__corporate_code=corporate_code).count()
            if employee_count != 1:
                # Employee not found — return appropriate response
                res = {
                    'statuscode': 404,
                    'status': 'false',
                    'message': 'No Active Employee Register in Svasthya Portal'
                }
                return HttpResponse(JSONRenderer().render(res), content_type='application/json')

            else:
                # Employee exists — return login success response
                employee = models.EmployeeDetail.objects.get(employee_code=employee_code,corporate__corporate_code=corporate_code)
                employee.employee_from = 'EBPF'
                employee.save()
                serializer = EmployeeDetailSerializer(employee)
                data = serializer.data

                login_via = employee.corporate.login_via
                data.update({'login_via': login_via, 'user_type': 'employee'})
                res = {
                    'statuscode': 200,
                    'status': 'Success',
                    'message': 'Login Successfully.',
                    'data': data
                }
                return HttpResponse(JSONRenderer().render(res), content_type='application/json')

        except Exception as e:
            import traceback
            traceback.print_exc()
            res = {
                'statuscode': 500,
                'status': 'false',
                'message': 'Internal server error.',
                'error': str(e)
            }
            return HttpResponse(JSONRenderer().render(res), content_type='application/json')


#####working SOS with newly added employee
# @csrf_exempt
# def redirect_login_wellness(request):
#     if request.method == 'POST':
#         try:
#             python_data = JSONParser().parse(io.BytesIO(request.body))
#             encrypted_text = python_data.get('encrypted_text')

#             data_get = encrypt_data(encrypted_text)
#             print("Decrypted data -->", data_get)

#             corporate_code = data_get.get('corporate_code')
#             employee_code = data_get.get('employee_code')
            

#             # Fetch corporate object first (assuming this is needed for ForeignKey)
#             corporate = models.CorporateDetail.objects.filter(corporate_code=corporate_code).first()
#             if not corporate:
#                 res = {
#                     'statuscode': 406,
#                     'status': 'false',
#                     'message': 'Enter Valid Corporate.'
#                 }
#                 return HttpResponse(JSONRenderer().render(res), content_type='application/json')

#             # Try to find employee by employee_code and hr_corporate_code
#             employee = models.EmployeeDetail.objects.filter(
#                 employee_code=employee_code,
#                 hr_corporate_code=corporate_code
#             ).first()

#             if not employee:
#                 # Employee not found — create new employee
                
#                 # Validate required fields
#                 required_fields = ['mobile', 'email', 'employee_code', 'corporate_code', 'employee_name', 'date_of_birth', 'gender']
#                 for field in required_fields:
#                     if not data_get.get(field):
#                         res = {
#                             'statuscode': 400,
#                             'status': 'false',
#                             'message': f'Missing required field: {field}'
#                         }
#                         return HttpResponse(JSONRenderer().render(res), content_type='application/json')

#                 now = datetime.now()
#                 current_time = now.strftime("%Y-%m-%d, %H:%M:%S")

#                 today_str = datetime.today().strftime('%Y-%m-%d')
#                 dob_raw = data_get.get('date_of_birth')

#                 dob = None
#                 if dob_raw:
#                     for fmt in ('%Y-%m-%d', '%d-%b-%Y', '%d-%B-%Y'):
#                         try:
#                             dob = datetime.strptime(dob_raw, fmt).date()
#                             break
#                         except Exception:
#                             continue

#                 employee = models.EmployeeDetail.objects.create(
#                     corporate=corporate,
#                     employee_name=data_get.get('employee_name'),
#                     employee_code=str(data_get.get('employee_code')).upper(),
#                     department='Admin',
#                     date_of_join=today_str,
#                     date_of_birth=dob,
#                     gender_id=4,  # You can replace with data_get.get('gender') if appropriate
#                     mobile='+91 ' + str(data_get.get('mobile', '')),
#                     email=data_get.get('email'),
#                     hr_employee='Shalini Fernandes',
#                     hr_corporate_code=corporate_code,
#                     address='Mumbai',
#                     pincode='400006',
#                     state='Maharashtra',
#                     city='Mumbai',
#                     status='Active',
#                     created_at=current_time
#                 )

#                 # Add self dependent relation
#                 self_id = models.Relation.objects.filter(relation='Self').values_list('id', flat=True).first()
#                 if self_id:
#                     models.EmployeeDependent.objects.create(
#                         employee=employee,
#                         dependent_name=data_get.get('employee_name'),
#                         dependent_relation_id=6,
#                         date_of_birth=dob,
#                         gender_id=4,
#                         created_at=current_time
#                     )

#                 serializer = EmployeeDetailSerializer(employee)
#                 data = serializer.data
                
#                 login_via = employee.corporate.login_via
#                 data.update({'login_via':login_via, 'user_type':'employee'})
#                 res = {
#                     'statuscode': 200,
#                     'status': 'Success',
#                     'message': 'Employee created and logged in successfully.',
#                     'data': data
#                 }
#                 return HttpResponse(JSONRenderer().render(res), content_type='application/json')

#             else:
#                 # Employee exists — return login success response
#                 serializer = EmployeeDetailSerializer(employee)
#                 data = serializer.data

#                 login_via = employee.corporate.login_via
#                 data.update({'login_via':login_via, 'user_type':'employee'})
#                 res = {
#                     'statuscode': 200,
#                     'status': 'Success',
#                     'message': 'Login Successfully.',
#                     'data': data
#                 }
#                 return HttpResponse(JSONRenderer().render(res), content_type='application/json')

#         except Exception as e:
#             import traceback
#             traceback.print_exc()
#             res = {
#                 'statuscode': 500,
#                 'status': 'false',
#                 'message': 'Internal server error.',
#                 'error': str(e)
#             }
#             return HttpResponse(JSONRenderer().render(res), content_type='application/json')



####commneted on 13 Oct 2025 by shubham

# @csrf_exempt
# def redirect_login_wellness(request):
#     if request.method == 'POST':
#         python_data = JSONParser().parse(io.BytesIO(request.body))
#         encrypted_text = python_data.get('encrypted_text')
#         data_get = encrypt_data(encrypted_text)
#         corporate_code = data_get.get('corporateCode')
#         employee_code = data_get.get('employeeCode')
#         check_corporate = models.CorporateDetail.objects.filter(corporate_code = corporate_code).count()
#         if check_corporate == 1:
#             get_corporate_id = models.CorporateDetail.objects.filter(corporate_code = corporate_code).values_list('id', flat=True)[0]
#             check_employee = models.EmployeeDetail.objects.filter(employee_code = employee_code,corporate_id = get_corporate_id).count()
#             if check_employee == 1:
#                 digits = '123456789'
#                 OTP = ""
#                 for i in range(6):
#                     OTP += digits[math.floor(random.random() * 9)]

#                 OTP = '111111'
#                 employee = models.EmployeeDetail.objects.get(employee_code = employee_code)
#                 employee.OTP = OTP 
#                 employee.save()
#                 employee_id = employee.id
#                 login_via = employee.corporate.login_via
#                 serialiser = EmployeeDetailSerializer(employee)
#                 data = serialiser.data
#                 data.update({'login_via':login_via, 'user_type':'employee', 'OTP':OTP})
#                 # create_history = models.EmployeeLoginHistory.objects.create(
#                 #     employee_id = employee_id,
#                 #     email = email,
#                 #     time = current_time
#                 # ).save()
#                 message = "Dear User, OTP for login into portal is "+OTP+" and valid till 2 minutes. Do not share this OTP to anyone for security reasons. -Vakare Management Consultants LLP"
#                 RecepientMobile = mobile.replace("+91", "").strip()
#                 CountryCode = "91"
#                 send_sms = requests.get("https://api.authkey.io/request?authkey="+AUTHKEY+"&mobile="+RecepientMobile+"&country_code="+CountryCode+"&sms="+message+"&sender="+SENDER_ID+"&pe_id="+ENTITY_ID+"&template_id="+DLT_TEMPLATE_ID)

#                 res = {
#                     'statuscode' : 200,
#                     'status':'Success',
#                     'message':"Login Successfully." ,
#                     'data':data
#                     }                                                        
#                 json_data = JSONRenderer().render(res)
#                 return HttpResponse(json_data, content_type= 'application/json')  
#             else:
#                 res = {
#                     'statuscode' : 406,
#                     'status':'false',
#                     'message' : "Employee not found."
#                     }
#                 json_data = JSONRenderer().render(res)
#                 return HttpResponse(json_data, content_type= 'application/json') 
#         else:  
#             res = {
#                 'statuscode' : 406,
#                 'status':'false',
#                 'message' : "Enter Valid Corporate."
#                 }
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def add_dependent_individual_employee(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        
        dependent_relation = python_data.get('dependent_relation')
        date_of_birth = python_data.get('date_of_birth')
        gender = python_data.get('gender')
        dependent_name = python_data.get('dependent_name')
        flag = python_data.get('flag')

        if flag == 'individual':
            individual = python_data.get('individual')
            
            child_id = models.Relation.objects.filter(relation = 'Child').values_list('id', flat=True)[0]

            child_count = models.IndividualDependent.objects.filter(individual=individual, dependent_relation_id = child_id).count()
            if dependent_relation != child_id:
                dependent_check = models.IndividualDependent.objects.filter(individual_id = individual,dependent_relation_id = dependent_relation).count()
                if dependent_check == 0:
                    dependent_create = models.IndividualDependent.objects.create(
                        individual_id = individual,
                        dependent_name = dependent_name,
                        dependent_relation_id = dependent_relation, 
                        date_of_birth = date_of_birth,
                        gender_id = gender,
                        created_at = current_time
                    ).save()
                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':"Dependent Added Successfully." ,
                        }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')  
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "You already create dependent using this Relation."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 

            elif dependent_relation == child_id:
                if child_count < 3:
                    dependent_create = models.IndividualDependent.objects.create(
                        individual_id = individual,
                        dependent_name = dependent_name,
                        dependent_relation_id = dependent_relation, 
                        date_of_birth = date_of_birth,
                        gender_id = gender,
                        created_at = current_time
                    ).save()
                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':"Dependent Added Successfully." ,
                        }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')  
                
                
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "You already added 3 child."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Something Went wrong."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        elif flag == 'employee':
            employee = python_data.get('employee')
            child_id = models.Relation.objects.filter(relation = 'Child').values_list('id', flat=True)[0]

            child_count = models.EmployeeDependent.objects.filter(employee = employee, dependent_relation_id = child_id).count()
            if dependent_relation != child_id:
                dependent_check = models.EmployeeDependent.objects.filter(employee_id = employee,dependent_relation_id = dependent_relation).count()
                if dependent_check == 0:
                    dependent_create = models.EmployeeDependent.objects.create(
                        employee_id = employee,
                        dependent_name = dependent_name,
                        dependent_relation_id = dependent_relation, 
                        date_of_birth = date_of_birth,
                        gender_id = gender,
                        created_at = current_time
                    ).save()
                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':"Dependent Added Successfully." ,
                        }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')  
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "You already create dependent using this Relation."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 

            elif dependent_relation == child_id:
                if child_count < 3:
                    dependent_create = models.EmployeeDependent.objects.create(
                        employee_id = employee,
                        dependent_name = dependent_name,
                        dependent_relation_id = dependent_relation, 
                        date_of_birth = date_of_birth,
                        gender_id = gender,
                        created_at = current_time
                    ).save()
                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':"Dependent Added Successfully." ,
                        }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')  
                
                
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "You already added 3 child."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Something Went wrong."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def update_dependent_individual_employee(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))        
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        
        id = python_data.get('id')

        dependent_relation = python_data.get('dependent_relation')
        date_of_birth = python_data.get('date_of_birth')
        gender = python_data.get('gender')
        dependent_name = python_data.get('dependent_name')
        flag = python_data.get('flag')

        if flag == 'individual':        
            individual = python_data.get('individual')
            child_id = models.Relation.objects.filter(relation = 'Child').values_list('id', flat=True)[0]


            check_dependent = models.IndividualDependent.objects.filter(id = id, individual=individual).count()
            if check_dependent == 1:
                if dependent_relation != child_id:
                    dependent_relation_check = models.IndividualDependent.objects.filter(id = id, individual=individual, dependent_relation= dependent_relation).count()
                    if dependent_relation_check == 1:
                        dependent = models.IndividualDependent.objects.get(id = id)
                        dependent.dependent_name = python_data.get('dependent_name', dependent.dependent_name)
                        dependent.dependent_relation_id = python_data.get('dependent_relation', dependent.dependent_relation)
                        dependent.date_of_birth = python_data.get('date_of_birth', dependent.date_of_birth)
                        dependent.gender_id = python_data.get('gender', dependent.gender)
                        dependent.save()
                        
                        res = {
                            'statuscode' : 200,
                            'status':'Success',
                            'message':"Dependent Update Successfully." ,
                            }                                                        
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')  
                    else:
                        dependent_relation_check = models.IndividualDependent.objects.filter(individual=individual, dependent_relation= dependent_relation).count()
                        if dependent_relation_check == 0:
                            dependent = models.IndividualDependent.objects.get(id = id)
                            dependent.dependent_name = python_data.get('dependent_name', dependent.dependent_name)
                            dependent.dependent_relation_id = python_data.get('dependent_relation', dependent.dependent_relation)
                            dependent.date_of_birth = python_data.get('date_of_birth', dependent.date_of_birth)
                            dependent.gender_id = python_data.get('gender', dependent.gender)
                            dependent.save()
                            
                            res = {
                                'statuscode' : 200,
                                'status':'Success',
                                'message':"Dependent Update Successfully." ,
                                }                                                        
                            json_data = JSONRenderer().render(res)
                            return HttpResponse(json_data, content_type= 'application/json')  
                        else:
                            res = {
                                'statuscode' : 406,
                                'status':'false',
                                'message':"Dependent Relation already exists." ,
                                }                                                        
                            json_data = JSONRenderer().render(res)
                            return HttpResponse(json_data, content_type= 'application/json')

                elif dependent_relation == child_id:
                    child_count = models.IndividualDependent.objects.filter(individual=individual,dependent_relation_id = child_id).count()

                    if child_count <= 3:
                        dependent = models.IndividualDependent.objects.get(id = id)
                        dependent.dependent_name = python_data.get('dependent_name', dependent.dependent_name)
                        dependent.dependent_relation_id = python_data.get('dependent_relation', dependent.dependent_relation)
                        dependent.date_of_birth = python_data.get('date_of_birth', dependent.date_of_birth)
                        dependent.gender_id = python_data.get('gender', dependent.gender)
                        dependent.save()
                        
                        
                        res = {
                            'statuscode' : 200,
                            'status':'Success',
                            'message':"Dependent Update Successfully." ,
                            }                                                        
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')  
                    
                    
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "You already added 3 child."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Something Went wrong."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        
        elif flag == 'employee':
            employee = python_data.get('employee')
            child_id = models.Relation.objects.filter(relation = 'Child').values_list('id', flat=True)[0]
            check_dependent = models.EmployeeDependent.objects.filter(id = id, employee=employee).count()
            if check_dependent == 1:
                if dependent_relation != child_id:
                    dependent_relation_check = models.EmployeeDependent.objects.filter(id = id, employee=employee, dependent_relation= dependent_relation).count()
                    if dependent_relation_check == 1:
                        dependent = models.EmployeeDependent.objects.get(id = id)
                        dependent.dependent_name = python_data.get('dependent_name', dependent.dependent_name)
                        dependent.dependent_relation_id = python_data.get('dependent_relation', dependent.dependent_relation)
                        dependent.date_of_birth = python_data.get('date_of_birth', dependent.date_of_birth)
                        dependent.gender_id = python_data.get('gender', dependent.gender)
                        dependent.save()
                        
                        res = {
                            'statuscode' : 200,
                            'status':'Success',
                            'message':"Dependent Update Successfully." ,
                            }                                                        
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')  
                    else:
                        dependent_relation_check = models.EmployeeDependent.objects.filter(employee=employee, dependent_relation= dependent_relation).count()
                        if dependent_relation_check == 0:
                            dependent = models.EmployeeDependent.objects.get(id = id)
                            dependent.dependent_name = python_data.get('dependent_name', dependent.dependent_name)
                            dependent.dependent_relation_id = python_data.get('dependent_relation', dependent.dependent_relation)
                            dependent.date_of_birth = python_data.get('date_of_birth', dependent.date_of_birth)
                            dependent.gender_id = python_data.get('gender', dependent.gender)
                            dependent.save()
                            
                            res = {
                                'statuscode' : 200,
                                'status':'Success',
                                'message':"Dependent Update Successfully." ,
                                }                                                        
                            json_data = JSONRenderer().render(res)
                            return HttpResponse(json_data, content_type= 'application/json')  
                        else:
                            res = {
                                'statuscode' : 406,
                                'status':'false',
                                'message':"Dependent Relation already exists." ,
                                }                                                        
                            json_data = JSONRenderer().render(res)
                            return HttpResponse(json_data, content_type= 'application/json')

                elif dependent_relation == child_id:
                    child_count = models.EmployeeDependent.objects.filter(employee=employee, dependent_relation_id = child_id).count()

                    if child_count <= 3:
                        dependent = models.EmployeeDependent.objects.get(id = id)
                        dependent.dependent_name = python_data.get('dependent_name', dependent.dependent_name)
                        dependent.dependent_relation_id = python_data.get('dependent_relation', dependent.dependent_relation)
                        dependent.date_of_birth = python_data.get('date_of_birth', dependent.date_of_birth)
                        dependent.gender_id = python_data.get('gender', dependent.gender)
                        dependent.save()
                        
                        
                        res = {
                            'statuscode' : 200,
                            'status':'Success',
                            'message':"Dependent Update Successfully." ,
                            }                                                        
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')  
                    
                    
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "You already added 3 child."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Something Went wrong."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def individual_status_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_individual = models.IndividualUserDetail.objects.filter(id = id).count()
        if check_individual == 1:
            individual_data = models.IndividualUserDetail.objects.get(id = id)
            individual_data.status = status
            individual_data.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : 'Individual status update Successfully.'
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def individual_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        individual = python_data.get('id')
        check_individual = models.IndividualUserDetail.objects.filter(id = individual).count()
        if check_individual == 1:
            
            individual_details = models.IndividualUserDetail.objects.get(id = individual)
            individual_details.status = 'Inactive'
            individual_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Individual Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid Individual ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def create_order_apiview(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        amount = python_data.get('amount')

        
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            amount = float(python_data.get("amount", 0)) * 100  # Razorpay requires amount in paise
            currency = "INR"
            order_data = {
                "amount": amount,
                "currency": currency,
                "payment_capture": 1,  # Auto capture payment
            }
            order = client.order.create(order_data)
            
            res = {
                'statuscode' : 200,
                'status':'true',
                "order_id": order["id"],
                "amount":amount / 100,
                'message':'Payment successful!'
                }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        
        except Exception as e:

            # return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            res = {
                'statuscode' : 406,
                'status':'true',
                "error": str(e),
                'message':'Payment successful!'
                } 
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def verify_payment_apiview(request):
    if request.method == 'POST':
        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        python_data = JSONParser().parse(io.BytesIO(request.body))
        
    
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_payment_id = python_data.get("razorpay_payment_id")
            razorpay_order_id = python_data.get("razorpay_order_id")
            razorpay_signature = python_data.get("razorpay_signature")
            # package = python_data.get("package")
            amount = python_data.get("amount")
            user = python_data.get("user")

            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }

            # Verify the payment signature
            client.utility.verify_payment_signature(params_dict)
            
        
            fetch_data = client.payment.fetch(razorpay_payment_id)
            method = fetch_data.get('method')
            transaction_id = fetch_data.get('id')
            res = {
                'statuscode' : 200,
                'status':'true',
                'message':'Payment successful!',
                'method': method,
                'transaction_id': transaction_id,
                }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')

        except razorpay.errors.SignatureVerificationError:
            
            res = {
                'statuscode' : 400,
                'status':'false',
                'message':'Payment verification failed!'
                }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def staff_module_rights(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        module = python_data.get('module_id', None)
        staff = python_data.get('staff')
        if module != None:
            check_staff = models.StaffDetail.objects.filter(id = staff).count()
            if check_staff == 1:
                get_all_staff = models.AdminModuleRights.objects.filter(staff_id = staff, module= module)
                serialiser = AdminModuleRightsSerializer(get_all_staff, many=True)
                all_data = serialiser.data

                res = {
                    'statuscode' : 200,
                    'status':'Success',
                    'data':all_data[0]
                    }                                                        
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')  
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message':'User Not found.'
                    }                                                        
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')

        if module == None:
            check_staff = models.StaffDetail.objects.filter(id = staff).count()
            if check_staff == 1:
                get_all_staff = models.AdminModuleRights.objects.filter(staff_id = staff).order_by('-id')
                serialiser = AdminModuleRightsSerializer(get_all_staff, many=True)
                all_data = serialiser.data
                res = {
                    'statuscode' : 200,
                    'status':'Success',
                    'data':all_data
                    }                                                        
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')  
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message':'User Not found.'
                    }                                                        
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def give_access(request):
    if request.method == 'POST':
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        all_user = models.StaffDetail.objects.all()
        for user in all_user:
            
            list_module = models.Module.objects.all()
            for module in list_module:
                module_id = module.id

                check_module_access = models.AdminModuleRights.objects.filter(module_id = module_id,staff_id = user).count()
                if check_module_access == 0:
                    admin_rights = models.AdminModuleRights.objects.create(
                        module_id = module_id,
                        staff_id = user.id,
                        module_access = 'active',
                        edit_access = 'inactive',
                        view_access = 'active',
                        delete_access = 'active',
                        created_at = current_time
                    )
                    admin_rights.save()

        res = {
            'statuscode' : 200,
            'status':'Success'
            }                                                        
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json')  



@csrf_exempt
def staff_module_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        staff = python_data.get('staff')
        check_admin_rights = models.AdminModuleRights.objects.filter(id = id, staff=staff).count()
        if check_admin_rights == 1:
            rights = models.AdminModuleRights.objects.get(id = id)
            rights.module_access = python_data.get('module_access', rights.module_access)
            rights.edit_access =  python_data.get('edit_access', rights.edit_access)
            rights.view_access =  python_data.get('view_access', rights.view_access)
            rights.delete_access = python_data.get('delete_access', rights.delete_access)
            rights.save()

            res = {
                'statuscode' : 200,
                'status':'true',
                'message':'Data update succsfully'
                }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:

            res = {
                'statuscode' : 200,
                'status':'false',
                'message':'User Not found.'
                }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def vendor_wise_package_list(request):
    if request.method == 'POST':
        vendor_id = request.POST['vendor']
        if vendor_id.isdigit():
            check_vendor = models.VendorDetail.objects.filter(id = vendor_id).count()
            if check_vendor == 1:
                get_all_package = models.PackageDetail.objects.filter(vendor = vendor_id)
                serialiser = PackageVendorSerializer(get_all_package, many=True)
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'data':serialiser.data
                }                                                        
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
        else:
            list_vendor = vendor_id.split(',')
            list_data = []
            for vendor_id in list_vendor:
                check_vendor = models.VendorDetail.objects.filter(id = vendor_id).count()
                if check_vendor == 1:
                    get_all_package = models.PackageDetail.objects.filter(vendor = vendor_id)
                    for package in get_all_package:
                        serialiser = PackageVendorSerializer(package)
                        list_data.append(serialiser.data)
            
            res = {
                'statuscode' : 200,
                'status':'true',
                'data':list_data
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def offer_create(request):
    if request.method == 'POST':
        python_data={}
        for i,j in request.FILES.items():
            python_data.update({i:j})

        for i,j in request.POST.items():
            python_data.update({i:j})

        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        offer = models.OfferDetail.objects.create(
            title = python_data.get('title'),
            offer_code = python_data.get('offer_code'),
            type_of_discount = python_data.get('type_of_discount'),
            discount = python_data.get('discount'),
            type_of_service_id = python_data.get('type_of_service'),
            package_id = python_data.get('package'),
            duration_id = python_data.get('duration'),
            max_usage_count = python_data.get('max_usage_count'),
            no_of_uses_per_customer = python_data.get('no_of_uses_per_customer'),
            publish_date = python_data.get('publish_date'),
            publish_time = python_data.get('publish_time'),
            start_date = python_data.get('start_date'),
            end_date = python_data.get('end_date'),
            content = python_data.get('content'),
            status = 'Inactive',
            created_at = current_date
        )
        offer.save()
        # if python_data.get('platform') == '':
        #     offer.platform.set([])
        # else:
        #     offer.platform.set((python_data.get('platform', offer.platform)))


        if python_data.get('platform') == '':
            offer.platform.set([])
        elif python_data.get('platform').isdigit():
            offer.platform.set([eval(python_data.get('platform'))])
        else:
            offer.platform.set(eval(python_data.get('platform', offer.platform)))
                        
        res = {
            'statuscode' : 200,
            'status':'true',
            'message':'Offer Create successfully.'
        }                                                        
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def list_all_offer(request):
    if request.method == 'POST':
        all_offer = models.OfferDetail.objects.all().order_by('-id')
        serialiser = OfferDetailSerializer(all_offer, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
                

        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def offer_update(request):
    if request.method == 'POST':
        python_data={}
        for i,j in request.FILES.items():
            python_data.update({i:j})

        for i,j in request.POST.items():
            python_data.update({i:j})

        id = python_data.get('id')
        check_offer = models.OfferDetail.objects.filter(id = id).count()
        if check_offer == 1:
            offer_detail = models.OfferDetail.objects.get(id = id)

            offer_detail.title = python_data.get('title', offer_detail.title)
            offer_detail.offer_code = python_data.get('offer_code', offer_detail.offer_code)
            offer_detail.type_of_discount = python_data.get('type_of_discount', offer_detail.type_of_discount)
            offer_detail.discount = python_data.get('discount', offer_detail.discount)
            offer_detail.type_of_service_id = python_data.get('type_of_service', offer_detail.type_of_service)
            offer_detail.package_id = python_data.get('package', offer_detail.package)
            offer_detail.duration_id = python_data.get('duration', offer_detail.duration)
            offer_detail.max_usage_count = python_data.get('max_usage_count', offer_detail.max_usage_count)
            offer_detail.no_of_uses_per_customer = python_data.get('no_of_uses_per_customer')
            offer_detail.publish_date = python_data.get('publish_date', offer_detail.publish_date)
            offer_detail.publish_time = python_data.get('publish_time',  offer_detail.publish_time)
            offer_detail.start_date = python_data.get('start_date', offer_detail.start_date )
            offer_detail.end_date = python_data.get('end_date', offer_detail.end_date)
            offer_detail.content = python_data.get('content', offer_detail.content)
            offer_detail.status = python_data.get('status', offer_detail.status)
        
            offer_detail.save()

            if python_data.get('platform') == '':
                offer_detail.platform.set([])
            elif python_data.get('platform').isdigit():
                offer_detail.platform.set([eval(python_data.get('platform'))])
            else:
                offer_detail.platform.set(eval(python_data.get('platform', offer_detail.platform)))
                            
            res = {
                'statuscode' : 200,
                'status':'true',
                'message':'Offer Update successfully.'
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message':'Something went wrong.'
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def all_notification_user(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        flag = python_data.get('flag')
        user = python_data.get('user')
        if flag == 'employee':
            all_notification = models.NotificationDetail.objects.filter(employee =user).order_by('-id')
            serialiser = NotificationNameSerializer(all_notification, many=True)
            
            res = {
                'statuscode' : 200,
                'status':'true',
                'data':serialiser.data
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')    
        
        elif flag == 'individual':
            all_notification = models.NotificationDetail.objects.filter(individual =user).order_by('-id')
            serialiser = NotificationNameSerializer(all_notification, many=True)
            
            res = {
                'statuscode' : 200,
                'status':'true',
                'data':serialiser.data
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message':'Something went wrong.'
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
    else:
        res = {
                'statuscode' : 406,
                'status':'false',
                'message':'Something went wrong.'
        }                                                        
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def notification_detail(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_notification = models.NotificationDetail.objects.filter(id = id).count()
        if check_notification == 1:
            notification = models.NotificationDetail.objects.get(id = id)
            notification.user_read = 'true'
            notification.save()
            serialiser = NotificationDetailSerializer(notification)
            
            res = {
                'statuscode' : 200,
                'status':'true',
                'data':serialiser.data
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 460,
                'status':'false',
                'message':'Something went wrong.'
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def all_transaction_list(request):
    if request.method == 'POST':
        
        all_transaction = models.Transaction.objects.all().order_by('-id')
        serialiser = TransactionSerializer(all_transaction, many=True)
        res = {
            'statuscode' : 200,
            'status':'true',
            'data':serialiser.data
        }                                                        
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json')
    
@csrf_exempt
def user_transaction_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        flag = python_data.get('flag')
        user = python_data.get('user')
        if flag == 'individual':
            all_transaction = models.Transaction.objects.filter(individual = user).order_by('-id')
            serialiser = TransactionSerializer(all_transaction, many=True)
            res = {
                'statuscode' : 200,
                'status':'true',
                'data':serialiser.data
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        
        elif flag == 'employee':
            all_transaction = models.Transaction.objects.filter(employee = user).order_by('-id')
            serialiser = TransactionSerializer(all_transaction, many=True)
            res = {
                'statuscode' : 200,
                'status':'true',
                'data':serialiser.data
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 460,
                'status':'false',
                'message':'Something went wrong.'
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')

    
@csrf_exempt
def tomorrow_check(request):
    if request.method == 'POST':
        
        now = datetime.now()
        formatted_date = now.strftime("%B %d, %Y")
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        current_time = now.strftime("%Y%m%d%H%M%S")

        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = time.strftime("%H:%M:%S", time.localtime())

        presentday = datetime.now()
        tomorrow = presentday + timedelta(1)
        tomorrow = tomorrow.strftime('%Y-%m-%d')

        check_already_send = models.NotificationDetail.objects.filter(notification_type = 'Gentle Reminder',appointment_date = tomorrow).count()
        if check_already_send == 0:
            get_center_id = models.TypeOfVisit.objects.filter(type_of_visit='At Center').values_list('id', flat=True)[0]
            get_hybrid_id = models.TypeOfVisit.objects.filter(type_of_visit='Hybrid').values_list('id', flat=True)[0]
            list_appointment = models.AppointmentDetail.objects.filter(Q(type_of_visit = get_center_id) | Q(type_of_visit = get_hybrid_id), confirm_appointment_date =tomorrow)
            for appointment in list_appointment:
                get_data = models.AppointmentDetail.objects.get(id = appointment.id)
                center_address = get_data.center.center_name + ', ' + get_data.center.address + ', ' + get_data.center.city + '-' + get_data.center.pincode
                package = get_data.package.id
                center = get_data.center.id
                
                appointment_type = get_data.appointment_type
                if (appointment_type).lower() == 'employee':
                    recipient_name = appointment.patient.dependent_name
                    employee = appointment.employee.id
                    individual = None
                else:
                    recipient_name = appointment.individual_patient.dependent_name
                    individual = appointment.individual.id
                    employee = None

                notification = models.NotificationDetail.objects.create(
                    title = 'Gentle Reminder: Your Health Check-Up is Tomorrow',
                    notification_type = 'Gentle Reminder',
                    # appointment_date = tomorrow,
                    user_type = appointment_type,
                    employee_id = employee,
                    individual_id = individual,
                    center_id = center,
                    package_id = package,
                    location = center_address,
                    recipient_name = recipient_name,
                    appointment_date= tomorrow,
                    created_date = current_date,
                    created_time = curr_time,
                    user_read = 'false'
                ).save()
        else:
            pass

        res = {
            'statuscode' : 200,
            'status':'true',
            
        }                                                        
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json')

def invoice_template(request):
    return render(request, 'invoice_template.html')



@csrf_exempt
def add_to_cart_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        user_type = python_data.get('user_type')
        appointment = python_data.get('appointment')
        if user_type == 'employee':
            employee = python_data.get('employee')
            patient = python_data.get('patient')
            package = python_data.get('package')
            check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
            if check_employee == 1:
                check_dependent = models.EmployeeDependent.objects.filter(employee = employee, id = patient).count()
                if check_dependent == 1:
                    check_package = models.PackageDetail.objects.filter(id = package).count()
                    if check_package == 1:
                        get_amount = models.PackageDetail.objects.filter(id = package).values_list('offer_price', flat=True)[0]
                        check_add_to_cart = models.AddToCart.objects.filter(employee_id = employee,patient_id = patient,package_id = package).count()
                        if check_add_to_cart == 0:
                            add_to_cart = models.AddToCart.objects.create(
                                user_type = python_data.get('user_type'),
                                appointment_id = appointment,
                                employee_id = employee,
                                patient_id = patient,
                                package_id = package,
                                amount = get_amount,
                                individual_id = None,
                                individual_patient_id = None,
                                created_at = current_date
                            )
                            add_to_cart.save()
                            res = {
                                'statuscode' : 200,
                                'status':'true',
                                'message':'Your Package Added to Cart.'
                            }                                                        
                            json_data = JSONRenderer().render(res)
                            return HttpResponse(json_data, content_type= 'application/json')
                        else:
                            res = {
                                'statuscode' : 406,
                                'status':'false',
                                'message':'Package with this dependent already in cart.'
                            }                                                        
                            json_data = JSONRenderer().render(res)
                            return HttpResponse(json_data, content_type= 'application/json')
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message':'Enter valid Package.'
                        }                                                        
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message':'Enter valid Dependent.'
                    }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')         
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message':'Enter valid Employee.'
                }                                                        
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')    

        elif user_type == 'individual':
            individual = python_data.get('individual')
            individual_patient = python_data.get('patient')
            package = python_data.get('package')
            check_individual = models.IndividualUserDetail.objects.filter(id = individual).count()
            if check_individual == 1:
                check_dependent = models.IndividualDependent.objects.filter(individual = individual, id = individual_patient).count()
                if check_dependent == 1:
                    check_package = models.PackageDetail.objects.filter(id = package).count()
                    if check_package == 1:
                        get_amount = models.PackageDetail.objects.filter(id = package).values_list('offer_price', flat=True)[0]
                        check_add_to_cart = models.AddToCart.objects.filter(individual_id = individual,individual_patient_id = individual_patient,package_id = package).count()
                        if check_add_to_cart == 0:

                            add_to_cart = models.AddToCart.objects.create(
                                user_type = python_data.get('user_type'),
                                appointment_id = appointment,
                                employee_id = None,
                                patient_id = None,
                                package_id = package,
                                amount = get_amount,
                                individual_id = individual,
                                individual_patient_id = individual_patient,
                                created_at = current_date
                            )
                            add_to_cart.save()
                            res = {
                                'statuscode' : 200,
                                'status':'true',
                                'message':'Your Package Added to Cart.'
                            }                                                        
                            json_data = JSONRenderer().render(res)
                            return HttpResponse(json_data, content_type= 'application/json')
                        else:
                            res = {
                                'statuscode' : 406,
                                'status':'false',
                                'message':'Package with this dependent already in cart.'
                            }                                                        
                            json_data = JSONRenderer().render(res)
                            return HttpResponse(json_data, content_type= 'application/json')
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message':'Enter valid Package.'
                        }                                                        
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message':'Enter valid Dependent.'
                    }                                                        
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')         
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message':'Enter valid Individual.'
                }                                                        
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message':'Enter valid User Type.'
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def add_to_cart_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        user_type = python_data.get('user_type')
        id = python_data.get('id')

        total_amount = 0
        platform_charge = 0

        if user_type == 'employee':
            get_all_data = models.AddToCart.objects.filter(employee = id).order_by('-id')
            list_data = []
            for data in get_all_data:
                get_data = models.AddToCart.objects.get(id = data.id)
                
                package = data.package.id
                employee = data.employee.id
                patient = data.patient.id
                
                get_package_payment_tags = models.PackageDetail.objects.filter(id = package).values_list('tags', flat=True)[0]
                package_payment_tags = models.PaymentTags.objects.filter(id = get_package_payment_tags).values_list('payment_tags', flat=True)[0]
                
                if package_payment_tags == 'Corporate pay':
                    check_appointment = models.AppointmentDetail.objects.filter(package =package, employee =employee, patient= patient).exclude(status='add_to_cart').count()
                    if check_appointment != 0:
                        amount = data.amount
                    
                    elif check_appointment == 0:
                        amount = 0

                elif package_payment_tags == 'Self Pay':                            
                        amount = data.amount


                serialiser = AddToCartSerializer(get_data).data
                serialiser.update({'amount':amount})
                list_data.append(serialiser)

                # total_amount += float(amount)
                # platform_charge = float(math.ceil(total_amount * (0.02)))

                total_amount += math.ceil(float(amount))
                platform_charge = math.ceil(total_amount * 0.02)

                sgst = float(math.ceil(total_amount * (0.09)))
                cgst = float(math.ceil(total_amount * (0.09)))

            res = {
                'statuscode' : 200,
                'status':'true',
                'data':list_data,
                'total_amount':total_amount,
                'platform_charge':platform_charge,
                # 'sgst' : sgst,
                # 'cgst' : cgst,
                # 'grand_total': total_amount + sgst + cgst + platform_charge
                'grand_total': total_amount + platform_charge
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        
        
        
        elif user_type == 'individual':
            get_all_data = models.AddToCart.objects.filter(individual = id).order_by('-id')
            
            for data in get_all_data:
                # total_amount += float(data.amount)
                total_amount += math.ceil(float(data.amount))

            serialiser = AddToCartSerializer(get_all_data, many=True)
            # platform_charge = float(math.ceil(total_amount * (0.02)))
            platform_charge = math.ceil(total_amount * 0.02)
            sgst = float(math.ceil(total_amount * (0.09)))
            cgst = float(math.ceil(total_amount * (0.09)))

            res = {
                'statuscode' : 200,
                'status':'true',
                'data':serialiser.data,
                'total_amount':total_amount,
                'platform_charge':platform_charge,
                # 'sgst' : sgst,
                # 'cgst' : cgst,
                # 'grand_total': total_amount + sgst + cgst + platform_charge
                'grand_total': total_amount + platform_charge

            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message':'Enter valid User Type.'
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')


@csrf_exempt
def add_to_cart_count(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        user_type = python_data.get('user_type')
        id = python_data.get('id')


        if user_type == 'employee':
            count = models.AddToCart.objects.filter(employee = id).count()

            res = {
                'statuscode' : 200,
                'status':'true',
                'count':count,

            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
            
        elif user_type == 'individual':
            count = models.AddToCart.objects.filter(individual = id).count()
                                                     
            res = {
                'statuscode' : 200,
                'status':'true',
                'count':count,

            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message':'Enter valid User Type.'
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')




@csrf_exempt
def add_to_cart_delete(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')

        check_cart = models.AddToCart.objects.filter(id = id).count()
        if check_cart == 1:
            get_appointment = models.AddToCart.objects.filter(id = id).values_list('appointment', flat=True)[0]
            appointment = models.AppointmentDetail.objects.get(id = get_appointment)
            appointment.delete()
        
            # get_cart = models.AddToCart.objects.get(id = id)
            # get_cart.delete()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message':"Delete Package Successfully."
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'False',
                'message':"Something went wrong."
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')



@csrf_exempt
def appointment_date_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_appointment = models.AppointmentDetail.objects.filter(id = id).count()
        if check_appointment == 1:
            appointment = models.AppointmentDetail.objects.get(id = id)
            appointment.appointment_date_1 = python_data.get('appointment_date_1', appointment.appointment_date_1)
            appointment.appointment_date_2 = python_data.get('appointment_date_2', appointment.appointment_date_2)
            appointment.home_sample_date_1 = python_data.get('home_sample_date_1', appointment.home_sample_date_1)
            appointment.home_sample_date_2 = python_data.get('home_sample_date_2', appointment.home_sample_date_2)
            appointment.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message':"Date Selected Successfully."
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'False',
                'message':"Something went wrong."
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def add_to_card_transaction_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        flag = python_data.get('flag', 'employee')
        add_to_cart = python_data.get('add_to_cart')
        method = python_data.get('method', None)
        transaction_id = python_data.get('transaction_id', None)
        is_payment = python_data.get('is_payment')


        now = datetime.now()

        formatted_date = now.strftime("%B %d, %Y")
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        current_time = now.strftime("%Y%m%d%H%M%S")
        current_date_booking = now.strftime("%Y%m%d")

        if flag == 'employee':

            for cart in add_to_cart:
                cart = models.AddToCart.objects.get(id = cart)
                employee = cart.employee.id
                check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
                list_data = []
                if check_employee == 1:                    
                    package = cart.package.id
                    appointment = cart.appointment.id
                    patient = cart.patient.id
                    center = cart.appointment.center.id

                    type_of_visit = models.PackageDetail.objects.filter(id = package).values_list('type_of_visit', flat=True)[0]
                    appointment_create = models.AppointmentDetail.objects.get(id = appointment)
                    appointment_create.status = 'Request Received'
                    appointment_create.save()
                    appointment_id = appointment_create.id
                    appointment_date_1 = appointment_create.appointment_date_1
                    appointment_date_2 = appointment_create.appointment_date_2

                
                    package_data = models.PackageDetail.objects.get(id = package)
                    package_type = package_data.package_type
                    amount = package_data.offer_price
                    platform_charge = math.ceil(float(amount)*float(0.02))
                    total_amount = float(platform_charge) + float(amount)

                    corporate_id = models.EmployeeDetail.objects.filter(id = employee).values_list('corporate', flat=True)[0]

                    if is_payment == False:
                        amount = 0
                    ### Invoice Data
                    total_today_appointment = models.Transaction.objects.filter(created_at =current_date).count()
                    formatted_num = format(total_today_appointment, '03d')
                    all_appointment = models.AppointmentDetail.objects.all().count()
                    all_formatted_num = format(all_appointment, '05d')
                    
                    booking_id = 'BKG-' + str(current_date_booking) + '-' +str(formatted_num)
                    
                    invoice_id = f'25-26/{formatted_num}/IN-{all_formatted_num}'
                    # 25-26/0001/IN-00001
                    transaction_create = models.Transaction.objects.create(
                        transaction_type = package_type,
                        appointment_id = appointment_create.id,
                        is_payment = is_payment,
                        booking_id = booking_id,
                        method = method,
                        transaction_id = transaction_id,
                        invoice_id = invoice_id,
                        individual_id=None,
                        corporate_id=corporate_id,
                        employee_id=employee,
                        package_id=package,
                        amount=amount,
                        platform_charge = platform_charge,
                        total_amount = total_amount,
                        patient_id = patient,
                        status='Paid',
                        reason = 'Paid but Appointment/Report is pending.',
                        created_at=current_date
                    ).save()

                    notification = models.NotificationDetail.objects.create(
                        title = 'Health Checkup Request Received',
                        notification_type = 'Acknowledgment',
                        preferred_appointment_date1 = appointment_date_1,
                        preferred_appointment_date2 = appointment_date_2,
                        user_type = 'employee',
                        employee_id = employee,
                        center_id = center,
                        package_id = package,
                        type_of_visit_id = type_of_visit,
                        created_date = current_date,
                        created_time = curr_time,
                        user_read = 'false'
                    ).save()

                    cart = models.AddToCart.objects.get(id = cart.id)
                    cart.delete()

                    recipient_name = appointment_create.patient.dependent_name
                    recipient_number = appointment_create.employee.mobile
                    recipient_email = appointment_create.employee.email
                    recipient_address = appointment_create.employee.address + ', ' + appointment_create.employee.city + ' - ' + appointment_create.employee.pincode

                    center_name = appointment_create.center.center_name
                    center_address = appointment_create.center.address + ', ' + appointment_create.center.city + ' - ' + appointment_create.center.pincode


                    invoice_date = formatted_date

                    package_name = appointment_create.package.package_name
                    package_service = appointment_create.package.type_of_service.type_of_service
                    
                    package_amount = appointment_create.package.MRP
                    package_discount_price = appointment_create.package.discount_price
                    package_offer_price = appointment_create.package.offer_price
                
                    amount_in_words = num2words(package_offer_price, lang='en').capitalize() + " only"
                    
                    center_state = appointment_create.center.state
                    appointment_id = appointment_create.id

                    if center_state == 'Maharashtra':
                        package_SGST = appointment_create.package.sgst
                        package_SGST_amount = appointment_create.package.sgst_amount
                        package_CGST = appointment_create.package.cgst
                        package_CGST_amount = appointment_create.package.cgst_amount

                        context= {
                            "recipient_name":recipient_name,
                            "recipient_number":recipient_number,
                            "recipient_email":recipient_email,
                            "recipient_address":recipient_address,
                            
                            "center_name":center_name,
                            "center_address":center_address,
                            "invoice_id":invoice_id,
                            "invoice_date":invoice_date,
                            "booking_id":booking_id,

                            "package_name":package_name,
                            "package_service":package_service,
                            "package_amount":package_amount,
                            "package_discount_price":package_discount_price,
                            "amount_in_words":amount_in_words,
                            "package_offer_price":package_offer_price,
                            "platform_charge":platform_charge,
                            # "total_amount":total_amount,
                            "method":method,

                            "flag":True,
                            "package_SGST":package_SGST,
                            "package_SGST_amount":package_SGST_amount,
                            "package_CGST":package_CGST,
                            "package_CGST_amount":package_CGST_amount,
                            "appointment_id":appointment_id
                        }    
                    else:
                        package_IGST = appointment_create.package.igst
                        package_IGST_amount = appointment_create.package.igst_amount
                        
                        context= {
                            "recipient_name":recipient_name,
                            "recipient_number":recipient_number,
                            "recipient_address":recipient_address,
                            "center_name":center_name,
                            "center_address":center_address,
                            "invoice_id":invoice_id,
                            "invoice_date":invoice_date,
                            "booking_id":booking_id,
                            "method":method,

                            "package_name":package_name,
                            "package_service":package_service,
                            "package_amount":package_amount,
                            "package_discount_price":package_discount_price,
                            "amount_in_words":amount_in_words,
                            "package_offer_price":total_amount,
                            "platform_charge":platform_charge,
                            # "total_amount":total_amount,

                            "flag":False,
                            "package_IGST":package_IGST,
                            "package_IGST_amount":package_IGST_amount,
                            "appointment_id":appointment_id
                        }
                    
                    data = createPDF(context)
                    
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'true',
                        'message' : "something went wrong.",
                        
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "You're appointment book successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        
        elif flag == 'individual':
          
            for cart in add_to_cart:
                cart = models.AddToCart.objects.get(id = cart)
                individual = cart.individual.id
                check_individual = models.IndividualUserDetail.objects.filter(id = individual).count()

                list_data = []
                if check_individual == 1:                    
                    package = cart.package.id
                    appointment = cart.appointment.id
                    patient = cart.individual_patient.id
                    center = cart.appointment.center.id

                    type_of_visit = models.PackageDetail.objects.filter(id = package).values_list('type_of_visit', flat=True)[0]
                    appointment_create = models.AppointmentDetail.objects.get(id = appointment)
                    appointment_create.status = 'Request Received'
                    appointment_create.save()
                    appointment_id = appointment_create.id
                    appointment_date_1 = appointment_create.appointment_date_1
                    appointment_date_2 = appointment_create.appointment_date_2

                    if is_payment == False:
                        amount = 0
                    ### Invoice Data
                    total_today_appointment = models.Transaction.objects.filter(created_at =current_date).count()
                    formatted_num = format(total_today_appointment, '03d')
                    all_appointment = models.AppointmentDetail.objects.all().count()
                    all_formatted_num = format(all_appointment, '05d')

                    booking_id = 'BKG-' + str(current_date_booking) + '-' +str(formatted_num)
                    
                    invoice_id = f'25-26/{formatted_num}/IN-{all_formatted_num}'

                    package_data = models.PackageDetail.objects.get(id = package)
                    package_type = package_data.package_type
                    amount = package_data.offer_price
                    platform_charge = math.ceil(float(amount)*float(0.02))
                    total_amount = float(platform_charge) + float(amount)

                    transaction_create = models.Transaction.objects.create(
                        transaction_type = package_type,
                        appointment_id = appointment_create.id,
                        is_payment = is_payment,
                        booking_id = booking_id,
                        invoice_id = invoice_id,
                        individual_id=individual,
                        method = method,
                        transaction_id = transaction_id,
                        corporate_id=None,
                        employee_id=None,
                        package_id=package,
                        amount=amount,
                        individual_patient_id = patient,
                        status='Paid',
                        reason = 'Paid but Appointment/Report is pending.',
                        created_at=current_date
                    ).save()

                    notification = models.NotificationDetail.objects.create(
                        title = 'Health Checkup Request Received',
                        notification_type = 'Acknowledgment',
                        preferred_appointment_date1 = appointment_date_1,
                        preferred_appointment_date2 = appointment_date_2,
                        user_type = 'individual',
                        individual_id = individual,
                        center_id = center,
                        package_id = package,
                        type_of_visit_id = type_of_visit,
                        created_date = current_date,
                        created_time = curr_time,
                        user_read = 'false'
                    ).save()
                    
                    cart = models.AddToCart.objects.get(id = cart.id)
                    cart.delete()
                    
                    recipient_name = appointment_create.individual_patient.dependent_name
                    recipient_number = appointment_create.individual.mobile
                    recipient_email = appointment_create.individual.email
                    recipient_address = appointment_create.individual.address + ', ' + appointment_create.individual.city + ' - ' + appointment_create.individual.pincode

                    center_name = appointment_create.center.center_name
                    center_address = appointment_create.center.address + ', ' + appointment_create.center.city + ' - ' + appointment_create.center.pincode


                    invoice_date = formatted_date

                    package_name = appointment_create.package.package_name
                    package_service = appointment_create.package.type_of_service.type_of_service
                    
                    package_amount = appointment_create.package.MRP
                    package_discount_price = appointment_create.package.discount_price
                    package_offer_price = appointment_create.package.offer_price
                
                    amount_in_words = num2words(package_offer_price, lang='en').capitalize() + " only"
                    
                    center_state = appointment_create.center.state
                    appointment_id = appointment_create.id


                    if center_state == 'Maharashtra':
                        package_SGST = appointment_create.package.sgst
                        package_SGST_amount = appointment_create.package.sgst_amount
                        package_CGST = appointment_create.package.cgst
                        package_CGST_amount = appointment_create.package.cgst_amount

                        context= {
                            "recipient_name":recipient_name,
                            "recipient_number":recipient_number,
                            "recipient_email":recipient_email,
                            "recipient_address":recipient_address,
                            
                            "center_name":center_name,
                            "center_address":center_address,
                            "invoice_id":invoice_id,
                            "invoice_date":invoice_date,
                            "booking_id":booking_id,
                            "method":method,

                            "package_name":package_name,
                            "package_service":package_service,
                            "package_amount":package_amount,
                            "package_discount_price":package_discount_price,
                            "amount_in_words":amount_in_words,
                            "package_offer_price":total_amount,
                            "platform_charge":platform_charge,
                            # "total_amount":total_amount,


                            "flag":True,
                            "package_SGST":package_SGST,
                            "package_SGST_amount":package_SGST_amount,
                            "package_CGST":package_CGST,
                            "package_CGST_amount":package_CGST_amount,
                            "appointment_id":appointment_id
                        }    
                    else:
                        package_IGST = appointment_create.package.igst
                        package_IGST_amount = appointment_create.package.igst_amount
                        
                        context= {
                            "recipient_name":recipient_name,
                            "recipient_number":recipient_number,
                            "recipient_address":recipient_address,
                            "center_name":center_name,
                            "center_address":center_address,
                            "invoice_id":invoice_id,
                            "invoice_date":invoice_date,
                            "booking_id":booking_id,
                            "method":method,

                            "package_name":package_name,
                            "package_service":package_service,
                            "package_amount":package_amount,
                            "package_discount_price":package_discount_price,
                            "amount_in_words":amount_in_words,
                            "package_offer_price":total_amount,
                            "platform_charge":platform_charge,
                            # "total_amount":total_amount,

                            "flag":False,
                            "package_IGST":package_IGST,
                            "package_IGST_amount":package_IGST_amount,
                            "appointment_id":appointment_id

                        }


                    data = createPDF(context)
                    
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'true',
                        'message' : "something went wrong.",
                        
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "You're appointment book successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def center_holiday_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))

        center = python_data.get('center')
        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        
        list_data = []
        check_center = models.CenterDetail.objects.filter(id = center).count()
        if check_center == 1:
            get_all_holiday = models.HolidayDetail.objects.filter(center = center, status = 'Active')
            for holiday in get_all_holiday:
                get_date = models.HolidayDetail.objects.get(id = holiday.id)
                start_date = get_date.start_date
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                
                end_date = get_date.end_date
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                
                if start_date >= current_date or end_date >= current_date:
                    serialiser = HolidayDetailDateSerializer(get_date).data
                    list_data.append(serialiser)


            res = {
                'statuscode' : 200,
                'status':'true',
                'data':list_data
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'False',
                'message':"Enter Valid Center ID."
            }                                                        
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')




@csrf_exempt
def center_list_testing_ebpf(request):
    if request.method == 'POST':
        
        get_all_center = models.CenterDetail.objects.all()
        serialiser = CenterTestSerializer(get_all_center, many=True)
        res = {
            'statuscode' : 200,
            'status':'true',
            'data':serialiser.data
        }                                                        
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json')
    

@csrf_exempt
def package_list_employee_test(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')

        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        
        if check_employee == 1:
            
            employee = models.EmployeeDetail.objects.get(id = employee)
            employee_gender = employee.gender.gender
            # employee_gender = 'All'
            get_dependent = models.EmployeeDependent.objects.filter(employee = employee.id).count()
            
            if get_dependent > 0:
                all_genders = list(models.EmployeeDependent.objects.filter(employee=employee.id).values_list('gender__gender', flat=True).distinct())
                if not employee_gender in all_genders:
                    all_genders.append(employee_gender)
            
            if 'Male' in all_genders and 'Female' in all_genders and 'All' not in all_genders:
                all_genders.append('All')

            
            gender_ids = list(models.Gender.objects.filter(gender__in=all_genders).values_list('id', flat=True))
            
            corporate = employee.corporate_id
            list_data = []
            
            package_count = models.PackageDetail.objects.filter(corporate=corporate,gender_id__in=gender_ids).count()

            get_all_package = models.PackageDetail.objects.filter(corporate=corporate,gender_id__in=gender_ids).order_by('-id')

            for package in get_all_package:
                package_data = models.PackageDetail.objects.get(id = package.id)
                serialiser = PackageDetailSerializer(package_data)
                data = serialiser.data
                center_count = models.CenterDetail.objects.filter(package = package_data).count()
                if center_count == 1:
                    center_data = models.CenterDetail.objects.get(package = package_data)
                    center_serialiser = CenterDataSerializer(center_data)
                    data.update({'center':center_serialiser.data})
                list_data.append(data)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def service_wise_package_list_employee_test(request):
        if request.method == 'POST':
            python_data = JSONParser().parse(io.BytesIO(request.body))
            employee = python_data.get('employee')
            check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
            list_data = []
            if check_employee == 1:
                employee = models.EmployeeDetail.objects.get(id = employee)
                employee_gender = employee.gender.gender
                get_dependent = models.EmployeeDependent.objects.filter(employee = employee.id).count()            
                if get_dependent > 0:
                    data_data = list(models.EmployeeDependent.objects.filter(employee=employee.id))
                    data_update = []
                    all_gender = []
                    for single_data in data_data:
                        gender = single_data.gender.gender
                        all_gender.append(gender)
                        birth_date = single_data.date_of_birth

                        try:
                            dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                            dob =  dt.strftime('%Y-%m-%d')
                        except ValueError:
                            try:
                                dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                dob = dt.strftime('%Y-%m-%d')
                            except ValueError:
                                pass


                        dob = datetime.strptime(dob, '%Y-%m-%d').date()
                        today = date.today()
                        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                        if age < 40:
                            age = 'Below 40'
                        else:
                            age = 'Above 40'

                        data_update.append((single_data.gender.gender, age))
                    
                    data_update = list(set(data_update))

                    genders = [item[0] for item in data_update]
                    
                    all_gender = list(set(all_gender))
                    data_update.append(('All', 'All'))
                    data_update.append(('All', 'Above 40'))
                    data_update.append(('All', 'Below 40'))
                    if 'Male' in all_gender:
                        data_update.append(('Male', 'All'))
                    if 'Female' in all_gender:
                        data_update.append(('Female', 'All'))
                
                data_update = list(set(data_update))
                list_id = [] 
                for gender, age_group in data_update:
                    gender_id = models.Gender.objects.filter(gender=gender).values_list('id', flat=True)[0]
                    age_category_id = models.AgeCategory.objects.filter(age_category=age_group).values_list('id', flat=True)[0]
                    list_id.append((gender_id, age_category_id))
                
                corporate = employee.corporate_id

                all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
                for service in all_service:

                    service_dictionary = {}
                    filters = Q()
                    for gender_id, age_category_id in list_id:
                        filters |= Q(gender_id=gender_id, age_category_id=age_category_id)

                    list_package_data = []
                    
                    get_all_package = models.PackageDetail.objects.filter(type_of_service=service.id,corporate = corporate).filter(filters).order_by('-id')
                    for package_data in get_all_package:
                        if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                            package_serialiser = PackageDetailSerializer(package_data)
                            list_package_data.append(package_serialiser.data)
        
                    get_all_individual_package = models.PackageDetail.objects.filter(type_of_service=service.id,package_type='Individual').filter(filters).order_by('-id')
                    for package_individual in get_all_individual_package:
                        if models.CenterDetail.objects.filter(package = package_individual.id).count() > 0:
                            serialiser = PackageDetailSerializer(package_individual)
                            list_package_data.append(serialiser.data)
                    
                    if list_package_data != []:
                        service_dictionary.update({'service':service.type_of_service, 'data':list_package_data})
                        list_data.append(service_dictionary)

            
            res = {
                'statuscode' : 200,
                'status':'true',
                'data' : list_data
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def service_wise_package_list_employee_test_two(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')
        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        list_data = []
        if check_employee == 1:
            employee = models.EmployeeDetail.objects.get(id = employee)
            corporate = employee.corporate_id

            all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
            for service in all_service:
                
                service_dictionary = {}
                list_package_data = []
                package_list = []
                get_all_package = models.PackageDetail.objects.filter(type_of_service=service.id,corporate = corporate)
                for package_data in get_all_package:
                    if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                        package = models.PackageDetail.objects.get(id = package_data.id)
                        age_category = package.age_category.age_category
                        package_gender = package.gender.gender

                        relation_data = list(package_data.relation_with_employee.values_list('relation', flat=True))
                        list_data = []
                        for relation in relation_data:

                            check_relation = models.EmployeeDependent.objects.filter(employee = employee, dependent_relation__relation = relation).count()
                            if check_relation == 1:
                                single_data = models.EmployeeDependent.objects.get(employee = employee, dependent_relation__relation = relation)
                                gender = single_data.gender.gender
                                birth_date = single_data.date_of_birth
                                
                                try:
                                    dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                                    dob =  dt.strftime('%Y-%m-%d')
                                except ValueError:
                                    try:
                                        dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                        dob = dt.strftime('%Y-%m-%d')
                                    except ValueError:
                                        pass


                                dob = datetime.strptime(dob, '%Y-%m-%d').date()
                                today = date.today()
                                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                                if age < 40:
                                    age = 'Below 40'
                                else:
                                    age = 'Above 40'

                                if (age_category == age or age_category == "All") and (package_gender == gender or package_gender == 'All'):
                                    package_list.append(package_data)

                        package_list = list(set(package_list))
                        package_serialiser = PackageDetailSerializer(package_list, many=True)
                        
                get_all_individual_package = models.PackageDetail.objects.filter(type_of_service=service.id,package_type='Individual')
                for package_data in get_all_individual_package:
                    if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                        package = models.PackageDetail.objects.get(id = package_data.id)
                        age_category = package.age_category.age_category
                        package_gender = package.gender.gender

                        relation_data = list(package_data.relation_with_employee.values_list('relation', flat=True))
                        list_data = []
                        for relation in relation_data:
                            check_relation = models.EmployeeDependent.objects.filter(employee = employee, dependent_relation__relation = relation).count()
                            if check_relation == 1:
                                single_data = models.EmployeeDependent.objects.get(employee = employee, dependent_relation__relation = relation)
                                gender = single_data.gender.gender
                                birth_date = single_data.date_of_birth
                                
                                try:
                                    dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                                    dob =  dt.strftime('%Y-%m-%d')
                                except ValueError:
                                    try:
                                        dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                        dob = dt.strftime('%Y-%m-%d')
                                    except ValueError:
                                        pass


                                dob = datetime.strptime(dob, '%Y-%m-%d').date()
                                today = date.today()
                                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                                if age < 40:
                                    age = 'Below 40'
                                else:
                                    age = 'Above 40'

                                if (age_category == age or age_category == "All") and (package_gender == gender or package_gender == 'All'):
                                    package_list.append(package_data)
                                    
                        package_list = list(set(package_list))
                        package_serialiser = PackageDetailSerializer(package_list, many=True)
                        
            if package_list != []:
                service_dictionary.update({'service':service.type_of_service, 'data':package_serialiser.data})
                list_data.append(service_dictionary)

        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def employee_to_individual_register(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        corporate_code = python_data.get('corporate_code')
        mobile = python_data.get('mobile')
        check_corporate = models.CorporateDetail.objects.filter(corporate_code = corporate_code, status= 'Inactive').count()
        if check_corporate == 1:
            get_corporate_id = models.CorporateDetail.objects.get(corporate_code = corporate_code)
            check_mobile = models.EmployeeDetail.objects.filter(mobile = mobile, corporate_id= get_corporate_id).count()
            if check_mobile == 1:
                employee = models.EmployeeDetail.objects.get(mobile = mobile).id
                
                OTP = '111111'
                now = datetime.now()
                current_date_data = now.strftime("%Y-%m-%d")
                current_time = datetime.strptime(current_date_data, '%Y-%m-%d').date()

                emp = models.EmployeeDetail.objects.get(id = employee)
                emp.status = 'Inactive'
                emp.save()
                serialiser = EmployeeDetailSerializer(emp)
                data = serialiser.data
                all_dependent = models.EmployeeDependent.objects.filter(employee = emp).order_by('id')
                dependent_serialiser = EmployeeDependentSerializer(all_dependent, many=True).data

                all_appointment = models.AppointmentDetail.objects.filter(employee = employee)
                appointment_seraliser = AppointmentDetailSerializer(all_appointment, many=True).data     

                data.update({'dependent_data':dependent_serialiser, 'appointment_data':appointment_seraliser})

                email = data['email']
                mobile = data['mobile']
                

                
                check_email = models.IndividualUserDetail.objects.filter(email = email).count()
                if check_email == 1:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Email Already registered, Please try with other.",
                        'is_email_register':"true"
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    email = email

                check_mobile = models.IndividualUserDetail.objects.filter(mobile = mobile).count()
                if check_mobile == 0:

                    user = models.IndividualUserDetail.objects.create(
                        name = data['employee_name'],
                        date_of_birth = data['date_of_birth'],
                        gender_id = data['gender'],
                        mobile = mobile,
                        email = data['email'],
                        address = data['address'],
                        pincode = data['pincode'],
                        state= data['state'],
                        city= data['city'],
                        status = 'Active',
                        created_at = current_time,
                        OTP = OTP
                    )
                    user.save()
                    individual_id = user.id

                    all_dependent_data = data['dependent_data']

                    for dependent_data in all_dependent_data:

                        
                        self_create = models.IndividualDependent.objects.create(
                            individual_id = individual_id,
                            dependent_name = dependent_data['dependent_name'],
                            dependent_relation_id = dependent_data['dependent_relation'], 
                            date_of_birth = dependent_data['date_of_birth'],
                            gender_id = dependent_data['gender'],
                            created_at = current_time
                        ).save()

                    all_appointment_data = data['appointment_data']
                    for appointment in all_appointment_data:
                        update_appointment = models.AppointmentDetail.objects.get(id = appointment['id'])
                        update_appointment.individual_id = individual_id
                        update_appointment.save()
                        
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Register Successfully.",
                        # 'data':data

                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                    

                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Mobile Number Already registered, Please try with other.",

                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        
            else:
                res = {
                    'statuscode' : 401,
                    'status':'false',
                    'message' : "Enter Mobile Number not register under this corporate.",

                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid corporate Code.",

                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def expiry_corporate_list(request):
    if request.method == 'POST':
        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()
        
        get_all_corporate = models.CorporateDetail.objects.filter(status = 'Active')
        for corporate in get_all_corporate:
            end_date = models.CorporateDetail.objects.filter(id = corporate.id).values_list('end_date', flat=True)[0]
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if current_date > end_date:
                update_corporate = models.CorporateDetail.objects.get(id = corporate.id)
                update_corporate.status = 'Inactive'
                update_corporate.save()

        get_all_package = models.PackageDetail.objects.filter(status = 'Active')
        for package in get_all_package:
            end_date = models.PackageDetail.objects.filter(id = package.id).values_list('end_date', flat=True)[0]
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if current_date > end_date:
                update_package = models.PackageDetail.objects.get(id = package.id)
                update_package.status = 'Inactive'
                update_package.save()
        
        res = {
            'statuscode' : 200,
            'status':'true',
            # 'data':serialiser.data
        }                                                        
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def user_data_svasthya(request):
    if request.method == "POST":
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            action = python_data.get('Action', '')

            # If Action is GetAllData, return all employees without validation
            if action == 'GetAllData':
                page_number = int(python_data.get('PageNumber', 1))
                page_size = int(python_data.get('PageSize', 10))

                all_employees = models.EmployeeDetail.objects.all().order_by('id')
                start = (page_number - 1) * page_size
                end = start + page_size
                employees_page = all_employees[start:end]

                employee_serializer = EmployeeDetailSerializer(employees_page, many=True).data

                res = {
                    'statuscode': 200,
                    'status': 'true',
                    'user_data': employee_serializer,
                    'total_count': all_employees.count(),
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            # For other actions, validate required params
            required_params = ['Action', 'Username', 'Password', 'PageNumber', 'PageSize', 'CorporateCode', 'EmployeeCode']
            if not all(param in python_data and python_data[param] not in [None, '', 'null'] for param in required_params):
                res = {
                    'statuscode': 400,
                    'status': 'false',
                    'message': 'Missing or invalid required parameters.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            if action != 'GetBookingDatabyEmployeeCodeAndCorporateCode':
                res = {
                    'statuscode': 400,
                    'status': 'false',
                    'message': 'Invalid Action.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            corporate_code = python_data['CorporateCode']
            employee_code = python_data['EmployeeCode']

            try:
                get_user = models.EmployeeDetail.objects.get(
                    employee_code=employee_code,
                    hr_corporate_code=corporate_code
                )
            except models.EmployeeDetail.DoesNotExist:
                res = {
                    'statuscode': 406,
                    'status': 'false',
                    'message': 'User not found with provided CorporateCode and EmployeeCode.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            employee_serializer = EmployeeDetailSerializer(get_user).data

            appointment_detail = models.AppointmentDetail.objects.filter(employee=get_user.id)
            appointment_detail_serializer = EBPFUserAppointmentSerializer(appointment_detail, many=True).data

            res = {
                'statuscode': 200,
                'status': 'true',
                'user_data': employee_serializer,
                'appointment_data': appointment_detail_serializer
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        except Exception as e:
            import traceback
            traceback.print_exc()
            res = {
                'statuscode': 500,
                'status': 'false',
                'message': 'Internal server error.'
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

    else:
        res = {
            'statuscode': 405,
            'status': 'false',
            'message': 'Method not allowed.'
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')

@csrf_exempt
def booking_list_svasthya(request):
    if request.method == "POST":
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))

            action = python_data.get('Action', '')
            username = python_data.get('Username', '')
            password = python_data.get('Password', '')
            
            if username == "VIBPLAdmin" and password == "VIBPLAdmin@#$&*12345":

                # If Action is GetAllData, return all employees without validation
                if action == 'GetAllData':
                    page_number = int(python_data.get('PageNumber', 1))
                    page_size = int(python_data.get('PageSize', 10))

                    employee_data = models.AppointmentDetail.objects.filter(employee__employee_from ='EBPF').order_by('-id')

                    start = (page_number - 1) * page_size
                    end = start + page_size
                    employees_page = employee_data[start:end]

                    employee_serializer = AppointmentDetailEBPFSerializer(employees_page, many=True).data

                    res = {
                        'statuscode': 200,
                        'status': 'true',
                        'user_data': employee_serializer,
                        'total_count': employee_data.count(),
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                
                else:
                    res = {
                        'statuscode': 400,
                        'status': 'false',
                        'message': 'Enter Valid action.'
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
            
            else:
                res = {
                    'statuscode': 400,
                    'status': 'false',
                    'message': 'Enter Valid user credntials.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

        except Exception as e:
            res = {
                'statuscode': 500,
                'status': 'false',
                'message': 'Internal server error.'
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
    else:
        res = {
            'statuscode': 405,
            'status': 'false',
            'message': 'Method not allowed.'
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')

@csrf_exempt
def employee_booking_list_svasthya(request):
    if request.method == "POST":
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))

            action = python_data.get('Action', '')
            username = python_data.get('Username', '')
            password = python_data.get('Password', '')
            employee_code = python_data.get('EmployeeCode', '')
            corporate_code = python_data.get('Corporatecode', '')

            if username == "VIBPLAdmin" and password == "VIBPLAdmin@#$&*12345":

                # If Action is GetAllData, return all employees without validation
                if action == 'GetAllData':
                    page_number = int(python_data.get('PageNumber', 1))
                    page_size = int(python_data.get('PageSize', 10))

                    check_employee = models.EmployeeDetail.objects.filter(employee_code =employee_code,corporate__corporate_code = corporate_code  ).count()
                    if check_employee == 1:
                        
                        employee_data = models.AppointmentDetail.objects.filter(employee__employee_code =employee_code)

                        start = (page_number - 1) * page_size
                        end = start + page_size
                        employees_page = employee_data[start:end]

                        employee_serializer = AppointmentDetailEBPFSerializer(employees_page, many=True).data

                        res = {
                            'statuscode': 200,
                            'status': 'true',
                            'user_data': employee_serializer,
                            'total_count': employee_data.count(),
                        }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type='application/json')
                    else:
                        res = {
                            'statuscode': 400,
                            'status': 'false',
                            'message': 'Corporate/Employee with this code not found.'
                        }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type='application/json')
                
                else:
                    res = {
                        'statuscode': 400,
                        'status': 'false',
                        'message': 'Enter Valid action.'
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
            
            else:
                res = {
                    'statuscode': 400,
                    'status': 'false',
                    'message': 'Enter Valid user credntials.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

        except Exception as e:
            res = {
                'statuscode': 500,
                'status': 'false',
                'message': 'Internal server error.'
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
    else:
        res = {
            'statuscode': 405,
            'status': 'false',
            'message': 'Method not allowed.'
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def employee_booking_detail_svasthya(request):
    if request.method == "POST":
        
        python_data = JSONParser().parse(io.BytesIO(request.body))


        action = python_data.get('Action', '')
        username = python_data.get('Username', '')
        password = python_data.get('Password', '')
        booking_id = python_data.get('BookingId', '')

        if username == "VIBPLAdmin" and password == "VIBPLAdmin@#$&*12345":

            # If Action is GetAllData, return all employees without validation
            if action == 'GetAllData':

                # page_number = int(python_data.get('PageNumber', 1))
                # page_size = int(python_data.get('PageSize', 10))

                check_data = models.AppointmentDetail.objects.filter(id =booking_id).count()
                if check_data == 1:
                    employee_data = models.AppointmentDetail.objects.get(id =booking_id)

                    # start = (page_number - 1) * page_size
                    # end = start + page_size
                    # employees_page = employee_data[start:end]

                    employee_serializer = AppointmentDetailSerializer(employee_data).data
                    
                    check_transaction = models.Transaction.objects.filter(appointment = booking_id).count()
                    if check_transaction == 1:
                        transaction = models.Transaction.objects.get(appointment = booking_id)
                        transaction_data = TransactionSerializer(transaction).data
                        employee_serializer.update({'transaction':transaction_data})

                    res = {
                        'statuscode': 200,
                        'status': 'true',
                        'user_data': employee_serializer,
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                else:
                    res = {
                        'statuscode': 400,
                        'status': 'false',
                        'message': 'Enter Valid ID.'
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
            else:
                res = {
                    'statuscode': 400,
                    'status': 'false',
                    'message': 'Enter Valid action.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            
        else:
            res = {
                'statuscode': 400,
                'status': 'false',
                'message': 'Enter Valid user credntials.'
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        
    else:
        res = {
            'statuscode': 405,
            'status': 'false',
            'message': 'Method not allowed.'
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')
           
####commneted on 13 Oct 2025 by Shubham For Fetching Bookiing Details to TPI
# @csrf_exempt
# def user_data_svasthya(request):
#     if request.method == "POST":
#         python_data = JSONParser().parse(io.BytesIO(request.body))

#         print("python_data--user_data_svasthya-->",python_data)


        
#         email = python_data.get('email',None)

#         if email not in [None,'','null']:
#             if models.IndividualUserDetail.objects.filter(email = email).exists():
#                 get_user = models.IndividualUserDetail.objects.get(email = email)

#                 user_serializer = IndividualUserDetailSerializer(get_user).data

#                 appointment_detail = models.AppointmentDetail.objects.filter(individual = get_user.id)
#                 appointment_detail_serializer = EBPFUserAppointmentSerializer(appointment_detail, many=True).data

#                 # transaction_history = models.TransactionHistory.objects.filter(user)

#                 res={
#                     'statuscode':200,
#                     'status':'true',
#                     'user_data':user_serializer,
#                     'appointment_data':appointment_detail_serializer
#                 }
#                 json_data = JSONRenderer().render(res)
#                 return HttpResponse(json_data, content_type= 'application/json')
            
#             else:
#                 res={
#                     'statuscode':406,
#                     'status':'false',
#                     'message':'User Not Exists',
#                 }
#                 json_data = JSONRenderer().render(res)
#                 return HttpResponse(json_data, content_type= 'application/json')
        
        
#         else:
#             res={
#                 'statuscode':406,
#                 'status':'false',
#                 'message':'Email Not Found',
#             }
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data, content_type= 'application/json')





@csrf_exempt
def package_export(request):
    if request.method == "POST":
        
        package_list = models.PackageDetail.objects.all().order_by('id')
        serialiser = PackageExportSerialiser(package_list, many=True).data
       

        headers = [
            'package_type',	'package_name',	'package_code',	'MRP',	'vendor',	'base_amount',	'profit',	'tax',	
            'tax_amount',	'igst',	'igst_amount',	'sgst',	'sgst_amount',	'cgst',	'cgst_amount',	'discount_price',
            'offer_price',	'corporate_selection',	'corporate',	'start_date',	'end_date','description',
            'relation_with_employee',	'status',	'created_at',	'type_of_service',	
            'type_of_visit',	'age_category',	'gender',	'billing_cycle','tags',
            'total_test_number', 'test_list']
        

        wb = op.Workbook()
        ws = wb.active
        ws.title = "Users"

        ws.append(headers) 
        field_map = {
            
            'package_type':'package_type',	
            'package_name':'package_name',	
            'package_code':'package_code',	
            'MRP':'MRP',	
            'vendor':'vendor',	
            'base_amount':'base_amount',	
            'profit':'profit',	
            'tax':'tax',	
            'tax_amount':'tax_amount',	
            'igst':'igst',	
            'igst_amount':'igst_amount',	
            'sgst':'sgst',	
            'sgst_amount':'sgst_amount',	
            'cgst':'cgst',	
            'cgst_amount':'cgst_amount',	
            'discount_price':'discount_price',	
            'offer_price':'offer_price',	
            'corporate_selection':'corporate_selection',	
            'corporate':'corporate',	
            'start_date':'start_date',	
            'end_date':'end_date',	
            'description':'description',	
            'relation_with_employee':'relation_with_employee',	
            'status':'status',	
            'created_at':'created_at',	
            'type_of_service':'type_of_service',	
            
            'type_of_visit':'type_of_visit',	
            'age_category':'age_category',	
            'gender':'gender',	
            'billing_cycle':'billing_cycle',	
            'tags':'tags',	
            'total_test_number':'total_test_number',	
            'test_list':'test_list',	
            

        }
        
        
        for row in serialiser:
            ws.append([row.get(field_map[h], "") for h in headers])
        
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="package_list.xlsx"'
        wb.save(response)

        return response



@csrf_exempt
def center_export(request):
    if request.method == "POST":
        package_list = models.CenterDetail.objects.all().order_by('id')
        serialiser = CenterExportSerialiser(package_list, many=True).data

        headers = ['type_of_service','vendor','package','center_name','address','pincode','state','city',
        'location','latitude','longitude','status','created_at']

        wb = op.Workbook()
        ws = wb.active
        ws.title = "Users"
        ws.append(headers) 
        
        field_map = {
            
            'center_name':'center_name',
            'type_of_service':'type_of_service',
            'vendor':'vendor',
            'package':'package',
            'address':'address',
            'pincode':'pincode',
            'state':'state',
            'city':'city',
            'location':'location',
            'latitude':'latitude',
            'longitude':'longitude',
            'status':'status',
            'created_at':'created_at'
            

        }
        
        
        for row in serialiser:
            ws.append([row.get(field_map[h], "") for h in headers])
        
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="center_list.xlsx"'
        wb.save(response)

        return response



@csrf_exempt
def appointment_export(request):
    if request.method == "POST":
        package_list = models.AppointmentDetail.objects.all().order_by('id')
        serialiser = AppointmentExportSerialiser(package_list, many=True).data
        
        headers = ['appointment_type','package','center','vendor','type_of_visit','employee','patient',
        'individual','individual_patient','report','appointment_date_1','appointment_date_2',
        'home_sample_date_1','home_sample_date_2','confirm_appointment_date','confirm_home_sample_date',
        'reason','remark','report_date','status','created_at']

        wb = op.Workbook()
        ws = wb.active
        ws.title = "Users"
        ws.append(headers) 
        
        field_map = {
            
            'appointment_type':'appointment_type', 
            'package':'package', 
            'center':'center', 
            'vendor':'vendor', 
            'type_of_visit':'type_of_visit', 
            'employee':'employee', 
            'patient':'patient', 
            'individual':'individual', 
            'individual_patient':'individual_patient', 
            'report':'report', 
            'appointment_date_1':'appointment_date_1', 
            'appointment_date_2':'appointment_date_2', 
            'home_sample_date_1':'home_sample_date_1', 
            'home_sample_date_2':'home_sample_date_2', 
            'confirm_appointment_date':'confirm_appointment_date', 
            'confirm_home_sample_date':'confirm_home_sample_date', 
            'reason':'reason', 
            'remark':'remark', 
            'report_date':'report_date', 
            'status':'status', 
            'created_at':'created_at'    

        }
        
        
        for row in serialiser:
            ws.append([row.get(field_map[h], "") for h in headers])
        
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="appointment_list.xlsx"'
        wb.save(response)

        return response


@csrf_exempt
def test_category_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        test_category = python_data.get('test_category')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_staff_type = models.TestCategory.objects.filter(test_category = test_category).count()
        if check_staff_type == 0:
            level = models.TestCategory.objects.create(
                test_category = test_category,
                status = 'Active',
                created_at = current_time
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Test category Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Test Category already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def test_category_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        test_category = python_data.get('test_category')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_test = models.TestCategory.objects.filter(test_category = test_category).count()
        if check_test == 0:
            test = models.TestCategory.objects.get(id = id)
            test.test_category = python_data.get('test_category', test.test_category)
            test.status = python_data.get('status', test.status)
            test.save()
                
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Test category update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            check_test = models.TestCategory.objects.filter(id = id, test_category = test_category).count()
            if check_test == 1:
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Test category update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Test Category already Created."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_test_category_list(request):
    if request.method == 'POST':
        all_staff_level = models.TestCategory.objects.all().order_by('-id')
        serialiser = TestCategoryTransaction(all_staff_level, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def test_sub_category_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        test_category = python_data.get('test_category')
        test_subcategory = python_data.get('test_subcategory')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_staff_type = models.TestSubCategory.objects.filter(test_category = test_category, test_subcategory= test_subcategory).count()
        if check_staff_type == 0:
            level = models.TestSubCategory.objects.create(
                test_category_id = test_category,
                test_subcategory = test_subcategory,
                status = 'Active',
                created_at = current_time
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Test Subcategory Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Test Subcategory already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def test_sub_category_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        test_category = python_data.get('test_category')
        test_subcategory = python_data.get('test_subcategory')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_test = models.TestSubCategory.objects.filter(test_category = test_category, test_subcategory= test_subcategory).count()
        if check_test == 0:
            test = models.TestSubCategory.objects.get(id = id)
            test.test_category_id = python_data.get('test_category', test.test_category)
            test.test_subcategory = python_data.get('test_subcategory', test.test_subcategory)
            test.status = python_data.get('status', test.status)
            test.save()
                
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Test Subcategory update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            check_test = models.TestSubCategory.objects.filter(id = id, test_category = test_category, test_subcategory= test_subcategory).count()
            if check_test == 1:
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Test Subcategory update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Test Subcategory already Created."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_test_subcategory_list(request):
    if request.method == 'POST':
        all_staff_level = models.TestSubCategory.objects.all().order_by('-id')
        serialiser = TestSubCategoryTransaction(all_staff_level, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def test_category_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_status = models.TestCategory.objects.filter(id = id).count()
        if check_status == 1:
            test_details = models.TestCategory.objects.get(id = id)
            test_details.status = status
            test_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Status Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def all_active_test_category_list(request):
    if request.method == 'POST':
        all_test = models.TestCategory.objects.filter(status='Active').order_by('-id')
        serialiser = TestCategoryTransaction(all_test, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def test_sub_category_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_status = models.TestSubCategory.objects.filter(id = id).count()
        if check_status == 1:
            test_details = models.TestSubCategory.objects.get(id = id)
            test_details.status = status
            test_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Status Delete Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def all_active_test_subcategory_list(request):
    if request.method == 'POST':
        all_test = models.TestSubCategory.objects.filter(status='Active').order_by('-id')
        serialiser = TestSubCategoryTransaction(all_test, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def compare_package(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        package = python_data.get('package')
        list_data = []
        for pack in package:
            get_details = models.PackageDetail.objects.get(id = pack)
            serialiser = ComparePackageListSerialiser(get_details).data

            category_list = models.TestsProductDetail.objects.filter(package = pack).distinct()

            list_category = []
            for category in category_list:
                list_category.append(category.test_category.id)
            list_dict_data = []
            unique_category = list(set(list_category))
            # for category in unique_category:
            #     dict_data = {}
            #     category_count = models.TestsProductDetail.objects.filter(package = pack,test_category = category, test_subcategory= None).count()
            #     category_data = models.TestCategory.objects.get(id = category)
            #     category_name = category_data.test_category
                
            #     if category_count == 1:
            #         category_value = models.TestsProductDetail.objects.get(package = pack,test_category = category)
            #         value = category_value.value
            #     else:
            #         category_value = models.TestsProductDetail.objects.filter(package = pack,test_category = category)
            #         value = TestsProductDetailSerialiser(category_value, many=True).data

            #     dict_data.update({'category_name':category_name, 'value':value})
            #     list_dict_data.append(dict_data)
            # serialiser.update({'data':list_dict_data})
            for category in unique_category:
                dict_data = {}
                category_count = models.TestsProductDetail.objects.filter(package = pack,test_category = category, test_category__status ='Active' ).count()
                category_data = models.TestCategory.objects.get(id = category)
                category_name = category_data.test_category 
                if category_count == 1:
                    category_value = models.TestsProductDetail.objects.get(package = pack,test_category = category, test_category__status ='Active', test_subcategory= None)
                    value = category_value.value
                else:
                    category_value = models.TestsProductDetail.objects.filter(package = pack,test_category = category, test_category__status ='Active', test_subcategory__status ='Active' )
                    value = TestsProductDetailSerialiser(category_value, many=True).data
                # print(value, 'value data')
                dict_data.update({'category_name':category_name, 'value':value})
                list_dict_data.append(dict_data)
            serialiser.update({'data':list_dict_data})


            list_data.append(serialiser)

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def compare_package_list(request):
    if request.method == 'POST':
        get_details = models.PackageDetail.objects.all().order_by('-id')
        serialiser = ComparePackageListSerialiser(get_details, many=True).data

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def web_service_list(request):
    if request.method == 'POST':
        get_details = models.TypeOfService.objects.all()
        serialiser = TypeOfServiceSerializer(get_details, many=True).data

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def web_package_list_home(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        service = python_data.get('service', None)

        if service == None or service == '':
            get_all_individual_package = models.PackageDetail.objects.filter(package_type='Individual', status='Active')[:10]
            serialiser = PackageDetailSerializer(get_all_individual_package, many=True).data
        else:
            individual_count = models.PackageDetail.objects.filter(type_of_service = service, package_type='Individual', status='Active').count()
            get_all_individual_package = models.PackageDetail.objects.filter(type_of_service = service, package_type='Individual', status='Active')[:10]
            serialiser = PackageDetailSerializer(get_all_individual_package, many=True).data

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def web_package_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        service = python_data.get('service', None)

        if service == None or service == '':
            get_all_individual_package = models.PackageDetail.objects.filter(package_type='Individual', status='Active')
            serialiser = PackageDetailSerializer(get_all_individual_package, many=True).data
        else:
            individual_count = models.PackageDetail.objects.filter(type_of_service = service, package_type='Individual', status='Active').count()
            get_all_individual_package = models.PackageDetail.objects.filter(type_of_service = service, package_type='Individual', status='Active')
            serialiser = PackageDetailSerializer(get_all_individual_package, many=True).data

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def package_filter_list(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        package_type = python_data.get('package_type', None)
        gender = python_data.get('gender', None)
        age_category = python_data.get('age_category', None)
        type_of_visit = python_data.get('type_of_visit', None)
        type_of_service = python_data.get('type_of_service', None)
        
        
        filter_condition = {}
        if type_of_visit != "All":
            filter_condition['type_of_visit'] = type_of_visit
        
        # if age_category != "All":
        #     filter_condition['age_category'] = age_category

        get_all_package = models.PackageDetail.objects.filter(package_type=package_type, gender = gender, **filter_condition,  type_of_service= type_of_service, status='Active')
        serialiser = ComparePackageListSerialiser(get_all_package, many=True).data
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def employee_address_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        address_check = models.EmployeeAddressDetail.objects.filter(id = id).count()
        if address_check == 1:
            address_update = models.EmployeeAddressDetail.objects.get(id = id)
            address_update.employee_id = python_data.get('employee', address_update.employee_id)
            address_update.address_type = python_data.get('address_type', address_update.address_type)
            address_update.address = python_data.get('address', address_update.address)
            address_update.latitude = python_data.get('latitude', address_update.latitude)
            address_update.longitude = python_data.get('longitude', address_update.longitude)
            address_update.state = python_data.get('state', address_update.state)
            address_update.pincode = python_data.get('pincode', address_update.pincode)
            address_update.city = python_data.get('city', address_update.city)
            address_update.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message':'Address update successfully.',
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message':'Something went wrong.',
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def employee_address_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        if models.EmployeeAddressDetail.objects.filter(employee_id = python_data.get('employee')).count() == 0:
            is_selected = True
        else:
            is_selected = False
        
        address = models.EmployeeAddressDetail.objects.create(
            employee_id = python_data.get('employee'),
            address_type = python_data.get('address_type'),
            address = python_data.get('address'),
            latitude = python_data.get('latitude'),
            longitude = python_data.get('longitude'),
            state = python_data.get('state'),
            pincode = python_data.get('pincode'),
            city = python_data.get('city'),
            mobile = python_data.get('mobile'),
            created_at = current_time,
            is_selected = is_selected
        ).save()
    
    res = {
        'statuscode' : 200,
        'status':'true',
        'message':'Address added successfully.',
        }
    json_data = JSONRenderer().render(res)
    return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def individual_address_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        if models.IndividualAddressDetail.objects.filter(individual_id = python_data.get('individual')).count() == 0:
            is_selected = True
        else:
            is_selected = False

        address = models.IndividualAddressDetail.objects.create(
            individual_id = python_data.get('individual'),
            address_type = python_data.get('address_type'),
            address = python_data.get('address'),
            latitude = python_data.get('latitude'),
            longitude = python_data.get('longitude'),
            pincode = python_data.get('pincode'),
            state = python_data.get('state'),
            city = python_data.get('city'),
            mobile = python_data.get('mobile'),
            is_selected = is_selected,
            created_at = current_time
        ).save()
    
    res = {
        'statuscode' : 200,
        'status':'true',
        'message':'Address added successfully.',
        }
    json_data = JSONRenderer().render(res)
    return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def individual_address_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        address_check = models.IndividualAddressDetail.objects.filter(id = id).count()
        if address_check == 1:
            address_update = models.IndividualAddressDetail.objects.get(id = id)
            address_update.individual_id = python_data.get('individual', address_update.individual)
            address_update.address_type = python_data.get('address_type', address_update.address_type)
            address_update.address = python_data.get('address', address_update.address)
            address_update.latitude = python_data.get('latitude', address_update.latitude)
            address_update.longitude = python_data.get('longitude', address_update.longitude)
            address_update.state = python_data.get('state', address_update.state)
            address_update.pincode = python_data.get('pincode', address_update.pincode)
            address_update.mobile = python_data.get('mobile', address_update.mobile)
            address_update.city = python_data.get('city', address_update.city)
            address_update.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message':'Address update successfully.',
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message':'Something went wrong.',
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def package_detail(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        
        package = models.PackageDetail.objects.get(id = id)
        serialiser = PackageDetailSerializer(package).data
        
        category_list = models.TestsProductDetail.objects.filter(package = package).distinct()

        list_category = []
        for category in category_list:
            list_category.append(category.test_category.id)
        list_dict_data = []
        unique_category = list(set(list_category))
        for category in unique_category:
            dict_data = {}
            category_count = models.TestsProductDetail.objects.filter(package = package,test_category = category, test_category__status ='Active' ).count()
            # category_count = models.TestsProductDetail.objects.filter(package = package,test_category = category, value = 'True').count()
            # category_value = models.TestsProductDetail.objects.filter(package = package,test_category = category).values_list('value', flat=True)[0]
            print(category_count, 'count')
            category_data = models.TestCategory.objects.get(id = category)
            category_name = category_data.test_category 
            if category_count == 1:
                category_value = models.TestsProductDetail.objects.get(package = package,test_category = category, test_category__status ='Active', test_subcategory= None)
                value = category_value.value
            else:
                category_value = models.TestsProductDetail.objects.filter(package = package,test_category = category, test_category__status ='Active', test_subcategory__status ='Active' )
                value = TestsProductDetailSerialiser(category_value, many=True).data
            # print(value, 'value data')
            dict_data.update({'category_name':category_name, 'value':value})
            list_dict_data.append(dict_data)
        serialiser.update({'data':list_dict_data})


        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def employee_address_create_temp(request):
    if request.method == 'POST':
        all_employee = models.IndividualUserDetail.objects.all()
        for emp in all_employee:
            address = models.IndividualAddressDetail.objects.create(
                individual_id = emp.id,
                address_type = 'Home',
                address = emp.address,
                state = emp.state,
                pincode = emp.pincode,
                city = emp.city,
                created_at = emp.created_at,
            ).save()
        
    res = {
        'statuscode' : 200,
        'status':'true',
        'message':'Address added successfully.',
        }
    json_data = JSONRenderer().render(res)
    return HttpResponse(json_data, content_type= 'application/json') 





@csrf_exempt
def lat_long_test(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        user_lat = float(python_data.get('user_lat'))
        user_lon = float(python_data.get('user_lon'))
        radius_km = python_data.get('radius_km')

        lat_delta = radius_km / 111
        lon_delta = radius_km / (111 * cos(radians(user_lat)))

        min_lat = user_lat - lat_delta
        max_lat = user_lat + lat_delta
        min_lon = user_lon - lon_delta
        max_lon = user_lon + lon_delta

        filter_data = models.CenterDetail.objects.filter(
            latitude__range=(min_lat, max_lat),
            longitude__range=(min_lon, max_lon)
        )
        # # print(qs, 'qs data')
        # # ---- Then calculate exact distance ----
        # filter_data = filter_data.annotate(
        #     distance=6371 * ACos(
        #         Cos(Radians(user_lat)) *
        #         Cos(Radians(F('latitude'))) *
        #         Cos(Radians(F('longitude')) - Radians(user_lon)) +
        #         Sin(Radians(user_lat)) *
        #         Sin(Radians(F('latitude')))
        #     )
        # ).filter(
        #     distance__lte=radius_km
        # ).order_by("distance")


        # filter_data = models.CenterDetail.objects.annotate(
        #     lat_f=Cast('latitude', FloatField()),
        #     lon_f=Cast('longitude', FloatField()),
        # ).annotate(
        #     distance=ExpressionWrapper(
        #         6371 * ACos(
        #             Cos(Radians(user_lat)) *
        #             Cos(Radians(F('lat_f'))) *
        #             Cos(Radians(F('lon_f')) - Radians(user_lon)) +
        #             Sin(Radians(user_lat)) *
        #             Sin(Radians(F('lat_f')))
        #         ),
        #         output_field=FloatField()
        #     )
        # )



        serialiser = CenterDetailSerialiser(filter_data, many=True).data

                
    res = {
        'statuscode' : 200,
        'status':'true',
        'data':serialiser
        }
    json_data = JSONRenderer().render(res)
    return HttpResponse(json_data, content_type= 'application/json') 





@csrf_exempt
def service_wise_package_list_employee_check(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        employee = python_data.get('employee')

        # user_lat = float(python_data.get('user_lat'))
        # user_lon = float(python_data.get('user_lon'))
        # radius_km = python_data.get('radius_km')

        # lat_delta = radius_km / 111
        # lon_delta = radius_km / (111 * cos(radians(user_lat)))

        # min_lat = user_lat - lat_delta
        # max_lat = user_lat + lat_delta
        # min_lon = user_lon - lon_delta
        # max_lon = user_lon + lon_delta


        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        list_data = []
        if check_employee == 1:
            employee = models.EmployeeDetail.objects.get(id = employee)
            corporate = employee.corporate_id

            all_service = models.TypeOfService.objects.filter(status = 'Active')
            for service in all_service:   
                service_dictionary = {}
                list_package_data = []
                package_list = []
                get_all_package = models.PackageDetail.objects.filter(type_of_service=service.id,corporate = corporate, status='Active')

                for package_data in get_all_package:
                    if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                    # if models.CenterDetail.objects.filter(package = package_data.id, latitude__range=(min_lat, max_lat),longitude__range=(min_lon, max_lon)).count() > 0:
                        package = models.PackageDetail.objects.get(id = package_data.id)
                        age_category = package.age_category.age_category
                        package_gender = package.gender.gender

                        relation_data = list(package_data.relation_with_employee.values_list('relation', flat=True))
                        for relation in relation_data:
                            check_relation = models.EmployeeDependent.objects.filter(employee = employee, dependent_relation__relation = relation).count()
                            if check_relation == 1:
                                single_data = models.EmployeeDependent.objects.get(employee = employee, dependent_relation__relation = relation)
                                gender = single_data.gender.gender
                                birth_date = single_data.date_of_birth
                                
                                try:
                                    dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                                    dob =  dt.strftime('%Y-%m-%d')
                                except ValueError:
                                    try:
                                        dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                        dob = dt.strftime('%Y-%m-%d')
                                    except ValueError:
                                        pass


                                dob = datetime.strptime(dob, '%Y-%m-%d').date()
                                today = date.today()
                                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

                                if age < 40:
                                    age = 'Below 40'
                                else:
                                    age = 'Above 40'
                                if (age_category == age or age_category == "All") and (package_gender == gender or package_gender == 'All'):
                                    package_list.append(package_data)

                        # package_list = list(set(package_list))
                        package_list = list(dict.fromkeys(package_list))
                        package_serialiser = PackageDetailSerializer(package_list, many=True)
                        
                get_all_individual_package = models.PackageDetail.objects.filter(type_of_service=service.id,package_type='Individual', status='Active')
                for package_data in get_all_individual_package:
                    if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                        package = models.PackageDetail.objects.get(id = package_data.id)
                        age_category = package.age_category.age_category
                        package_gender = package.gender.gender

                        relation_data = list(package_data.relation_with_employee.values_list('relation', flat=True))
                        for relation in relation_data:
                            check_relation = models.EmployeeDependent.objects.filter(employee = employee, dependent_relation__relation = relation).count()
                            if check_relation == 1:
                                single_data = models.EmployeeDependent.objects.get(employee = employee, dependent_relation__relation = relation)
                                gender = single_data.gender.gender
                                birth_date = single_data.date_of_birth
                                
                                try:
                                    dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                                    dob =  dt.strftime('%Y-%m-%d')
                                except ValueError:
                                    try:
                                        dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                        dob = dt.strftime('%Y-%m-%d')
                                    except ValueError:
                                        pass


                                dob = datetime.strptime(dob, '%Y-%m-%d').date()
                                today = date.today()
                                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                                if age < 40:
                                    age = 'Below 40'
                                else:
                                    age = 'Above 40'

                                if (age_category == age or age_category == "All") and (package_gender == gender or package_gender == 'All'):
                                    package_list.append(package_data)
                                    
                        # package_list = list(set(package_list))
                        package_list = list(dict.fromkeys(package_list))
                        package_serialiser = PackageDetailSerializer(package_list, many=True)
                
                if package_list != []:
                    service_dictionary.update({'service':service.type_of_service, 'data':package_serialiser.data})
                    list_data.append(service_dictionary)

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def service_wise_package_list_individual_check(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        individual = python_data.get('individual')
        flag = python_data.get('flag')
        if flag == "lat_long":
            user_lat = float(python_data.get('user_lat'))
            user_lon = float(python_data.get('user_lon'))
            radius_km = python_data.get('radius_km')
        elif flag == "address":
            address = python_data.get('address')

            individual = models.IndividualAddressDetail.objects.get(id = address)
            user_lat = individual.latitude
            user_lon = individual.longitude
        else:
            individual = models.IndividualAddressDetail.objects.get(individual = individual).first()
            user_lat = individual.latitude
            user_lon = individual.longitude

        lat_delta = radius_km / 111
        lon_delta = radius_km / (111 * cos(radians(user_lat)))

        min_lat = user_lat - lat_delta
        max_lat = user_lat + lat_delta
        min_lon = user_lon - lon_delta
        max_lon = user_lon + lon_delta
        check_individual = models.IndividualUserDetail.objects.filter(id = individual).count()
        list_data = []

        if check_individual == 1:
            individual = models.IndividualUserDetail.objects.get(id = individual)
            individual_gender = individual.gender.gender

            all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
            for service in all_service:   
                service_dictionary = {}
                list_package_data = []
                package_list = []

                get_all_individual_package = models.PackageDetail.objects.filter(type_of_service=service.id,package_type='Individual', status='Active')
                for package_data in get_all_individual_package:
                    # if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                    if models.CenterDetail.objects.filter(package = package_data.id, latitude__range=(min_lat, max_lat),longitude__range=(min_lon, max_lon)).count() > 0:
                        package = models.PackageDetail.objects.get(id = package_data.id)
                        age_category = package.age_category.age_category
                        package_gender = package.gender.gender

                        relation_data = list(package_data.relation_with_employee.values_list('relation', flat=True))
                        for relation in relation_data:
                            check_relation = models.IndividualDependent.objects.filter(individual = individual, dependent_relation__relation = relation).count()
                            if check_relation == 1:
                                single_data = models.IndividualDependent.objects.get(individual = individual, dependent_relation__relation = relation)
                                gender = single_data.gender.gender
                                birth_date = single_data.date_of_birth
                                
                                try:
                                    dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                                    dob =  dt.strftime('%Y-%m-%d')
                                except ValueError:
                                    try:
                                        dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                        dob = dt.strftime('%Y-%m-%d')
                                    except ValueError:
                                        pass


                                dob = datetime.strptime(dob, '%Y-%m-%d').date()
                                today = date.today()
                                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                                if age < 40:
                                    age = 'Below 40'
                                else:
                                    age = 'Above 40'

                                if (age_category == age or age_category == "All") and (package_gender == gender or package_gender == 'All'):
                                    package_list.append(package_data)
                                    
                        package_list = list(set(package_list))
                        package_serialiser = PackageDetailSerializer(package_list, many=True)
                
                if package_list != []:
                    service_dictionary.update({'service':service.type_of_service, 'data':package_serialiser.data})
                    list_data.append(service_dictionary)

        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def address_select_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        flag = python_data.get('flag')
        id = python_data.get('id')
        if flag == 'employee':
            address = models.EmployeeAddressDetail.objects.get(id = id)
            employee = address.employee.id
            all_employee = models.EmployeeAddressDetail.objects.filter(employee = employee)
            for emp in all_employee:
                address_update = models.EmployeeAddressDetail.objects.get(id = emp.id)
                address_update.is_selected = False
                address_update.save()
            address.is_selected = True
            address.save()

        elif flag == 'individual':
            address = models.IndividualAddressDetail.objects.get(id = id)
            individual = address.individual.id
            all_employee = models.IndividualAddressDetail.objects.filter(individual = individual)
            for emp in all_employee:
                address_update = models.IndividualAddressDetail.objects.get(id = emp.id)
                address_update.is_selected = False
                address_update.save()
            address.is_selected = True
            address.save()

    res = {
        'statuscode' : 200,
        'status':'true',
        'message':'Address added successfully.',
        }
    json_data = JSONRenderer().render(res)
    return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def individual_address_delete(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')

        address = models.IndividualAddressDetail.objects.get(id = id)
        address.delete()

        res = {
            'statuscode' : 200,
            'status':'true',
            'message':'Address Deleted.',
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def employee_address_delete(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')

        address = models.EmployeeAddressDetail.objects.get(id = id)
        address.delete()

        res = {
            'statuscode' : 200,
            'status':'true',
            'message':'Address Deleted.',
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def package_filter_list_check(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        package_type = python_data.get('package_type', None)
        gender = python_data.get('gender', None)
        age_category = python_data.get('age_category', None)
        type_of_visit = python_data.get('type_of_visit', None)
        type_of_service = python_data.get('type_of_service', None)
        radius_km = 10
        filter_condition = {}
        if type_of_visit != "All":
            filter_condition['type_of_visit'] = type_of_visit
        
        gender_data = models.Gender.objects.get(id = gender).gender
        if gender_data != "All":
            filter_condition['gender'] = gender
        
        if package_type == "Corporate": 
            employee = python_data.get('employee')
            flag = python_data.get('flag')
            if flag == "lat_long":
                user_lat = float(python_data.get('user_lat'))
                user_lon = float(python_data.get('user_lon'))
                radius_km = 10
            elif flag == "address":

                address = python_data.get('address')

                employee = models.EmployeeAddressDetail.objects.get(id = address)
                user_lat = float(employee.latitude)
                user_lon = float(employee.longitude)
            else:
                employee = models.EmployeeAddressDetail.objects.get(employee = employee).first()
                user_lat = float(employee.latitude)
                user_lon = float(employee.longitude)

        elif package_type == "Individual": 
            individual = python_data.get('individual', None)  
            employee = python_data.get('employee', None)

            flag = python_data.get('flag')
            if flag == "lat_long":
                user_lat = float(python_data.get('user_lat'))
                user_lon = float(python_data.get('user_lon'))
                radius_km = 10
            elif flag == "address":

                address = python_data.get('address')

                if individual:
                    individual = models.IndividualAddressDetail.objects.get(id = address)
                    user_lat = float(individual.latitude)
                    user_lon = float(individual.longitude)
                    
                else:
                    employee = models.EmployeeAddressDetail.objects.get(id = address)
                    user_lat = float(employee.latitude)
                    user_lon = float(employee.longitude)
            else:
                if individual:
                    individual = models.IndividualAddressDetail.objects.get(individual = individual).first()
                    user_lat = float(individual.latitude)
                    user_lon = float(individual.longitude)
                else:
                    employee = models.EmployeeAddressDetail.objects.get(id = address)
                    user_lat = float(employee.latitude)
                    user_lon = float(employee.longitude)
        
        
        lat_delta = radius_km / 111
        lon_delta = radius_km / (111 * cos(radians(user_lat)))

        min_lat = user_lat - lat_delta
        max_lat = user_lat + lat_delta
        min_lon = user_lon - lon_delta
        max_lon = user_lon + lon_delta

        list_data = []
        get_all_package = models.PackageDetail.objects.filter(package_type=package_type, **filter_condition,  type_of_service= type_of_service, status='Active')
        for package in get_all_package:
            if models.CenterDetail.objects.filter(package = package.id, latitude__range=(min_lat, max_lat),longitude__range=(min_lon, max_lon)).count() > 0:
                package = models.PackageDetail.objects.get(id = package.id)
                serialiser = ComparePackageListSerialiser(package).data
                list_data.append(serialiser)

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data,
            'flag':flag
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def service_wise_package_list_individual_check_test(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        individual = python_data.get('individual')
        flag = python_data.get('flag')
        if flag == "lat_long":
            user_lat = float(python_data.get('user_lat'))
            user_lon = float(python_data.get('user_lon'))
            radius_km = python_data.get('radius_km')
        elif flag == "address":
            address = python_data.get('address')

            individual = models.IndividualAddressDetail.objects.get(id = address)
            user_lat = individual.latitude
            user_lon = individual.longitude
        else:
            individual = models.IndividualAddressDetail.objects.get(individual = individual).first()
            user_lat = individual.latitude
            user_lon = individual.longitude

        lat_delta = radius_km / 111
        lon_delta = radius_km / (111 * cos(radians(user_lat)))

        min_lat = user_lat - lat_delta
        max_lat = user_lat + lat_delta
        min_lon = user_lon - lon_delta
        max_lon = user_lon + lon_delta

        package_type = python_data.get('package_type', None)
        gender = python_data.get('gender', None)
        age_category = python_data.get('age_category', None)
        type_of_visit = python_data.get('type_of_visit', None)
        type_of_service = python_data.get('type_of_service', None)

        filter_condition = {}
        if type_of_visit != "All":
            filter_condition['type_of_visit'] = type_of_visit


        check_individual = models.IndividualUserDetail.objects.filter(id = individual).count()
        list_data = []

        if check_individual == 1:
            individual = models.IndividualUserDetail.objects.get(id = individual)
            individual_gender = individual.gender.gender

            if type_of_service == None:
                all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
                for service in all_service:   
                    service_dictionary = {}
                    list_package_data = []
                    package_list = []

                    get_all_individual_package = models.PackageDetail.objects.filter(type_of_service=service.id,package_type='Individual', status='Active')
                    for package_data in get_all_individual_package:
                        # if models.CenterDetail.objects.filter(package = package_data.id).count() > 0:
                        if models.CenterDetail.objects.filter(package = package_data.id, latitude__range=(min_lat, max_lat),longitude__range=(min_lon, max_lon)).count() > 0:
                            package = models.PackageDetail.objects.get(id = package_data.id)
                            age_category = package.age_category.age_category
                            package_gender = package.gender.gender

                            relation_data = list(package_data.relation_with_employee.values_list('relation', flat=True))
                            for relation in relation_data:
                                check_relation = models.IndividualDependent.objects.filter(individual = individual, dependent_relation__relation = relation).count()
                                if check_relation == 1:
                                    single_data = models.IndividualDependent.objects.get(individual = individual, dependent_relation__relation = relation)
                                    gender = single_data.gender.gender
                                    birth_date = single_data.date_of_birth
                                    
                                    try:
                                        dt = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
                                        dob =  dt.strftime('%Y-%m-%d')
                                    except ValueError:
                                        try:
                                            dt = datetime.strptime(birth_date, '%Y-%m-%d')
                                            dob = dt.strftime('%Y-%m-%d')
                                        except ValueError:
                                            pass


                                    dob = datetime.strptime(dob, '%Y-%m-%d').date()
                                    today = date.today()
                                    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                                    if age < 40:
                                        age = 'Below 40'
                                    else:
                                        age = 'Above 40'

                                    if (age_category == age or age_category == "All") and (package_gender == gender or package_gender == 'All'):
                                        package_list.append(package_data)
                                        
                            package_list = list(set(package_list))
                            package_serialiser = PackageDetailSerializer(package_list, many=True)
                    
                    if package_list != []:
                        service_dictionary.update({'service':service.type_of_service, 'data':package_serialiser.data})
                        list_data.append(service_dictionary)

            
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def package_detail_slug(request, slug):
    if request.method == 'POST':
        package = models.PackageDetail.objects.get(slug = slug)
        serialiser = PackageDetailSerializer(package).data
        
        category_list = models.TestsProductDetail.objects.filter(package = package).distinct()
        list_category = []
        for category in category_list:
            list_category.append(category.test_category.id)
        list_dict_data = []
        unique_category = list(set(list_category))
        # for category in unique_category:
        #     dict_data = {}
        #     category_count = models.TestsProductDetail.objects.filter(package = package,test_category = category, test_subcategory= None).count()
        #     category_data = models.TestCategory.objects.get(id = category)
        #     category_name = category_data.test_category
        #     print()
        #     if category_count == 1:
        #         category_value = models.TestsProductDetail.objects.get(package = package,test_category = category, test_subcategory= None)
        #         value = category_value.value
        #     else:
        #         category_value = models.TestsProductDetail.objects.filter(package = package,test_category = category, test_subcategory= None)
        #         value = TestsProductDetailSerialiser(category_value, many=True).data

        #     dict_data.update({'category_name':category_name, 'value':value})
        #     list_dict_data.append(dict_data)
        # serialiser.update({'data':list_dict_data})


        for category in unique_category:
            dict_data = {}
            category_count = models.TestsProductDetail.objects.filter(package = package,test_category = category, test_category__status ='Active' ).count()
            category_data = models.TestCategory.objects.get(id = category)
            category_name = category_data.test_category 
            if category_count == 1:
                category_value = models.TestsProductDetail.objects.get(package = package,test_category = category, test_category__status ='Active', test_subcategory= None)
                value = category_value.value
            else:
                category_value = models.TestsProductDetail.objects.filter(package = package,test_category = category, test_category__status ='Active', test_subcategory__status ='Active' )
                value = TestsProductDetailSerialiser(category_value, many=True).data
            # print(value, 'value data')
            dict_data.update({'category_name':category_name, 'value':value})
            list_dict_data.append(dict_data)
        serialiser.update({'data':list_dict_data})


        res = {
            'statuscode' : 200,
            'status':'true',
            'data':serialiser
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def search_package_individual(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        search = python_data.get('search')
        
        package = models.PackageDetail.objects.filter(package_name__icontains = search, status= 'Active')
        serialiser = PackageNameSerializer(package, many=True).data
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data':serialiser
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


# ============================================================
# DARWINBOX ACCESS TOKEN
# ============================================================

def get_darwinbox_access_token(flag):

    if flag is True:
        payload = {
            "grant_type": "client_credentials",
            "client_id": settings.DARWINBOX_CLIENT_ID,
            "client_secret": settings.DARWINBOX_REPORT_CLIENT_SECRET,
        }

    else:
        payload = {
            "grant_type": "client_credentials",
            "client_id": settings.DARWINBOX_CLIENT_ID,
            "client_secret": settings.DARWINBOX_IMPORT_CLIENT_SECRET,
        }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        settings.DARWINBOX_TOKEN_URL,
        data=payload,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    token_data = response.json()

    access_token = token_data.get("access_token")

    if not access_token:
        raise KeyError("access_token")

    return access_token


# ============================================================
# DARWINBOX REPORT DATA + DATABASE IMPORT
# ============================================================

@csrf_exempt
def darwinbox_report_data(request):

    # python_data = JSONParser().parse(io.BytesIO(request.body))
    # report_id = python_data.get("report_id")
    # get_latest_report = python_data.get("get_latest_report", 1)

    report_id = "4789d215e4aa8a"
    get_latest_report = 1
    # --------------------------------------------------------
    # Validate report_id
    # --------------------------------------------------------

    if not report_id:
        res = {
                "status": False,
                "message": "report_id is required",
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

    try:

        # ====================================================
        # STEP 1: Get Darwinbox OAuth token
        # ====================================================

        access_token = get_darwinbox_access_token(flag=True)

        # ====================================================
        # STEP 2: Prepare report payload
        # ====================================================

        payload = {
            "report_id": report_id,
            "get_latest_report": get_latest_report,
        }

        # ====================================================
        # STEP 3: Prepare headers
        # ====================================================
        print('Test 1')
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        if getattr(settings, "DARWINBOX_COOKIE", None):
            headers["Cookie"] = settings.DARWINBOX_COOKIE

        # ====================================================
        # STEP 4: Get report information
        # ====================================================

        response = requests.post(
            settings.DARWINBOX_REPORT_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()
        print('Test 2')

        # ====================================================
        # STEP 5: Parse Darwinbox response
        # ====================================================

        try:
            response_data = response.json()

        except ValueError:

            res = {
                    "status": False,
                    "message": "Invalid response received from Darwinbox",
                    "raw_response": response.text,
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        # ====================================================
        # STEP 6: Get download URL
        # ====================================================
        print('Test 3')
        
        download_url = (
            response_data
            .get("response", {})
            .get("data_download_link")
        )

        if not download_url:

            res = {
                    "status": False,
                    "message": "data_download_link not found",
                    "darwinbox_response": response_data,
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 

        # ====================================================
        # STEP 7: Download CSV from Darwinbox
        # ====================================================
        print('Test 4')

        download_response = requests.get(
            download_url,
            timeout=60,
        )

        download_response.raise_for_status()

        # ====================================================
        # STEP 8: Read CSV
        # ====================================================

        csv_content = download_response.content.decode(
            "utf-8-sig"
        )

        csv_file = io.StringIO(csv_content)

        reader = csv.DictReader(csv_file)

        rows = list(reader)

        # ====================================================
        # STEP 9: Import into database
        # ====================================================

        created_count = 0
        updated_count = 0
        failed_count = 0

        errors = []

        with transaction.atomic():

            for row_number, row in enumerate(
                rows,
                start=2
            ):
                print(row_number, row, 'data fetch ')
                try:

                    # ----------------------------------------
                    # Get Darwinbox values
                    # ----------------------------------------

                    company = (
                        row.get("Company") or ""
                    ).strip()

                    employee_id = (
                        row.get("Employee Id") or ""
                    ).strip()

                    unique_user_id = (
                        row.get("Unique User Id") or ""
                    ).strip()

                    first_name = (
                        row.get("First Name") or ""
                    ).strip()

                    last_name = (
                        row.get("Last Name") or ""
                    ).strip()

                    gender = (
                        row.get("Gender") or ""
                    ).strip()

                    date_of_birth = (
                        row.get("Date Of Birth") or ""
                    ).strip()

                    date_of_joining = (
                        row.get("Date Of Joining") or ""
                    ).strip()

                    personal_email = (
                        row.get("Personal Email Id") or ""
                    ).strip()

                    personal_mobile = (
                        row.get("Personal Mobile Number") or ""
                    ).strip()

                    office_location = (
                        row.get("Office Location") or ""
                    ).strip()

                    # ----------------------------------------
                    # Validate unique user id
                    # ----------------------------------------

                    if not unique_user_id:

                        failed_count += 1

                        errors.append({
                            "row": row_number,
                            "error": "Unique User Id is missing",
                        })

                        continue

                    # ----------------------------------------
                    # Convert dates
                    # ----------------------------------------

                    dob = None
                    doj = None

                    if date_of_birth:

                        dob = datetime.strptime(
                            date_of_birth,
                            "%d-%m-%Y"
                        ).date()

                    if date_of_joining:

                        doj = datetime.strptime(
                            date_of_joining,
                            "%d-%m-%Y"
                        ).date()

                    # ==================================================
                    # DATABASE CODE GOES HERE
                    # ==================================================

                    # Example:
                    #
                    employee, created = models.HohEmployee.objects.update_or_create(
                        unique_user_id=unique_user_id,
                        defaults={
                            "company": company,
                            "employee_id": employee_id or None,
                            "first_name": first_name,
                            "last_name": last_name,
                            "gender": gender,
                            "date_of_birth": dob,
                            "date_of_joining": doj,
                            "personal_email": personal_email,
                            "personal_mobile": personal_mobile,
                            "office_location": office_location,
                        }
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                    # ==================================================
                    # TEMPORARY
                    # Remove after adding your actual model
                    # ==================================================

                    created_count += 1

                except Exception as row_error:

                    failed_count += 1

                    errors.append({
                        "row": row_number,
                        "error": str(row_error),
                    })

        # ====================================================
        # STEP 10: Return response
        # ====================================================

        res = {
                "status": True,
                "message": "Darwinbox report fetched and processed successfully",
                "download_url":download_url,
                "report": {
                    "report_id": report_id,
                    "report_name": (
                        response_data
                        .get("response", {})
                        .get("summary", {})
                        .get("report_name")
                    ),
                    "data_count": (
                        response_data
                        .get("response", {})
                        .get("summary", {})
                        .get("data_count")
                    ),
                },

                "import": {
                    "total_records": len(rows),
                    "created": created_count,
                    "updated": updated_count,
                    "failed": failed_count,
                },

                "errors": errors,
            }

        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

    # ========================================================
    # EXCEPTIONS
    # ========================================================

    except requests.exceptions.Timeout:

        res = {
                "status": False,
                "message": "Darwinbox API request timed out",
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

    except requests.exceptions.HTTPError as e:

        res = {
                "status": False,
                "message": "Darwinbox API authentication/request failed",
                "error": str(e),
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

    except KeyError:

        res = {
                "status": False,
                "message": "Access token was not returned by Darwinbox",
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

    except requests.exceptions.RequestException as e:

        res = {
                "status": False,
                "message": "Unable to connect to Darwinbox",
                "error": str(e),
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

    except Exception as e:

        res = {
                "status": False,
                "message": "Something went wrong",
                "error": str(e),
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 
    
# ============================================================
# DARWINBOX IMPORT DATA
# ============================================================

@csrf_exempt
def darwinbox_import_data(request):
    python_data = JSONParser().parse(io.BytesIO(request.body))
    import_id = python_data.get("import_id")
    group_company = python_data.get("group_company")
    import_data = python_data.get("import_data")


    # --------------------------------------------------------
    # Validate import_id
    # --------------------------------------------------------

    if not import_id:
        res = {
                "status": False,
                "message": "import_id is required",
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

    # --------------------------------------------------------
    # Validate group_company
    # --------------------------------------------------------

    if not group_company:
        res = {
                "status": False,
                "message": "group_company is required",
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

    # --------------------------------------------------------
    # Validate import_data
    # --------------------------------------------------------

    if not isinstance(import_data, list):
        res = {
                "status": False,
                "message": "import_data must be a list",
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

    try:

        # ----------------------------------------------------
        # Step 1: Get OAuth access token
        # ----------------------------------------------------

        access_token = get_darwinbox_access_token(flag=False)

        # ----------------------------------------------------
        # Step 2: Prepare payload
        # ----------------------------------------------------

        payload = {
            "api_key": settings.DARWINBOX_IMPORT_API_KEY,
            "import_id": import_id,
            "group_company": group_company,
            "import_data": import_data,
        }

        # ----------------------------------------------------
        # Step 3: Prepare headers
        # ----------------------------------------------------

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        # Add Cookie only if configured
        if getattr(settings, "DARWINBOX_COOKIE", None):
            headers["Cookie"] = settings.DARWINBOX_COOKIE

        # ----------------------------------------------------
        # Step 4: Call Darwinbox Import API
        # ----------------------------------------------------

        response = requests.post(
            settings.DARWINBOX_IMPORT_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )

        # ----------------------------------------------------
        # Step 5: Parse response
        # ----------------------------------------------------

        try:
            response_data = response.json()

        except ValueError:
            response_data = {
                "raw_response": response.text
            }

        print(
            "Darwinbox Import Status:",
            response.status_code
        )

        print(
            "Darwinbox Import Response:",
            response_data
        )

        # ----------------------------------------------------
        # Return Darwinbox response
        # ----------------------------------------------------

        # return Response(
        #     response_data,
        #     status=response.status_code,
        # )
        json_data = JSONRenderer().render(response_data)
        return HttpResponse(json_data, content_type= 'application/json') 

    except requests.exceptions.Timeout:

        res = {
                "status": False,
                "message": "Darwinbox API request timed out",
            }
        json_data = JSONRenderer().render(response_data)
        return HttpResponse(json_data, content_type= 'application/json') 

    except requests.exceptions.HTTPError as e:

        res = {
                "status": False,
                "message": "Darwinbox authentication/request failed",
                "error": str(e),
            }
        json_data = JSONRenderer().render(response_data)
        return HttpResponse(json_data, content_type= 'application/json') 

    except KeyError:

        res = {
                "status": False,
                "message": "Access token was not returned by Darwinbox",
            }
        json_data = JSONRenderer().render(response_data)
        return HttpResponse(json_data, content_type= 'application/json') 

    except requests.exceptions.RequestException as e:

        res = {
                "status": False,
                "message": "Unable to connect to Darwinbox",
                "error": str(e),
            }
        json_data = JSONRenderer().render(response_data)
        return HttpResponse(json_data, content_type= 'application/json') 

    except Exception as e:

        res = {
                "status": False,
                "message": "Something went wrong",
                "error": str(e),
            }
        json_data = JSONRenderer().render(response_data)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def all_hoh_employee_list(request):
    if request.method == 'POST':
        hoh_employee = models.HohEmployee.objects.all().order_by('-id')
        serialiser = HohEmployeeSerializer(hoh_employee, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
       
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


# ============================================================
# SWAGGER SCHEMAS FOR DARWINBOX & APPOINTMENT APIS
# ============================================================

candidate_appointment_create_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['hoh_employee', 'package'],
    properties={
        'hoh_employee': openapi.Schema(type=openapi.TYPE_INTEGER, description='Candidate ID (HohEmployee ID)', example=1),
        'package': openapi.Schema(type=openapi.TYPE_INTEGER, description='Package ID (PackageDetail ID)', example=2),
        'center': openapi.Schema(type=openapi.TYPE_INTEGER, description='Diagnostic Center ID (CenterDetail ID)', example=1),
        'vendor': openapi.Schema(type=openapi.TYPE_INTEGER, description='Vendor ID (optional, auto-derived from package)', example=1),
        'type_of_visit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Type of Visit ID (optional, auto-derived from package)', example=1),
        'appointment_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 1 (YYYY-MM-DD)', example='2026-10-15'),
        'appointment_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 2 (YYYY-MM-DD)', example='2026-10-16'),
        'home_sample_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 1 (YYYY-MM-DD)', example='2026-10-14'),
        'home_sample_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 2 (YYYY-MM-DD)', example='2026-10-15'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status (default: Request Received)', example='Request Received'),
        'reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason / Note', example='Annual Pre-Employment checkup'),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description='Additional remark', example='Fasting required'),
    }
)

candidate_appointment_update_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['id'],
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='DarwinboxCandidateAppointment ID', example=1),
        'hoh_employee': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Candidate ID', example=1),
        'package': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Package ID', example=2),
        'center': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Center ID', example=1),
        'vendor': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Vendor ID', example=1),
        'type_of_visit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated Type of Visit ID', example=1),
        'appointment_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 1', example='2026-10-15'),
        'appointment_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 2', example='2026-10-16'),
        'home_sample_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 1', example='2026-10-14'),
        'home_sample_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 2', example='2026-10-15'),
        'confirm_appointment_date': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmed checkup date', example='2026-10-15'),
        'confirm_home_sample_date': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmed home sample date', example='2026-10-14'),
        'date_of_appointment': openapi.Schema(type=openapi.TYPE_STRING, description='Date of appointment', example='2026-10-15'),
        'reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason', example='Updated schedule'),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description='Remark', example='Morning slot'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status', example='Confirmed'),
        'report_date': openapi.Schema(type=openapi.TYPE_STRING, description='Report date', example='2026-10-17'),
    }
)

candidate_appointment_reschedule_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['appointment', 'status'],
    properties={
        'appointment': openapi.Schema(type=openapi.TYPE_INTEGER, description='DarwinboxCandidateAppointment ID (or id)', example=1),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status: "Confirmed" or "Rescheduled"', example='Rescheduled'),
        'confirm_appointment_date': openapi.Schema(type=openapi.TYPE_STRING, description='New appointment date (YYYY-MM-DD)', example='2026-10-20'),
        'confirm_home_sample_date': openapi.Schema(type=openapi.TYPE_STRING, description='New home sample date (YYYY-MM-DD)', example='2026-10-19'),
        'rescheduled_by': openapi.Schema(type=openapi.TYPE_STRING, description='Role/entity that rescheduled (Staff / Candidate / Vendor / Admin)', example='Staff'),
        'reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason for reschedule', example='Candidate requested later date due to travel'),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description='Remark', example='Rescheduled to next Monday 9 AM'),
        'center': openapi.Schema(type=openapi.TYPE_INTEGER, description='Center ID if center changed', example=1),
    }
)

candidate_appointment_cancel_done_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['appointment', 'status'],
    properties={
        'appointment': openapi.Schema(type=openapi.TYPE_INTEGER, description='DarwinboxCandidateAppointment ID (or id)', example=1),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status: "Reports Uploaded" or "Cancel"', example='Reports Uploaded'),
        'report': openapi.Schema(type=openapi.TYPE_FILE, description='PDF/Image health checkup report file'),
        'report_date': openapi.Schema(type=openapi.TYPE_STRING, description='Date report was generated/uploaded (YYYY-MM-DD)', example='2026-10-21'),
        'reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason for cancellation (if status is Cancel)', example='Candidate declined offer'),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description='Additional remarks', example='Normal results'),
    }
)

candidate_appointment_date_update_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['id'],
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='DarwinboxCandidateAppointment ID', example=1),
        'appointment_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 1', example='2026-10-22'),
        'appointment_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 2', example='2026-10-23'),
        'home_sample_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 1', example='2026-10-21'),
        'home_sample_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 2', example='2026-10-22'),
    }
)

candidate_appointment_id_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['id'],
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='DarwinboxCandidateAppointment ID', example=1),
    }
)

candidate_appointment_full_manage_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    description='Comprehensive endpoint accepting ALL DarwinboxCandidateAppointment & Reschedule parameters in a single API call.',
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Appointment ID (optional, updates if provided, creates if omitted)', example=1),
        'hoh_employee': openapi.Schema(type=openapi.TYPE_INTEGER, description='Candidate ID (HohEmployee ID)', example=1),
        'package': openapi.Schema(type=openapi.TYPE_INTEGER, description='Package ID (PackageDetail ID)', example=2),
        'center': openapi.Schema(type=openapi.TYPE_INTEGER, description='Diagnostic Center ID (CenterDetail ID)', example=1),
        'vendor': openapi.Schema(type=openapi.TYPE_INTEGER, description='Vendor ID (VendorDetail ID)', example=1),
        'type_of_visit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Type of Visit ID (TypeOfVisit ID)', example=1),
        'appointment_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 1', example='2026-10-15'),
        'appointment_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred checkup date 2', example='2026-10-16'),
        'home_sample_date_1': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 1', example='2026-10-14'),
        'home_sample_date_2': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred home sample date 2', example='2026-10-15'),
        'confirm_appointment_date': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmed checkup date', example='2026-10-15'),
        'confirm_home_sample_date': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmed home sample date', example='2026-10-14'),
        'date_of_appointment': openapi.Schema(type=openapi.TYPE_STRING, description='Date of appointment', example='2026-10-15'),
        'new_appointment_date': openapi.Schema(type=openapi.TYPE_STRING, description='New appointment date (for reschedule audit)', example='2026-10-20'),
        'new_home_sample_date': openapi.Schema(type=openapi.TYPE_STRING, description='New home sample date (for reschedule audit)', example='2026-10-19'),
        'rescheduled_by': openapi.Schema(type=openapi.TYPE_STRING, description='Role/person who rescheduled (Staff/Candidate/Vendor)', example='Staff'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status: Request Received | Confirmed | Rescheduled | Reports Uploaded | Cancel', example='Confirmed'),
        'reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason note', example='Pre-employment checkup'),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description='Additional remark', example='Confirmed for 10 AM'),
        'report_date': openapi.Schema(type=openapi.TYPE_STRING, description='Report upload date', example='2026-10-21'),
    }
)


# ============================================================
# DARWINBOX CANDIDATE APPOINTMENT VIEWS
# ============================================================

@swagger_auto_schema(
    method='post',
    operation_description="Create a new Darwinbox candidate appointment with candidate ID, package, center, preferred dates, and notes.",
    request_body=candidate_appointment_create_schema,
    responses={200: "Success response with created appointment data"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_create(request):
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            hoh_employee = python_data.get('hoh_employee') or python_data.get('hoh_employee_id')
            package = python_data.get('package') or python_data.get('package_id')
            center = python_data.get('center') or python_data.get('center_id')
            vendor = python_data.get('vendor') or python_data.get('vendor_id')
            type_of_visit = python_data.get('type_of_visit') or python_data.get('type_of_visit_id')
            appointment_date_1 = python_data.get('appointment_date_1') or python_data.get('health_checkup_date')
            appointment_date_2 = python_data.get('appointment_date_2')
            home_sample_date_1 = python_data.get('home_sample_date_1')
            home_sample_date_2 = python_data.get('home_sample_date_2')

            now = datetime.now()
            current_date_data = now.strftime('%Y-%m-%d')
            current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()

            if package:
                package_obj = models.PackageDetail.objects.filter(id=package).first()
                if package_obj:
                    if not vendor and package_obj.vendor_id:
                        vendor = package_obj.vendor_id
                    if not type_of_visit and package_obj.type_of_visit_id:
                        type_of_visit = package_obj.type_of_visit_id

            status = python_data.get('status', 'Request Received')

            appointment = models.DarwinboxCandidateAppointment.objects.create(
                hoh_employee_id=hoh_employee,
                package_id=package,
                center_id=center,
                vendor_id=vendor,
                type_of_visit_id=type_of_visit,
                appointment_date_1=appointment_date_1,
                appointment_date_2=appointment_date_2,
                home_sample_date_1=home_sample_date_1,
                home_sample_date_2=home_sample_date_2,
                reason=python_data.get('reason'),
                remark=python_data.get('remark') or python_data.get('remarks'),
                status=status,
                created_at=str(current_date)
            )

            serializer = DarwinboxCandidateAppointmentSerializer(appointment)
            res = {
                'statuscode': 200,
                'status': 'true',
                'message': 'Darwinbox candidate appointment created successfully',
                'data': serializer.data
            }
        except Exception as e:
            res = {
                'statuscode': 400,
                'status': 'false',
                'message': str(e)
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='post',
    operation_description="Update any fields of an existing Darwinbox candidate appointment.",
    request_body=candidate_appointment_update_schema,
    responses={200: "Success response with updated appointment data"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_update(request):
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('id') or python_data.get('appointment')
            
            if not appointment_id:
                res = {'statuscode': 400, 'status': 'false', 'message': 'id is required'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).first()
            if not appointment:
                res = {'statuscode': 404, 'status': 'false', 'message': 'Appointment not found'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            if 'hoh_employee_id' in python_data or 'hoh_employee' in python_data:
                emp_id = python_data.get('hoh_employee_id') or python_data.get('hoh_employee')
                appointment.hoh_employee = models.HohEmployee.objects.filter(id=emp_id).first() if emp_id else None

            if 'vendor_id' in python_data or 'vendor' in python_data:
                vendor_id = python_data.get('vendor_id') or python_data.get('vendor')
                appointment.vendor = models.VendorDetail.objects.filter(id=vendor_id).first() if vendor_id else None

            if 'package_id' in python_data or 'package' in python_data:
                package_id = python_data.get('package_id') or python_data.get('package')
                appointment.package = models.PackageDetail.objects.filter(id=package_id).first() if package_id else None

            if 'center_id' in python_data or 'center' in python_data:
                center_id = python_data.get('center_id') or python_data.get('center')
                appointment.center = models.CenterDetail.objects.filter(id=center_id).first() if center_id else None

            if 'type_of_visit_id' in python_data or 'type_of_visit' in python_data:
                type_of_visit_id = python_data.get('type_of_visit_id') or python_data.get('type_of_visit')
                appointment.type_of_visit = models.TypeOfVisit.objects.filter(id=type_of_visit_id).first() if type_of_visit_id else None

            if 'appointment_date_1' in python_data:
                appointment.appointment_date_1 = python_data.get('appointment_date_1')
            if 'appointment_date_2' in python_data:
                appointment.appointment_date_2 = python_data.get('appointment_date_2')
            if 'home_sample_date_1' in python_data:
                appointment.home_sample_date_1 = python_data.get('home_sample_date_1')
            if 'home_sample_date_2' in python_data:
                appointment.home_sample_date_2 = python_data.get('home_sample_date_2')
            if 'confirm_appointment_date' in python_data:
                appointment.confirm_appointment_date = python_data.get('confirm_appointment_date')
            if 'confirm_home_sample_date' in python_data:
                appointment.confirm_home_sample_date = python_data.get('confirm_home_sample_date')
            if 'date_of_appointment' in python_data:
                appointment.date_of_appointment = python_data.get('date_of_appointment')
            if 'reason' in python_data:
                appointment.reason = python_data.get('reason')
            if 'remark' in python_data or 'remarks' in python_data:
                appointment.remark = python_data.get('remark') or python_data.get('remarks')
            if 'status' in python_data:
                appointment.status = python_data.get('status')
            if 'report_date' in python_data:
                appointment.report_date = python_data.get('report_date')

            appointment.save()
            serializer = DarwinboxCandidateAppointmentSerializer(appointment)
            res = {
                'statuscode': 200,
                'status': 'true',
                'message': 'Darwinbox candidate appointment updated successfully',
                'data': serializer.data
            }
        except Exception as e:
            res = {
                'statuscode': 400,
                'status': 'false',
                'message': str(e)
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    methods=['get', 'post'],
    operation_description="Get list of all Darwinbox candidate appointments (ordered by newest first).",
    responses={200: "List of DarwinboxCandidateAppointment records"}
)
@api_view(['GET', 'POST'])
@csrf_exempt
def all_darwinbox_candidate_appointment_list(request):
    if request.method in ['POST', 'GET']:
        appointments = models.DarwinboxCandidateAppointment.objects.all().order_by('-id')
        serializer = DarwinboxCandidateAppointmentSerializer(appointments, many=True)
        res = {
            'statuscode': 200,
            'status': 'true',
            'data': serializer.data
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='get',
    operation_description="Get detailed view of a single Darwinbox candidate appointment by ID.",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="Appointment ID", type=openapi.TYPE_INTEGER),
    ],
    responses={200: "DarwinboxCandidateAppointment details"}
)
@swagger_auto_schema(
    method='post',
    operation_description="Get detailed view of a single Darwinbox candidate appointment by ID.",
    request_body=candidate_appointment_id_schema,
    responses={200: "DarwinboxCandidateAppointment details"}
)
@api_view(['GET', 'POST'])
@csrf_exempt
def get_darwinbox_candidate_appointment_detail(request):
    if request.method in ['POST', 'GET']:
        if request.method == 'POST':
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('id') or python_data.get('appointment')
        else:
            appointment_id = request.GET.get('id') or request.GET.get('appointment')

        if not appointment_id:
            res = {'statuscode': 400, 'status': 'false', 'message': 'id is required'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).first()
        if not appointment:
            res = {'statuscode': 404, 'status': 'false', 'message': 'Appointment not found'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        serializer = DarwinboxCandidateAppointmentSerializer(appointment)
        res = {
            'statuscode': 200,
            'status': 'true',
            'data': serializer.data
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='get',
    operation_description="Alias of get_darwinbox_candidate_appointment_detail (data check by ID).",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="Appointment ID", type=openapi.TYPE_INTEGER),
    ],
    responses={200: "DarwinboxCandidateAppointment details"}
)
@swagger_auto_schema(
    method='post',
    operation_description="Alias of get_darwinbox_candidate_appointment_detail (data check by ID).",
    request_body=candidate_appointment_id_schema,
    responses={200: "DarwinboxCandidateAppointment details"}
)
@api_view(['GET', 'POST'])
@csrf_exempt
def darwinbox_candidate_appointment_data_check(request):
    return get_darwinbox_candidate_appointment_detail(request)


@swagger_auto_schema(
    method='post',
    operation_description="Delete a Darwinbox candidate appointment by ID.",
    request_body=candidate_appointment_id_schema,
    responses={200: "Appointment deleted successfully"}
)
@api_view(['POST'])
@csrf_exempt
def delete_darwinbox_candidate_appointment(request):
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('id') or python_data.get('appointment')
            if not appointment_id:
                res = {'statuscode': 400, 'status': 'false', 'message': 'id is required'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).first()
            if not appointment:
                res = {'statuscode': 404, 'status': 'false', 'message': 'Appointment not found'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            appointment.delete()
            res = {
                'statuscode': 200,
                'status': 'true',
                'message': 'Appointment deleted successfully'
            }
        except Exception as e:
            res = {'statuscode': 400, 'status': 'false', 'message': str(e)}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='post',
    operation_description="Alias to delete a Darwinbox candidate appointment by ID.",
    request_body=candidate_appointment_id_schema,
    responses={200: "Appointment deleted successfully"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_delete(request):
    return delete_darwinbox_candidate_appointment(request)


@swagger_auto_schema(
    method='post',
    operation_description="Upload report and mark completed ('Reports Uploaded') or Cancel an appointment ('Cancel').",
    request_body=candidate_appointment_cancel_done_schema,
    responses={200: "Status update success message"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_cancel_done(request):
    if request.method == 'POST':
        python_data = {}
        for i, j in request.FILES.items():
            python_data.update({i: j})
        for i, j in request.POST.items():
            python_data.update({i: j})

        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()

        appointment_id = python_data.get('appointment') or python_data.get('id')
        status = python_data.get('status')
        report = python_data.get('report')
        reason = python_data.get('reason')
        remark = python_data.get('remark') or python_data.get('remarks')
        report_date = python_data.get('report_date')

        check_appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).count()
        if check_appointment == 1:
            appointment = models.DarwinboxCandidateAppointment.objects.get(id=appointment_id)
            if status == 'Reports Uploaded':
                if report:
                    appointment.report = report
                appointment.status = 'Reports Uploaded'
                appointment.remark = remark if remark else appointment.remark
                appointment.report_date = report_date if report_date else str(current_date)
                appointment.save()

                res = {
                    'statuscode': 200,
                    'status': 'true',
                    'message': 'Darwinbox candidate report Uploaded successfully.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

            elif status == 'Cancel':
                appointment.status = 'Cancel'
                appointment.reason = reason
                appointment.remark = remark
                appointment.save()

                res = {
                    'statuscode': 200,
                    'status': 'true',
                    'message': 'Darwinbox candidate appointment Cancelled successfully.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            else:
                res = {
                    'statuscode': 406,
                    'status': 'false',
                    'message': 'Enter valid status.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
        else:
            res = {
                'statuscode': 406,
                'status': 'false',
                'message': 'Enter valid appointment.'
            }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='post',
    operation_description="Upload report for Darwinbox candidate appointment.",
    request_body=candidate_appointment_cancel_done_schema,
    responses={200: "Report uploaded successfully"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_report_upload(request):
    return darwinbox_candidate_appointment_cancel_done(request)


@swagger_auto_schema(
    method='post',
    operation_description="Confirm or Reschedule a Darwinbox candidate appointment. When status is 'Rescheduled', an audit record is created in RescheduleDarwinboxCandidateAppointment.",
    request_body=candidate_appointment_reschedule_schema,
    responses={200: "Reschedule or Confirmation success message with updated appointment and audit record"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_booking_reschedule(request):
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('appointment') or python_data.get('id')
            status = python_data.get('status', 'Rescheduled')

            now = datetime.now()
            current_date_data = now.strftime('%Y-%m-%d')
            current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()

            check_appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).count()
            if check_appointment == 1:
                appointment = models.DarwinboxCandidateAppointment.objects.get(id=appointment_id)
                if status == 'Confirmed':
                    appointment.remark = python_data.get('remark') or python_data.get('remarks', appointment.remark)
                    appointment.confirm_appointment_date = python_data.get('confirm_appointment_date', appointment.confirm_appointment_date)
                    appointment.confirm_home_sample_date = python_data.get('confirm_home_sample_date', appointment.confirm_home_sample_date)
                    appointment.status = 'Confirmed'
                    if 'center' in python_data or 'center_id' in python_data:
                        appointment.center_id = python_data.get('center') or python_data.get('center_id')
                    appointment.save()

                    res = {
                        'statuscode': 200,
                        'status': 'true',
                        'message': 'Your Darwinbox candidate appointment Booked successfully.'
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')

                elif status == 'Rescheduled':
                    old_appointment_date = appointment.confirm_appointment_date or appointment.appointment_date_1
                    old_home_sample_date = appointment.confirm_home_sample_date or appointment.home_sample_date_1
                    new_appointment_date = python_data.get('confirm_appointment_date') or python_data.get('new_appointment_date') or python_data.get('new_health_checkup_date') or appointment.confirm_appointment_date
                    new_home_sample_date = python_data.get('confirm_home_sample_date') or python_data.get('new_home_sample_date') or appointment.confirm_home_sample_date
                    rescheduled_by = python_data.get('rescheduled_by', 'Staff')
                    reason = python_data.get('reason', appointment.reason)
                    remark = python_data.get('remark') or python_data.get('remarks', appointment.remark)

                    reschedule_record = models.RescheduleDarwinboxCandidateAppointment.objects.create(
                        appointment=appointment,
                        hoh_employee=appointment.hoh_employee,
                        rescheduled_by=rescheduled_by,
                        old_appointment_date=old_appointment_date,
                        new_appointment_date=new_appointment_date,
                        old_home_sample_date=old_home_sample_date,
                        new_home_sample_date=new_home_sample_date,
                        reason=reason,
                        remark=remark,
                        status='Rescheduled',
                        created_at=str(current_date)
                    )

                    appointment.remark = remark
                    appointment.reason = reason
                    appointment.confirm_appointment_date = new_appointment_date
                    appointment.confirm_home_sample_date = new_home_sample_date
                    appointment.status = 'Rescheduled'
                    if 'center' in python_data or 'center_id' in python_data:
                        appointment.center_id = python_data.get('center') or python_data.get('center_id')
                    appointment.save()

                    serializer = DarwinboxCandidateAppointmentSerializer(appointment)
                    reschedule_serializer = RescheduleDarwinboxCandidateAppointmentSerializer(reschedule_record)

                    res = {
                        'statuscode': 200,
                        'status': 'true',
                        'message': 'Your Darwinbox candidate appointment Rescheduled successfully.',
                        'data': serializer.data,
                        'reschedule_record': reschedule_serializer.data
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
                else:
                    res = {
                        'statuscode': 406,
                        'status': 'false',
                        'message': 'Enter valid Status.'
                    }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')
            else:
                res = {
                    'statuscode': 406,
                    'status': 'false',
                    'message': 'Enter valid appointment.'
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
        except Exception as e:
            res = {'statuscode': 400, 'status': 'false', 'message': str(e)}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    method='post',
    operation_description="Alias to reschedule a Darwinbox candidate appointment.",
    request_body=candidate_appointment_reschedule_schema,
    responses={200: "Reschedule success message"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_reschedule(request):
    return darwinbox_candidate_appointment_booking_reschedule(request)


@swagger_auto_schema(
    method='post',
    operation_description="Update preferred dates for a Darwinbox candidate appointment.",
    request_body=candidate_appointment_date_update_schema,
    responses={200: "Appointment date updated successfully"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_date_update(request):
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('id') or python_data.get('appointment')
            appointment_date_1 = python_data.get('appointment_date_1')
            appointment_date_2 = python_data.get('appointment_date_2')
            home_sample_date_1 = python_data.get('home_sample_date_1')
            home_sample_date_2 = python_data.get('home_sample_date_2')

            check_appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).count()
            if check_appointment == 1:
                appointment = models.DarwinboxCandidateAppointment.objects.get(id=appointment_id)
                if appointment_date_1:
                    appointment.appointment_date_1 = appointment_date_1
                if appointment_date_2:
                    appointment.appointment_date_2 = appointment_date_2
                if home_sample_date_1:
                    appointment.home_sample_date_1 = home_sample_date_1
                if home_sample_date_2:
                    appointment.home_sample_date_2 = home_sample_date_2
                appointment.save()

                serializer = DarwinboxCandidateAppointmentSerializer(appointment)
                res = {
                    'statuscode': 200,
                    'status': 'true',
                    'message': 'Appointment date updated successfully',
                    'data': serializer.data
                }
            else:
                res = {
                    'statuscode': 406,
                    'status': 'false',
                    'message': 'Enter valid appointment.'
                }
        except Exception as e:
            res = {'statuscode': 400, 'status': 'false', 'message': str(e)}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


@swagger_auto_schema(
    methods=['get', 'post'],
    operation_description="Get reschedule audit history for Darwinbox candidate appointments (optionally filter by appointment_id).",
    manual_parameters=[
        openapi.Parameter('appointment_id', openapi.IN_QUERY, description="Optional appointment ID to filter", type=openapi.TYPE_INTEGER),
    ],
    responses={200: "List of RescheduleDarwinboxCandidateAppointment records"}
)
@api_view(['GET', 'POST'])
@csrf_exempt
def reschedule_darwinbox_candidate_appointment_list(request):
    if request.method in ['POST', 'GET']:
        if request.method == 'POST':
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('appointment_id') or python_data.get('appointment')
        else:
            appointment_id = request.GET.get('appointment_id') or request.GET.get('appointment')

        if appointment_id:
            records = models.RescheduleDarwinboxCandidateAppointment.objects.filter(appointment_id=appointment_id).order_by('-id')
        else:
            records = models.RescheduleDarwinboxCandidateAppointment.objects.all().order_by('-id')

        serializer = RescheduleDarwinboxCandidateAppointmentSerializer(records, many=True)
        res = {
            'statuscode': 200,
            'status': 'true',
            'data': serializer.data
        }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


# ============================================================
# UNIFIED ALL-PARAMETER ENDPOINT FOR DARWINBOX CANDIDATE APPOINTMENTS
# ============================================================

@swagger_auto_schema(
    method='post',
    operation_description="Unified single endpoint accepting ALL Darwinbox candidate appointment parameters (create, update, reschedule, confirm, cancel, and audit logging).",
    request_body=candidate_appointment_full_manage_schema,
    responses={200: "Success response with full appointment and optional reschedule record"}
)
@api_view(['POST'])
@csrf_exempt
def darwinbox_candidate_appointment_full_manage(request):
    """
    Unified endpoint accepting ALL DarwinboxCandidateAppointment & Reschedule parameters in one place.
    """
    if request.method == 'POST':
        try:
            python_data = JSONParser().parse(io.BytesIO(request.body))
            appointment_id = python_data.get('id') or python_data.get('appointment')
            hoh_employee = python_data.get('hoh_employee') or python_data.get('hoh_employee_id')
            package = python_data.get('package') or python_data.get('package_id')
            center = python_data.get('center') or python_data.get('center_id')
            vendor = python_data.get('vendor') or python_data.get('vendor_id')
            type_of_visit = python_data.get('type_of_visit') or python_data.get('type_of_visit_id')
            appointment_date_1 = python_data.get('appointment_date_1')
            appointment_date_2 = python_data.get('appointment_date_2')
            home_sample_date_1 = python_data.get('home_sample_date_1')
            home_sample_date_2 = python_data.get('home_sample_date_2')
            confirm_appointment_date = python_data.get('confirm_appointment_date')
            confirm_home_sample_date = python_data.get('confirm_home_sample_date')
            date_of_appointment = python_data.get('date_of_appointment')
            new_appointment_date = python_data.get('new_appointment_date') or confirm_appointment_date
            new_home_sample_date = python_data.get('new_home_sample_date') or confirm_home_sample_date
            rescheduled_by = python_data.get('rescheduled_by', 'Staff')
            reason = python_data.get('reason')
            remark = python_data.get('remark') or python_data.get('remarks')
            status = python_data.get('status')
            report_date = python_data.get('report_date')

            now = datetime.now()
            current_date_data = now.strftime('%Y-%m-%d')
            current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()

            if package:
                package_obj = models.PackageDetail.objects.filter(id=package).first()
                if package_obj:
                    if not vendor and package_obj.vendor_id:
                        vendor = package_obj.vendor_id
                    if not type_of_visit and package_obj.type_of_visit_id:
                        type_of_visit = package_obj.type_of_visit_id

            reschedule_record = None

            if appointment_id:
                appointment = models.DarwinboxCandidateAppointment.objects.filter(id=appointment_id).first()
                if not appointment:
                    res = {'statuscode': 404, 'status': 'false', 'message': 'Appointment not found'}
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type='application/json')

                old_appointment_date = appointment.confirm_appointment_date or appointment.appointment_date_1
                old_home_sample_date = appointment.confirm_home_sample_date or appointment.home_sample_date_1

                if hoh_employee:
                    appointment.hoh_employee_id = hoh_employee
                if package:
                    appointment.package_id = package
                if center:
                    appointment.center_id = center
                if vendor:
                    appointment.vendor_id = vendor
                if type_of_visit:
                    appointment.type_of_visit_id = type_of_visit
                if appointment_date_1 is not None:
                    appointment.appointment_date_1 = appointment_date_1
                if appointment_date_2 is not None:
                    appointment.appointment_date_2 = appointment_date_2
                if home_sample_date_1 is not None:
                    appointment.home_sample_date_1 = home_sample_date_1
                if home_sample_date_2 is not None:
                    appointment.home_sample_date_2 = home_sample_date_2
                if confirm_appointment_date is not None:
                    appointment.confirm_appointment_date = confirm_appointment_date
                if confirm_home_sample_date is not None:
                    appointment.confirm_home_sample_date = confirm_home_sample_date
                if date_of_appointment is not None:
                    appointment.date_of_appointment = date_of_appointment
                if reason is not None:
                    appointment.reason = reason
                if remark is not None:
                    appointment.remark = remark
                if report_date is not None:
                    appointment.report_date = report_date

                if status == 'Rescheduled':
                    appointment.status = 'Rescheduled'
                    if new_appointment_date:
                        appointment.confirm_appointment_date = new_appointment_date
                    if new_home_sample_date:
                        appointment.confirm_home_sample_date = new_home_sample_date

                    reschedule_record = models.RescheduleDarwinboxCandidateAppointment.objects.create(
                        appointment=appointment,
                        hoh_employee=appointment.hoh_employee,
                        rescheduled_by=rescheduled_by,
                        old_appointment_date=old_appointment_date,
                        new_appointment_date=appointment.confirm_appointment_date,
                        old_home_sample_date=old_home_sample_date,
                        new_home_sample_date=appointment.confirm_home_sample_date,
                        reason=reason,
                        remark=remark,
                        status='Rescheduled',
                        created_at=str(current_date)
                    )
                elif status:
                    appointment.status = status

                appointment.save()
                serializer = DarwinboxCandidateAppointmentSerializer(appointment)
                res_data = {
                    'statuscode': 200,
                    'status': 'true',
                    'message': 'Darwinbox candidate appointment updated successfully',
                    'data': serializer.data
                }
                if reschedule_record:
                    res_data['reschedule_record'] = RescheduleDarwinboxCandidateAppointmentSerializer(reschedule_record).data
                json_data = JSONRenderer().render(res_data)
                return HttpResponse(json_data, content_type='application/json')
            else:
                appointment = models.DarwinboxCandidateAppointment.objects.create(
                    hoh_employee_id=hoh_employee,
                    package_id=package,
                    center_id=center,
                    vendor_id=vendor,
                    type_of_visit_id=type_of_visit,
                    appointment_date_1=appointment_date_1,
                    appointment_date_2=appointment_date_2,
                    home_sample_date_1=home_sample_date_1,
                    home_sample_date_2=home_sample_date_2,
                    confirm_appointment_date=confirm_appointment_date,
                    confirm_home_sample_date=confirm_home_sample_date,
                    date_of_appointment=date_of_appointment,
                    reason=reason,
                    remark=remark,
                    report_date=report_date,
                    status=status or 'Request Received',
                    created_at=str(current_date)
                )
                serializer = DarwinboxCandidateAppointmentSerializer(appointment)
                res = {
                    'statuscode': 200,
                    'status': 'true',
                    'message': 'Darwinbox candidate appointment created successfully',
                    'data': serializer.data
                }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
        except Exception as e:
            res = {'statuscode': 400, 'status': 'false', 'message': str(e)}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')