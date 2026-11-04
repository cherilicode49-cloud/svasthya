from svasthyapp.apis.base import *
from svasthyapp.models import masters_models

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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 





@csrf_exempt
def staff_department_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.StaffDepartment.objects.filter(id = id).count()
        if check_department == 1:
            staff_department = python_data.get('staff_department')
            status = python_data.get('status')
            if staff_department:
                check_staff_department = models.StaffDepartment.objects.filter(id = id, staff_department = staff_department).count()
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def staff_department_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        staff = python_data.get('id')
        check_staff = models.StaffDepartment.objects.filter(id = staff).count()
        if check_staff == 1:
            
            staff_details = models.StaffDepartment.objects.get(id = staff)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Staff Delete Successfully."
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




@csrf_exempt
def type_of_access_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.TypeOfAccess.objects.filter(id = id).count()
        if check_department == 1:
            type_of_access = python_data.get('type_of_access')
            status = python_data.get('status')
            if type_of_access:
                check_type_of_access = models.TypeOfAccess.objects.filter(id = id, type_of_access = type_of_access).count()
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def type_of_access_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        staff = python_data.get('id')
        check_staff = models.TypeOfAccess.objects.filter(id = staff).count()
        if check_staff == 1:
            
            staff_details = models.TypeOfAccess.objects.get(id = staff)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Type of Access Delete Successfully."
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
def staff_level_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.StaffLevel.objects.filter(id = id).count()
        if check_department == 1:
            staff_level = python_data.get('staff_level')
            status = python_data.get('status')
            if staff_level:
                check_staff_level = models.StaffLevel.objects.filter(id = id, staff_level = staff_level).count()
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def staff_level_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        staff = python_data.get('id')
        check_staff = models.StaffLevel.objects.filter(id = staff).count()
        if check_staff == 1:
            
            staff_details = models.StaffLevel.objects.get(id = staff)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Staff Level Delete Successfully."
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
def staff_type_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.StaffType.objects.filter(id = id).count()
        if check_department == 1:
            staff_type = python_data.get('staff_type')
            status = python_data.get('status')
            if staff_type:
                check_staff_type = models.StaffType.objects.filter(id = id, staff_type = staff_type).count()
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def staff_type_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        staff = python_data.get('id')
        check_staff = models.StaffType.objects.filter(id = staff).count()
        if check_staff == 1:
            
            staff_details = models.StaffType.objects.get(id = staff)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Staff Type Delete Successfully."
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





