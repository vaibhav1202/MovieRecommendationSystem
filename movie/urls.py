from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from movie import views
from django.views.generic.base import RedirectView
from rest_framework import routers


router = routers.DefaultRouter() 
router.register(r'userid', views.BasedOnIdViewSet)
router.register(r'title', views.BasedOnTitleViewSet)
 
urlpatterns = [
    path(r'api/', include(router.urls)),    
    path('', RedirectView.as_view(url="api/")),
]

