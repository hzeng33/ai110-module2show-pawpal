"""PawPal logic layer: core backend classes.
Owner manages Pets, each Pet holds Tasks, and the Scheduler retrieves and
organizes tasks across all of an owner's pets.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, time, timedelta


@dataclass
class Task:
    """A single care activity for a pet."""

    description: str
    time: time                  # when the task should happen
    duration: int = 30          # how long it takes, in minutes      
    priority: str = "medium"    # "low", "medium", or "high"    
    frequency: str = "daily"    # how often, e.g. "daily", "weekly", "once"
    completed: bool = False     # completion status
    due_date: date = field(default_factory=date.today)
    pet: "Pet | None" = field(default=None, repr=False, compare=False)

    def mark_complete(self) -> None:
        """Mark this task as done and, for recurring tasks, enqueue the next occurrence.

        Daily tasks spawn a copy of themselves with due_date advanced by one day.
        Weekly tasks advance by seven days. "Once" tasks are simply marked done.
        The new instance is appended to the same pet's task list via the pet
        backreference set by Pet.add_task, so no external caller has to know
        the task got rescheduled.

        Completing an already-completed task is a no-op: it never spawns a
        second future instance, so callers can safely re-invoke this.
        """
        if self.completed:
            return  # already done — don't reschedule a duplicate

        self.completed = True

        if self.frequency == "daily":
            step = timedelta(days=1)
        elif self.frequency == "weekly":
            step = timedelta(weeks=1)
        else:
            return  # "once" — nothing to reschedule

        if self.pet is None:
            return  # not attached to any pet yet, so no list to add to

        next_instance = replace(
            self,
            completed=False,
            due_date=self.due_date + step,
        )
        self.pet.add_task(next_instance)



@dataclass
class Pet:
    """Stores pet details and its list of tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        task.pet = self
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

    def sort_by_time(self) -> list[Task]:
        """Return all tasks ordered by due date, then scheduled time (earliest first).

        Sorting on ``due_date`` before ``time`` keeps tasks in true calendar
        order, so a task due tomorrow at 06:00 comes after one due today at
        18:00 rather than being reordered by clock time alone.
        """
        return sorted(
            self.owner.get_all_tasks(), key=lambda t: (t.due_date, t.time)
        )

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Return tasks matching the given filters.

        pet_name: only tasks belonging to the pet with this name.
        completed: True for done, False for pending, None for both.
        """
        results: list[Task] = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                results.append(task)
        return results

    def expand_recurring(
        self, start_date: date, horizon_days: int = 7
    ) -> list[tuple[date, Task]]:
        """Expand each task across a date range based on its frequency.

        daily  → every day in the window
        weekly → same weekday as start_date only
        once   → only on start_date

        Each emitted occurrence is an independent copy dated to its day, so
        mutating one day's task (e.g. marking it complete) never affects the
        others or the original stored task.
        """
        results: list[tuple[date, Task]] = []
        for offset in range(horizon_days):
            day = start_date + timedelta(days=offset)
            for task in self.owner.get_all_tasks():
                if task.frequency == "daily":
                    pass
                elif task.frequency == "weekly" and day.weekday() == start_date.weekday():
                    pass
                elif task.frequency == "once" and day == start_date:
                    pass
                else:
                    continue
                results.append((day, replace(task, due_date=day)))
        return results

    def find_conflicts(self) -> list[str]:
        """Return warning messages for tasks whose time windows overlap.

        Compares every pair of tasks in start-time order and checks whether
        one starts before the other ends. Duration is treated as minutes,
        so start times are converted to minutes-since-midnight for the check.

        Only tasks that fall on the same due_date are compared, so recurring
        tasks scheduled for different days never register as conflicts.

        Same-pet overlap  → hard conflict (one pet cannot do two things at once).
        Cross-pet overlap → soft conflict (the owner is double-booked).

        Always returns a list (possibly empty). Never raises, so callers can
        print, log, or ignore the warnings without wrapping in try/except.
        """
        tasks = self.sort_by_time()
        warnings: list[str] = []
        for i, a in enumerate(tasks):
            a_end = a.time.hour * 60 + a.time.minute + a.duration
            for b in tasks[i + 1:]:
                if b.due_date != a.due_date:
                    break  # sorted by (due_date, time): no later task shares a's day

                b_start = b.time.hour * 60 + b.time.minute
                if b_start >= a_end:
                    continue

                a_time = a.time.strftime("%H:%M")
                b_time = b.time.strftime("%H:%M")
                if a.pet is not None and a.pet is b.pet:
                    warnings.append(
                        f"WARNING: {a.pet.name} has overlapping tasks — "
                        f"{a.description} at {a_time} and {b.description} at {b_time}."
                    )
                else:
                    a_pet = a.pet.name if a.pet else "unknown"
                    b_pet = b.pet.name if b.pet else "unknown"
                    warnings.append(
                        f"WARNING: owner double-booked — {a_pet}'s {a.description} "
                        f"at {a_time} overlaps with {b_pet}'s {b.description} at {b_time}."
                    )
        return warnings


