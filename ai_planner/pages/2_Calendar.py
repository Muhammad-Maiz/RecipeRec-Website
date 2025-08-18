import streamlit as st
import pandas as pd
from datetime import date, datetime, time
import plotly.express as px

from core.db import get_session
from core.models import Task
from ui.components import inject_styles

st.set_page_config(page_title="Calendar • AI Planner", page_icon="📅", layout="wide")
inject_styles()

st.title("📅 Calendar")

plan_date = st.date_input("Date", value=date.today())

with get_session() as session:
	start_dt = datetime.combine(plan_date, time(0, 0))
	end_dt = datetime.combine(plan_date, time(23, 59))
	rows = (
		session.query(Task)
		.filter(Task.scheduled_start != None)  # noqa: E711
		.filter(Task.scheduled_start >= start_dt, Task.scheduled_end <= end_dt)
		.order_by(Task.scheduled_start.asc())
		.all()
	)

if not rows:
	st.info("No scheduled tasks on this date.")
else:
	data = [
		{
			"Task": r.title,
			"Start": r.scheduled_start,
			"Finish": r.scheduled_end,
			"Priority": r.priority.title(),
		}
		for r in rows
	]
	df = pd.DataFrame(data)
	fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Priority")
	fig.update_yaxes(autorange="reversed")
	st.plotly_chart(fig, use_container_width=True)