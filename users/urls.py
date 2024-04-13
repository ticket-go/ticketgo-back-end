from django.urls import path
from users.api.viewsets import LoginViewSet, CustomUserViewSet

urlpatterns = [
    path('register/', CustomUserViewSet.as_view(), name='register'),
    path('login/', LoginViewSet.as_view(), name='login'),
    
]