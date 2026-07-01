from datetime import time
from pawpal_system import Pet, Task
 
 
def test_mark_complete_changes_status():
    """Calling mark_complete() flips a task from not done to done."""
    task = Task("Feed", time(8, 0))
    assert task.completed is False
 
    task.mark_complete()
 
    assert task.completed is True
 
 
def test_add_task_increases_count():
    """Adding a task to a pet raises that pet's task count by one."""
    pet = Pet("Rex", "dog")
    assert len(pet.get_tasks()) == 0
 
    pet.add_task(Task("Walk", time(9, 0)))
 
    assert len(pet.get_tasks()) == 1