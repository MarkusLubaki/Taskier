from nicegui import ui
import tasks


def toggle(task_id, done):
    tasks.set_done(task_id, done)
    task_list.refresh()


def remove(task_id):
    tasks.delete_task(task_id)
    task_list.refresh()


def clear_all():
    tasks.clear_tasks()
    dialog.close()
    task_list.refresh()


@ui.refreshable
def task_list():
    rows = tasks.list_tasks()
    if not rows:
        ui.label("No tasks yet")
        return
    for task_id, title, about, is_done in rows:
        with ui.row().classes("items-center"):
            ui.checkbox(
                value=bool(is_done),
                on_change=lambda e, t=task_id: toggle(t, e.value),
            )
            label = ui.label(f"{title} - {about}")
            if is_done:
                label.classes("line-through text-gray-500")
            ui.button(icon="delete", on_click=lambda t=task_id: remove(t))


def add():
    if not title_input.value.strip():
        ui.notify("The task needs a title")
        return
    tasks.add_task(title_input.value, about_input.value)
    title_input.value = ""
    about_input.value = ""
    task_list.refresh()


with ui.dialog() as dialog, ui.card():
    ui.label("Delete ALL tasks?")
    with ui.row():
        ui.button("Cancel", on_click=dialog.close)
        ui.button("Delete all", on_click=clear_all, color="red")

with ui.card().classes("w-full max-w-xl mx-auto mt-8"):
    ui.label("Taskier").classes("text-2xl font-bold w-full text-center")
    title_input = ui.input("Task").classes("w-full")
    about_input = ui.input("About").classes("w-full")
    with ui.row():
        ui.button("Add", on_click=add)
        ui.button("Clear all", on_click=dialog.open, color="red")
    task_list()

ui.run(title="Taskier")