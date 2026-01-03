from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 Include app urls ONLY
    path('', include('myapp.urls')),
]
