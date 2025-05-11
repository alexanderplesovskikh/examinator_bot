CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    message_content TEXT NOT NULL,
    recipient TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    operation_type VARCHAR(50) NOT NULL, -- 'send' или 'update'
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP,
    message_id INTEGER,
    updating_event_id INTEGER -- ID события, которое редактируем
);
