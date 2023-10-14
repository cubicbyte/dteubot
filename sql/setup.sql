CREATE TABLE chats (
    chat_id BIGINT NOT NULL,
    group_id INT NOT NULL DEFAULT -1,
    lang_code VARCHAR(10) NOT NULL,
    cl_notif_15m BOOL NOT NULL DEFAULT FALSE,
    cl_notif_1m BOOL NOT NULL DEFAULT FALSE,
    seen_settings BOOL NOT NULL DEFAULT FALSE,
    accessible BOOL NOT NULL DEFAULT TRUE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (chat_id)
);

-- Notifications indexes
CREATE INDEX cl_notif_15m_idx ON chats (cl_notif_15m);
CREATE INDEX cl_notif_1m_idx ON chats (cl_notif_1m);


CREATE TABLE users (
    user_id BIGINT NOT NULL,
    first_name VARCHAR(64) NOT NULL DEFAULT '',
    username VARCHAR(32) NOT NULL DEFAULT '',
    is_admin BOOL NOT NULL DEFAULT FALSE,
    referral VARCHAR(64) NOT NULL DEFAULT '',
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
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
