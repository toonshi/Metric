from django.urls import path
from . import views

app_name = "hospitals"
urlpatterns = [
path('institution', views.institution_detail, name="institution"),
]