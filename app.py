from nicegui import app, ui
import tasks

ui.colors(primary="#22c55e")

# Background image
app.add_static_files("/assets", "assets")

ui.add_css("""
body::before {
    content: "";
    position: fixed;
    inset: 0;
    background: url("/assets/background.jpeg") center / cover no-repeat;
    filter: blur(6px);
    transform: scale(1.05);
    z-index: -1;
}
body, .q-layout, .q-page, .nicegui-content {
    background: transparent !important;
}
""")

editing = {"id": None}

# Functions 
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


def edit(task_id, title, about):
    editing["id"] = task_id
    edit_title.value = title
    edit_about.value = about
    edit_dialog.open()


def save_edit():
    if not edit_title.value.strip():
        ui.notify("The task needs a title")
        return
    tasks.update_task(editing["id"], edit_title.value, edit_about.value)
    edit_dialog.close()
    task_list.refresh()


def add():
    if not title_input.value.strip():
        ui.notify("The task needs a title")
        return
    tasks.add_task(title_input.value, about_input.value)
    title_input.value = ""
    about_input.value = ""
    task_list.refresh()


@ui.refreshable
def task_list():
    rows = tasks.list_tasks()
    if not rows:
        ui.label("No tasks yet")
        return
    for task_id, title, about, is_done in rows:
        with ui.row().classes("items-center group"):
            ui.checkbox(
                value=bool(is_done),
                on_change=lambda e, t=task_id: toggle(t, e.value),
            )
            label = ui.label(f"{title} - {about}")
            if is_done:
                label.classes("line-through text-gray-500")
            ui.button(
                icon="edit",
                on_click=lambda t=task_id, ti=title, ab=about: edit(t, ti, ab),
            ).props("flat round").classes(
                "opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity"
            )
            ui.button(
                icon="delete",
                on_click=lambda t=task_id: remove(t),
            ).classes("opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity")


# Popups
with ui.dialog() as dialog, ui.card():
    ui.label("Delete ALL tasks?")
    with ui.row():
        ui.button("Cancel", on_click=dialog.close)
        ui.button("Delete all", on_click=clear_all, color="red")

with ui.dialog() as edit_dialog, ui.card().classes("w-96"):
    ui.label("Edit task").classes("text-xl font-bold")
    edit_title = ui.input("Task").classes("w-full")
    edit_about = ui.input("About").classes("w-full")
    with ui.row():
        ui.button("Cancel", on_click=edit_dialog.close)
        ui.button("Save", on_click=save_edit)

# Main 
with ui.card().classes("w-full max-w-xl mx-auto mt-8"):
    ui.label("Taskier").classes("text-2xl font-bold w-full text-center")
    dark = ui.dark_mode()
    ui.button(icon="dark_mode", on_click=dark.toggle).props("flat round")
    title_input = ui.input("Task").classes("w-full")
    about_input = ui.input("About").classes("w-full")
    with ui.row():
        ui.button("Add", on_click=add)
        ui.button("Clear all", on_click=dialog.open, color="red")
    task_list()

ui.run(title="Taskier")