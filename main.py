from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler
 
 
def print_schedule(scheduler: Scheduler) -> None:
    """Print an aligned 'Today's Schedule' ordered by time."""
    owner = scheduler.owner
 
    # Map each task back to its pet's name for display.
    pet_of = {
        id(task): pet.name
        for pet in owner.pets
        for task in pet.tasks
    }
 
    width = 46
    print("=" * width)
    print(f"Today's Schedule for {owner.name}".center(width))
    print("=" * width)
 
    for task in scheduler.organize_by_time():
        marker = "[x]" if task.completed else "[ ]"
        print(
            f"  {task.time.strftime('%H:%M')}  "
            f"{pet_of[id(task)]:<6} "
            f"{task.description:<22} {marker}"
        )
 
    print("=" * width)
 
 
if __name__ == "__main__":
    owner = Owner("Alex")
 
    rex = Pet("Rex", "dog")
    milo = Pet("Milo", "cat")
    owner.add_pet(rex)
    owner.add_pet(milo)
 
    milo.add_task(Task("Feed", time(7, 30)))
    rex.add_task(Task("Morning walk", time(8, 0)))
    milo.add_task(Task("Vet visit", time(14, 0), frequency="once"))
    rex.add_task(Task("Evening walk", time(18, 0)))
 
    scheduler = Scheduler(owner)
    print_schedule(scheduler)