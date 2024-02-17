# urls.py

from django.urls import path
from . import views

app_name = "hospitals"
urlpatterns = [
    path('institution', views.institution_detail, name="institution"),
    path('institution/<int:institution_id>/', views.institution_detail, name="institution_detail"),
    path('institution-list/', views.institution_list, name="institution_list"),
    path('submit-review/<int:institution_id>/', views.review_submit, name="submit_review"),  # Include the review_submit URL pattern with institution_id
]
