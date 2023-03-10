from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete-task/<int:id>/', views.deleteTask, name='delete'),
    path('finish/<int:id>/', views.finishTask, name='update'),
    path('edit/<int:id>/', views.EditTask.as_view(), name='edit'),
]
