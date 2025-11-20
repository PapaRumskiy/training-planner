from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ExerciseViewSet, WorkOutViewSet, WorkoutExerciseViewSet, CalendarViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'workouts', WorkOutViewSet)
router.register(r'workoutexercises', WorkoutExerciseViewSet)
router.register(r'calendars', CalendarViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
