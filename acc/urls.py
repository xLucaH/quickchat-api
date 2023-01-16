from django.urls import path, include

from acc import views

urlpatterns = [
    path('users/signup/', views.signup, name='signup'),
    path('users/login/', views.login, name='login'),
]
