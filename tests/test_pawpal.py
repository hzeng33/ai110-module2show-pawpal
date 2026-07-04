from datetime import date, time
from pawpal_system import Owner, Pet, Scheduler, Task


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


# --- Sorting correctness -------------------------------------------------


def test_sort_by_time_returns_chronological_order():
    """Scheduler.sort_by_time() returns tasks earliest-first regardless of
    the order they were added."""
    pet = Pet("Rex", "dog")
    pet.add_task(Task("Dinner", time(18, 0)))
    pet.add_task(Task("Breakfast", time(7, 0)))
    pet.add_task(Task("Lunch", time(12, 0)))
    owner = Owner("Sam", [pet])
    scheduler = Scheduler(owner)

    ordered = scheduler.sort_by_time()

    assert [t.time for t in ordered] == [time(7, 0), time(12, 0), time(18, 0)]


def test_sort_by_time_empty_when_no_tasks():
    """Sorting an owner with no tasks yields an empty list, not an error."""
    owner = Owner("Sam", [Pet("Rex", "dog")])
    scheduler = Scheduler(owner)

    assert scheduler.sort_by_time() == []


def test_sort_by_time_is_stable_for_equal_times():
    """Two tasks at the exact same time keep their insertion order."""
    pet = Pet("Rex", "dog")
    first = Task("Pill", time(8, 0))
    second = Task("Feed", time(8, 0))
    pet.add_task(first)
    pet.add_task(second)
    scheduler = Scheduler(Owner("Sam", [pet]))

    ordered = scheduler.sort_by_time()

    assert ordered[0] is first
    assert ordered[1] is second


# --- Recurrence logic ----------------------------------------------------


def test_mark_complete_daily_spawns_next_day():
    """Completing a daily task adds a fresh instance due the following day."""
    pet = Pet("Rex", "dog")
    task = Task("Walk", time(9, 0), frequency="daily", due_date=date(2026, 7, 4))
    pet.add_task(task)

    task.mark_complete()

    assert len(pet.get_tasks()) == 2
    new_task = pet.get_tasks()[1]
    assert new_task.completed is False
    assert new_task.due_date == date(2026, 7, 5)
    assert new_task.description == "Walk"


def test_mark_complete_weekly_spawns_seven_days_later():
    """Completing a weekly task advances the next instance by a week."""
    pet = Pet("Rex", "dog")
    task = Task("Bath", time(10, 0), frequency="weekly", due_date=date(2026, 7, 4))
    pet.add_task(task)

    task.mark_complete()

    assert pet.get_tasks()[1].due_date == date(2026, 7, 11)


def test_mark_complete_once_does_not_spawn():
    """A one-off task is marked done but never reschedules itself."""
    pet = Pet("Rex", "dog")
    task = Task("Vet visit", time(14, 0), frequency="once")
    pet.add_task(task)

    task.mark_complete()

    assert len(pet.get_tasks()) == 1
    assert task.completed is True


# --- Conflict detection --------------------------------------------------


def test_find_conflicts_flags_overlapping_times():
    """Two tasks whose windows overlap produce a warning."""
    pet = Pet("Rex", "dog")
    pet.add_task(Task("Walk", time(9, 0), duration=30))
    pet.add_task(Task("Feed", time(9, 15), duration=30))
    scheduler = Scheduler(Owner("Sam", [pet]))

    warnings = scheduler.find_conflicts()

    assert len(warnings) == 1
    assert "overlapping" in warnings[0]


def test_find_conflicts_ignores_adjacent_tasks():
    """A task ending exactly when the next begins is not a conflict."""
    pet = Pet("Rex", "dog")
    pet.add_task(Task("Walk", time(9, 0), duration=30))
    pet.add_task(Task("Feed", time(9, 30), duration=30))
    scheduler = Scheduler(Owner("Sam", [pet]))

    assert scheduler.find_conflicts() == []


