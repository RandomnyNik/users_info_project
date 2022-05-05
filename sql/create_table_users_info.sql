CREATE TABLE IF NOT EXISTS "users_info" (
        "count_of_messages"     INTEGER,
        "count_of_questions"   INTEGER,
        "count_of_answers"      INTEGER,
        "user_id"               INTEGER,
        "level"                 TEXT,
        "id_question"           INTEGER,
        "id"            INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
)
