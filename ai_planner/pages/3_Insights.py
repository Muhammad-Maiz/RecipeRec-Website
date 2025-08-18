import streamlit as st
from core.db import get_session
from core.models import Task
from core.llm import suggest_task_breakdown
from ui.components import inject_styles

st.set_page_config(page_title="Insights • AI Planner", page_icon="💡", layout="wide")
inject_styles()

st.title("💡 Insights")

st.subheader("Task Suggestions")

with get_session() as session:
	t = session.query(Task).order_by(Task.created_at.desc()).first()

if not t:
	st.info("Add a task first to see suggestions.")
else:
	st.markdown(f"Most recent task: **{t.title}**")
	if t.description:
		st.caption(t.description)

	if st.button("Suggest breakdown"):
		ideas = suggest_task_breakdown(t.title, t.description or "")
		if ideas:
			st.success("Here are some suggested subtasks:")
			for i in ideas:
				st.markdown(f"- {i}")
		else:
			st.warning("No API key configured. Add `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in your .env to enable suggestions.")