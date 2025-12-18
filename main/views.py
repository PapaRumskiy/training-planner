import json
from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets

from .models import User, Exercise, WorkOut, WorkoutExercise, Calendar
from .serializers import (
    UserSerializer, ExerciseSerializer, WorkOutSerializer,
    WorkoutExerciseSerializer, CalendarSerializer
)
from .forms import MyUserCreationForm

# ... (Всі твої ViewSets залишаються без змін) ...
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class WorkOutViewSet(viewsets.ModelViewSet):
    queryset = WorkOut.objects.all()
    serializer_class = WorkOutSerializer


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer


class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer


def index(request):
    return render(request, "main/index.html")


def exercises(request):
    exercises_list = Exercise.objects.all()
    return render(request, "main/exercises.html", {"exercises": exercises_list})


def workouts(request):
    return render(request, "main/workouts.html")


@login_required
def profile(request):
    user = request.user

    # 1. Рахуємо записи
    # Використовуємо filter, щоб рахувати тільки виконані
    done_qs = Calendar.objects.filter(user=user, status='done')
    done_count = done_qs.count()

    # 2. Історія (останні тренування зверху)
    history = done_qs.order_by('-date')

    # 3. Калорії (твоя формула)
    total_calories = done_count * 350

    # 4. Стрік (твоя логіка)
    dates = done_qs.values_list('date', flat=True).distinct().order_by('-date')
    streak = 0
    today = date.today()

    if dates:
        last_workout = dates[0]
        # Перевіряємо сьогодні або вчора
        if last_workout == today or last_workout == today - timedelta(days=1):
            streak = 1
            current_check = last_workout - timedelta(days=1)
            for d in dates[1:]:
                if d == current_check:
                    streak += 1
                    current_check -= timedelta(days=1)
                elif d > current_check:
                    continue
                else:
                    break
        else:
            streak = 0

    context = {
        'done_count': done_count,  # Для верхнього блоку
        'total_completed': done_count,  # Для заголовка таблиці
        'history': history,  # Список для таблиці
        'total_calories': total_calories,
        'streak': streak
    }
    return render(request, "main/profile.html", context)

@login_required
def calendar(request):
    return render(request, "main/calendar.html")


@login_required
def get_trainings(request):
    # Беремо події тільки поточного користувача
    events = Calendar.objects.filter(user=request.user)
    events_data = []

    for event in events:
        events_data.append({
            'id': event.id,
            'title': event.note,
            'start': event.date,
            'allDay': True,
            # Важливо передати статус, щоб JS розфарбував кольори
            'extendedProps': {'status': event.status}
        })

    return JsonResponse(events_data, safe=False)



@csrf_exempt
@login_required
def add_calendar_entry(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            date_val = data['date']
            note = data.get('note', '')
            status = data.get('status', 'planned')

            calendar_entry = Calendar.objects.create(user=user, date=date_val, note=note, status=status)
            return JsonResponse({
                'id': calendar_entry.id,
                'date': calendar_entry.date,
                'note': calendar_entry.note,
                'status': calendar_entry.status
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = MyUserCreationForm()
    return render(request, 'main/registration.html', {'form': form})


@login_required
def mark_training_done(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            date_str = data.get('date')  # Очікуємо 'YYYY-MM-DD'

            if not date_str:
                return JsonResponse({'status': 'error', 'message': 'Дата не вказана'}, status=400)

            # 1. Перевірка дати (Заборона майбутнього)
            selected_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            today = timezone.now().date()

            if selected_date > today:
                return JsonResponse({'status': 'error', 'message': 'Не можна відмічати майбутні дні!'}, status=400)

            # 2. Логіка Toggle (Шукаємо чи є запис)
            existing_record = Calendar.objects.filter(
                user=request.user,
                date=selected_date,
                status='done'
            ).first()

            if existing_record:
                # СКАСУВАННЯ: Якщо є - видаляємо
                existing_record.delete()
                action = 'removed'
            else:
                # ДОДАВАННЯ: Якщо немає - створюємо
                Calendar.objects.create(
                    user=request.user,
                    date=selected_date,
                    note="Виконано",
                    status='done'
                )
                action = 'added'

            return JsonResponse({'status': 'ok', 'action': action})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@login_required
def delete_calendar_entry(request, entry_id):
    if request.method == "DELETE":
        entry = get_object_or_404(Calendar, id=entry_id, user=request.user)
        entry.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)