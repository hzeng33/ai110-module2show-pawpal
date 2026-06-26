"""PawPal logic layer: backend class skeletons.

Generated from the UML. Data holders use dataclasses; Scheduler is the
engine. Method bodies are left as stubs to be filled in.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    task_id: int
    pet_id: int
    name: str
    duration: int                       # minutes the task takes
    priority: Priority = Priority.MEDIUM

    def edit(self, **fields) -> None:
        """Update duration, priority, or name in place."""


@dataclass
class Pet:
    pet_id: int
    name: str
    species: str
    owner_id: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""

    def edit_task(self, task_id: int, **fields) -> None:
        """Find a task by id and update its fields."""

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""


@dataclass
class Owner:
    owner_id: int
    name: str
    available_minutes: int              # free time budget for the day
    window_start: time                  # when the free window begins
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Attach a pet to this owner."""

    def edit_pet(self, pet_id: int, **fields) -> None:
        """Find a pet by id and update its fields."""

    def list_pets(self) -> list[Pet]:
        """Return this owner's pets."""

    def all_tasks(self) -> list[Task]:
        """Flatten and return tasks across all pets."""


@dataclass
class Placement:
    task: Task
    start_time: time
    end_time: time


@dataclass
class Schedule:
    scheduled: list[Placement] = field(default_factory=list)
    inapplicable: list[Task] = field(default_factory=list)


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_schedule(self) -> Schedule:
        """Pack the owner's tasks into the free window by priority.

        Returns a Schedule split into scheduled placements and
        inapplicable tasks that did not fit the available budget.
        """

    def format_schedule(self) -> str:
        """Render the generated schedule for display."""