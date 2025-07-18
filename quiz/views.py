from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST

from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .Options import CustomUserCreationForm 
from .models import Quiz, Question, Result
from .Options import QuizForm
from .serializers import QuizSerializer, QuestionSerializer, ResultSerializer


# Home Page - List all quizzes
def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/home.html', {'quizzes': quizzes})


# Take a quiz
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                selected = form.cleaned_data.get(f'question_{question.id}')
                if selected == question.correct_answer:
                    score += 1
            # Save result
            Result.objects.create(user=request.user, quiz=quiz, score=score)
            return render(request, 'quiz/result.html', {
                'score': score,
                'total': questions.count(),
                'quiz': quiz,
            })
    else:
        form = QuizForm(questions=questions)

    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'form': form,
    })


# Quiz history page
@login_required
def quiz_history(request):
    results = Result.objects.filter(user=request.user).select_related('quiz').order_by('-id')
    return render(request, 'quiz/history.html', {'results': results})


# User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/register.html', {'form': form})


#  Custom Logout View (fixes 405 error)
@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

#  REST API: Quiz ViewSet
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.AllowAny]  # Optional: change to IsAuthenticated if needed


# REST API: Question ViewSet
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]


# REST API: Result ViewSet
class ResultViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Result.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
