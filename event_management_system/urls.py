from django.contrib import admin
from django.urls import path, include
from home.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
]
