from django.conf import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
]

if settings.DEBUG:
    urlpatterns.append(
        path("__reload__/", include("django_browser_reload.urls"))
    )
