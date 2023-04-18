from django.urls import path, include

urlpatterns = [
    path('auth/', include('django_cicd.authentication.urls')),
]
