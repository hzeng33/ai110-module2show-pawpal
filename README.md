# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

### A sample of the app's CLI:

Running `python main.py` produces the following schedule in the terminal:

```
Today's Schedule for Alex

Daily plan for Rex (dog):
  08:00 — Morning walk (30 min) [priority: high]
  18:00 — Evening walk (30 min) [priority: medium]

Daily plan for Milo (cat):
  07:30 — Feed (10 min) [priority: high]
  14:00 — Vet visit (60 min) [priority: high]

```

## 🧪 Testing PawPal+

Run the full test suite from the project root:

```bash
python -m pytest
```

The tests live in `tests/test_pawpal.py` and cover the core scheduling behaviors:

- **Task completion** — `mark_complete()` flips a task's `completed` status, and re-completing an already-done task is a no-op (no duplicate reschedule).
- **Sorting correctness** — `sort_by_time()` orders tasks by due date then time (so tomorrow at 06:00 sorts after today at 18:00), is stable for identical times, and returns an empty list when there are no tasks.
- **Recurrence logic** — completing a `daily` task spawns a new instance due the next day, `weekly` advances by seven days, and `once` never reschedules; `expand_recurring()` emits independent per-day copies that don't alias each other.
- **Conflict detection** — `find_conflicts()` flags overlapping time windows, ignores back-to-back tasks and tasks on different days, and distinguishes same-pet clashes from cross-pet owner double-bookings.
- **Filtering behavior** — `filter_tasks()` filters by pet name, by completion status (including the `completed=False` case), and returns an empty list for an unknown pet.

Terminal output of a successful test run:

```
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\ai110-module2show-pawpal
collected 18 items

tests\test_pawpal.py ..................                                  [100%]

============================= 18 passed in 0.02s ==============================
```

## 📐 Smarter Scheduling

PawPal+ adds four algorithmic layers on top of the basic Owner/Pet/Task model. Each one is implemented as a method on the `Scheduler` class in `pawpal_system.py`, plus one small extension to `Task.mark_complete` that auto-reschedules recurring tasks.

| Feature                    | Method(s)                                                                       | Notes                                                                                                                                                                                                          |
| -------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sorting by time            | `Scheduler.sort_by_time()`                                                      | Sorts every task across all pets in chronological order using a lambda key on `task.time`.                                                                                                                     |
| Filtering by pet or status | `Scheduler.filter_tasks(pet_name=None, completed=None)`                         | Filters by pet name, completion status, or both. No arguments returns everything.                                                                                                                              |
| Conflict detection         | `Scheduler.find_conflicts()`                                                    | Detects overlapping time windows and distinguishes same-pet clashes from owner double-bookings. Returns warning strings; never raises.                                                                         |
| Recurring tasks            | `Scheduler.expand_recurring(start_date, horizon_days)` + `Task.mark_complete()` | `expand_recurring` emits `(date, task)` pairs across a date window based on frequency (`daily`, `weekly`, `once`). `mark_complete` auto-adds the next instance via `timedelta` when a recurring task finishes. |

Run `python main.py` to see all four features exercised against a demo owner with two pets.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
