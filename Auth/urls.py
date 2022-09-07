from django.urls import path

from .views import login, logout, register, resetpassword, checkresetcode, confirmreset

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('resetpassword/', resetpassword, name='resetpassword'),
    path('checkresetcode/', checkresetcode, name='checkresetcode'),
    path('confirmreset/', confirmreset, name='confirmreset'),
]