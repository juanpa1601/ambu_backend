from django.urls import path
from staff.views import (
    LoginView,
    LogoutView,
    ListUsersView,
    GetDetailUserView,
    ChangeUserStatusView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='staff_login'),
    path('logout/', LogoutView.as_view(), name='staff_logout'),
    path('list_users/', ListUsersView.as_view(), name='staff_list_users'),
    path('<int:system_user_id>/get_detail_user/', GetDetailUserView.as_view(), name='staff_get_detail_user'),
    path('<int:system_user_id>/change_status/', ChangeUserStatusView.as_view(), name='staff_change_user_status'),
]