INSERT INTO chats (
    chat_id,
    group_id,
    lang_code,
    cl_notif_15m,
    cl_notif_1m,
    cl_notif_next_part,
    seen_settings,
    accessible
) VALUES (
    :chat_id,
    :group_id,
    :lang_code,
    :cl_notif_15m,
    :cl_notif_1m,
    :cl_notif_next_part,
    :seen_settings,
    :accessible
) ON CONFLICT (chat_id) DO UPDATE SET
    group_id = :group_id,
    lang_code = :lang_code,
    cl_notif_15m = :cl_notif_15m,
    cl_notif_1m = :cl_notif_1m,
    cl_notif_next_part = :cl_notif_next_part,
    seen_settings = :seen_settings,
    accessible = :accessible;
