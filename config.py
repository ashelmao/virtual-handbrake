"""
Configuration manager for Virtual Handbrake.

Resolves the config file path correctly whether running as a Python script
or as a frozen PyInstaller executable:
  - Script mode  → config.json next to this .py file
  - Frozen mode  → config.json next to the .exe

The config file is user-editable JSON that lives *beside* the binary,
NOT inside the PyInstaller bundle, so it persists across launches.
"""

import json
import os
import shutil
import sys
from copy import deepcopy

# ─── Default configuration ───────────────────────────────────────────────────

DEFAULTS = {
    "device_name": "",
    "vjoy_device": 1,
    "axis": "X",
    "poll_rate": 120,
    "mode": "Instant",
    "engage_speed": 200,
    "release_speed": 333,
    "stages": [
        {"label": "Disengaged",  "percent": 0,   "button": 14, "editable": False, "removable": False},
        {"label": "Engaged",     "percent": 100, "button": 14, "editable": True,  "removable": False},
    ],
}

CONFIG_FILENAME = "config.json"

# ─── Path resolution ─────────────────────────────────────────────────────────

def _app_dir() -> str:
    """Return the directory where the running application lives.

    * Frozen (PyInstaller --onefile or --onedir): folder containing the .exe
    * Normal script: folder containing *this* .py file
    """
    if getattr(sys, "frozen", False):
        # PyInstaller sets sys.executable to the .exe path
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _bundle_dir() -> str:
    """Return the PyInstaller bundle temp dir (sys._MEIPASS) or the script dir."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.dirname(os.path.abspath(__file__))


def config_path() -> str:
    """Full path to the config JSON on disk."""
    return os.path.join(_app_dir(), CONFIG_FILENAME)


def _ensure_config_exists() -> None:
    """If no config.json exists next to the exe, copy the bundled default out."""
    dest = config_path()
    if not os.path.isfile(dest):
        bundled = os.path.join(_bundle_dir(), CONFIG_FILENAME)
        if os.path.isfile(bundled):
            shutil.copy2(bundled, dest)

# ─── Load / Save ─────────────────────────────────────────────────────────────

def load() -> dict:
    """Load configuration from disk, falling back to defaults for any
    missing keys.  If the file doesn't exist, returns a full copy of DEFAULTS."""
    _ensure_config_exists()
    cfg = deepcopy(DEFAULTS)
    path = config_path()
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                user = json.load(f)
            # Merge top-level keys (user values override defaults)
            for key in DEFAULTS:
                if key in user:
                    cfg[key] = user[key]
        except (json.JSONDecodeError, OSError) as exc:
            print(f"[config] Failed to read {path}: {exc}  — using defaults")
    return cfg


def save(cfg: dict) -> None:
    """Persist a configuration dict to disk as pretty-printed JSON."""
    path = config_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except OSError as exc:
        print(f"[config] Failed to write {path}: {exc}")
