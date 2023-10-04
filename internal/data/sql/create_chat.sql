INSERT INTO chats (chat_id, lang_code)
VALUES ($1, $2)
RETURNING *;