from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.profiles, name="profiles"),
    path('profile/<str:pk>/', views.profile, name="profile"),
    # Login/Register -- Logout
    path('login', views.loginPage, name="login"),
    path('register', views.registerUser, name="register"),
    path('logout', views.logoutUser, name="logout"),
    path('account', views.accountUser, name="account"),
    path('editAccount', views.editAccount, name="editAccount"),
    path('createSkill', views.skill_create, name="createSkill"),
    path('updateSkill/<str:pk>', views.skill_update, name="updateSkill"),
    path('deleteSkill/<str:pk>', views.skill_delete, name="deleteSkill"),

]