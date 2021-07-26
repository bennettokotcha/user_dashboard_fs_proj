from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.register_page),
    path('login', views.login_page),
    path('login-user', views.login_proccess),
    path('register-admin', views.register_admin),
    path('dashboard/admin', views.user_admin_page),
    path('user/new', views.add_user_page),
    path('admin/edit/<int:id>', views.admin_edit_page),
    path('add-user/proccess', views.add_user_proccess),
    path('users/edit/<int:id>', views.user_edit_page),
    path('edit/<int:id>/proccess', views.edit_info_proccess),
    path('user/remove/<int:number>', views.remove_user),
    path('logout', views.logout),
]