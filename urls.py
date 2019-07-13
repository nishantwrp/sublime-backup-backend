from django.urls import path,include
from .views import *
urlpatterns = [
    path('auth/register/',RegisterView.as_view()),
    path('auth/',LoginView.as_view()),
    path('connect/',CheckView.as_view())
]
