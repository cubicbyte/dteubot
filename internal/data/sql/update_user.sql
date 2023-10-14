UPDATE users SET
    first_name = :first_name,
    last_name = :last_name,
    username = :username,
    lang_code = :lang_code,
    is_admin = :is_admin,
    referral = :referral
WHERE user_id = :user_id;