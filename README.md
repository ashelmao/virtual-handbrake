# Virtual Handbrake

A virtual handbrake application that maps joystick/wheel button presses to a vJoy axis, enabling multi-stage handbrake functionality in racing simulators.

## Features

- **Multi-stage handbrake** — Define multiple engage stages (e.g. 0%, 50%, 100%) each bound to a different button
- **Instant or Smooth mode** — Choose between immediate activation or configurable engage/release ramp speeds
- **vJoy output** — Maps to any vJoy device and axis (X, Y, Z, RX, RY, RZ, Slider 0/1)
- **Live arc gauge** — Visual feedback showing current handbrake percentage with color-coded status
- **Input Viewer** — Real-time display of all axes, buttons, and hats on the selected device
- **Debug window** — Live telemetry with an activation graph over time
- **Persistent config** — Settings are saved to `config.json` and restored on launch
- **Frameless dark UI** — Clean, modern interface built with PySide6

## Requirements

- Windows
- Python 3.10+
- [vJoy](https://github.com/njz3/vJoy) installed and configured
- A joystick or racing wheel (any DirectInput device)

## Installation

```bash
pip install pygame pyvjoy PySide6
```

## Usage

```bash
python handbrake_ui.py
```

1. Select your input device from the dropdown
2. Configure button bindings for each stage under **MAPPING**
3. Set vJoy device, axis, poll rate, and mode under **CONFIGURATION**
4. Click **Start**

### Stages

| Stage | Description |
|-------|-------------|
| **First stage** | The resting / minimum position (usually 0%) |
| **Middle stages** | Optional intermediate positions (add with "+ Add Stage") |
| **Last stage** | Full engagement (usually 100%) |

Right-click a bind button to set it to **None** — a None-bound stage activates when no other buttons are pressed.

### Modes

- **Instant** — Output jumps directly to the highest active stage percentage
- **Smooth** — Output ramps toward the target at configurable engage/release speeds (%/s)

## Configuration

Settings are stored in `config.json` next to the executable. The file is created automatically on first run and updated every time the app is closed.

```json
{
  "device_name": "",
  "vjoy_device": 1,
  "axis": "X",
  "poll_rate": 120,
  "mode": "Instant",
  "engage_speed": 500,
  "release_speed": 300,
  "stages": [
    {"label": "First stage", "percent": 0, "button": 14, "editable": false},
    {"label": "Last stage", "percent": 100, "button": 14, "editable": false}
  ]
}
```

## Building

To compile into a standalone exe:

```bash
pip install pyinstaller
pyinstaller handbrake.spec --noconfirm
```

The output will be at `dist/VirtualHandbrake.exe`. Ship `config.json` alongside it (or let the app generate a default on first launch).

## License

MIT
