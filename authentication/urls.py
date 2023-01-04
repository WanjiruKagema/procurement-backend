from django.urls import path
from .views import RegisterView, CustomAuthToken, UserLogout

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', CustomAuthToken.as_view()),
    path('logout', UserLogout.as_view())
]
