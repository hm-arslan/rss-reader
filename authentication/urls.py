from django.urls import path
from .views import register, login, test_token, logout

urlpatterns = [
    path('register', register),
    path('login', login),
    path('test-token', test_token),
    path('logout', logout),
]
