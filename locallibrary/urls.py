from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('catalog.urls')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('accounts/', include('django.contrib.auth.urls')),
]
