from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoginApiView, RegisterUserView, UsersListView, UserView

router = DefaultRouter()
router.register('users', UsersListView, basename='user_list')

urlpatterns = [
    path('v1/auth/signup/', RegisterUserView.as_view(), name='register_user'),
    path('v1/auth/token/', LoginApiView.as_view(), name='login_api_view'),
    path('v1/users/me/', UserView.as_view(), name='user_view'),
    path('v1/', include(router.urls))
]
