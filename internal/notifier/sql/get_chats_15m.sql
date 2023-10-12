SELECT
    chat_id,
    group_id,
    lang_code
FROM
    chats
WHERE
    cl_notif_15m AND
    accessible AND
    group_id != -1;
