import streamlit as st
from pawpal_system import Pet, Owner, Task, Scheduler
from datetime import time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
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
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

pet_names = [pet.name for pet in st.session_state.owner.pets]

if pet_names:
    selected_pet_name = st.selectbox("Which pet?", pet_names)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_time = st.time_input("Time", value=time(8, 0))
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        target_pet = next(pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name)
        target_pet.add_task(
            Task(task_title, task_time, duration=int(duration), priority=priority)
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
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    ordered_tasks = scheduler.organize_by_time()

    if ordered_tasks:
        st.table(
            [
                {
                    "time": t.time.strftime("%H:%M"),
                    "description": t.description,
                    "duration_minutes": t.duration,
                    "priority": t.priority,
                    "completed": t.completed,
                }
                for t in ordered_tasks
            ]
        )
    else:
        st.info("No tasks to schedule yet. Add a pet and some tasks above.")
