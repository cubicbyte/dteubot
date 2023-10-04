INSERT INTO users (user_id)
VALUES ($1)
RETURNING *;