SELECT
    chat_id,
    group_id,
    lang_code,
    cl_notif_next_part
FROM
    chats
WHERE
    cl_notif_15m AND
    accessible AND
    group_id != -1;
