from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from quiz.views import logout_view  # import your logout view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='quiz/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
