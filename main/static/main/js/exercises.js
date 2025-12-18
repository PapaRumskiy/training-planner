document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    // Ініціалізація календаря
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'uk',
        firstDay: 1,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek'
        },
        selectable: true,

        // Завантажуємо реальні події з БД
        events: '/api/get-trainings/',

        // ВИКЛИК МОДАЛКИ ПРИ КЛІКУ
        dateClick: function(info) {
            showModal(info.dateStr, calendar);
        }
    });

    calendar.render();
});

// ФУНКЦІЯ МОДАЛЬНОГО ВІКНА
function showModal(date, calendarInstance) {
    const modal = document.getElementById('modal');
    const noteInput = document.getElementById('note-input');
    const submitBtn = document.getElementById('submit-button');

    // Показуємо модалку (використовуємо flex для центрування, як у твоїх стилях)
    modal.style.display = 'flex';

    // Очищуємо поле перед введенням
    noteInput.value = '';

    // Обробка натискання кнопки "Submit"
    submitBtn.onclick = function() {
        const title = noteInput.value;
        // Отримуємо статус із радіокнопок
        const statusElement = document.querySelector('input[name="status"]:checked');
        const status = statusElement ? statusElement.value : 'planned';

        if (title) {
            // ВІДПРАВКА НА СЕРВЕР
            fetch('/api/add_calendar_entry/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    date: date,
                    note: title,
                    status: status
                })
            })
            .then(response => {
                if (!response.ok) throw new Error('Помилка сервера');
                return response.json();
            })
            .then(data => {
                // Додаємо подію на календар без перезавантаження
                calendarInstance.addEvent({
                    id: data.id,
                    title: title,
                    start: date,
                    allDay: true
                });

                // Закриваємо модалку
                modal.style.display = 'none';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Не вдалося зберегти тренування');
            });
        }
    };
}

// ФУНКЦІЯ ДЛЯ ОТРИМАННЯ CSRF-ТОКЕНА (Обов'язково для Django POST запитів)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggleTraining(trainingId, dateStr, element) {
    fetch('/mark_training_done/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // функція для токена
        },
        body: JSON.stringify({
            training_id: trainingId,
            date: dateStr
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'error') {
            alert(data.message); // "Не можна виконувати тренування наперед!"
        } else if (data.status === 'ok') {
            // Змінюємо вигляд клітинки/кнопки
            if (data.action === 'added') {
                element.classList.add('completed-training'); // Зелений, наприклад
                element.innerText = "Виконано";
            } else {
                element.classList.remove('completed-training'); // Повертаємо як було
                element.innerText = "Виконати";
            }
        }
    });
}
