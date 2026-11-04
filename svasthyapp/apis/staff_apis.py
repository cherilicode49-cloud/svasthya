from svasthyapp.apis.base import *
from svasthyapp.models import staff_models

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


