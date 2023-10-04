UPDATE users SET
    first_name = :first_name,
    username = :username,
    is_admin = :is_admin
WHERE user_id = :user_id;