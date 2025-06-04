from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #Web Application Endpoint
    path('students/', include('apps.students.urls')),

    #Api Endpoint
    path('api/v1/', include('apps.api.urls')),


    path('', include('apps.agents.urls')),
]
