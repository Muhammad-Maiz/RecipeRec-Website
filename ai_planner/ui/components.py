import streamlit as st
from pathlib import Path


def inject_styles() -> None:
	css_path = Path(__file__).resolve().parents[1] / "assets" / "styles.css"
	try:
		with open(css_path, "r", encoding="utf-8") as f:
			st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
	except Exception:
		pass


def priority_badge(priority: str) -> str:
	klass = {
		"high": "priority-high",
		"medium": "priority-med",
		"low": "priority-low",
	}.get(priority, "priority-med")
	return f"<span class='badge {klass}'>{priority.title()}</span>"