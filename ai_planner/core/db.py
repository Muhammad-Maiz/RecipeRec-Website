import os
from dataclasses import dataclass
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()


@dataclass
class StoragePaths:
	root: Path
	db_path: str
	ics_path: str


def _ensure_dirs(root: Path) -> None:
	(root / "data").mkdir(parents=True, exist_ok=True)
	(root / "exports").mkdir(parents=True, exist_ok=True)


_engine = None
_SessionLocal = None
_storage: StoragePaths | None = None


def init_storage() -> StoragePaths:
	global _engine, _SessionLocal, _storage
	if _storage is not None:
		return _storage

	root = Path(__file__).resolve().parents[1]
	_ensure_dirs(root)
	db_path = str(root / "data" / "ai_planner.db")
	ics_path = str(root / "exports" / "schedule.ics")

	_engine = create_engine(f"sqlite:///{db_path}", echo=False, future=True)
	_SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)
	_storage = StoragePaths(root=root, db_path=db_path, ics_path=ics_path)
	return _storage


def get_engine():
	if _engine is None:
		init_storage()
	return _engine


def get_session():
	if _SessionLocal is None:
		init_storage()
	return _SessionLocal()