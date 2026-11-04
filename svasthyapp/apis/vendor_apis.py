from svasthyapp.apis.base import *
from svasthyapp.models import vendor_models

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



