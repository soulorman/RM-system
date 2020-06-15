from django.urls import path
from user import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login,name='login'),
    path('index/', views.index,name='index'),
    path('logout/', views.logout,name='logout'),
    
    path('create/ajax/', views.create_ajax, name="create_ajax"),
    path('delete/ajax/', views.delete_ajax, name="delete_ajax"),
    path('changepass/ajax/', views.changepass_ajax, name="changepass_ajax"),
]