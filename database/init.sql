CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_date TIMESTAMP,
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS registrations (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    participant_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_registrations_event_id ON registrations(event_id);
CREATE INDEX IF NOT EXISTS idx_events_event_date ON events(event_date);

INSERT INTO events (title, description, event_date, location) VALUES
('Python конференция', 'Ежегодная встреча Python разработчиков', '2025-06-15 10:00:00', 'Москва, ул. Ленина 1'),
('Docker воркшоп', 'Практический курс по контейнеризации', '2025-07-20 14:00:00', 'Санкт-Петербург, пр. Невский 50'),
('Web разработка', 'Современные подходы к фронтенду', '2025-08-10 11:00:00', 'Онлайн');