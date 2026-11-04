from svasthyapp.apis.base import *
from svasthyapp.models import package_models

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

