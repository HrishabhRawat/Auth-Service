from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserPasswordchangeView, SendUserPasswordEmailview

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name= 'profile'),
    path('change-password/', UserPasswordchangeView.as_view(), name='password-change'),
    path('send-rest-password-email/', SendUserPasswordEmailview.as_view(), name = 'send-rest-password-email'),

    
]
