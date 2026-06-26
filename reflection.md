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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
