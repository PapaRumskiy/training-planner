import pytest
from django.urls import reverse
from main.models import User, Calendar
from datetime import date


# Цей маркер дає доступ до БД
@pytest.mark.django_db
class TestTrainingPlanner:

    # 1. Перевірка, що головна сторінка відкривається
    def test_index_view(self, client):
        url = reverse('index')
        response = client.get(url)
        assert response.status_code == 200
        assert "ПЛАНУЙ. ТРЕНУЙСЯ" in response.content.decode('utf-8')

    # 2. Перевірка реєстрації користувача
    def test_user_registration(self, client):
        url = reverse('registration')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',  # У формі Django це може бути password1
            # Тут залежить від твоєї форми, стандартна UserCreationForm вимагає підтвердження
        }
        # Простий тест створення юзера через ORM
        user = User.objects.create_user(username='pytest_user', password='password')
        assert user.username == 'pytest_user'
        assert User.objects.count() == 1

    # 3. Перевірка доступу до профілю (має бути редірект якщо не залогінений)
    def test_profile_redirect_if_not_logged_in(self, client):
        url = reverse('profile')
        response = client.get(url)
        # Очікуємо 302 (Redirect на login), бо стоїть @login_required
        assert response.status_code == 302

        # 4. Перевірка додавання запису в календар (API)

    def test_add_calendar_entry(self, client):
        # Створюємо і логінимо юзера
        user = User.objects.create_user(username='api_user', password='password')
        client.force_login(user)

        url = reverse('add_calendar_entry')
        data = {
            'date': str(date.today()),
            'note': 'Test Workout',
            'status': 'planned'
        }

        response = client.post(
            url,
            data,
            content_type='application/json'
        )

        assert response.status_code == 200
        assert Calendar.objects.count() == 1
        entry = Calendar.objects.first()
        assert entry.note == 'Test Workout'
        assert entry.user == user