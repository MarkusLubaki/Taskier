import tasks

while True:
    choice = input("What do you want to do? (add/list/delete/done/clear/quit): ").strip().lower()

    if choice == "add":
        title = input("Enter the task: ")
        about = input("What is this about: ")
        tasks.add_task(title, about)
    elif choice == "list":
        for row in tasks.list_tasks():
            print(row)
    elif choice == "delete":
        task_id = input("Enter the id of the task to delete: ")
        if tasks.delete_task(task_id) == 0:
            print("No task with that id")
        else:
            print("Task deleted")
    elif choice == "done":
        task_id = input("Enter the id of the task to mark done: ")
        if tasks.mark_done(task_id) == 0:
            print("No task with that id")
        else:
            print("Task marked as done")
    elif choice == "clear":
        confirm = input("Delete ALL tasks? (y/n): ").strip().lower()
        if confirm == "y":
            tasks.clear_tasks()
            print("All tasks cleared")
        else:
            print("Cancelled")
    elif choice == "quit":
        tasks.conn.close()
        break
    else:
        print("Not an option")