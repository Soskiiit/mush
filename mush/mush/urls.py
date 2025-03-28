from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('catalog.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('guide/', include('guide.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns.append(
        path('__reload__/', include('django_browser_reload.urls'))
    )
