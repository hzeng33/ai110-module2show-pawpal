from datetime import date, time
from pawpal_system import Owner, Pet, Task, Scheduler


def format_task(task: Task) -> str:
    line = (
        f"  {task.time.strftime('%H:%M')} — "
        f"{task.description} ({task.duration} min) "
        f"[priority: {task.priority}]"
    )
    if task.completed:
        line += " (done)"
    return line


def print_tasks(title: str, tasks: list[Task]) -> None:
    print(title)
    if not tasks:
        print("  (none)")
    for task in tasks:
        print(format_task(task))
    print()


if __name__ == "__main__":
    owner = Owner("Alex")

    rex = Pet("Rex", "dog")
    milo = Pet("Milo", "cat")
    owner.add_pet(rex)
    owner.add_pet(milo)

    # Deliberately added out of chronological order — sort_by_time should reorder them.
    rex.add_task(Task("Evening walk", time(18, 0), duration=30, priority="medium"))
    milo.add_task(
        Task("Vet visit", time(14, 0), duration=60, priority="high", frequency="once")
    )
    rex.add_task(Task("Morning walk", time(8, 0), duration=30, priority="high"))
    milo.add_task(Task("Feed", time(7, 30), duration=10, priority="high"))
    rex.add_task(Task("Midday brush", time(12, 30), duration=15, priority="low"))
    # Overlaps with Milo's 14:00 vet visit — should show up as a conflict.
    rex.add_task(Task("Grooming", time(14, 30), duration=45, priority="medium"))
    # Same-pet conflict: overlaps with Rex's 08:00 Morning walk.
    rex.add_task(Task("Fetch training", time(8, 15), duration=20,priority="medium"))


    # Complete one task so the completion filter has something to show.
    milo.tasks[0].mark_complete()

    scheduler = Scheduler(owner)

    print_tasks(
        f"All tasks for {owner.name}, sorted by time:",
        scheduler.sort_by_time(),
    )
    print_tasks("Only Rex's tasks:", scheduler.filter_tasks(pet_name="Rex"))
    print_tasks("Pending tasks only:", scheduler.filter_tasks(completed=False))

    print("3-day plan starting today:")
    today = date.today()
    for day, task in scheduler.expand_recurring(today, horizon_days=3):
        print(f"  {day} {task.time.strftime('%H:%M')} — {task.description} ({task.frequency})")

    print("\nScheduling conflicts:")
    warnings = scheduler.find_conflicts()
    if not warnings:
        print("  (none)")
    for warning in warnings:
        print(f"  {warning}")


    # Complete Rex's Morning walk — a new instance should auto-appear for tomorrow.
    for t in rex.tasks:
        if t.description == "Morning walk":
            t.mark_complete()
            break

    print("\nRex's tasks after completing Morning walk (new instance should appear for tomorrow):")
    for t in rex.tasks:
        status = "done" if t.completed else "pending"
        print(f"  {t.due_date} {t.time.strftime('%H:%M')} — {t.description} [{status}]")
