import sqlite3
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, about TEXT ,is_done INTEGER DEFAULT 0)")

# Tasks Functions
def add_task():
    title = input("Enter the task: ")
    about = input("What is this about: ")
    cursor.execute("INSERT INTO tasks (title, about) VALUES (?, ?)", (title, about))

def list_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    print(tasks)

def delete_task():
    task_id = input("Enter the id of the task to delete: ")
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id))

def mark_done():
    task_id = input("Enter the id of the task to mark done: ")
    cursor.execute("UPDATE tasks SET is_done = 1 WHERE id = ?", (task_id))

def clear_tasks():
    cursor.execute("DELETE FROM tasks")


# Loop for the "menu"
while True:
    choice = input("What do you want to do? (add/list/delete/done/clear/quit): ")
    print("You chose:", choice)

    if choice == "add":
        add_task()
    elif choice == "list":
        list_tasks()
    elif choice == "delete":
        delete_task()
    elif choice == "done":
        mark_done()
    elif choice == "clear":
        clear_tasks()
    elif choice == "quit":
        break
    else:
        print("Not an option")

conn.commit()
conn.close()