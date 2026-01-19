from django.urls import path
from staff.views import (
    LoginView,
    LogoutView,
    ListUsersView,
    GetDetailUserView,
    ChangeUserStatusView,
    GetProfileInformationView,
    ValidateSessionView,
    CreateUserView,
    EditProfileView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='staff_login'),
    path('logout/', LogoutView.as_view(), name='staff_logout'),
    path('list_users/', ListUsersView.as_view(), name='staff_list_users'),
    path('<int:system_user_id>/get_detail_user/', GetDetailUserView.as_view(), name='staff_get_detail_user'),
    path('<int:system_user_id>/change_status/', ChangeUserStatusView.as_view(), name='staff_change_user_status'),
    path('get_profile_information/', GetProfileInformationView.as_view(), name='staff_get_profile_information'),
    path('validate_session/', ValidateSessionView.as_view(), name='staff_validate_session'),
    path('create_user/', CreateUserView.as_view(), name='staff_create_user'),
    path('edit_profile/', EditProfileView.as_view(), name='staff_edit_profile'),
]