@csrf_exempt
def type_of_industry_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        type_of_industry = python_data.get('type_of_industry')
        check_type_of_industry = models.TypeOfIndustry.objects.filter(type_of_industry = type_of_industry).count()
        if check_type_of_industry == 0:
            level = models.TypeOfIndustry.objects.create(
                type_of_industry = type_of_industry,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Type of Industry Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Type of Industry already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        



@csrf_exempt
def type_of_industry_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.TypeOfIndustry.objects.filter(id = id).count()
        if check_department == 1:
            type_of_industry = python_data.get('type_of_industry')
            status = python_data.get('status')
            if type_of_industry:
                check_type_of_industry = models.TypeOfIndustry.objects.filter(id = id, type_of_industry = type_of_industry).count()
                if check_type_of_industry == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Type of Industry Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_type_of_industry = models.TypeOfIndustry.objects.filter(type_of_industry = type_of_industry).count()
                    if check_type_of_industry == 0:
                        level = models.TypeOfIndustry.objects.get(id = id)
                        level.type_of_industry = type_of_industry
                        level.status = python_data.get('status', level.status)
                        level.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Type of Industry Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Type of Industry already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                level = models.TypeOfIndustry.objects.get(id = id)
                level.status = python_data.get('status', level.status)
                level.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Type of Industry Status Update Successfully."
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
def all_type_of_industry_list(request):
    if request.method == 'POST':
        all_type_of_industry = models.TypeOfIndustry.objects.all().order_by('-id')
        serialiser = TypeOfIndustrySerializer(all_type_of_industry, many=True)
        
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
def type_of_industry_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        industry = python_data.get('id')
        check_staff = models.TypeOfIndustry.objects.filter(id = industry).count()
        if check_staff == 1:
            
            staff_details = models.TypeOfIndustry.objects.get(id = industry)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Type of Industry Delete Successfully."
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




@csrf_exempt
def all_active_type_of_industry_list(request):
    if request.method == 'POST':
        type_of_industry = models.TypeOfIndustry.objects.filter(status='Active').order_by('-id')
        serialiser = TypeOfIndustrySerializer(type_of_industry, many=True)
        
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
def duration_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        duration = python_data.get('duration')
        check_duration = models.Duration.objects.filter(duration = duration).count()
        if check_duration == 0:
            duration = models.Duration.objects.create(
                duration = duration,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Duration Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Duration already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        



@csrf_exempt
def duration_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_duration = models.Duration.objects.filter(id = id).count()
        if check_duration == 1:
            duration = python_data.get('duration')
            status = python_data.get('status')
            if duration:
                check_duration = models.Duration.objects.filter(id = id, duration = duration).count()
                if check_duration == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Duration Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_duration = models.Duration.objects.filter(duration = duration).count()
                    if check_duration == 0:
                        level = models.Duration.objects.get(id = id)
                        level.duration = duration
                        level.status = python_data.get('status', level.status)
                        level.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Duration Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Duration already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                level = models.Duration.objects.get(id = id)
                level.status = python_data.get('status', level.status)
                level.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Duration Status Update Successfully."
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
def all_duration_list(request):
    if request.method == 'POST':
        all_duration = models.Duration.objects.all().order_by('-id')
        serialiser = DurationSerializer(all_duration, many=True)
        
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
def duration_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        duration = python_data.get('id')
        check_duration = models.Duration.objects.filter(id = duration).count()
        if check_duration == 1:
            
            duration_details = models.Duration.objects.get(id = duration)
            duration_details.status = 'Inactive'
            duration_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Duration Delete Successfully."
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




@csrf_exempt
def all_active_duration_list(request):
    if request.method == 'POST':
        duration = models.Duration.objects.filter(status='Active').order_by('-id')
        serialiser = DurationSerializer(duration, many=True)
        
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
def platform_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        platform = python_data.get('platform')
        check_platform = models.Platform.objects.filter(platform = platform).count()
        if check_platform == 0:
            platform = models.Platform.objects.create(
                platform = platform,
                status = 'Active'
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Platform Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "This Platform already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        


@csrf_exempt
def platform_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_platform = models.Platform.objects.filter(id = id).count()
        if check_platform == 1:
            platform = python_data.get('platform')
            status = python_data.get('status')
            if platform:
                check_platform = models.Platform.objects.filter(id = id, platform = platform).count()
                if check_platform == 1:
                    res = {
                        'statuscode' : 200,
                        'status':'true',
                        'message' : "Platform Update Successfully."
                        }
                    json_data = JSONRenderer().render(res)
                    return HttpResponse(json_data, content_type= 'application/json') 
                else:
                    check_platform = models.Platform.objects.filter(platform = platform).count()
                    if check_platform == 0:
                        level = models.Platform.objects.get(id = id)
                        level.platform = platform
                        level.status = python_data.get('status', level.status)
                        level.save()
                        res = {
                            'statuscode' : 200,
                            'status':'true',
                            'message' : "Platform Update Successfully."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
                    else:
                        res = {
                            'statuscode' : 406,
                            'status':'false',
                            'message' : "This Platform already Created."
                            }
                        json_data = JSONRenderer().render(res)
                        return HttpResponse(json_data, content_type= 'application/json') 
            if status:
                level = models.Platform.objects.get(id = id)
                level.status = python_data.get('status', level.status)
                level.save()
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Platform Status Update Successfully."
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
def all_platform_list(request):
    if request.method == 'POST':
        all_platform = models.Platform.objects.all().order_by('-id')
        serialiser = PlatformSerializer(all_platform, many=True)
        
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
def platform_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        platform = python_data.get('id')
        check_platform = models.Platform.objects.filter(id = platform).count()
        if check_platform == 1:
            
            platform_details = models.Platform.objects.get(id = platform)
            platform_details.status = 'Inactive'
            platform_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Platform Delete Successfully."
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
def all_active_platform_list(request):
    if request.method == 'POST':
        platform = models.Platform.objects.filter(status='Active').order_by('-id')
        serialiser = PlatformSerializer(platform, many=True)
        
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
def age_category_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.AgeCategory.objects.filter(id = id).count()
        if check_department == 1:
            age_category = python_data.get('age_category')
            status = python_data.get('status')
            if age_category:
                check_age_category = models.AgeCategory.objects.filter(id = id, age_category = age_category).count()
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def age_category_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        age = python_data.get('id')
        check_staff = models.AgeCategory.objects.filter(id = age).count()
        if check_staff == 1:
            
            staff_details = models.AgeCategory.objects.get(id = age)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Age Category Delete Successfully."
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





@csrf_exempt
def gender_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.Gender.objects.filter(id = id).count()
        if check_department == 1:
            gender = python_data.get('gender')
            status = python_data.get('status')
            if gender:
                check_gender = models.Gender.objects.filter(id = id, gender = gender).count()
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def gender_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        gender = python_data.get('id')
        check_staff = models.Gender.objects.filter(id = gender).count()
        if check_staff == 1:
            
            staff_details = models.Gender.objects.get(id = gender)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Gender Delete Successfully."
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




@csrf_exempt
def relation_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.Relation.objects.filter(id = id).count()
        if check_department == 1:
            relation = python_data.get('relation')
            status = python_data.get('status')
            if relation:
                check_relation = models.Relation.objects.filter(id = id, relation = relation).count()
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def relation_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        relation = python_data.get('id')
        check_staff = models.Relation.objects.filter(id = relation).count()
        if check_staff == 1:
            
            staff_details = models.Relation.objects.get(id = relation)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Relation Delete Successfully."
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




@csrf_exempt
def type_of_service_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.TypeOfService.objects.filter(id = id).count()
        if check_department == 1:
            type_of_service = python_data.get('type_of_service')
            status = python_data.get('status')
            if type_of_service:
                check_type_of_service = models.TypeOfService.objects.filter(id = id, type_of_service = type_of_service).count()
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def type_of_service_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        service = python_data.get('id')
        check_staff = models.TypeOfService.objects.filter(id = service).count()
        if check_staff == 1:
            
            staff_details = models.TypeOfService.objects.get(id = service)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Type of Service Delete Successfully."
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





@csrf_exempt
def type_of_visit_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.TypeOfVisit.objects.filter(id = id).count()
        if check_department == 1:
            type_of_visit = python_data.get('type_of_visit')
            status = python_data.get('status')
            if type_of_visit:
                check_type_of_visit = models.TypeOfVisit.objects.filter(id = id, type_of_visit = type_of_visit).count()
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def type_of_visit_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        visit = python_data.get('id')
        check_staff = models.TypeOfVisit.objects.filter(id = visit).count()
        if check_staff == 1:
            
            staff_details = models.TypeOfVisit.objects.get(id = visit)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Type of Visit Delete Successfully."
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




@csrf_exempt
def parent_company_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.ParentCompany.objects.filter(id = id).count()
        if check_department == 1:
            parent_company = python_data.get('parent_company')
            status = python_data.get('status')
            if parent_company:
                check_parent_company = models.ParentCompany.objects.filter(id = id, parent_company = parent_company).count()
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 





@csrf_exempt
def parent_company_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        visit = python_data.get('id')
        check_staff = models.ParentCompany.objects.filter(id = visit).count()
        if check_staff == 1:
            
            staff_details = models.ParentCompany.objects.get(id = visit)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Parent Company Delete Successfully."
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





@csrf_exempt
def billing_cycle_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.BillingCycle.objects.filter(id = id).count()
        if check_department == 1:
            billing_cycle = python_data.get('billing_cycle')
            status = python_data.get('status')
            if billing_cycle:
                check_billing_cycle = models.BillingCycle.objects.filter(id = id, billing_cycle = billing_cycle).count()
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def billing_cycle_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        cycle = python_data.get('id')
        check_staff = models.BillingCycle.objects.filter(id = cycle).count()
        if check_staff == 1:
            
            staff_details = models.BillingCycle.objects.get(id = cycle)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Billing Cycle Delete Successfully."
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




@csrf_exempt
def weekdays_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.Weekdays.objects.filter(id = id).count()
        if check_department == 1:
            weekdays = python_data.get('weekdays')
            status = python_data.get('status')
            if weekdays:
                check_weekdays = models.Weekdays.objects.filter(id = id, weekdays = weekdays).count()
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def weekdays_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        week = python_data.get('id')
        check_staff = models.Weekdays.objects.filter(id = week).count()
        if check_staff == 1:
            
            staff_details = models.Weekdays.objects.get(id = week)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Weekedays Delete Successfully."
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






@csrf_exempt
def holidays_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.Holidays.objects.filter(id = id).count()
        if check_department == 1:
            holidays = python_data.get('holidays')
            status = python_data.get('status')
            if holidays:
                check_holidays = models.Holidays.objects.filter(id = id, holidays = holidays).count()
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
def holidays_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        holiday = python_data.get('id')
        check_staff = models.Holidays.objects.filter(id = holiday).count()
        if check_staff == 1:
            
            staff_details = models.Holidays.objects.get(id = holiday)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Holidays Delete Successfully."
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





@csrf_exempt
def payment_tags_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
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
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        check_department = models.PaymentTags.objects.filter(id = id).count()
        if check_department == 1:
            payment_tags = python_data.get('payment_tags')
            status = python_data.get('status')
            if payment_tags:
                check_payment_tags = models.PaymentTags.objects.filter(id = id, payment_tags = payment_tags).count()
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
def payment_tags_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        tags = python_data.get('id')
        check_staff = models.PaymentTags.objects.filter(id = tags).count()
        if check_staff == 1:
            
            staff_details = models.PaymentTags.objects.get(id = tags)
            staff_details.status = 'Inactive'
            staff_details.save()
        
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Payment Tags Delete Successfully."
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
       
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
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
        
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
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
        
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
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
        data = json.dumps(res)
        encoded_dict = str(data).encode('utf-8')
        data = base64.b64encode(encoded_dict)
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, content_type= 'application/json') 





@csrf_exempt
def test_category_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        test_category = python_data.get('test_category')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_staff_type = models.TestCategory.objects.filter(test_category = test_category).count()
        if check_staff_type == 0:
            level = models.TestCategory.objects.create(
                test_category = test_category,
                status = 'Active',
                created_at = current_time
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Test category Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Test Category already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def test_category_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        test_category = python_data.get('test_category')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_test = models.TestCategory.objects.filter(test_category = test_category).count()
        if check_test == 0:
            test = models.TestCategory.objects.get(id = id)
            test.test_category = python_data.get('test_category', test.test_category)
            test.status = python_data.get('status', test.status)
            test.save()
                
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Test category update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            check_test = models.TestCategory.objects.filter(id = id, test_category = test_category).count()
            if check_test == 1:
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Test category update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Test Category already Created."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def all_test_category_list(request):
    if request.method == 'POST':
        all_staff_level = models.TestCategory.objects.all().order_by('-id')
        serialiser = TestCategoryTransaction(all_staff_level, many=True)
        
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
def test_sub_category_create(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        test_category = python_data.get('test_category')
        test_subcategory = python_data.get('test_subcategory')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_staff_type = models.TestSubCategory.objects.filter(test_category = test_category, test_subcategory= test_subcategory).count()
        if check_staff_type == 0:
            level = models.TestSubCategory.objects.create(
                test_category_id = test_category,
                test_subcategory = test_subcategory,
                status = 'Active',
                created_at = current_time
            ).save()
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Test Subcategory Create Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            res = {
                'statuscode' : 406,
                'status':'false',
                'message' : "Test Subcategory already Created."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 




@csrf_exempt
def test_sub_category_update(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        test_category = python_data.get('test_category')
        test_subcategory = python_data.get('test_subcategory')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        check_test = models.TestSubCategory.objects.filter(test_category = test_category, test_subcategory= test_subcategory).count()
        if check_test == 0:
            test = models.TestSubCategory.objects.get(id = id)
            test.test_category_id = python_data.get('test_category', test.test_category)
            test.test_subcategory = python_data.get('test_subcategory', test.test_subcategory)
            test.status = python_data.get('status', test.status)
            test.save()
                
            res = {
                'statuscode' : 200,
                'status':'true',
                'message' : "Test Subcategory update Successfully."
                }
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type= 'application/json') 
        else:
            check_test = models.TestSubCategory.objects.filter(id = id, test_category = test_category, test_subcategory= test_subcategory).count()
            if check_test == 1:
                res = {
                    'statuscode' : 200,
                    'status':'true',
                    'message' : "Test Subcategory update Successfully."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 
            else:
                res = {
                    'statuscode' : 406,
                    'status':'false',
                    'message' : "Test Subcategory already Created."
                    }
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type= 'application/json') 



@csrf_exempt
def all_test_subcategory_list(request):
    if request.method == 'POST':
        all_staff_level = models.TestSubCategory.objects.all().order_by('-id')
        serialiser = TestSubCategoryTransaction(all_staff_level, many=True)
        
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
def test_category_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_status = models.TestCategory.objects.filter(id = id).count()
        if check_status == 1:
            test_details = models.TestCategory.objects.get(id = id)
            test_details.status = status
            test_details.save()
        
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
def all_active_test_category_list(request):
    if request.method == 'POST':
        all_test = models.TestCategory.objects.filter(status='Active').order_by('-id')
        serialiser = TestCategoryTransaction(all_test, many=True)
        
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
def test_sub_category_delete_inactive(request):
    if request.method == 'POST':
        python_data = JSONParser().parse(io.BytesIO(request.body))
        id = python_data.get('id')
        status = python_data.get('status')
        check_status = models.TestSubCategory.objects.filter(id = id).count()
        if check_status == 1:
            test_details = models.TestSubCategory.objects.get(id = id)
            test_details.status = status
            test_details.save()
        
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
def all_active_test_subcategory_list(request):
    if request.method == 'POST':
        all_test = models.TestSubCategory.objects.filter(status='Active').order_by('-id')
        serialiser = TestSubCategoryTransaction(all_test, many=True)
        
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


