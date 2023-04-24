from django.urls import path
import viewer.views as v 


urlpatterns = [
    path('', v.home, name='home'),
]
