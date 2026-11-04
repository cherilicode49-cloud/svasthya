"""
URL configuration for svasthya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include


# handler404 = 'svasthyapp.views.custom_404'

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('svasthyapp.urls')),
    
# ]


from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from svasthyapp.swagger import schema_view, api_endpoints_catalog

handler404 = 'svasthyapp.views.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Swagger & ReDoc Endpoints
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-api-swagger'),
    path('api/swagger-endpoints/', api_endpoints_catalog, name='api-endpoints-catalog'),
    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-api-json'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-api-docs'),

    path('', include('svasthyapp.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

