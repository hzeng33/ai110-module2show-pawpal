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

I used AI across the whole project, but in different ways for each phase. Early on it helped me brainstorm the class design and turn my UML into clean Python stubs, and later I leaned on it more for wiring the scheduler logic into the Streamlit UI and refactoring the README. The prompts that worked best were specific and file-based, like "here is my final `pawpal_system.py`, update the UML to match" or "Please help fix the issues you flagged earilier in `pawpal_system.py`."

**b. Judgment and verification**

One moment I did not accept a suggestion as-is was the conflict warnings. The assistant first put every conflict into one plain warning box, but I had it split them by severity so a same-pet clash shows as a red error and an owner double-booking shows as a yellow warning, because those mean different things to a pet owner. To verify what the AI wrote, I ran `main.py` and the test suite instead of trusting the code by reading it, which caught cases like conflicts still being computed on the full schedule even when the view was filtered.

**c. AI Strategy**

- **Which AI features were most effective for building your scheduler?**

The most effective feature was letting the assistant read my actual files before it suggested anything, so its edits matched my real class names and methods instead of a generic template. Inline edits directly in `app.py` and `pawpal_system.py` were faster than copying snippets back and forth, and having it run `main.py` to capture real output kept my README honest.

- **Give one example of an AI suggestion you rejected or modified.**

My initial UML had two extra helper classes, `Placement` and `Schedule`, to hold scheduler output, and AI was willing to build them out. I dropped them and kept the scheduler returning plain lists of tasks, because the helper classes added structure I never actually needed and made the design harder to follow.

- **How did separate chat sessions per phase help you stay organized?**

Using a fresh session for each phase kept each conversation focused on one goal, so the design chat did not get tangled up with debugging or documentation. It also made it easy to go back and find where a decision was made, since each phase had its own clean history.

- **What did you learn about being the "lead architect"?**

I learned that the AI is very fast at producing code but it does not own the design, so it will happily build whatever I ask for even if it makes the system messier. My job was to hold the vision, reject suggestions that did not fit, and verify the output by running it rather than assuming it was correct. The best results came when I made the decisions and used AI to execute them quickly, not when I let it decide the structure for me.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
  If among levels from 1-5, I would give a 4.
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with how the AI helped me brainstorm the UML design and implement the sorting and filtering logic for the app.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I am happy with how the project turned out, so I would keep it mostly as the current version.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

For designing systems, I learned that it is important to understand the relationships between the objects. For working with AI, I learned that I should run every piece of code the AI generates to verify it, and then give follow-up prompts to ask for corrections when something is wrong.
