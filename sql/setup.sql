CREATE TABLE chats (
    id BIGINT NOT NULL,
    group_id INT NOT NULL DEFAULT -1,
    lang_code VARCHAR(10) NOT NULL,
    cl_notif_15m BOOL NOT NULL DEFAULT FALSE,
    cl_notif_1m BOOL NOT NULL DEFAULT FALSE,
    cl_notif_next_part BOOL NOT NULL DEFAULT FALSE,
    seen_settings BOOL NOT NULL DEFAULT FALSE,
    accessible BOOL NOT NULL DEFAULT TRUE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Notifications indexes
CREATE INDEX cl_notif_15m_idx ON chats (cl_notif_15m);
CREATE INDEX cl_notif_1m_idx ON chats (cl_notif_1m);


CREATE TABLE users (
    id BIGINT NOT NULL,
    first_name VARCHAR(64) NOT NULL DEFAULT '',
    last_name VARCHAR(64) NOT NULL DEFAULT '',
    username VARCHAR(32) NOT NULL DEFAULT '',
    is_admin BOOL NOT NULL DEFAULT FALSE,
    referral VARCHAR(64) NOT NULL DEFAULT '',
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);


-- Button clicks statistics
CREATE TABLE button_clicks (
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    message_id INT NOT NULL,
    query VARCHAR(64) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX button_click_chat_id_idx ON button_clicks (chat_id);


-- Commands statistics
CREATE TABLE commands (
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    message_id INT NOT NULL,
    command VARCHAR(64) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX command_chat_id_idx ON commands (chat_id);


CREATE FUNCTION get_daily_activity(start_date DATE, end_date DATE)
RETURNS TABLE (
    day DATE,
    activity BIGINT
) AS $$
BEGIN
    RETURN QUERY
    WITH daily_data AS (
        SELECT date_trunc('day', timestamp)::DATE AS day,
               COUNT(*) AS activity
        FROM button_clicks
        WHERE timestamp >= start_date AND timestamp < end_date + INTERVAL '1 day'
        GROUP BY day

        UNION ALL

        SELECT date_trunc('day', timestamp)::DATE AS day,
               COUNT(*) AS activity
        FROM commands
        WHERE timestamp >= start_date AND timestamp < end_date + INTERVAL '1 day'
        GROUP BY day
    )
    SELECT daily_data.day, SUM(daily_data.activity::integer) AS activity
    FROM daily_data
    GROUP BY daily_data.day
    ORDER BY day;
END;
$$ LANGUAGE plpgsql;


CREATE FUNCTION get_dau(start_date DATE, end_date DATE)
RETURNS TABLE (
    day DATE,
    dau BIGINT
) AS $$
BEGIN
    RETURN QUERY
    WITH daily_users AS (
        SELECT date_trunc('day', timestamp)::DATE AS day,
               COUNT(DISTINCT user_id) AS dau
        FROM (
            SELECT * FROM button_clicks
            WHERE timestamp >= start_date AND timestamp < end_date + INTERVAL '1 day'
            UNION ALL
            SELECT * FROM commands
            WHERE timestamp >= start_date AND timestamp < end_date + INTERVAL '1 day'
        ) AS t
        GROUP BY day
    )
    SELECT * FROM daily_users
    ORDER BY day;
END;
$$ LANGUAGE plpgsql;
