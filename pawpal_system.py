"""PawPal logic layer: core backend classes.

Owner manages Pets, each Pet holds Tasks, and the Scheduler retrieves and
organizes tasks across all of an owner's pets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time


@dataclass
class Task:
    """A single care activity for a pet."""

    description: str
    time: time                  # when the task should happen
    duration: int = 30          # how long it takes, in minutes      
    priority: str = "medium"    # "low", "medium", or "high"    
    frequency: str = "daily"    # how often, e.g. "daily", "weekly", "once"
    completed: bool = False     # completion status

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    """Stores pet details and its list of tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return list(self.tasks)


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Flatten and return tasks across all pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The brain: retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> list[Task]:
        """Retrieve every task from the owner's pets."""
        return self.owner.get_all_tasks()

    def organize_by_time(self) -> list[Task]:
        """Return all tasks ordered by their scheduled time."""
        return sorted(self.owner.get_all_tasks(), key=lambda t: t.time)

    def pending_tasks(self) -> list[Task]:
        """Return tasks that are not completed yet."""
        return [t for t in self.owner.get_all_tasks() if not t.completed]