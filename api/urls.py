from django.urls import path
from .views import RegisterView, UserListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/', UserListView.as_view(), name='users'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
