"""
URL configuration for jobportal project.

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
from django.contrib.auth import views as auth_views
from jobs import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 


urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/add/', views.AddJobView.as_view(), name='add_job'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # auth Views
    path('login/', auth_views.LoginView.as_view(template_name='jobs/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

    # password Reset Views
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='jobs/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='jobs/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='jobs/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='jobs/password_reset_complete.html'), name='password_reset_complete'),
    
    #jwt token urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       # get token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  
    # API Views
    path('api/jobs/', views.JobApiView.as_view(), name='job_api'),
    path('api/jobs/<int:pk>/', views.JobDetailApiView.as_view(), name='job_detail_api'),
]