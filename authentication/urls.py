from django.urls import path
from .views import set_csrf_token, login_view, logout_view, CheckAuth

urlpatterns = [
  path('set-csrf/', set_csrf_token, name='Set-CSRF'),
  path('login/', login_view, name='Login'),
  path('logout/', logout_view, name='Logout'),
  path('test-auth/', CheckAuth.as_view(), name='Test-Auth')
]
