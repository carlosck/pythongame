from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from login import views

urlpatterns = [
    url(r'^auth/',views.AuthView.as_view(),name='auth-view'),
    url(r'^',views.TestView.as_view(),name='test-view'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)