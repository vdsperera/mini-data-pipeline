import json
import os
from pathlib import Path

class State:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.data = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return {"completed": [], "failed": {}}
        try:
            with self.path.open("r", encoding="utf-8") as f:
                d = json.load(f)
                return {
                    "completed": list(d.get("completed", [])),
                    "failed": dict(d.get("failed", {})) if isinstance(d.get("failed"), dict) else {str(x): "" for x in d.get("failed", [])},
                }
        except Exception:
            return {"completed": [], "failed": {}}

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)
        os.replace(tmp, self.path)

    def is_done(self, item_id: int | str) -> bool:
        return item_id in self.data["completed"] or str(item_id) in [str(x) for x in self.data["completed"]]

    def mark_done(self, item_id: int | str) -> None:
        if not self.is_done(item_id):
            self.data["completed"].append(item_id)
        self.data["failed"].pop(str(item_id), None)
        self._save()

    def mark_failed(self, item_id: int | str, reason: str = "") -> None:
        self.data["failed"][str(item_id)] = reason
        self._save()

def load_state(path: Path) -> dict:
    s = State(path)
    failed = [int(k) if isinstance(k, str) and k.isdigit() else k for k in s.data["failed"].keys()]
    return {"completed": s.data["completed"], "failed": failed}

def save_state(path: Path, state: dict) -> None:
    s = State(path)
    s.data["completed"] = state.get("completed", [])
    if isinstance(state.get("failed"), dict):
        s.data["failed"] = state["failed"]
    else:
        s.data["failed"] = {str(k): "" for k in state.get("failed", [])}
    s._save()
