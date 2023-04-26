from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('viewer.urls')),
    path('admin/', admin.site.urls),
]

# one-time startup function after server-starts
def _startup():
    from viewer.utils import setup
    setup() 
   
    
_startup()