import streamlit as st
from pawpal_system import Pet, Owner, Task, Scheduler
from datetime import time

# Common care tasks offered as quick picks; "Custom…" lets the user type their own.
COMMON_TASKS = [
    "Morning walk",
    "Evening walk",
    "Feed breakfast",
    "Feed dinner",
    "Fresh water",
    "Medication",
    "Brush / groom",
    "Litter box cleaning",
    "Playtime",
    "Training",
    "Bath",
    "Vet visit",
]

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A smart pet care planning assistant — plan the day, spot conflicts, care with confidence.")

with st.expander("What PawPal+ does", expanded=False):
    st.markdown(
        """
**PawPal+** helps a pet owner plan care tasks across all of their pets. It:
- Tracks care tasks (what, when, how long, and how important)
- Orders the day for you, earliest task first
- **Flags conflicts** — when one pet is booked twice, or when you're stretched
  across two pets at once
- Lets you filter down to a single pet or hide finished tasks
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
else:
    st.session_state.owner.name = owner_name

if st.button("Add pet"):
    st.session_state.owner.add_pet(Pet(pet_name, species))


st.markdown("### Tasks")

pet_names = [pet.name for pet in st.session_state.owner.pets]

if pet_names:
    selected_pet_name = st.selectbox("Which pet?", pet_names)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_choice = st.selectbox("Task", COMMON_TASKS + ["Custom…"])
        if task_choice == "Custom…":
            task_title = st.text_input("Custom task name", value="", placeholder="e.g. Nail trim")
        else:
            task_title = task_choice
    with col2:
        task_time = st.time_input("Time", value=time(8, 0))
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        if not task_title.strip():
            st.warning("Please enter a task name before adding.")
        else:
            target_pet = next(pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name)
            target_pet.add_task(
                Task(task_title.strip(), task_time, duration=int(duration), priority=priority)
            )
else:
    st.info("Add a pet first before adding tasks.")

if st.session_state.owner.pets:
    st.write("Current pets and tasks:")
    for pet in st.session_state.owner.pets:
        st.markdown(f"**{pet.name}** ({pet.species})")
        tasks = pet.get_tasks()
        if tasks:
            st.table(
                [
                    {
                        "description": t.description,
                        "time": t.time.strftime("%H:%M"),
                        "duration_minutes": t.duration,
                        "priority": t.priority,
                        "completed": t.completed,
                    }
                    for t in tasks
                ]
            )
        else:
            st.caption("No tasks yet for this pet.")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a time-ordered plan and let PawPal+ check it for conflicts.")

scheduler = Scheduler(st.session_state.owner)

# Let the owner narrow the plan before generating it.
filter_pets = ["All pets"] + [pet.name for pet in st.session_state.owner.pets]
fcol1, fcol2 = st.columns(2)
with fcol1:
    which_pet = st.selectbox("Show tasks for", filter_pets)
with fcol2:
    status_filter = st.selectbox("Status", ["All", "Pending", "Completed"])

# Remember that a plan was generated so it survives the reruns that
# checkbox clicks trigger — otherwise the plan would vanish on every toggle.
if st.button("Generate schedule"):
    st.session_state.schedule_built = True

if st.session_state.get("schedule_built"):
    pet_name = None if which_pet == "All pets" else which_pet
    completed = {"All": None, "Pending": False, "Completed": True}[status_filter]

    # Filter first, then order the surviving tasks by time.
    matching = scheduler.filter_tasks(pet_name=pet_name, completed=completed)
    ordered_tasks = sorted(matching, key=lambda t: (t.due_date, t.time))

    if not ordered_tasks:
        st.info("No tasks match these filters. Add tasks above or widen the filters.")
    else:
        # --- Conflict check: surface the scheduler's smartest feature -----------
        conflicts = scheduler.find_conflicts()
        if not conflicts:
            st.success("✅ No scheduling conflicts — this plan is clear to go.")
        else:
            st.markdown("#### ⚠️ Conflicts detected")
            for msg in conflicts:
                # Strip the backend's "WARNING: " prefix for cleaner UI copy.
                text = msg.replace("WARNING: ", "")
                if "overlapping tasks" in msg:
                    # Same pet, same time — physically impossible. Hard stop.
                    st.error(f"🔴 **Impossible for one pet:** {text}")
                else:
                    # Owner double-booked across pets — doable, but tight.
                    st.warning(f"🟡 **You're double-booked:** {text}")

        # --- The ordered plan (with interactive "done" toggles) ----------------
        st.markdown("#### 📋 Your plan")
        widths = [1.2, 1.5, 3, 1.3, 1.2, 0.9]
        header = st.columns(widths)
        for col, label in zip(header, ["Time", "Pet", "Task", "Duration", "Priority", "Done"]):
            col.markdown(f"**{label}**")

        for t in ordered_tasks:
            row = st.columns(widths)
            row[0].write(t.time.strftime("%H:%M"))
            row[1].write(t.pet.name if t.pet else "—")
            row[2].write(t.description)
            row[3].write(f"{t.duration} min")
            row[4].write(t.priority)
            # Checkbox is the source of truth; writing back updates the Pet's
            # actual Task object, which lives in session_state and persists.
            is_done = row[5].checkbox(
                "done",
                value=t.completed,
                key=f"done_{id(t)}",
                label_visibility="collapsed",
            )
            if is_done != t.completed:
                t.completed = is_done
                st.rerun()

        st.caption(f"{len(ordered_tasks)} task(s), ordered earliest first.")
