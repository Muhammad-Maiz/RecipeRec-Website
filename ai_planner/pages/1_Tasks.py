import streamlit as st
from datetime import datetime

from core.db import get_session
from core.models import Task
from ui.components import inject_styles, priority_badge

st.set_page_config(page_title="Tasks • AI Planner", page_icon="✅", layout="wide")
inject_styles()

st.title("✅ Tasks")

st.sidebar.header("Filters")
with st.sidebar:
	priority_filter = st.multiselect("Priority", options=["high", "medium", "low"], default=["high", "medium", "low"])
	q = st.text_input("Search")

with get_session() as session:
	query = session.query(Task)
	if priority_filter:
		query = query.filter(Task.priority.in_(priority_filter))
	if q:
		like = f"%{q}%"
		query = query.filter((Task.title.ilike(like)) | (Task.description.ilike(like)) | (Task.tags.ilike(like)))
	tasks = query.order_by(Task.created_at.desc()).all()

col1, col2 = st.columns([1, 2])
with col1:
	st.subheader("New Task")
	title = st.text_input("Title", key="new_title")
	description = st.text_area("Description", key="new_desc", height=100)
	priority = st.selectbox("Priority", ["high", "medium", "low"], index=1, key="new_priority")
	duration = st.number_input("Duration (minutes)", min_value=15, max_value=480, value=60, step=15, key="new_duration")
	due = st.date_input("Due date", key="new_due")
	tags = st.text_input("Tags", key="new_tags")
	if st.button("Add", type="primary"):
		if title.strip():
			with get_session() as session:
				session.add(Task(
					title=title.strip(),
					description=description.strip(),
					priority=priority,
					duration_minutes=int(duration),
					due_at=datetime.combine(due, datetime.min.time()),
					tags=tags.strip(),
				))
				st.success("Task added")
				st.rerun()
		else:
			st.warning("Title required")

with col2:
	st.subheader("All Tasks")
	if not tasks:
		st.info("No tasks yet")
	else:
		for t in tasks:
			cols = st.columns([6, 2, 2, 2])
			with cols[0]:
				st.markdown(f"**{t.title}**  " + priority_badge(t.priority), unsafe_allow_html=True)
				if t.description:
					st.caption(t.description)
				if t.tags:
					st.caption(f"Tags: {t.tags}")
			with cols[1]:
				st.text(f"{t.duration_minutes} min")
			with cols[2]:
				if t.scheduled_start:
					st.text(t.scheduled_start.strftime('%Y-%m-%d %H:%M'))
				else:
					st.text("Not scheduled")
			with cols[3]:
				if st.button("Delete", key=f"del_{t.id}"):
					with get_session() as session:
						obj = session.get(Task, t.id)
						session.delete(obj)
						st.rerun()