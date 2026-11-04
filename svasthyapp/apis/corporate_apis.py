from svasthyapp.apis.base import *
from svasthyapp.models import corporate_models

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

