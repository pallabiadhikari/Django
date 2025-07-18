from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import QuizViewSet, QuestionViewSet, ResultViewSet
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'results', ResultViewSet, basename='result')

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('history/', views.quiz_history, name='quiz_history'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='quiz/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('api/', include(router.urls)),
]
