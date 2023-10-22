INSERT INTO users (
    user_id,
    first_name,
    last_name,
    username,
    lang_code,
    is_premium,
    is_admin,
    referral
) VALUES (
    :user_id,
    :first_name,
    :last_name,
    :username,
    :lang_code,
    :is_premium,
    :is_admin,
    :referral
) ON CONFLICT (user_id) DO UPDATE SET
    first_name = :first_name,
    last_name = :last_name,
    username = :username,
    lang_code = :lang_code,
    is_premium = :is_premium,
    is_admin = :is_admin,
    referral = :referral;
