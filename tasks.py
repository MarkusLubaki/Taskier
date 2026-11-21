import sqlite3

# Create the DB
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS tasks ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "title TEXT, about TEXT, is_done INTEGER DEFAULT 0)"
)
conn.commit()


def add_task(title, about):
    cursor.execute("INSERT INTO tasks (title, about) VALUES (?, ?)", (title, about))
    conn.commit()


def list_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()


def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return cursor.rowcount  


def mark_done(task_id):
    cursor.execute("UPDATE tasks SET is_done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    return cursor.rowcount


def clear_tasks():
    cursor.execute("DELETE FROM tasks")
    conn.commit()


def set_done(task_id, done):
    cursor.execute("UPDATE tasks SET is_done = ? WHERE id = ?", (1 if done else 0, task_id))
    conn.commit()
    return cursor.rowcount


def update_task(task_id, title, about):
    cursor.execute(
        "UPDATE tasks SET title = ?, about = ? WHERE id = ?",
        (title, about, task_id),
    )
    conn.commit()
    return cursor.rowcount