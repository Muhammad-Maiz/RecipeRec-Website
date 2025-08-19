from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base

from .db import Base, get_engine


class Task(Base):
	__tablename__ = "tasks"

	id = Column(Integer, primary_key=True)
	title = Column(String(200), nullable=False)
	description = Column(Text, nullable=True)
	priority = Column(String(16), default="medium")
	duration_minutes = Column(Integer, default=30)
	due_at = Column(DateTime, nullable=True)
	tags = Column(String(200), nullable=True)

	scheduled_start = Column(DateTime, nullable=True)
	scheduled_end = Column(DateTime, nullable=True)

	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self) -> str:
		return f"<Task id={self.id} title={self.title!r}>"


# Create tables on import
engine = get_engine()
Base.metadata.create_all(engine)