CREATE TABLE IF NOT EXISTS group_schedule (
    group_id INTEGER,
    date TEXT,
    lessons TEXT,
    updated INTEGER,
    PRIMARY KEY (group_id, date)
);
CREATE INDEX IF NOT EXISTS group_schedule_date_idx ON group_schedule (date);
CREATE INDEX IF NOT EXISTS group_schedule_group_id_idx ON group_schedule (group_id);
