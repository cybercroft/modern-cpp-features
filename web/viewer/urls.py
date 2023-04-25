from django.urls import path
import viewer.views as v 


urlpatterns = [
    path('', v.home, name='home'),
    path('refresh', v.refresh, name='refresh'),
    path('version/<int:pk>/', v.version_detail, name='version-detail'),
    path('feature/<int:pk>/', v.feature_detail, name='feature-detail'),
    path('feature/search/', v.feature_search, name='feature-search'),
]
