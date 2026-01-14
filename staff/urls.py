from django.urls import path
from staff.views import (
    LoginView,
    LogoutView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='staff_login'),
    path('logout/', LogoutView.as_view(), name='staff_logout'),
]