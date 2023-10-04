CREATE TABLE chats (
                                chat_id BIGINT,
                                group_id INT DEFAULT NULL,
                                lang_code VARCHAR(10) DEFAULT NULL,
                                cl_notif_15m BOOL NOT NULL DEFAULT FALSE,
                                cl_notif_1m BOOL NOT NULL DEFAULT FALSE,
                                seen_settings BOOL NOT NULL DEFAULT FALSE,
                                accessible BOOL NOT NULL DEFAULT TRUE,
                                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                PRIMARY KEY (chat_id)
);

CREATE TABLE users (
                       user_id BIGINT,
                       first_name VARCHAR(64) NOT NULL,
                       username VARCHAR(32) DEFAULT NULL,
                       is_admin BOOL NOT NULL DEFAULT FALSE,
                       referrer VARCHAR(64) DEFAULT NULL,
                       created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                       updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                       PRIMARY KEY (user_id)
);
