from svasthyapp.apis.base import *
from svasthyapp.models import auth_models

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
        OTP = '121212'

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



