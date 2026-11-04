from django.shortcuts import render
from svasthyapp import models
import io
from rest_framework.parsers import JSONParser
from datetime import datetime, timedelta
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import base64
import math, random 
from .serializer import AdminUserSerializer, CorporateSerializer, StaffDepartmentSerializer, StaffSerializer, VendorSerializer, \
    TypeOfAccessSerializer, StaffLevelSerializer, StaffTypeSerializer, AgeCategorySerializer, GenderSerializer, RelationSerializer, TypeOfServiceSerializer, \
    TypeOfVisitSerializer, ParentCompanySerializer, BillingCycleSerializer, WeekdaysSerializer, HolidaysSerializer, PaymentTagsSerializer, EmployeeDetailSerializer, \
    CorporateDataSerializer, PackageDetailSerializer, CenterDetailSerializer, EmployeeDataSerializer, VendorNameSerializer, PackageNameSerializer, HolidayDetailSerializer, \
    StaffDataSerializer, HealthTipsSerializer, EmployeeDependentSerializer, AppointmentDetailSerializer, CenterDataSerializer
    
import requests
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import xlrd as xl
import xlrd 
from django.http import JsonResponse
from openpyxl import load_workbook
from openpyxl.styles import PatternFill




@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)

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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        user_type = python_data.get('user_type')
        mobile = python_data.get('mobile', None)
        digits = "123456789"
        # OTP = ""
        # for i in range(6):
        #     OTP += digits[math.floor(random.random() * 9)]

        OTP = '111111'

        if user_type == 'admin':
            check_email = models.AdminUser.objects.filter(mobile = mobile).count()
            if check_email == 1:
                user = models.AdminUser.objects.get(mobile = mobile)
                user.OTP = OTP
                user.save()

                res = {
                    'statuscode' : 200,
                    'status':'Success',
                    'message':'OTP send successfully.',
                    'otp' : OTP
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')       
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Valid Mobile Number."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')       
        elif user_type == 'vendor':
            print(python_data, 'data')
            vendor_code = python_data.get('vendor_code')
            email = python_data.get('email', None)
            mobile = python_data.get('mobile', None)
            vendor_id = models.VendorDetail.objects.filter(vendor_code=vendor_code).values_list('id', flat=True)[0]
            
            if email != None:

                check_email = models.VendorDetail.objects.filter(id=vendor_id, email = email).count()
                if check_email == 1:
                    vendor = models.VendorDetail.objects.get(email = email)
                    vendor.OTP = OTP
                    vendor.save()

                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':'OTP send successfully.',
                        'otp' : OTP
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Email."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')       
            
            elif mobile != None:
                check_email = models.VendorDetail.objects.filter(id=vendor_id, mobile = mobile).count()
                if check_email == 1:
                    vendor = models.VendorDetail.objects.get(mobile = mobile)
                    vendor.OTP = OTP
                    vendor.save()

                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':'OTP send successfully.',
                        'otp' : OTP
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Mobile."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')       


        elif user_type == 'employee':
            print(python_data, 'data')
            corporate_code = python_data.get('corporate_code')
            email = python_data.get('email', None)
            mobile = python_data.get('mobile', None)
            corporate_id = models.CorporateDetail.objects.filter(corporate_code=corporate_code).values_list('id', flat=True)[0]
            
            if email != None:

                check_email = models.EmployeeDetail.objects.filter(corporate_id=corporate_id, email = email).count()
                if check_email == 1:
                    employee = models.EmployeeDetail.objects.get(email = email)
                    employee.OTP = OTP
                    employee.save()

                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':'OTP send successfully.',
                        'otp' : OTP
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Email."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')       
            
            elif mobile != None:
                check_email = models.EmployeeDetail.objects.filter(corporate_id=corporate_id, mobile = mobile).count()
                if check_email == 1:
                    employee = models.EmployeeDetail.objects.get(mobile = mobile)
                    employee.OTP = OTP
                    employee.save()

                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':'OTP send successfully.',
                        'otp' : OTP
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Mobile."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')       

        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid user type."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json')   


@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        user_type = python_data.get('user_type')
        mobile = python_data.get('mobile', None)
        OTP = python_data.get('OTP')
    
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        
        if user_type == 'admin':
            check_mobile = models.AdminUser.objects.filter(mobile = mobile).count()
            if check_mobile == 1:
                get_otp = models.AdminUser.objects.filter(mobile = mobile).values_list('OTP', flat=True)[0]
                if get_otp == OTP:
                    admin = models.AdminUser.objects.get(mobile = mobile)
                    admin_email = admin.email
                    admin_user = admin.id
                    serialiser = AdminUserSerializer(admin)
                    data = serialiser.data
                    data.update({'user_type':user_type})

                    create_history = models.AdminUserLoginHistory.objects.create(
                        admin_user_id = admin_user,
                        email = admin_email,
                        time = current_time
                    ).save()

                    
                    
                    res = {
                        'statuscode' : 200,
                        'status':'Success',
                        'message':"Login Successfully." ,
                        'data':data
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message':"You've Entered wrong OTP." 
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json')       
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Enter Valid Email."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
        
        elif user_type == 'vendor':
            email = python_data.get('email', None)
            mobile = python_data.get('mobile', None)
            if email != None:
                check_email = models.VendorDetail.objects.filter(email = email).count()
                if check_email == 1:
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
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')       
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message':"You've Entered wrong OTP." 
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Email."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
            
            elif mobile != None:
                check_email = models.VendorDetail.objects.filter(mobile = mobile).count()
                if check_email == 1:
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
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')       
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message':"You've Entered wrong OTP." 
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Mobile."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                    

                    
        elif user_type == 'employee':
            email = python_data.get('email', None)
            mobile = python_data.get('mobile', None)
            if email != None:
                check_email = models.EmployeeDetail.objects.filter(email = email).count()
                if check_email == 1:
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
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')       
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message':"You've Entered wrong OTP." 
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Email."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 

            elif mobile != None:
                check_mobile = models.EmployeeDetail.objects.filter(mobile = mobile).count()
                if check_mobile == 1:
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
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')       
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message':"You've Entered wrong OTP." 
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json')       
                else:
                    res = {
                        'statuscode' : 406,
                        'status':'false',
                        'message' : "Enter Valid Mobile Number."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
        
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Enter Valid User Type."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
    


@csrf_exempt
def staff_register(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        mobile = python_data.get('mobile')
        email = python_data.get('email')
        print(python_data, 'python_data')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_mobile = models.StaffDetail.objects.filter(mobile = mobile).count()
        if check_mobile == 0:
            check_email = models.StaffDetail.objects.filter(email = email).count()
            if check_email == 0:
                staff = models.StaffDetail.objects.create(
                    name = python_data.get('name'),
                    staff_code = python_data.get('staff_code'),
                    department_id = python_data.get('department'),
                    type_of_access_id = python_data.get('type_of_access'),
                    staff_type_id = python_data.get('staff_type'),
                    staff_level_id = python_data.get('staff_level'),
                    mobile = python_data.get('mobile'),
                    email = python_data.get('email'),
                    status = 'Active',
                    created_at = current_time
                )
                staff.save()

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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_staff = models.StaffDetail.objects.filter(id = id).count()
        if check_staff == 1:
            staff = models.StaffDetail.objects.get(id = id)
            staff.name = python_data.get('name', staff.name)
            staff.staff_code = python_data.get('staff_code', staff.staff_code)
            staff.staff_type_id = python_data.get('staff_type', staff.staff_type)
            staff.department_id = python_data.get('department', staff.department)
            staff.type_of_access_id = python_data.get('type_of_access', staff.type_of_access)
            staff.staff_level_id = python_data.get('staff_level', staff.staff_level)
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def corporate_register(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        mobile = python_data.get('mobile')
        email = python_data.get('email')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_mobile = models.CorporateDetail.objects.filter(mobile = mobile).count()
        if check_mobile == 0:
            check_email = models.CorporateDetail.objects.filter(email = email).count()
            if check_email == 0:
                corporate = models.CorporateDetail.objects.create(
                    parent_company_id = python_data.get('parent_company', None),
                    corporate_name = python_data.get('corporate_name'),
                    corporate_code = python_data.get('corporate_code'),
                    
                    type_of_corporation = python_data.get('type_of_corporation'),
                    industry = python_data.get('industry'),
                    spoke_person = python_data.get('spoke_person'),
                    mobile = python_data.get('mobile'),
                    email = python_data.get('email'),
                    pan_card = python_data.get('pan_card'),
                    GST_no = python_data.get('GST_no'),
                    billing_cycle_id = python_data.get('billing_cycle'),
                    start_date = python_data.get('start_date'),
                    address = python_data.get('address'),
                    pincode = python_data.get('pincode'),
                    state = python_data.get('state'),
                    city = python_data.get('city'),
                    level1_id = python_data.get('level1'),
                    level2_id = python_data.get('level2'),
                    login_via = python_data.get('login_via'),
                    status = 'Active',
                    created_at = current_time
                )
                corporate.save()

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
def corporate_update(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_coporate = models.CorporateDetail.objects.filter(id = id).count()
        if check_coporate == 1:
            corporate = models.CorporateDetail.objects.get(id = id)
            corporate.parent_company_id = python_data.get('parent_company', corporate.parent_company)
            corporate.corporate_code = python_data.get('corporate_code', corporate.corporate_code)
            corporate.corporate_name = python_data.get('corporate_name', corporate.corporate_name)
            corporate.type_of_corporation = python_data.get('type_of_corporation', corporate.type_of_corporation)
            corporate.industry = python_data.get('industry', corporate.industry)
            corporate.spoke_person = python_data.get('spoke_person', corporate.spoke_person)
            corporate.pan_card = python_data.get('pan_card', corporate.pan_card)
            corporate.GST_no = python_data.get('GST_no', corporate.GST_no)
            corporate.billing_cycle_id = python_data.get('billing_cycle', corporate.billing_cycle)
            corporate.start_date = python_data.get('start_date', corporate.start_date)
            corporate.address = python_data.get('address', corporate.address)
            corporate.pincode = python_data.get('pincode', corporate.pincode)
            corporate.state = python_data.get('state', corporate.state)
            corporate.city = python_data.get('city', corporate.city)
            corporate.level1_id = python_data.get('level1', corporate.level1)
            corporate.level2_id = python_data.get('level2', corporate.level2)
            corporate.login_via = python_data.get('login_via', corporate.login_via)
            corporate.save()

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
                'message' : "Enter valid Corporate."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def corporate_status_update(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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






@csrf_exempt
def list_all_corporate(request):
    if request.method == 'POST':
        all_corporate = models.CorporateDetail.objects.all().order_by('-id')
        serialiser = CorporateSerializer(all_corporate, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def active_all_corporate(request):
    if request.method == 'POST':
        all_corporate = models.CorporateDetail.objects.filter(status= 'Active').order_by('-id')
        serialiser = CorporateDataSerializer(all_corporate, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def vendor_register(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        mobile = python_data.get('mobile')
        email = python_data.get('email')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_mobile = models.VendorDetail.objects.filter(mobile = mobile).count()
        if check_mobile == 0:
            check_email = models.VendorDetail.objects.filter(email = email).count()
            if check_email == 0:
                vendor = models.VendorDetail.objects.create(
                    vendor_name = python_data.get('vendor_name', None),
                    vendor_code = python_data.get('vendor_code'),
                    type_of_service_id = python_data.get('type_of_service'),
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_vendor = models.VendorDetail.objects.filter(id = id).count()
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
                'message' : "Enter valid Vendor."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def vendor_code_check(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        vendor_code = python_data.get('vendor_code')

        check_vendor_code = models.VendorDetail.objects.filter(vendor_code = vendor_code).count()
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
                'message':"You've Enter wrong Corporate Code."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def list_all_vendor(request):
    if request.method == 'POST':
        all_vendor = models.VendorDetail.objects.all().order_by('-id')
        serialiser = VendorSerializer(all_vendor, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def vendor_status_update(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.StaffDepartment.objects.filter(id = id).count()
        if check_department == 1:
            staff_department = python_data.get('staff_department')
            status = python_data.get('status')
            if staff_department:
                check_staff_department = models.StaffDepartment.objects.filter(id = id, staff_department = staff_department).count()
                print(check_staff_department, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def type_of_access_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.TypeOfAccess.objects.filter(id = id).count()
        if check_department == 1:
            type_of_access = python_data.get('type_of_access')
            status = python_data.get('status')
            if type_of_access:
                check_type_of_access = models.TypeOfAccess.objects.filter(id = id, type_of_access = type_of_access).count()
                print(check_type_of_access, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def staff_level_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.StaffLevel.objects.filter(id = id).count()
        if check_department == 1:
            staff_level = python_data.get('staff_level')
            status = python_data.get('status')
            if staff_level:
                check_staff_level = models.StaffLevel.objects.filter(id = id, staff_level = staff_level).count()
                print(check_staff_level, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def staff_type_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.StaffType.objects.filter(id = id).count()
        if check_department == 1:
            staff_type = python_data.get('staff_type')
            status = python_data.get('status')
            if staff_type:
                check_staff_type = models.StaffType.objects.filter(id = id, staff_type = staff_type).count()
                print(check_staff_type, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def age_category_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.AgeCategory.objects.filter(id = id).count()
        if check_department == 1:
            age_category = python_data.get('age_category')
            status = python_data.get('status')
            if age_category:
                check_age_category = models.AgeCategory.objects.filter(id = id, age_category = age_category).count()
                print(check_age_category, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def gender_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.Gender.objects.filter(id = id).count()
        if check_department == 1:
            gender = python_data.get('gender')
            status = python_data.get('status')
            if gender:
                check_gender = models.Gender.objects.filter(id = id, gender = gender).count()
                print(check_gender, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def relation_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.Relation.objects.filter(id = id).count()
        if check_department == 1:
            relation = python_data.get('relation')
            status = python_data.get('status')
            if relation:
                check_relation = models.Relation.objects.filter(id = id, relation = relation).count()
                print(check_relation, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def type_of_service_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.TypeOfService.objects.filter(id = id).count()
        if check_department == 1:
            type_of_service = python_data.get('type_of_service')
            status = python_data.get('status')
            if type_of_service:
                check_type_of_service = models.TypeOfService.objects.filter(id = id, type_of_service = type_of_service).count()
                print(check_type_of_service, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def type_of_visit_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.TypeOfVisit.objects.filter(id = id).count()
        if check_department == 1:
            type_of_visit = python_data.get('type_of_visit')
            status = python_data.get('status')
            if type_of_visit:
                check_type_of_visit = models.TypeOfVisit.objects.filter(id = id, type_of_visit = type_of_visit).count()
                print(check_type_of_visit, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def parent_company_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.ParentCompany.objects.filter(id = id).count()
        if check_department == 1:
            parent_company = python_data.get('parent_company')
            status = python_data.get('status')
            if parent_company:
                check_parent_company = models.ParentCompany.objects.filter(id = id, parent_company = parent_company).count()
                print(check_parent_company, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def billing_cycle_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.BillingCycle.objects.filter(id = id).count()
        if check_department == 1:
            billing_cycle = python_data.get('billing_cycle')
            status = python_data.get('status')
            if billing_cycle:
                check_billing_cycle = models.BillingCycle.objects.filter(id = id, billing_cycle = billing_cycle).count()
                print(check_billing_cycle, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def weekdays_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.Weekdays.objects.filter(id = id).count()
        if check_department == 1:
            weekdays = python_data.get('weekdays')
            status = python_data.get('status')
            if weekdays:
                check_weekdays = models.Weekdays.objects.filter(id = id, weekdays = weekdays).count()
                print(check_weekdays, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def holidays_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_department = models.Holidays.objects.filter(id = id).count()
        if check_department == 1:
            holidays = python_data.get('holidays')
            status = python_data.get('status')
            if holidays:
                check_holidays = models.Holidays.objects.filter(id = id, holidays = holidays).count()
                print(check_holidays, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def payment_tags_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        print(python_data, 'data')
        id = python_data.get('id')
        check_department = models.PaymentTags.objects.filter(id = id).count()
        if check_department == 1:
            payment_tags = python_data.get('payment_tags')
            status = python_data.get('status')
            if payment_tags:
                check_payment_tags = models.PaymentTags.objects.filter(id = id, payment_tags = payment_tags).count()
                print(check_payment_tags, 'depatmen count')
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
        json_data = JSONRenderer().render(res)
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
        json_data = JSONRenderer().render(res)
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
        json_data = JSONRenderer().render(res)
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
        json_data = JSONRenderer().render(res)
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
        json_data = JSONRenderer().render(res)
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
        json_data = JSONRenderer().render(res)
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
        json_data = JSONRenderer().render(res)
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
        json_data = JSONRenderer().render(res)
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
        json_data = JSONRenderer().render(res)
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
        json_data = JSONRenderer().render(res)
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
        json_data = JSONRenderer().render(res)
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def employee_register(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        mobile = python_data.get('mobile')
        email = python_data.get('email')
        print(python_data, 'python_data')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_mobile = models.EmployeeDetail.objects.filter(mobile = mobile).count()
        if check_mobile == 0:
            check_email = models.EmployeeDetail.objects.filter(email = email).count()
            if check_email == 0:
                emp = models.EmployeeDetail.objects.create(
                    corporate_id = python_data.get('corporate'),
                    employee_name = python_data.get('employee_name'),
                    employee_code = python_data.get('employee_code'),
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
            
                
                for count in range(1, 20):
                    print(count)
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
                        print(child_count, 'child_count')
                        print(dependent_relation_data, 'dependent_relation_data', child_id, 'child_id')
                        if dependent_relation_data != child_id:
                            print('time')
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
                                print('how')
                                
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        id = python_data.get('id')
        check_emp = models.EmployeeDetail.objects.filter(id = id).count()
        if check_emp == 1:
            employee = models.EmployeeDetail.objects.get(id = id)
            employee.corporate_id = python_data.get('corporate', employee.corporate)
            employee.employee_name = python_data.get('employee_name', employee.employee_name)
            employee.employee_code = python_data.get('employee_code', employee.employee_code)
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

            for count in range(1, 20):
                print(count)
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
                'message' : "Enter valid Employee."
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        all_emp = models.EmployeeDetail.objects.all().order_by('-id')
        list_data = []
        for emp in all_emp:
            emp = models.EmployeeDetail.objects.get(id = emp.id)
            serialiser = EmployeeDetailSerializer(emp)
            data = serialiser.data
            all_dependent = models.EmployeeDependent.objects.filter(employee = emp).order_by('id')
            
            list_dependent = []
            for dependent in all_dependent:
                self_id = models.Relation.objects.filter(relation = 'Self').values_list('id', flat=True)[0]
                relation = dependent.dependent_relation.id
                if self_id != relation:
                    dependent_serialiser = EmployeeDependentSerializer(dependent)
                    list_dependent.append(dependent_serialiser.data)
                
            data.update({'dependent_data':list_dependent})
            list_data.append(data)
                

        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
def package_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        print(python_data, 'python_data')
        package = models.PackageDetail.objects.create(
            package_name = python_data.get('package_name'),
            package_code = python_data.get('package_code'),
            MRP = python_data.get('MRP'),
            discount_price = python_data.get('discount_price'),
            offer_price = python_data.get('offer_price'),
            type_of_service_id = python_data.get('type_of_service'),
            type_of_visit_id = python_data.get('type_of_visit'),
            corporate_id = python_data.get('corporate'),
            start_date = python_data.get('start_date'),
            end_date = python_data.get('end_date'),
            billing_cycle_id = python_data.get('billing_cycle'),
            tags_id = python_data.get('tags'),
            description = python_data.get('description'),
            # package_applicable = python_data.get('package_applicable'),
            gender_id = python_data.get('gender'),
            age_category_id = python_data.get('age_category'),
            # relation_gender_id = python_data.get('relation_gender'),
            status = 'Active',
            created_at = current_time
        )
        package.save()
        
        if python_data.get('relation_with_employee') == '':
            print('First IF')
            package.relation_with_employee.set([])
        else:
            print('third IF')
            package.relation_with_employee.set((python_data.get('relation_with_employee', package.relation_with_employee)))
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'message' : "Package Added Successfully."
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 
        





@csrf_exempt
def package_update(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_package = models.PackageDetail.objects.filter(id = id).count()
        if check_package == 1:
            package = models.PackageDetail.objects.get(id = id)
            package.package_name = python_data.get('package_name', package.package_name)
            package.package_code = python_data.get('package_code', package.package_code)
            package.MRP = python_data.get('MRP', package.MRP)
            package.discount_price = python_data.get('discount_price', package.discount_price)
            package.offer_price = python_data.get('offer_price', package.offer_price)
            package.type_of_service_id = python_data.get('type_of_service', package.type_of_service)
            package.type_of_visit_id = python_data.get('type_of_visit', package.type_of_visit)
            package.corporate_id = python_data.get('corporate', package.corporate)
            package.start_date = python_data.get('start_date', package.start_date)
            package.end_date = python_data.get('end_date', package.end_date)
            package.billing_cycle_id = python_data.get('billing_cycle', package.billing_cycle)
            package.tags_id = python_data.get('tags', package.tags)
            package.description = python_data.get('description', package.description)
            # package.package_applicable = python_data.get('package_applicable', package.package_applicable)
            package.age_category_id = python_data.get('age_category', package.age_category)
            package.gender_id = python_data.get('gender', package.gender) 
            package.save()
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
def package_status_update(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        all_emp = models.PackageDetail.objects.all().order_by('-id')
        serialiser = PackageDetailSerializer(all_emp, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def employee_list_by_corporate(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")

        center = models.CenterDetail.objects.create(
            center_name = python_data.get('center_name'),
            address = python_data.get('address'),
            pincode = python_data.get('pincode'),
            state = python_data.get('state'),
            city = python_data.get('city'),
            location = python_data.get('location'),
            vendor_id = python_data.get('vendor'),
            package_id = python_data.get('package'),
            type_of_service_id = python_data.get('type_of_service'),
            latitude = python_data.get('latitude'),
            longitude = python_data.get('longitude'),
            status = 'Active',
            created_at = current_time
        )
        center.save()

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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
            center.vendor_id = python_data.get('vendor', center.vendor)
            center.package_id = python_data.get('package', center.package)
            center.type_of_service_id = python_data.get('type_of_service', center.type_of_service)
            center.latitude = python_data.get('latitude', center.latitude)
            center.longitude = python_data.get('longitude', center.longitude)
            
            center.save()
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
def center_status_update(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        all_center = models.CenterDetail.objects.all().order_by('-id')
        serialiser = CenterDetailSerializer(all_center, many=True)
        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def center_serivce_list_by_vendor(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        vendor = python_data.get('vendor')
        get_center_count = models.CenterDetail.objects.filter(vendor = vendor).count()
        print(get_center_count, 'get_center_count')
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        holiday = models.HolidayDetail.objects.create(
            vendor_id = python_data.get('vendor'),
            center_id = python_data.get('center'),
            type_of_service_id = python_data.get('type_of_service'),
            state = python_data.get('state'),
            city = python_data.get('city'),
            location = python_data.get('location'),
            weekly_off = python_data.get('weekly_off'),
            holiday = python_data.get('holiday'),
            status = 'Active'
        ).save()
        res = {
            'statuscode' : 200,
            'status':'true',
            'message' : "Holiday Create Successfully."
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 
        

@csrf_exempt
def holiday_update(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        check_holiday = models.HolidayDetail.objects.filter(id = id).count()
        if check_holiday == 1:
            holiday = models.HolidayDetail.objects.get(id = id)
            holiday.vendor_id =  python_data.get('vendor', holiday.vendor)
            holiday.center_id =  python_data.get('center', holiday.center)
            holiday.type_of_service_id =  python_data.get('type_of_service', holiday.type_of_service)
            holiday.state =  python_data.get('state', holiday.state)
            holiday.city =  python_data.get('city', holiday.city)
            holiday.location =  python_data.get('location', holiday.location)
            holiday.weekly_off =  python_data.get('weekly_off', holiday.weekly_off)
            holiday.holiday =  python_data.get('holiday', holiday.holiday)
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
def holiday_status_update(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
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
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 

@csrf_exempt
def corporate_code_check(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        corporate_code = python_data.get('corporate_code')

        check_corporate_code = models.CorporateDetail.objects.filter(corporate_code = corporate_code).count()
        if check_corporate_code == 1:
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
                'statuscode' : 406,
                'status':'false',
                'message':"You've Enter wrong Corporate Code."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def corporate_package_list(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        employee = python_data.get('employee')

        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        if check_employee == 1:
            employee = models.EmployeeDetail.objects.get(id = employee)
            corporate = employee.corporate.id
            all_emp = models.PackageDetail.objects.filter(corporate = corporate).order_by('-id')
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
            created_at = current_time
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
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)

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
        json_data = JSONRenderer().render(res)
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
def service_wise_package_list_employee(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        employee = python_data.get('employee')
        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        list_data = []
        if check_employee == 1:
            employee = models.EmployeeDetail.objects.get(id = employee)
            corporate = employee.corporate_id
            all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
            for service in all_service:
                package_count = models.PackageDetail.objects.filter(type_of_service = service.id, corporate = corporate).count()
                if package_count >= 1:
                    service_dictionary = {}
                    get_all_package = models.PackageDetail.objects.filter(type_of_service = service.id, corporate = corporate).order_by('-id')
                    serialiser = PackageDetailSerializer(get_all_package, many=True)
                    service_dictionary.update({'service':service.type_of_service, 'data':serialiser.data})
                    list_data.append(service_dictionary)

        
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : list_data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def search_package(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        employee = python_data.get('employee')
        search_by = python_data.get('search_by')
        search = python_data.get('search')
        print(python_data, 'python_data')
        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        search_list_data = []
        list_data = []
        if check_employee == 1:
            employee = models.EmployeeDetail.objects.get(id = employee)
            corporate = employee.corporate_id
            if search_by == 'Location':
                all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
                for service in all_service: 
                    package_count = models.PackageDetail.objects.filter(type_of_service = service.id, corporate = corporate).count()
                    if package_count >= 1:
                        get_all_package = models.PackageDetail.objects.filter(type_of_service = service.id, corporate = corporate).order_by('-id')
                    
                        for package in get_all_package:
                            package_data = models.PackageDetail.objects.get(id = package.id)
                            list_center = models.CenterDetail.objects.filter(package = package_data)
                            for center in list_center:
                                location_data = center.location
                                service_dictionary = {}
                                if location_data.lower() == search.lower(): 
                                    serialiser = PackageDetailSerializer(package_data)
                                    list_data.append(serialiser.data)
                                
                                if len(list_data) > 0:
                                    service_dictionary.update({'service':service.type_of_service, 'data':list_data})
                                    search_list_data.append(service_dictionary)

            elif search_by == 'Pincode':
                # get_all_package = models.PackageDetail.objects.filter(corporate = corporate).order_by('-id')
                # for package in get_all_package:
                #     package_data = models.PackageDetail.objects.get(id = package.id)
                #     list_pincode = models.CenterDetail.objects.filter(package = package_data)
                    
                #     for pincode in list_pincode:
                #         pincode_data = pincode.pincode
                #         print(pincode_data)
                #         if pincode_data.lower() == search.lower():                        
                    
                #             serialiser = PackageDetailSerializer(package_data)
                #             search_list_data.append(serialiser.data)
                all_service = models.TypeOfService.objects.filter(status = 'Active').order_by('-id')
                for service in all_service: 
                    package_count = models.PackageDetail.objects.filter(type_of_service = service.id, corporate = corporate).count()
                    if package_count >= 1:
                        get_all_package = models.PackageDetail.objects.filter(type_of_service = service.id, corporate = corporate).order_by('-id')
                    
                        for package in get_all_package:
                            package_data = models.PackageDetail.objects.get(id = package.id)
                            list_pincode = models.CenterDetail.objects.filter(package = package_data)
                            for pincode in list_pincode:
                                pincode_data = pincode.pincode
                                service_dictionary = {}
                                if pincode_data.lower() == search.lower(): 
                                    serialiser = PackageDetailSerializer(package_data)
                                    list_data.append(serialiser.data)
                                
                                if len(list_data) > 0:
                                    service_dictionary.update({'service':service.type_of_service, 'data':list_data})
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
        
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "You've Enter wrong user ID."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def package_list_employee(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        employee = python_data.get('employee')
        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        
        if check_employee == 1:
            employee = models.EmployeeDetail.objects.get(id = employee)
            corporate = employee.corporate_id
            list_data = []
            get_all_package = models.PackageDetail.objects.filter(corporate = corporate).order_by('-id')
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
def appoinment_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        employee = python_data.get('employee')
        patient = python_data.get('patient')
        package = python_data.get('package')
        center = python_data.get('center')
        appoinment_date_1 = python_data.get('appoinment_date_1')
        appoinment_date_2 = python_data.get('appoinment_date_2')
        home_sample_date_1 = python_data.get('home_sample_date_1')
        home_sample_date_2 = python_data.get('home_sample_date_2')
        
        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()

        
        check_employee = models.EmployeeDetail.objects.filter(id = employee).count()
        list_data = []
        if check_employee == 1:
            vendor_id = models.CenterDetail.objects.filter(id = center).values_list('vendor', flat=True)[0]
            appoinment_create = models.AppointmentDetail.objects.create(
                employee_id = employee,  
                patient_id = patient,
                package_id = package,
                center_id = center,
                vendor_id = vendor_id,
                appoinment_date_1 = appoinment_date_1, 
                appoinment_date_2 = appoinment_date_2,
                home_sample_date_1 = home_sample_date_1,
                home_sample_date_2 = home_sample_date_2,
                status = 'Pending',
                created_at = current_date
            ).save()

            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "You're appointment book successfully."
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


@csrf_exempt
def appoinment_booking_reschedule(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        appoinment = python_data.get('appoinment')
        status = python_data.get('status')
        print(python_data, 'python_datapython_data')
        check_appoinment = models.AppointmentDetail.objects.filter(id = appoinment).count()
        if check_appoinment == 1:
            if status == 'Booking':
                appointment = models.AppointmentDetail.objects.get(id = appoinment)
                appointment.remark = python_data.get('remark', appointment.remark)
                appointment.confirm_appoinment_date = python_data.get('confirm_appoinment_date', appointment.confirm_appoinment_date)
                appointment.confirm_home_sample_date = python_data.get('confirm_home_sample_date', appointment.confirm_home_sample_date)
                appointment.status = 'Booking'
                appointment.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your appoinetment Booked successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
            
            elif status == 'Rescheduled':
                appointment = models.AppointmentDetail.objects.get(id = appoinment)
                appointment.remark = python_data.get('remark', appointment.remark)
                appointment.reason = python_data.get('reason', appointment.reason)
                appointment.confirm_appoinment_date = python_data.get('confirm_appoinment_date', appointment.confirm_appoinment_date)
                appointment.confirm_home_sample_date = python_data.get('confirm_home_sample_date', appointment.confirm_home_sample_date)
                appointment.status = 'Rescheduled'
                appointment.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your appoinetment Rescheduled successfully."
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
                'message' : "Enter valid Appoinment."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def appoinment_cancel_done(request):
    if request.method == 'POST':
        python_data={}
        for i,j in request.FILES.items():
            python_data.update({i:j})
        
        for i,j in request.POST.items():
            python_data.update({i:j})

        now = datetime.now()
        current_date_data = now.strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date_data, '%Y-%m-%d').date()

        appoinment = python_data.get('appoinment')
        status = python_data.get('status')
        print(python_data, 'python_datapython_data')
        check_appoinment = models.AppointmentDetail.objects.filter(id = appoinment).count()
        if check_appoinment == 1:
            if status == 'Cancel':
                appointment = models.AppointmentDetail.objects.get(id = appoinment)
                appointment.reason = python_data.get('reason', appointment.reason)
                appointment.status = 'Cancel'
                appointment.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your appoinetment Cancel successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json')
            
            elif status == 'Done':
                appointment = models.AppointmentDetail.objects.get(id = appoinment)
                
                if type(python_data.get('report', appointment.report)) != str:         
                    appointment.report = python_data.get('report', appointment.report)
                    appointment.report_date = current_date
                appointment.status = 'Done'
                appointment.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Your appoinetment Done successfully."
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
                'message' : "Enter valid Appoinment."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def all_appoinment_list(request):
    if request.method == 'POST':
        all_appointment = models.AppointmentDetail.objects.all().order_by('-id')
        serialiser = AppointmentDetailSerializer(all_appointment, many=True)
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 


@csrf_exempt
def appoinment_list_for_vendor(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        vendor = python_data.get('vendor')
        check_vendor = models.VendorDetail.objects.filter(id = vendor).count()
        if check_vendor == 1:
            all_appointment = models.AppointmentDetail.objects.filter(vendor = vendor).order_by('-id')
            serialiser = AppointmentDetailSerializer(all_appointment, many=True)

            done_appointment_count = models.AppointmentDetail.objects.filter(vendor = vendor, status = 'Done').count()
            cancel_appointment_count = models.AppointmentDetail.objects.filter(vendor = vendor, status = 'Cancel').count()
            booking_appointment_count = models.AppointmentDetail.objects.filter(vendor = vendor, status = 'Booking').count()
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
def employee_appoinment_list(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        employee = python_data.get('employee')
        all_appointment = models.AppointmentDetail.objects.filter(employee = employee).order_by('-id')
        
        serialiser = AppointmentDetailSerializer(all_appointment, many=True)
        res = {
            'statuscode' : 200,
            'status':'true',
            'data' : serialiser.data
            }
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type= 'application/json') 




# @csrf_exempt
# def bulk_import(request):
#     if (request.method == "POST"):

#         # excel_file = request.FILES.get('file', None)
#         # print(excel_file, 'Checj ')
#         # module_name = request.POST.get('module_name', None)
#         # created_by = request.POST['id']

#         print(True)

#         excel_file = request.FILES['excel_file']


#         try:
#             fs = FileSystemStorage()
#             fs.delete('corporate1.xlsx')
#         except:
#             pass
            
#         fs = FileSystemStorage()
#         filename = fs.save('corporate1.xlsx', excel_file)
#         file_url = fs.url(filename)
        

#         file_path = fs.path(filename)  # Get the absolute file path
#         print(file_path, 'file_path')
#         letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',\
#             'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ']
#         # letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#         print(letters[0])

    
#         # Use openpyxl to load the workbook
#         workbook = load_workbook(file_path)
#         # print(workbook, 'workbookworkbookworkbook')
#         sheet = workbook.active  # Get the first sheet
#         invalid_count = 0
#         # Process rows
#         for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
#             # print(row_index, 'row_indexrow_indexrow_index')
#             if row_index == 1:
#                 continue
            
#             print(row)
#             weekeday = row[0]
#             status = row[1]
#             if status == None:
#                 get_cell = str(letters[1]) + str(row_index)
#                 print(get_cell)
#                 fill_color = PatternFill(start_color="FFFF00",  # Hex color code (yellow in this case)
#                         end_color="FFFF00",
#                         fill_type="solid")

#                 cell_bg1 = sheet[get_cell]
#                 cell_bg1.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
#                 workbook.save(file_path)
#                 invalid_count += 1
#             print(weekeday, status, 'Data ')
    
#         if invalid_count == 0:
#             flag = 'Valid'
#         else:
#             flag = 'Invalid'
            

#         response_data = {
#         "statuscode":200,
#         "status":"Success",
#         'message':'File Upload successulfully.',
#         "invalid_count":invalid_count,
#         "flag":flag
#        }
#     json_data = JSONRenderer().render(response_data)
#     return HttpResponse(json_data, content_type= 'application/json')


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
        print(python_data, 'python_data')
        
        Base_url = 'http://122.170.109.73:7700/media/'
        letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',\
                'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ']
            
        
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
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue
                
                print(row_index, row, 'CHeck row')
                name = row[0]
                mobile = row[1]
                email = row[2]
                staff_code = row[3]
                staff_type = row[4]
                staff_level = row[5]
                type_of_access = row[6]
                department = row[7]
                
                check_mobile = models.StaffDetail.objects.filter(mobile = mobile).count()
                if check_mobile != 0:
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                
                check_email = models.StaffDetail.objects.filter(email = email).count()
                if check_email != 0:
                    get_cell = str(letters[2]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_staff_code = models.StaffDetail.objects.filter(staff_code = staff_code).count()
                if check_staff_code != 0:
                    get_cell = str(letters[3]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_staff_type = models.StaffType.objects.filter(staff_type = staff_type).count()
                if check_staff_type == 0:
                    get_cell = str(letters[4]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                
                check_staff_level = models.StaffLevel.objects.filter(staff_level = staff_level).count()
                print(staff_level, check_staff_level, 'check_staff_level')
                if check_staff_level == 0:
                    get_cell = str(letters[5]) + str(row_index)
                    print(get_cell, 'get_cell')
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1
                
                check_type_of_access = models.TypeOfAccess.objects.filter(type_of_access = type_of_access).count()
                if check_type_of_access == 0:
                    get_cell = str(letters[6]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_department = models.StaffDepartment.objects.filter(staff_department = department).count()
                if check_department == 0:
                    get_cell = str(letters[7]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            print(invalid_count, 'invalid_count')

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'
            print(filename, 'filename')
            link = Base_url + filename
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
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue
                # mobile																		

                print(row_index, row, 'CHeck row')
                mobile = row[0]
                email = row[1]
                corporate_name = row[2]
                corporate_code = row[3]
                parent_company = row[4]
                type_of_corporation = row[5]
                industry = row[6]
                spoke_person = row[7]
                billing_cycle = row[8]
                level1 = row[9]
                level2 = row[10]
                pan_card = row[11]
                GST_no = row[12]
                start_date = row[13]
                address = row[14]
                pincode = row[15]
                state = row[16]
                city = row[17]
                login_via = row[18]
                
                check_mobile = models.CorporateDetail.objects.filter(mobile = mobile).count()
                if check_mobile != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                
                check_email = models.CorporateDetail.objects.filter(email = email).count()
                if check_email != 0:
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_corporate_code = models.CorporateDetail.objects.filter(corporate_code = corporate_code).count()
                if check_corporate_code != 0:
                    get_cell = str(letters[3]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_parent_company = models.ParentCompany.objects.filter(parent_company = parent_company).count()
                if check_parent_company == 0:
                    get_cell = str(letters[4]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                
                check_billing_cycle = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).count()
                if check_billing_cycle == 0:
                    get_cell = str(letters[8]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1
                
                if level1 != None:
                    check_level1 = models.StaffDetail.objects.filter(email = level1).count()
                    if check_level1 == 0:
                        get_cell = str(letters[9]) + str(row_index)
                        cell_bg = sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        workbook.save(file_path)
                        invalid_count += 1

                if level2 != None:
                    check_level2 = models.StaffDetail.objects.filter(email = level2).count()
                    if check_level2 == 0:
                        get_cell = str(letters[10]) + str(row_index)
                        cell_bg = sheet[get_cell]
                        cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                        workbook.save(file_path)
                        invalid_count += 1

            print(invalid_count, 'invalid_count')

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'
            print(filename, 'filename')
            link = Base_url + filename
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
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                print(row_index, row, 'CHeck row')
                mobile = row[0]
                email = row[1]
                vendor_name = row[2]
                vendor_code = row[3]
                type_of_service = row[4]
                type_of_visit = row[5]
                billing_cycle = row[6]
                start_date = row[7]
                end_date = row[8]
                GST_no = row[9]
                pincode = row[10]
                address = row[11]
                state = row[12]
                city = row[13]
                stakeholder_name = row[14]
                stakeholder_mobile = row[15]
                stakeholder_email = row[16]
                contact_person1 = row[17]
                contact_person_designation1 = row[18]
                contact_person_mobile1 = row[19]
                contact_person_email1 = row[20]
                contact_person2 = row[21]
                contact_person_designation2 = row[22]
                contact_person_mobile2 = row[23]
                contact_person_email2 = row[24]
                contact_person3 = row[25]
                contact_person_designation3 = row[26]
                contact_person_mobile3 = row[27]
                contact_person_email3 = row[28]
                login_via = row[29]
                
                check_mobile = models.VendorDetail.objects.filter(mobile = mobile).count()
                if check_mobile != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                
                check_email = models.VendorDetail.objects.filter(email = email).count()
                if check_email != 0:
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_vendor_code = models.VendorDetail.objects.filter(vendor_code = vendor_code).count()
                if check_vendor_code != 0:
                    get_cell = str(letters[3]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                if check_type_of_service == 0:
                    get_cell = str(letters[4]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                
                check_type_of_visit = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).count()
                if check_type_of_visit == 0:
                    get_cell = str(letters[5]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1
                
            
                check_billing_cycle = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).count()
                if check_billing_cycle == 0:
                    get_cell = str(letters[6]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                
            print(invalid_count, 'invalid_count')

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'
            print(filename, 'filename')
            link = Base_url + filename
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
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                # 															

                print(row_index, row, 'CHeck row')
                package_name = row[0]
                package_code = row[1]
                description = row[2]
                relation_with_employee = row[3]
                age_category = row[4]
                gender = row[5]
                corporate = row[6]
                type_of_service = row[7]
                type_of_visit = row[8]
                billing_cycle = row[9]
                tags = row[10]

                MRP = row[11]
                discount_price = row[12]
                offer_price = row[13]
                start_date = row[14]
                end_date = row[15]

                list_relation = relation_with_employee.split(',')
                relation_count = 0
                for relation in list_relation:
                    print(relation, 'relation')
                    check_relation = models.Relation.objects.filter(relation = relation).count()
                    print(check_relation, 'check_relation')
                    if check_relation != 1:
                        relation_count += 1
                
                print(relation_count, 'relation_count')
                if relation_count != 0:
                    get_cell = str(letters[3]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1
            

                check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                if check_type_of_service != 1:
                    get_cell = str(letters[7]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1
                
                check_type_of_visit = models.TypeOfVisit.objects.filter(type_of_visit = type_of_visit).count()
                if check_type_of_visit == 0:
                    get_cell = str(letters[8]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1
                
                check_corporate = models.CorporateDetail.objects.filter(corporate_code = corporate).count()
                if check_corporate == 0:
                    get_cell = str(letters[6]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1
                
                check_age_category = models.AgeCategory.objects.filter(age_category = age_category).count()
                if check_age_category == 0:
                    get_cell = str(letters[4]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1
                
                check_gender = models.Gender.objects.filter(gender = gender).count()
                if check_gender == 0:
                    get_cell = str(letters[5]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_billing_cycle = models.BillingCycle.objects.filter(billing_cycle = billing_cycle).count()
                if check_billing_cycle == 0:
                    get_cell = str(letters[9]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1
                

                check_tags = models.PaymentTags.objects.filter(payment_tags = tags).count()
                if check_tags == 0:
                    get_cell = str(letters[10]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

            print(invalid_count, 'invalid_count')

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'
            print(filename, 'filename')
            link = Base_url + filename
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
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                print(row_index, row, 'CHeck row')
                mobile = row[0]
                email = row[1]
                employee_name = row[2]
                employee_code = row[3]
                corporate = row[4]
                department = row[5]
                gender = row[6]
                date_of_join = row[7]
                date_of_birth = row[8]
                hr_employee = row[9]
                hr_corporate_code = row[10]
                address = row[11]
                pincode = row[12]
                state = row[13]
                city = row[14]
                
                check_mobile = models.EmployeeDetail.objects.filter(mobile = mobile).count()
                if check_mobile != 0:
                    get_cell = str(letters[0]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                
                check_email = models.EmployeeDetail.objects.filter(email = email).count()
                if check_email != 0:
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_employee_code = models.EmployeeDetail.objects.filter(employee_code = employee_code).count()
                if check_employee_code != 0:
                    get_cell = str(letters[3]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_gender = models.Gender.objects.filter(gender = gender).count()
                if check_gender == 0:
                    get_cell = str(letters[6]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1
                
                check_corporate = models.CorporateDetail.objects.filter(corporate_code = corporate).count()
                if check_corporate == 0:
                    get_cell = str(letters[4]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1
                

                
            print(invalid_count, 'invalid_count')

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'
            print(filename, 'filename')
            link = Base_url + filename
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
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                print(row_index, row, 'CHeck row')
                center_name = row[0]
                vendor = row[1]
                package = row[2]
                type_of_service = row[3]
                address = row[4]
                pincode = row[5]
                state = row[6]
                city = row[7]
                location = row[8]
                latitude = row[9]
                longitude = row[10]
                
                check_vendor = models.VendorDetail.objects.filter(vendor_code = vendor).count()
                if check_vendor != 1:
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                
                check_package = models.PackageDetail.objects.filter(package_code = package).count()
                if check_package != 1:
                    get_cell = str(letters[2]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                if check_type_of_service != 1:
                    get_cell = str(letters[3]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                
            print(invalid_count, 'invalid_count')

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'
            print(filename, 'filename')
            link = Base_url + filename
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
            for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_index == 1:
                    continue

                print(row_index, row, 'CHeck row')
                center = row[0]
                vendor = row[1]
                type_of_service = row[2]
                holiday = row[3]
                weekly_off = row[4]
                state = row[5]
                city = row[6]
                location = row[7]
                
                check_center = models.CenterDetail.objects.filter(center_name = center).count()
                if check_center != 1:
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_vendor = models.VendorDetail.objects.filter(vendor_code = vendor).count()
                if check_vendor != 1:
                    get_cell = str(letters[1]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                check_type_of_service = models.TypeOfService.objects.filter(type_of_service = type_of_service).count()
                if check_type_of_service != 1:
                    get_cell = str(letters[2]) + str(row_index)
                    cell_bg = sheet[get_cell]
                    cell_bg.fill = PatternFill(start_color="FFFF00", end_color="FFFF00",fill_type = "solid")
                    workbook.save(file_path)
                    invalid_count += 1

                
            print(invalid_count, 'invalid_count')

            if invalid_count == 0:
                flag = 'Valid'
            else:
                flag = 'Invalid'
            print(filename, 'filename')
            link = Base_url + filename
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

