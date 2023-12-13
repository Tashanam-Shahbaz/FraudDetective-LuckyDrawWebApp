from django.contrib import admin
from django.urls import path
from fruddecApp import views
 
urlpatterns = [
    path('', views.home, name='home'),
    path('signin/',views.signin, name='signin'),
    path('signout/',views.signout, name='signout'),
    path('signup/',views.signup, name='signup'),
    path('profile/',views.profile, name='profile'),
    path('deposit/',views.deposit,name='deposit'),
    path('user_admin/',views.user_admin,name='user_admin'),
    path('update_admin/',views.update_admin,name='update_admin'),
    path('add_user/',views.add_user,name='add_user'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]