from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('newsportal.posts.urls', 'newsportal.posts'), namespace='posts')),
    path('registration/', include('django.contrib.auth.urls')),
    path('signup/', include(('newsportal.registration.urls', 'newsportal.registration'), namespace='registration')),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)