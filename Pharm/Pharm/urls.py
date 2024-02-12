from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from hospitals.views import review_submit  # Correct import statement for the review_submit view

urlpatterns = [
    path('', include('main.urls', namespace="main")),
    path('', include('users.urls', namespace="users")),
    path('admin/', admin.site.urls),
    # Use the correct import statement for the review_submit view
    path('hospitals/<int:institution_id>/review_submit/', review_submit, name='review_submit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