def test_find_conflicts_cross_pet_is_double_booking():
    """Overlapping tasks on different pets warn about owner double-booking."""
    rex = Pet("Rex", "dog")
    milo = Pet("Milo", "cat")
    rex.add_task(Task("Walk", time(9, 0), duration=30))
    milo.add_task(Task("Groom", time(9, 15), duration=30))
    scheduler = Scheduler(Owner("Sam", [rex, milo]))

    warnings = scheduler.find_conflicts()

    assert len(warnings) == 1
    assert "double-booked" in warnings[0]


# --- Filtering behavior --------------------------------------------------


def test_filter_by_pet_name():
    """Filtering by pet name returns only that pet's tasks."""
    rex = Pet("Rex", "dog")
    milo = Pet("Milo", "cat")
    rex.add_task(Task("Walk", time(9, 0)))
    milo.add_task(Task("Groom", time(10, 0)))
    scheduler = Scheduler(Owner("Sam", [rex, milo]))

    results = scheduler.filter_tasks(pet_name="Rex")

    assert [t.description for t in results] == ["Walk"]


def test_filter_by_completed_false_returns_pending():
    """completed=False returns pending tasks (guards falsy-value handling)."""
    pet = Pet("Rex", "dog")
    done = Task("Walk", time(9, 0), completed=True)
    pending = Task("Feed", time(10, 0), completed=False)
    pet.add_task(done)
    pet.add_task(pending)
    scheduler = Scheduler(Owner("Sam", [pet]))

    results = scheduler.filter_tasks(completed=False)

    assert results == [pending]


def test_filter_unknown_pet_returns_empty():
    """Filtering by a pet that doesn't exist yields an empty list."""
    pet = Pet("Rex", "dog")
    pet.add_task(Task("Walk", time(9, 0)))
    scheduler = Scheduler(Owner("Sam", [pet]))

    assert scheduler.filter_tasks(pet_name="Ghost") == []


# --- Regression tests for date-aware / idempotent behavior ---------------


def test_sort_by_time_orders_by_date_then_time():
    """A task due tomorrow at 06:00 sorts after one due today at 18:00."""
    pet = Pet("Rex", "dog")
    tomorrow_early = Task("Pill", time(6, 0), due_date=date(2026, 7, 5))
    today_late = Task("Walk", time(18, 0), due_date=date(2026, 7, 4))
    pet.add_task(tomorrow_early)
    pet.add_task(today_late)
    scheduler = Scheduler(Owner("Sam", [pet]))

    ordered = scheduler.sort_by_time()

    assert ordered == [today_late, tomorrow_early]


def test_mark_complete_twice_does_not_duplicate():
    """Re-completing a daily task is a no-op — it spawns only one next instance."""
    pet = Pet("Rex", "dog")
    task = Task("Walk", time(9, 0), frequency="daily", due_date=date(2026, 7, 4))
    pet.add_task(task)

    task.mark_complete()
    task.mark_complete()

    assert len(pet.get_tasks()) == 2  # original + exactly one next instance


def test_expand_recurring_occurrences_are_independent():
    """Mutating one expanded occurrence must not affect the others."""
    pet = Pet("Rex", "dog")
    pet.add_task(Task("Walk", time(9, 0), frequency="daily"))
    scheduler = Scheduler(Owner("Sam", [pet]))

    expansion = scheduler.expand_recurring(date(2026, 7, 4), horizon_days=3)
    first_task = expansion[0][1]
    first_task.completed = True

    assert [t.completed for _, t in expansion[1:]] == [False, False]


def test_find_conflicts_ignores_different_days():
    """Overlapping clock times on different due dates are not conflicts."""
    pet = Pet("Rex", "dog")
    pet.add_task(Task("Walk", time(9, 0), duration=30, due_date=date(2026, 7, 4)))
    pet.add_task(Task("Feed", time(9, 15), duration=30, due_date=date(2026, 7, 5)))
    scheduler = Scheduler(Owner("Sam", [pet]))

    assert scheduler.find_conflicts() == []