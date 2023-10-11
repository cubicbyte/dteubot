SELECT *
FROM
    group_schedule
WHERE
    group_id = ? AND
    date BETWEEN ? AND ?;
