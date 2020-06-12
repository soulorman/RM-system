from django.urls import path
from user import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login,name='login'),
    path('index/', views.index,name='index'),
    path('logout/', views.logout,name='logout'),
    path('create/', views.create,name='create'),
    path('delete/', views.delete,name='delete'),
    path('update/', views.update,name='update'),
]