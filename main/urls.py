from django.urls import path
from . import views

urlpatterns = [
    path('', views.func_main),
    path('settings', views.func_settings),
    path('opportunities', views.func_opportunities)
]