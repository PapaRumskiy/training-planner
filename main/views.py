from django.shortcuts import render

from rest_framework import viewsets

from .models import User, Exercise, WorkOut, WorkoutExercise, Calendar

from .serializers import UserSerializer, ExerciseSerializer, WorkOutSerializer, WorkoutExerciseSerializer, CalendarSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class=UserSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class=ExerciseSerializer


class WorkOutViewSet(viewsets.ModelViewSet):
    queryset = WorkOut.objects.all()
    serializer_class=WorkOutSerializer


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    queryset = WorkoutExercise.objects.all()
    serializer_class=WorkoutExerciseSerializer


class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class=CalendarSerializer

    


def index(request):
    return render(request, "main/index.html")

def exercises(request):
    return render(request, "main/exercises.html")

def workouts(request):
    return render(request, "main/workouts.html")

def profile(request):
    return render(request, "main/profile.html")

def calendar(request):
    return render(request, "main/calendar.html")
