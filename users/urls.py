from django.urls import path
from users.api.viewsets import LoginViewSet, CustomUserViewSet, CustomUserUpdateViewSet, CustomUserChangePasswordViewSet, CustomUserChangeEmailViewSet

urlpatterns = [
    path('register/', CustomUserViewSet.as_view(), name='register'),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('update/', CustomUserUpdateViewSet.as_view(), name='user update'),
    path('change-password/', CustomUserChangePasswordViewSet.as_view(), name='change password'),
    path('change-email/', CustomUserChangeEmailViewSet.as_view(), name='change e-mail'),
    
]