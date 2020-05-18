from django.urls import path, include

from .views import signup, activate

urlpatterns = [
    path('', signup, name='signup'),
    path(r'activate/<uidb64>/<token>',
        activate, name='activate'),
]
