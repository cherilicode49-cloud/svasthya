import traceback
from django.shortcuts import render
from svasthyapp import models
from svasthyapp.models import (
    auth_models,
    masters_models,
    staff_models,
    corporate_models,
    vendor_models,
    center_models,
    employee_models,
    individual_models,
    package_models,
    appointment_models,
    orders_billing_models,
    engagement_models,
    hoh_models,
)
import io
from rest_framework.parsers import JSONParser
from datetime import datetime, timedelta, date
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import base64
import math, random 
from svasthyapp.serializer import AdminUserSerializer, CorporateSerializer, StaffDepartmentSerializer, StaffSerializer, VendorSerializer, \
    TypeOfAccessSerializer, StaffLevelSerializer, StaffTypeSerializer, AgeCategorySerializer, GenderSerializer, RelationSerializer, TypeOfServiceSerializer, \
    TypeOfVisitSerializer, ParentCompanySerializer, BillingCycleSerializer, WeekdaysSerializer, HolidaysSerializer, PaymentTagsSerializer, EmployeeDetailSerializer, \
    CorporateDataSerializer, PackageDetailSerializer, CenterDetailSerializer, EmployeeDataSerializer, VendorNameSerializer, PackageNameSerializer, HolidayDetailSerializer, \
    StaffDataSerializer, HealthTipsSerializer, EmployeeDependentSerializer, AppointmentDetailSerializer, CenterDataSerializer, IndividualUserDetailSerializer, \
    IndividualDependentSerializer, AdminModuleRightsSerializer, TypeOfIndustrySerializer, PackageVendorSerializer, AppointmentDetailEBPFSerializer, \
    NotificationNameSerializer, NotificationDetailSerializer, TransactionSerializer, AddToCartSerializer, ActiveCenterDetailTransaction, HolidayDetailDateSerializer, CenterTestSerializer, \
    PackageExportSerialiser, CenterExportSerialiser, AppointmentExportSerialiser, TestCategoryTransaction, TestSubCategoryTransaction, TestsProductDetailSerialiser, \
    ComparePackageListSerialiser, EmployeeAddressDetailSerialiser, IndividualAddressDetailSerialiser, CenterDetailSerialiser, HohEmployeeSerializer, DarwinboxCandidateAppointmentSerializer, \
    RescheduleDarwinboxCandidateAppointmentSerializer, RescheduleAppointmentSerializer
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings

import time
import os
import zipfile
import requests
from requests.auth import HTTPBasicAuth
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import xlrd as xl
import xlrd 
from django.http import JsonResponse
from openpyxl import load_workbook
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from openpyxl.styles import PatternFill
import openpyxl as op
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
from django.db.models import Q
from django.conf import settings
SITE_MEDIA_BASE_URL = settings.SITE_MEDIA_BASE_URL ## BASE URLs for media which is defind in setting.py

from django.shortcuts import render
import threading
import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re

import requests

from django.conf import settings

from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import csv
import io
from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from django.db import transaction
from django.utils.dateparse import parse_date

#### PDF
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.http import HttpResponse
from xhtml2pdf import pisa
import io
from num2words import num2words
# import datetime

import pdfkit
from django.core.files.base import ContentFile
from django.template.loader import get_template
from django.core.mail import send_mail

#### Radius code 
from math import cos, radians
from django.db.models import F
from django.db.models.functions import ACos, Cos, Sin, Radians, Cast
from django.db.models import FloatField, ExpressionWrapper


AUTHKEY = "91d8de23a0144ed5"
ENTITY_ID = "1101580270000085391"
SENDER_ID = "VMCLLP"
DLT_TEMPLATE_ID = "1107175370307466562"

