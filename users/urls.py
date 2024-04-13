from django.urls import path
from users.api.viewsets import LoginViewSet, CustomUserViewSet, CustomUserUpdateViewSet

urlpatterns = [
    path('register/', CustomUserViewSet.as_view(), name='register'),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('update/', CustomUserUpdateViewSet.as_view(), name='user update'),
]