from svasthyapp.apis.base import *
from svasthyapp.models import individual_models

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


