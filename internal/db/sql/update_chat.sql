UPDATE chats SET
    group_id = :group_id,
    lang_code = :lang_code,
    cl_notif_15m = :cl_notif_15m,
    cl_notif_1m = :cl_notif_1m,
    seen_settings = :seen_settings,
    accessible = :accessible
WHERE chat_id = :chat_id;