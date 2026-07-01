from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler
 
 
def print_schedule(owner: Owner) -> None:
    """Print a per-pet daily plan with tasks ordered by time."""
    print(f"Today's Schedule for {owner.name}\n")
 
    for pet in owner.pets:
        print(f"Daily plan for {pet.name} ({pet.species}):")
        for task in sorted(pet.get_tasks(), key=lambda t: t.time):
            line = (
                f"  {task.time.strftime('%H:%M')} \u2014 "
                f"{task.description} ({task.duration} min) "
                f"[priority: {task.priority}]"
            )
            if task.completed:
                line += " (done)"
            print(line)
        print()
 
 
if __name__ == "__main__":
    owner = Owner("Alex")
 
    rex = Pet("Rex", "dog")
    milo = Pet("Milo", "cat")
    owner.add_pet(rex)
    owner.add_pet(milo)
 
    rex.add_task(Task("Morning walk", time(8, 0), duration=30, priority="high"))
    rex.add_task(Task("Evening walk", time(18, 0), duration=30, priority="medium"))
    milo.add_task(Task("Feed", time(7, 30), duration=10, priority="high"))
    milo.add_task(
        Task("Vet visit", time(14, 0), duration=60, priority="high", frequency="once")
    )
 
    print_schedule(owner)