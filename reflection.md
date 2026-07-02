# PawPal+ Project Reflection

## 1. System Design

- The user is able to add user and the pet's information.
- The user is able to add and edit the task, which include duration and priority.
- The user is able to generate daily schedule based on the constraints and priorities.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design has four main classes: Owner, Pet, Task, and Scheduler. I also added two small helper classes, Placement and Schedule, to hold the scheduler output.

- Owner: stores the user's information and their free time budget for the day. It holds a list of pets and manages adding and editing them.
- Pet: stores one animal's information and holds a list of tasks. It manages adding, editing, and getting those tasks.
- Task: stores one care activity, including its duration and priority. It can update its own fields.
- Scheduler: it is the engine. It reads the owner's tasks and available time, then sorts the tasks by priority and packs them into the free window back to back.
- Placement: wraps one task with a start time and end time.
- Schedule: holds the result, split into scheduled tasks and inapplicable tasks that did not fit the available time.

The main idea is that Owner holds Pets, each Pet holds Tasks, and the Scheduler reasons about the tasks across time so the other classes stay simple.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler mainly reasons about three things: when a task happens, how long it takes, and how often it repeats. Time is the primary constraint because a daily plan only makes sense in order, and everything else is built on that chronological view. Duration matters second because it lets `find_conflicts` see whether two tasks actually overlap instead of only catching clashes at the exact same minute. Frequency drives `expand_recurring` so one stored task can populate a whole week without being copied. Priority is stored on each task but the algorithms do not sort or drop tasks based on it, because a pet owner already knows which tasks matter and I did not want the app to quietly reorder their day for them.

**b. Tradeoffs**

One tradeoff my scheduler makes is how it handles recurring tasks. Instead of storing a separate Task object for every date a pet needs walking or feeding, the scheduler only stores one Task per activity. The view that spans several days is built on the fly by the `expand_recurring` method, which walks through a date window and emits the same task once for each day it applies to.

The upside is that the data stays small and easy to change. A pet owner with ten daily habits does not end up with hundreds of records after a week, and editing the description or duration of a task updates every future occurrence in one place. That also matches how a pet owner actually thinks about their routine. They do not plan each Monday's morning walk as a fresh event. It is just "the morning walk."

The downside is that the scheduler cannot mark one specific future day as done without producing a new task. My `mark_complete` method works around this by spawning a copy with a bumped due date whenever a daily or weekly task is finished, but that means the same activity can show up in `expand_recurring` twice on the same day if both paths are used together. I decided this is fine for a single owner planning a week at a time. If this were a shared household calendar tracking dozens of animals across months of history, I would probably store dated instances directly and drop the expansion method.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
