from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-comment/', views.add_comment, name='add_comment'),
    path('logout/', views.logout, name='logout'),
    path('setup-users/', views.setup_users, name='setup_users'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]