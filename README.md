# Virtual Handbrake

A virtual handbrake application that maps physical joystick/wheel buttons to a vJoy virtual axis — designed for sim racing setups where a dedicated handbrake input isn't available.

Built with a custom dark UI using PySide6 and an arc gauge visualization.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Multi-stage handbrake** — Define multiple activation stages (e.g. 0%, 50%, 100%) each bound to a different button
- **Instant & Smooth modes** — Toggle between immediate activation or configurable ramp-up/ramp-down speeds
- **Arc gauge** — Real-time semicircular gauge showing current handbrake output
- **Input Viewer** — Live display of all axes, buttons, and hats on the connected device
- **Debug window** — Telemetry panel with a rolling activation graph
- **Configurable vJoy output** — Choose any vJoy device (1–16) and any axis (X, Y, Z, RX, RY, RZ, Slider 0/1)
- **Auto-detect Logitech wheels** — Automatically selects G920 or other Logitech devices when found
- **Persistent config** — Settings saved to `config.json` and restored on launch
- **Single-file exe** — Ships as a standalone `.exe` via PyInstaller

## Requirements

- **Windows** (vJoy is Windows-only)
- **[vJoy](https://sourceforge.net/projects/vjoystick/)** installed and configured with at least one virtual device
- **Python 3.10+** (if running from source)

### Python Dependencies

```
PySide6
pygame
pyvjoy
```

## Installation

### From Source

```bash
git clone https://github.com/ashelmao/virtual-handbrake.git
cd virtual-handbrake
pip install PySide6 pygame pyvjoy
python handbrake_ui.py
```

### Build Standalone Exe

```bash
pip install pyinstaller
pyinstaller handbrake.spec
```

The output binary will be in `dist/VirtualHandbrake.exe`.

## Usage

1. **Connect** your wheel/controller and make sure vJoy is installed
2. **Launch** the app — your device should be auto-detected
3. **Configure stages** — bind buttons for each handbrake stage (right-click a bind button to set it to "None", which activates when no other stage button is pressed)
4. **Set the output** — choose the vJoy device and axis your sim reads as the handbrake
5. **Pick a mode** — *Instant* for on/off response, *Smooth* for gradual engage/release
6. **Start** — the arc gauge shows live output; the status bar confirms the active mapping

### Stages

| Stage | Description |
|-------|-------------|
| First stage | Always present — defines the baseline (typically 0%) |
| Middle stages | Optional — add intermediate positions with custom percentages |
| Last stage | Always present — defines the maximum (typically 100%) |

The highest-percentage stage whose button is currently held wins. Stages bound to "None" activate only when no other button is pressed.

## Project Structure

```
handbrake_ui.py   — Main application (UI, gauge, input viewer, debug window)
config.py         — Config load/save with defaults and path resolution
config.json       — User settings (auto-generated on first run)
g920_input.py     — Minimal standalone script for quick G920 button-to-axis mapping
handbrake.spec    — PyInstaller build spec
```

## Configuration

Settings are stored in `config.json` next to the executable/script:

```json
{
  "device_name": "Logitech G HUB G920 Driving Force Racing Wheel USB",
  "vjoy_device": 1,
  "axis": "X",
  "poll_rate": 120,
  "mode": "Smooth",
  "engage_speed": 500,
  "release_speed": 300,
  "stages": [
    { "label": "First stage", "percent": 0, "button": 14, "editable": false },
    { "label": "Last stage", "percent": 100, "button": 15, "editable": false }
  ]
}
```

All settings are also editable through the UI.
