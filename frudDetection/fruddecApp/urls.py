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
     path('demo_frud_deposit/',views.demo_frud_deposit,name='demo_frud_deposit'),
    path('user_admin/',views.user_admin,name='user_admin'),
    path('update_admin/',views.update_admin,name='update_admin'),
    path('update_user_2/',views.update_user_2,name='update_user_by_user_self'),
    path('add_user/',views.add_user,name='add_user'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('select_winner/',views.select_winner,name='select_winner'),
    path('credit_monthly_return/',views.credit_monthly_return_view,name='credit_monthly_return'),
]