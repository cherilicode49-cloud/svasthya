from svasthyapp.apis.base import *
from svasthyapp.models import center_models

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





