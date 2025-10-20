# asha_project/urls.py
from django.contrib import admin
from django.urls import path, include
from core_app.views import landing_page_view # Import the new view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page_view, name='landing_page'), # Sets the landing page as the root
    path('', include('core_app.urls')), # Includes all other core_app URLs
]