"""
URL configuration for new_pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import  include
from app5 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path("logout/", views.logout, name="logout"),
    path('register/', views.register, name='register'),

    path('user_home/', views.user_home, name='user_home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path("profile/", views.profile, name="profile"),
    path("category/", views.category, name="category"),
    path("quiz/<str:category>/", views.quiz, name="quiz"),
    path("instruction/<str:category>/", views.instruction, name="instruction"),
    path("quiz/<str:category>/", views.quiz, name="quiz"),
    path("admin_index/", views.admin_home, name="admin_index"),
path(
    "manage_questions/",
    views.manage_questions,
    name="manage_questions"
),

path(
    "manage_category/<str:category>/",
    views.manage_category,
    name="manage_category",
),

path(
    "result/<int:attempt_id>/",
    views.result,
    name="result"
),


path("quizify-admin/manage-users/", views.manage_users, name="manage_users"),

path(
    "manage-users/view/<int:user_id>/",
    views.view_user,
    name="view_user",
),

path(
    "manage-users/delete/<int:user_id>/",
    views.delete_user,
    name="delete_user",
),

path(
    "statistics/",
    views.statistics,
    name="statistics",
),
path(
    "statistics/quiz-attempts/",
    views.quiz_attempts,
    name="quiz_attempts",
),
path(
    "statistics/category-details/",
    views.category_details,
    name="category_details",
),

]
