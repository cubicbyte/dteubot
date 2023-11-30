INSERT INTO users (
    id,
    first_name,
    last_name,
    username,
    is_admin,
    referral
) VALUES (
    :id,
    :first_name,
    :last_name,
    :username,
    :is_admin,
    :referral
) ON CONFLICT (id) DO UPDATE SET
    first_name = :first_name,
    last_name = :last_name,
    username = :username,
    is_admin = :is_admin,
    referral = :referral;
