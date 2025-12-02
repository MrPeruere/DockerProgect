const API_URL = '/api';

// Загрузка статистики на главной странице
if (document.getElementById('totalEvents')) {
    fetch(`${API_URL}/stats`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('totalEvents').textContent = data.events;
            document.getElementById('totalRegistrations').textContent = data.registrations;
        });
}

// Загрузка списка событий
if (document.getElementById('eventsList')) {
    loadEvents();
}

function loadEvents() {
    fetch(`${API_URL}/events`)
        .then(res => res.json())
        .then(events => {
            const container = document.getElementById('eventsList');
            container.innerHTML = events.map(event => `
                <div class="event-card">
                    <h3>${event.title}</h3>
                    <p>${event.description}</p>
                    <p><strong>Дата:</strong> ${new Date(event.event_date).toLocaleString('ru-RU')}</p>
                    <p><strong>Место:</strong> ${event.location}</p>
                </div>
            `).join('');
        });
}

// Создание нового события
if (document.getElementById('createEventForm')) {
    document.getElementById('createEventForm').addEventListener('submit', (e) => {
        e.preventDefault();

        const eventData = {
            title: document.getElementById('title').value,
            description: document.getElementById('description').value,
            event_date: document.getElementById('eventDate').value,
            location: document.getElementById('location').value
        };

        fetch(`${API_URL}/events`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(eventData)
        })
        .then(res => res.json())
        .then(() => {
            alert('Событие создано!');
            e.target.reset();
            loadEvents();
        });
    });
}

// Загрузка событий в select для регистрации
if (document.getElementById('eventSelect')) {
    fetch(`${API_URL}/events`)
        .then(res => res.json())
        .then(events => {
            const select = document.getElementById('eventSelect');
            select.innerHTML = '<option value="">Выберите мероприятие</option>' +
                events.map(e => `<option value="${e.id}">${e.title} - ${new Date(e.event_date).toLocaleDateString('ru-RU')}</option>`).join('');
        });
}

// Регистрация на событие
if (document.getElementById('registrationForm')) {
    document.getElementById('registrationForm').addEventListener('submit', (e) => {
        e.preventDefault();

        const eventId = document.getElementById('eventSelect').value;
        const regData = {
            participant_name: document.getElementById('participantName').value,
            email: document.getElementById('email').value
        };

        fetch(`${API_URL}/events/${eventId}/register`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(regData)
        })
        .then(res => res.json())
        .then(() => {
            document.getElementById('message').innerHTML = '<p style="color: green;">Вы успешно зарегистрированы!</p>';
            e.target.reset();
        })
        .catch(() => {
            document.getElementById('message').innerHTML = '<p style="color: red;">Ошибка регистрации</p>';
        });
    });
}