document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'uk',
        firstDay: 1,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek'
        },
        // Дозволяємо виділяти дні
        selectable: true,

        // 1. Події, які вже є (потім тут будуть дані з БД)
        events: [
            { title: 'Тренування (Тест)', start: '2025-12-17' }
        ],

        // 2. ФУНКЦІЯ: Що робити, коли клікнули на дату
        dateClick: function(info) {
            // Питаємо користувача назву (поки що просто стандартне вікно браузера)
            var title = prompt('Яке тренування додати на ' + info.dateStr + '?');

            if (title) {
                // Якщо ввели назву - додаємо подію на календар візуально
                calendar.addEvent({
                    title: title,
                    start: info.dateStr,
                    allDay: true
                });

                alert('Тренування "' + title + '" додано! (Поки що тільки візуально)');
            }
        }
    });

    calendar.render();
});