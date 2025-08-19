from __future__ import annotations

import os
from typing import Optional, List

try:
	from openai import OpenAI  # type: ignore
except Exception:
	OpenAI = None  # type: ignore

try:
	import anthropic  # type: ignore
except Exception:
	anthropic = None  # type: ignore


SYSTEM = "You are a helpful assistant that prioritizes tasks succinctly. Keep outputs brief and actionable."


def suggest_task_breakdown(title: str, description: str) -> Optional[List[str]]:
	api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
	if not api_key:
		return None
	try:
		if os.getenv("OPENAI_API_KEY") and OpenAI:
			client = OpenAI()
			prompt = f"Break the task into 3-6 actionable subtasks. Task: {title}. Details: {description}"
			resp = client.chat.completions.create(
				model="gpt-4o-mini",
				messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
				max_tokens=250,
			)
			text = resp.choices[0].message.content.strip()
			items = [line.strip("- ") for line in text.splitlines() if line.strip()]
			return items[:6]
		elif os.getenv("ANTHROPIC_API_KEY") and anthropic:
			client = anthropic.Anthropic()
			prompt = f"Break the task into 3-6 actionable subtasks. Task: {title}. Details: {description}"
			msg = client.messages.create(
				model="claude-3-haiku-20240307",
				max_tokens=250,
				messages=[{"role": "user", "content": prompt}],
			)
			text = "".join(block.get("text", "") for block in msg.content) if hasattr(msg, "content") else ""
			items = [line.strip("- ") for line in text.splitlines() if line.strip()]
			return items[:6]
	except Exception:
		return None
	return None