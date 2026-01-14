from django.urls import path
from staff.views import (
    LoginView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='staff_login'),
]