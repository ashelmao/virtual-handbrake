# Virtual Handbrake 🏎️💨

Turn any button on your wheel or controller into a handbrake for sim racing — no extra hardware needed!

Virtual Handbrake maps buttons on your existing device to a virtual axis using [vJoy](https://sourceforge.net/projects/vjoystick/), so your sim sees a real handbrake input.

![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ☕ Support the Project

If this app saved you from buying a $100+ handbrake, consider buying me a coffee! It helps keep the project alive and updates coming.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/ashelol)

---

## 🚀 How to Install & Play (No Coding Required!)

You don't need to know how to code to use this. Just follow these simple steps:

1. **Install vJoy:** Download and install **[vJoy](https://sourceforge.net/projects/vjoystick/)**. This is the magic that lets your computer pretend it has a handbrake plugged in.
2. **Download the App:** Go to the [Releases page](https://github.com/ashelmao/virtual-handbrake/releases) and download the latest `VirtualHandbrake.exe`.
3. **Run it:** Double-click the `.exe` file you just downloaded. That's it!

## 🎮 How to Set It Up

1. **Plug in your wheel/controller** before starting the app. It should detect it automatically (especially Logitech wheels like the G920).
2. **Bind your buttons:** Click the "Bind" buttons in the app and press the button on your wheel you want to use for the handbrake.
   - *Tip: You can set different buttons for different handbrake strengths (like 50% and 100%).*
3. **Choose your output:** Pick a vJoy device and axis (usually Device 1, Axis X is fine).
4. **Pick a mode:**
   - **Instant:** Handbrake snaps on and off instantly.
   - **Smooth:** Handbrake ramps up gradually (feels more realistic).
5. **Hit Start!** The gauge will show your handbrake working. Now go into your sim racing game's settings and map the handbrake to the vJoy axis you chose.

---

## 🛠️ For the Nerds (Building from Source)

If you *do* know how to code and want to run the Python script directly:

Requires **Python 3.10+** on Windows.

```bash
git clone https://github.com/ashelmao/virtual-handbrake.git
cd virtual-handbrake
pip install PySide6 pygame pyvjoy
python handbrake_ui.py
```
