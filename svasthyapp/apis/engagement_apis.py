from svasthyapp.apis.base import *
from svasthyapp.models import engagement_models

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


