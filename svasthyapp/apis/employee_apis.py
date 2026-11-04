from svasthyapp.apis.base import *
from svasthyapp.models import employee_models

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



