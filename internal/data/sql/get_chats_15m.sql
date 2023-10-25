SELECT
    *
FROM
    chats
WHERE
    cl_notif_15m AND
    accessible AND
    group_id != -1;
