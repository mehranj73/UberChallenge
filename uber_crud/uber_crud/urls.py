from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls')),
    path("api/v1/trips/", include('trips.urls'))
]
