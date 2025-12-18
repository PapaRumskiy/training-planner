from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ExerciseViewSet, WorkOutViewSet, WorkoutExerciseViewSet, CalendarViewSet
from . import views
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'workouts', WorkOutViewSet)
router.register(r'workoutexercises', WorkoutExerciseViewSet)
router.register(r'calendars', CalendarViewSet)

urlpatterns = [
    # Головні сторінки
    path('', views.index, name='index'),
    path('exercises/', views.exercises, name='exercises'), # ПОВЕРНУВ name='exercises'
    path('workouts/', views.workouts, name='workouts'),
    path('profile/', views.profile, name='profile'),
    path('calendar/', views.calendar, name='calendar'),

    # API для календаря
    path('api/add_calendar_entry/', views.add_calendar_entry, name='add_calendar_entry'),
    path('api/get-trainings/', views.get_trainings, name='get_trainings'), # ДОДАВ ЦЕЙ РЯДОК (Без нього не буде видно старих записів)

    # Авторизація
    path('registration/', views.register, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    path('api/delete_calendar_entry/<int:entry_id>/', views.delete_calendar_entry, name='delete_calendar_entry'),
]