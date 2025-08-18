from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import List

from ics import Calendar, Event

from .db import init_storage
from .models import Task


@dataclass
class Assignment:
	task_id: int
	start: datetime
	end: datetime


def _sort_key(task: Task) -> tuple:
	priority_rank = {"high": 0, "medium": 1, "low": 2}.get(task.priority, 1)
	due_ts = task.due_at.timestamp() if task.due_at else float("inf")
	return (priority_rank, due_ts, -task.duration_minutes)


def plan_day(session, plan_date: date, work_start: time, work_end: time) -> List[Assignment]:
	start_dt = datetime.combine(plan_date, work_start)
	end_dt = datetime.combine(plan_date, work_end)

	unscheduled = (
		session.query(Task)
		.filter(Task.scheduled_start == None)  # noqa: E711
		.order_by(Task.created_at.asc())
		.all()
	)
	unscheduled.sort(key=_sort_key)

	current = start_dt
	assignments: List[Assignment] = []
	for task in unscheduled:
		block = timedelta(minutes=max(15, int(task.duration_minutes)))
		if current + block > end_dt:
			break
		task.scheduled_start = current
		task.scheduled_end = current + block
		task.updated_at = datetime.utcnow()
		session.add(task)
		assignments.append(Assignment(task_id=task.id, start=current, end=current + block))
		current += block

	session.commit()
	_export_ics(session)
	return assignments


def _export_ics(session) -> None:
	storage = init_storage()
	cal = Calendar()
	all_tasks = session.query(Task).filter(Task.scheduled_start != None).all()  # noqa: E711
	for t in all_tasks:
		ev = Event()
		ev.name = t.title
		ev.begin = t.scheduled_start
		ev.end = t.scheduled_end
		ev.description = (t.description or "").strip()
		cal.events.add(ev)
	with open(storage.ics_path, "w", encoding="utf-8") as f:
		f.writelines(cal.serialize_iter())