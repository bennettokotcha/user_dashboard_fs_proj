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
    path('users/show/<int:id>', views.posts_page),
    path('edit-i/<int:id>/proccess', views.edit_info_proccess),
    path('edit-p/<int:id>/proccess', views.edit_password_proccess),
    path('edit-d/<int:id>/proccess', views.edit_desc_proccess),
    path('edit-user-i/<int:id>/process', views.edit_user_info),
    path('edit-user-p/<int:id>/proccess', views.edit_user_password),
    path('add-post/<int:id>', views.add_post_user),
    path('user/remove/<int:number>', views.remove_user),
    path('logout', views.logout),
]