import os
from datetime import date, datetime, time, timedelta
import pytz
import streamlit as st

from core.db import init_storage, get_session
from core.models import Task
from core.planner import plan_day
from ui.components import inject_styles


st.set_page_config(page_title="Personal AI Planner", page_icon="🗓️", layout="wide")
inject_styles()

init_storage()

st.title("🗓️ Personal AI Planner")
st.caption("Automate your tasks and daily schedule with an elegant UI.")

colA, colB, colC = st.columns([2, 1, 1])
with colA:
	work_date = st.date_input("Plan for date", value=date.today())
with colB:
	start_hour = st.slider("Work start hour", min_value=5, max_value=12, value=9)
with colC:
	end_hour = st.slider("Work end hour", min_value=12, max_value=23, value=17)

with st.expander("Quick add task", expanded=True):
	with st.form("quick_add_form", clear_on_submit=True):
		title = st.text_input("Title", placeholder="e.g., Draft project proposal")
		description = st.text_area("Details", height=80)
		priority = st.selectbox("Priority", ["high", "medium", "low"], index=1)
		duration = st.number_input("Duration (minutes)", min_value=15, max_value=480, value=60, step=15)
		due = st.date_input("Due date", value=work_date)
		tags = st.text_input("Tags (comma-separated)", placeholder="work, writing")
		submitted = st.form_submit_button("➕ Add Task")
		if submitted and title.strip():
			with get_session() as session:
				task = Task(
					title=title.strip(),
					description=description.strip(),
					priority=priority,
					duration_minutes=int(duration),
					due_at=datetime.combine(due, time(23, 59, 0)),
					tags=tags.strip(),
				)
				session.add(task)
				session.commit()
				st.success("Task added.")

col1, col2 = st.columns([1, 1])
with col1:
	if st.button("🧠 Plan My Day", use_container_width=True):
		with get_session() as session:
			assignments = plan_day(
				session=session,
				plan_date=work_date,
				work_start=time(start_hour, 0),
				work_end=time(end_hour, 0),
			)
			st.success(f"Planned {len(assignments)} task(s) for {work_date}.")

with col2:
	st.download_button(
		label="📥 Export ICS",
		data=open(init_storage().ics_path, "rb").read() if os.path.exists(init_storage().ics_path) else b"",
		file_name="schedule.ics",
		disabled=not os.path.exists(init_storage().ics_path),
		use_container_width=True,
	)

st.divider()

st.subheader("Today's Scheduled Tasks")

with get_session() as session:
	start_dt = datetime.combine(work_date, time(0, 0))
	end_dt = datetime.combine(work_date, time(23, 59))
	scheduled = (
		session.query(Task)
		.filter(Task.scheduled_start != None)  # noqa: E711
		.filter(Task.scheduled_start >= start_dt, Task.scheduled_end <= end_dt)
		.order_by(Task.scheduled_start.asc())
		.all()
	)

if not scheduled:
	st.info("No tasks scheduled yet.")
else:
	for t in scheduled:
		with st.container():
			st.markdown(f"**{t.title}** — {t.scheduled_start.strftime('%H:%M')} → {t.scheduled_end.strftime('%H:%M')}  ")
			if t.description:
				st.caption(t.description)