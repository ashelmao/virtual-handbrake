import sys
import math
import time
import threading
import pygame
import pyvjoy

import config
from collections import deque

from PySide6.QtCore import Qt, QTimer, Signal, QObject, QRectF, QPointF
from PySide6.QtGui import (
    QFont, QColor, QPainter, QPen, QPainterPath,
    QLinearGradient, QRadialGradient, QDesktopServices,
)
from PySide6.QtCore import QUrl as _QUrl
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QComboBox, QSpinBox, QPushButton, QFrame,
    QProgressBar, QMessageBox, QSizePolicy, QDialog, QScrollArea,
)


# ─────────────────────────── Stylesheet ──────────────────────────────────────

STYLESHEET = """
* {
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 13px;
}

QMainWindow {
    background: transparent;
}

QDialog {
    background-color: #0a0a10;
}

QWidget#central, QWidget#viewerCentral {
    background: transparent;
}

/* ── Labels ── */

QLabel {
    color: #d4d4d8;
    background: transparent;
}

QLabel#sectionHeader {
    font-size: 9px;
    font-weight: 700;
    color: #a1a1aa;
    letter-spacing: 1.4px;
    padding: 0px 2px;
}

QLabel#statusText {
    font-size: 11px;
    color: #a1a1aa;
}

QLabel#fieldLabel {
    font-size: 12px;
    color: #a1a1aa;
}

QLabel#barLabel {
    font-size: 13px;
    font-weight: 700;
    color: #71717a;
}

QLabel#axisValue {
    font-family: "Cascadia Code", "Consolas", monospace;
    font-size: 11px;
    color: #a1a1aa;
}

QLabel#dotLabel {
    font-size: 8px;
    color: #71717a;
}

/* ── Cards ── */

QFrame#card {
    background-color: rgba(255, 255, 255, 8);
    border: 1px solid rgba(255, 255, 255, 10);
    border-radius: 14px;
}

/* ── Stage Cards ── */

QFrame#stageRow {
    background-color: rgba(255, 255, 255, 5);
    border: 1px solid rgba(255, 255, 255, 6);
    border-radius: 10px;
}

QLabel#stageName {
    font-size: 12px;
    font-weight: 600;
    color: #d4d4d8;
    background: transparent;
    border: none;
}

QLabel#pctPill {
    font-size: 13px;
    color: #52525b;
    background-color: rgba(255, 255, 255, 4);
    border: 1px solid rgba(255, 255, 255, 6);
    border-radius: 8px;
    padding: 5px 8px;
    min-height: 20px;
    qproperty-alignment: AlignCenter;
}

/* ── Combo Box ── */

QComboBox {
    background-color: rgba(255, 255, 255, 10);
    color: #e4e4e7;
    border: 1px solid rgba(255, 255, 255, 12);
    border-radius: 8px;
    padding: 5px 28px 5px 10px;
    min-height: 20px;
}
QComboBox:hover {
    border: 1px solid rgba(255, 255, 255, 22);
    background-color: rgba(255, 255, 255, 14);
}
QComboBox:disabled {
    background-color: rgba(255, 255, 255, 3);
    color: #52525b;
    border: 1px solid rgba(255, 255, 255, 4);
}
QComboBox::drop-down {
    width: 0px;
    border: none;
    background: transparent;
}
QComboBox::down-arrow {
    width: 0px;
    height: 0px;
    image: none;
}
QComboBox QAbstractItemView {
    background-color: #1a1a22;
    color: #e4e4e7;
    selection-background-color: rgba(129, 140, 248, 35);
    border: 1px solid rgba(255, 255, 255, 12);
    border-radius: 8px;
    outline: none;
    padding: 4px;
}

/* ── Spin Box ── */

QSpinBox {
    background-color: rgba(255, 255, 255, 10);
    color: #e4e4e7;
    border: 1px solid rgba(255, 255, 255, 12);
    border-radius: 8px;
    padding: 5px 8px;
    min-height: 20px;
}
QSpinBox:hover {
    border: 1px solid rgba(255, 255, 255, 22);
    background-color: rgba(255, 255, 255, 14);
}
QSpinBox:disabled {
    background-color: rgba(255, 255, 255, 3);
    color: #52525b;
    border: 1px solid rgba(255, 255, 255, 4);
}
QSpinBox::up-button, QSpinBox::down-button {
    width: 0; height: 0; border: none;
}

/* ── Buttons ── */

QPushButton {
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton#bindBtn {
    background-color: rgba(255, 255, 255, 12);
    color: #c7d2fe;
    border: 1px solid rgba(129, 140, 248, 40);
    border-radius: 8px;
    padding: 6px 14px;
    font-weight: 600;
    font-size: 12px;
    min-height: 22px;
}
QPushButton#bindBtn:hover {
    background-color: rgba(129, 140, 248, 25);
    border-color: rgba(129, 140, 248, 70);
    color: #e0e7ff;
}
QPushButton#bindBtn:pressed {
    background-color: rgba(129, 140, 248, 35);
    border-color: rgba(129, 140, 248, 90);
}
QPushButton#bindBtn[listening="true"] {
    background-color: rgba(129, 140, 248, 30);
    border: 1px solid #818cf8;
    color: #e0e7ff;
}
QPushButton#bindBtn:disabled {
    background-color: rgba(255, 255, 255, 3);
    color: #52525b;
    border: 1px solid rgba(255, 255, 255, 5);
}

QPushButton#startBtn {
    background-color: rgba(52, 211, 153, 15);
    color: #6ee7b7;
    border: 1px solid rgba(52, 211, 153, 50);
    border-radius: 12px;
}
QPushButton#startBtn:hover {
    background-color: rgba(52, 211, 153, 30);
    border-color: rgba(52, 211, 153, 80);
    color: #a7f3d0;
}
QPushButton#startBtn:pressed {
    background-color: rgba(52, 211, 153, 45);
    border-color: #34d399;
}
QPushButton#startBtn:disabled {
    background-color: rgba(255, 255, 255, 3);
    color: #3f3f46;
    border: 1px solid rgba(255, 255, 255, 5);
}

QPushButton#stopBtn {
    background-color: rgba(248, 113, 113, 12);
    color: #fca5a5;
    border: 1px solid rgba(248, 113, 113, 40);
    border-radius: 12px;
}
QPushButton#stopBtn:hover {
    background-color: rgba(248, 113, 113, 25);
    border-color: rgba(248, 113, 113, 70);
    color: #fecaca;
}
QPushButton#stopBtn:pressed {
    background-color: rgba(248, 113, 113, 40);
    border-color: #f87171;
}
QPushButton#stopBtn:disabled {
    background-color: rgba(255, 255, 255, 3);
    color: #3f3f46;
    border: 1px solid rgba(255, 255, 255, 5);
}

QPushButton#refreshBtn {
    background-color: rgba(255, 255, 255, 10);
    color: #a1a1aa;
    border: 1px solid rgba(255, 255, 255, 10);
    padding: 5px 8px;
    font-size: 14px;
    border-radius: 8px;
}
QPushButton#refreshBtn:hover {
    background-color: rgba(255, 255, 255, 16);
    color: #e4e4e7;
}

QPushButton#ghostBtn {
    background-color: rgba(255, 255, 255, 2);
    color: #52525b;
    border: 1px solid rgba(255, 255, 255, 4);
    font-weight: 500;
    font-size: 12px;
    padding: 7px 14px;
    border-radius: 10px;
}
QPushButton#ghostBtn:hover {
    background-color: rgba(255, 255, 255, 6);
    border-color: rgba(255, 255, 255, 10);
    color: #a1a1aa;
}

QPushButton#removeStageBtn {
    background-color: rgba(239, 68, 68, 20);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 40);
    border-radius: 8px;
    padding: 0px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton#removeStageBtn:hover {
    background-color: rgba(239, 68, 68, 50);
    border-color: rgba(239, 68, 68, 80);
    color: #fecaca;
}
QPushButton#removeStageBtn:pressed {
    background-color: rgba(239, 68, 68, 70);
    border-color: #ef4444;
}
QPushButton#removeStageBtn:disabled {
    background-color: rgba(255, 255, 255, 3);
    color: #3f3f46;
    border: 1px solid rgba(255, 255, 255, 5);
}

QPushButton#addStageBtn {
    background-color: rgba(129, 140, 248, 8);
    color: #a5b4fc;
    border: 1px solid rgba(129, 140, 248, 25);
    font-weight: 500;
    font-size: 12px;
    padding: 6px 16px;
    border-radius: 10px;
}
QPushButton#addStageBtn:hover {
    background-color: rgba(129, 140, 248, 18);
    border-color: rgba(129, 140, 248, 50);
    color: #e0e7ff;
}

QPushButton#titleBtn {
    background: transparent;
    border: none;
    color: #71717a;
    font-size: 13px;
    padding: 2px;
    border-radius: 6px;
    font-weight: normal;
    min-width: 28px; max-width: 28px;
    min-height: 26px; max-height: 26px;
}
QPushButton#titleBtn:hover {
    background-color: rgba(255, 255, 255, 8);
    color: #a1a1aa;
}

QPushButton#closeBtn {
    background-color: rgba(239, 68, 68, 25);
    border: 1px solid rgba(239, 68, 68, 50);
    color: #fca5a5;
    font-size: 13px;
    padding: 2px;
    border-radius: 6px;
    font-weight: 600;
    min-width: 28px; max-width: 28px;
    min-height: 26px; max-height: 26px;
}
QPushButton#closeBtn:hover {
    background-color: rgba(239, 68, 68, 180);
    border-color: #ef4444;
    color: #fef2f2;
}
QPushButton#closeBtn:pressed {
    background-color: #dc2626;
    border-color: #dc2626;
    color: #ffffff;
}

QPushButton#utilBtn {
    background: transparent;
    border: none;
    color: #71717a;
    font-size: 14px;
    padding: 2px;
    border-radius: 6px;
    min-width: 28px; max-width: 28px;
    min-height: 26px; max-height: 26px;
}
QPushButton#utilBtn:hover {
    background-color: rgba(255, 255, 255, 8);
    color: #a1a1aa;
}

/* ── Progress Bar (used in Input Viewer) ── */

QProgressBar {
    background-color: rgba(255, 255, 255, 4);
    border: 1px solid rgba(255, 255, 255, 4);
    border-radius: 5px;
    text-align: center;
    min-height: 16px;
    max-height: 16px;
    color: transparent;
}

QProgressBar::chunk {
    background-color: #818cf8;
    border-radius: 4px;
}

/* ── Scroll Area ── */

QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    background: transparent;
    width: 5px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 12);
    border-radius: 2px;
    min-height: 30px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""


# ─────────────────────────── Arc Gauge ───────────────────────────────────────

class ArcGauge(QWidget):
    """Semicircular arc gauge showing handbrake percentage."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._status = "IDLE"
        self._color = QColor("#3f3f46")
        self.setMinimumHeight(200)
        self.setMinimumWidth(200)

    def setValue(self, v: int):
        self._value = max(0, min(100, v))
        self.update()

    def setStatus(self, text: str, color: QColor = None):
        self._status = text
        if color:
            self._color = color
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        cx = w / 2
        cy = h / 2 + 8
        radius = min(w, h) / 2 - 32
        thickness = 8

        arc_rect = QRectF(cx - radius, cy - radius, radius * 2, radius * 2)
        start_deg = 225
        sweep_deg = -270

        # ── Background track ──
        pen = QPen(QColor(255, 255, 255, 10), thickness, Qt.SolidLine, Qt.RoundCap)
        p.setPen(pen)
        p.drawArc(arc_rect, int(start_deg * 16), int(sweep_deg * 16))

        # ── Small tick marks at 0, 25, 50, 75, 100% ──
        for pct in (0, 25, 50, 75, 100):
            angle_rad = math.radians(start_deg + sweep_deg * pct / 100)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            r_in = radius + thickness / 2 + 3
            r_out = radius + thickness / 2 + 8
            p.setPen(QPen(QColor(255, 255, 255, 20), 1))
            p.drawLine(
                QPointF(cx + r_in * cos_a, cy - r_in * sin_a),
                QPointF(cx + r_out * cos_a, cy - r_out * sin_a),
            )

        # ── Fill arc ──
        if self._value > 0:
            fill_span = sweep_deg * self._value / 100
            accent = QColor("#818cf8")
            if self._value >= 100:
                accent = QColor("#34d399")
            elif self._value >= 75:
                # Blend towards green at high values
                t = (self._value - 75) / 25
                r = int(129 + (52 - 129) * t)
                g = int(140 + (211 - 140) * t)
                b = int(248 + (153 - 248) * t)
                accent = QColor(r, g, b)

            # Outer glow
            glow_pen = QPen(QColor(accent.red(), accent.green(), accent.blue(), 30),
                            thickness + 16, Qt.SolidLine, Qt.RoundCap)
            p.setPen(glow_pen)
            p.drawArc(arc_rect, int(start_deg * 16), int(fill_span * 16))

            # Main arc fill
            p.setPen(QPen(accent, thickness, Qt.SolidLine, Qt.RoundCap))
            p.drawArc(arc_rect, int(start_deg * 16), int(fill_span * 16))

            # ── Endpoint dot ──
            end_angle_rad = math.radians(start_deg + fill_span)
            dot_x = cx + radius * math.cos(end_angle_rad)
            dot_y = cy - radius * math.sin(end_angle_rad)

            # Dot glow
            glow = QRadialGradient(QPointF(dot_x, dot_y), 12)
            glow.setColorAt(0, QColor(accent.red(), accent.green(), accent.blue(), 60))
            glow.setColorAt(1, QColor(accent.red(), accent.green(), accent.blue(), 0))
            p.setPen(Qt.NoPen)
            p.setBrush(glow)
            p.drawEllipse(QPointF(dot_x, dot_y), 12, 12)

            # Dot itself
            p.setBrush(accent)
            p.drawEllipse(QPointF(dot_x, dot_y), 4, 4)

        # ── Value text ──
        value_font = QFont("Segoe UI Variable", 38)
        if not QFont("Segoe UI Variable").exactMatch():
            value_font = QFont("Segoe UI", 38)
        value_font.setWeight(QFont.Bold)
        p.setFont(value_font)
        p.setPen(QColor("#fafafa") if self._value > 0 else QColor("#52525b"))
        p.drawText(QRectF(cx - 90, cy - 36, 180, 48), Qt.AlignCenter,
                    f"{self._value}%")

        # ── Status text ──
        status_font = QFont("Segoe UI Variable", 9)
        if not QFont("Segoe UI Variable").exactMatch():
            status_font = QFont("Segoe UI", 9)
        status_font.setWeight(QFont.DemiBold)
        status_font.setLetterSpacing(QFont.AbsoluteSpacing, 2.0)
        p.setFont(status_font)
        p.setPen(self._color)
        p.drawText(QRectF(cx - 60, cy + 16, 120, 18), Qt.AlignCenter,
                    self._status)

        p.end()


# ─────────────────────────── Signal Bridge ───────────────────────────────────

class SignalBridge(QObject):
    bar_update = Signal(int)
    debug_update = Signal(dict)
    stage_highlight = Signal(int)  # index of active stage (-1 = none)


# ─────────────────────────── Bind Button ─────────────────────────────────────

class BindButton(QPushButton):
    """Captures joystick input when clicked, like game keybind fields."""

    button_bound = Signal(int)

    NONE_VALUE = -1  # sentinel: "active when nothing else is pressed"

    def __init__(self, initial_btn=0, parent=None):
        super().__init__(parent)
        self.setObjectName("bindBtn")
        self.setFixedWidth(100)
        self._button_num = initial_btn
        self._listening = False
        self._poll_timer = QTimer(self)
        self._poll_timer.setInterval(16)
        self._poll_timer.timeout.connect(self._poll_joystick)
        self._update_text()
        self.clicked.connect(self._start_listening)

    def value(self) -> int:
        return self._button_num

    def setValue(self, v: int):
        self._button_num = v
        self._update_text()

    def _update_text(self):
        if self._button_num == self.NONE_VALUE:
            self.setText("None")
        else:
            self.setText(f"Btn {self._button_num}")
        self.setProperty("listening", False)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        """Right-click sets the binding to None."""
        if event.button() == Qt.RightButton:
            if self._listening:
                self._cancel_listening()
            self._button_num = self.NONE_VALUE
            self._update_text()
            self.button_bound.emit(self.NONE_VALUE)
            return
        super().mousePressEvent(event)

    def _start_listening(self):
        if self._listening:
            return
        if pygame.joystick.get_count() == 0:
            return
        self._listening = True
        self.setText("Press …")
        self.setProperty("listening", True)
        self.style().unpolish(self)
        self.style().polish(self)
        pygame.event.pump()
        # Use the device selected in the main window's combo box
        dev_idx = 0
        win = self.window()
        if hasattr(win, 'device_combo'):
            dev_idx = win.device_combo.currentIndex()
        js = pygame.joystick.Joystick(dev_idx)
        js.init()
        self._js = js
        self._held = set()
        for i in range(js.get_numbuttons()):
            if js.get_button(i):
                self._held.add(i)
        self._poll_timer.start()

    def _poll_joystick(self):
        pygame.event.pump()
        for i in range(self._js.get_numbuttons()):
            if self._js.get_button(i) and i not in self._held:
                self._poll_timer.stop()
                self._listening = False
                self._button_num = i
                self._update_text()
                self.button_bound.emit(i)
                return
        if not self.hasFocus() and not self.underMouse():
            self._cancel_listening()

    def _cancel_listening(self):
        self._poll_timer.stop()
        self._listening = False
        self._update_text()

    def setEnabled(self, enabled):
        if not enabled and self._listening:
            self._cancel_listening()
        super().setEnabled(enabled)


# ─────────────────────────── Main Window ─────────────────────────────────────

class HandbrakeApp(QMainWindow):

    AXES = {
        "X":  pyvjoy.HID_USAGE_X,
        "Y":  pyvjoy.HID_USAGE_Y,
        "Z":  pyvjoy.HID_USAGE_Z,
        "RX": pyvjoy.HID_USAGE_RX,
        "RY": pyvjoy.HID_USAGE_RY,
        "RZ": pyvjoy.HID_USAGE_RZ,
        "Slider 0": pyvjoy.HID_USAGE_SL0,
        "Slider 1": pyvjoy.HID_USAGE_SL1,
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Virtual Handbrake")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(500)
        self._drag_pos = None

        self.running = False
        self.thread = None
        self.joystick = None
        self.vj = None
        self.vj_id = None
        self.devices: list[str] = []
        self.input_viewer = None
        self.debug_viewer = None

        self.signals = SignalBridge()
        self.signals.bar_update.connect(self._update_gauge)
        self.signals.debug_update.connect(self._forward_debug)
        self.signals.stage_highlight.connect(self._highlight_active_stage)

        pygame.display.init()
        pygame.joystick.init()

        self._build_ui()
        self._refresh_devices()
        self._load_config()

    # ──────────────────────────── Build UI ───────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Custom Titlebar ──────────────────────────────────────────────────
        titlebar = QWidget()
        titlebar.setFixedHeight(40)
        titlebar.setStyleSheet("background: transparent;")
        tb = QHBoxLayout(titlebar)
        tb.setContentsMargins(16, 8, 8, 0)
        tb.setSpacing(4)

        dot = QLabel("●")
        dot.setStyleSheet("color: #818cf8; font-size: 8px;")
        tb.addWidget(dot)

        app_label = QLabel("Virtual Handbrake")
        app_label.setStyleSheet("color: #71717a; font-size: 11px; font-weight: 600;")
        tb.addWidget(app_label)
        tb.addStretch()

        # Utility buttons in titlebar
        viewer_btn = QPushButton("🎮")
        viewer_btn.setObjectName("utilBtn")
        viewer_btn.setToolTip("Input Viewer")
        viewer_btn.clicked.connect(self._toggle_input_viewer)
        tb.addWidget(viewer_btn)

        debug_btn = QPushButton("🐛")
        debug_btn.setObjectName("utilBtn")
        debug_btn.setToolTip("Debug")
        debug_btn.clicked.connect(self._toggle_debug_viewer)
        tb.addWidget(debug_btn)

        heart_btn = QPushButton("♥")
        heart_btn.setObjectName("utilBtn")
        heart_btn.setToolTip("Support on Ko-fi")
        heart_btn.setStyleSheet("color: #f472b6;")
        heart_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(_QUrl("https://ko-fi.com/ashelol"))
        )
        tb.addWidget(heart_btn)

        tb.addSpacing(4)

        sep_line = QFrame()
        sep_line.setFixedWidth(1)
        sep_line.setFixedHeight(16)
        sep_line.setStyleSheet("background: rgba(255,255,255,8);")
        tb.addWidget(sep_line)
        tb.addSpacing(4)

        min_btn = QPushButton("─")
        min_btn.setObjectName("titleBtn")
        min_btn.clicked.connect(self.showMinimized)
        tb.addWidget(min_btn)

        close_btn = QPushButton("✕")
        close_btn.setObjectName("closeBtn")
        close_btn.clicked.connect(self.close)
        tb.addWidget(close_btn)

        outer.addWidget(titlebar)

        # ── Content ──────────────────────────────────────────────────────────
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        root = QVBoxLayout(content)
        root.setContentsMargins(24, 0, 24, 22)
        root.setSpacing(0)
        outer.addWidget(content, 1)

        # ── Arc Gauge (hero) ─────────────────────────────────────────────────
        self.gauge = ArcGauge()
        self.gauge.setFixedHeight(200)
        root.addWidget(self.gauge)
        root.addSpacing(4)

        # Status line
        self.status_label = QLabel("Idle  ·  no device selected")
        self.status_label.setObjectName("statusText")
        self.status_label.setAlignment(Qt.AlignCenter)
        root.addWidget(self.status_label)
        root.addSpacing(14)

        # ── Device Card ──────────────────────────────────────────────────────
        root.addWidget(self._section("DEVICE"))
        root.addSpacing(4)

        card_dev = self._card()
        dev_lay = QHBoxLayout(card_dev)
        dev_lay.setContentsMargins(14, 10, 10, 10)
        dev_lay.setSpacing(8)

        self.device_combo = QComboBox()
        self.device_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        dev_lay.addWidget(self.device_combo, 1)

        refresh = QPushButton("↻")
        refresh.setObjectName("refreshBtn")
        refresh.setFixedSize(32, 32)
        refresh.clicked.connect(self._refresh_devices)
        dev_lay.addWidget(refresh)

        root.addWidget(card_dev)
        root.addSpacing(10)

        # ── Stages ───────────────────────────────────────────────────────
        root.addWidget(self._section("STAGES"))
        root.addSpacing(4)

        self.stages_layout = QVBoxLayout()
        self.stages_layout.setSpacing(6)
        self.stages: list[dict] = []
        root.addLayout(self.stages_layout)

        self._add_stage(label="Disengaged", pct=0, pct_editable=False, removable=False, btn_val=14)
        self._add_stage(label="Engaged", pct=100, pct_editable=True, removable=False, btn_val=14)

        root.addSpacing(4)
        self.add_stage_btn = QPushButton("+  Add Stage")
        self.add_stage_btn.setObjectName("addStageBtn")
        self.add_stage_btn.setMinimumHeight(30)
        self.add_stage_btn.clicked.connect(self._add_middle_stage)
        root.addWidget(self.add_stage_btn)

        root.addSpacing(10)

        # ── Transition Card ──────────────────────────────────────────────────
        root.addWidget(self._section("TRANSITION"))
        root.addSpacing(4)

        card_trans = self._card()
        trans_lay = QVBoxLayout(card_trans)
        trans_lay.setContentsMargins(14, 10, 14, 10)
        trans_lay.setSpacing(6)

        # Mode row
        mode_row = QHBoxLayout()
        mode_row.setSpacing(12)
        lbl_mode = QLabel("Mode")
        lbl_mode.setObjectName("fieldLabel")
        mode_row.addWidget(lbl_mode)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Instant", "Smooth"])
        self.mode_combo.setFixedWidth(100)
        self.mode_combo.currentIndexChanged.connect(self._on_mode_changed)
        mode_row.addWidget(self.mode_combo)
        mode_row.addStretch()
        trans_lay.addLayout(mode_row)

        # Smooth settings (hidden by default)
        self.smooth_widget = QWidget()
        self.smooth_widget.setStyleSheet("background: transparent;")
        smooth_inner = QVBoxLayout(self.smooth_widget)
        smooth_inner.setContentsMargins(0, 4, 0, 0)
        smooth_inner.setSpacing(10)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: rgba(255, 255, 255, 5);")
        smooth_inner.addWidget(sep)

        speed_row = QHBoxLayout()
        speed_row.setSpacing(12)

        lbl_engage = QLabel("Engage")
        lbl_engage.setObjectName("fieldLabel")
        speed_row.addWidget(lbl_engage)
        self.engage_speed_spin = QSpinBox()
        self.engage_speed_spin.setRange(10, 10000)
        self.engage_speed_spin.setValue(200)
        self.engage_speed_spin.setSuffix(" ms")
        self.engage_speed_spin.setFixedWidth(90)
        speed_row.addWidget(self.engage_speed_spin)

        lbl_release = QLabel("Release")
        lbl_release.setObjectName("fieldLabel")
        speed_row.addWidget(lbl_release)
        self.release_speed_spin = QSpinBox()
        self.release_speed_spin.setRange(10, 10000)
        self.release_speed_spin.setValue(333)
        self.release_speed_spin.setSuffix(" ms")
        self.release_speed_spin.setFixedWidth(90)
        speed_row.addWidget(self.release_speed_spin)

        speed_row.addStretch()
        smooth_inner.addLayout(speed_row)
        self.smooth_widget.setVisible(False)
        trans_lay.addWidget(self.smooth_widget)

        root.addWidget(card_trans)
        root.addSpacing(10)

        # ── Output Card ──────────────────────────────────────────────────────
        root.addWidget(self._section("OUTPUT"))
        root.addSpacing(4)

        card_out = self._card()
        out_lay = QHBoxLayout(card_out)
        out_lay.setContentsMargins(14, 10, 14, 10)
        out_lay.setSpacing(12)

        lbl_vjoy = QLabel("vJoy Device")
        lbl_vjoy.setObjectName("fieldLabel")
        out_lay.addWidget(lbl_vjoy)
        self.vjoy_spin = QSpinBox()
        self.vjoy_spin.setRange(1, 16)
        self.vjoy_spin.setValue(1)
        self.vjoy_spin.setFixedWidth(40)
        out_lay.addWidget(self.vjoy_spin)

        lbl_axis = QLabel("Axis")
        lbl_axis.setObjectName("fieldLabel")
        out_lay.addWidget(lbl_axis)
        self.axis_combo = QComboBox()
        self.axis_combo.addItems(list(self.AXES.keys()))
        self.axis_combo.setFixedWidth(100)
        out_lay.addWidget(self.axis_combo)

        lbl_rate = QLabel("Poll Rate")
        lbl_rate.setObjectName("fieldLabel")
        out_lay.addWidget(lbl_rate)
        self.rate_spin = QSpinBox()
        self.rate_spin.setRange(30, 1000)
        self.rate_spin.setValue(120)
        self.rate_spin.setSuffix(" Hz")
        self.rate_spin.setFixedWidth(80)
        out_lay.addWidget(self.rate_spin)

        out_lay.addStretch()
        root.addWidget(card_out)
        root.addSpacing(14)

        # ── Action Buttons ───────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.start_btn = QPushButton("▶   Start")
        self.start_btn.setObjectName("startBtn")
        self.start_btn.setMinimumHeight(44)
        self.start_btn.clicked.connect(self._start)
        btn_row.addWidget(self.start_btn)

        self.stop_btn = QPushButton("■   Stop")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setMinimumHeight(44)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self._stop)
        btn_row.addWidget(self.stop_btn)

        root.addLayout(btn_row)

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _on_mode_changed(self, index):
        self.smooth_widget.setVisible(index == 1)
        self.adjustSize()

    @staticmethod
    def _section(text):
        lbl = QLabel(text)
        lbl.setObjectName("sectionHeader")
        return lbl

    # ──────────────────────────── Config ──────────────────────────────────────

    def _load_config(self):
        """Populate every widget from the saved config.json."""
        cfg = config.load()

        # Device — try to re-select by remembered name
        name = cfg.get("device_name", "")
        if name:
            for i in range(self.device_combo.count()):
                if self.device_combo.itemText(i) == name:
                    self.device_combo.setCurrentIndex(i)
                    break

        # vJoy / axis / rate
        self.vjoy_spin.setValue(cfg.get("vjoy_device", 1))
        axis_name = cfg.get("axis", "X")
        idx = self.axis_combo.findText(axis_name)
        if idx >= 0:
            self.axis_combo.setCurrentIndex(idx)
        self.rate_spin.setValue(cfg.get("poll_rate", 120))

        # Mode
        mode = cfg.get("mode", "Instant")
        mode_idx = self.mode_combo.findText(mode)
        if mode_idx >= 0:
            self.mode_combo.setCurrentIndex(mode_idx)

        # Smooth speeds
        self.engage_speed_spin.setValue(cfg.get("engage_speed", 200))
        self.release_speed_spin.setValue(cfg.get("release_speed", 333))

        # Stages — rebuild from config
        saved_stages = cfg.get("stages", [])
        if saved_stages:
            # Clear existing stages
            for s in list(self.stages):
                s["widget"].setParent(None)
                s["widget"].deleteLater()
            self.stages.clear()

            for sd in saved_stages:
                self._add_stage(
                    label=sd.get("label"),
                    pct=sd.get("percent", 50),
                    pct_editable=sd.get("editable", True),
                    removable=sd.get("removable", sd.get("editable", True)),
                    btn_val=sd.get("button", 0),
                )

    def _save_config(self):
        """Gather current widget state and write config.json."""
        # Device name
        dev_name = ""
        if self.devices:
            dev_name = self.device_combo.currentText()

        stages_out = []
        for s in self.stages:
            stages_out.append({
                "label":    s["name_lbl"].text(),
                "percent":  s["pct_spin"].value(),
                "button":   s["bind_btn"].value(),
                "editable": s["pct_editable"],
                "removable": s["removable"],
            })

        cfg = {
            "device_name":   dev_name,
            "vjoy_device":   self.vjoy_spin.value(),
            "axis":          self.axis_combo.currentText(),
            "poll_rate":     self.rate_spin.value(),
            "mode":          self.mode_combo.currentText(),
            "engage_speed":  self.engage_speed_spin.value(),
            "release_speed": self.release_speed_spin.value(),
            "stages":        stages_out,
        }
        config.save(cfg)

    @staticmethod
    def _card():
        f = QFrame()
        f.setObjectName("card")
        return f

    # ── Frameless window painting ────────────────────────────────────────────

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(0.5, 0.5, self.width() - 1, self.height() - 1)
        p.setPen(QPen(QColor(255, 255, 255, 12), 1.0))
        p.setBrush(QColor(10, 10, 16, 248))
        p.drawRoundedRect(rect, 16, 16)
        p.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.position().y() < 40:
            self._drag_pos = event.globalPosition().toPoint() - self.pos()
        else:
            self._drag_pos = None

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and (event.buttons() & Qt.LeftButton):
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    # ──────────────────────────── Devices ────────────────────────────────────

    def _refresh_devices(self):
        pygame.joystick.quit()
        pygame.joystick.init()
        self.devices.clear()
        self.device_combo.clear()
        auto_select = 0
        for i in range(pygame.joystick.get_count()):
            js = pygame.joystick.Joystick(i)
            js.init()
            name = js.get_name()
            if "vjoy" in name.lower():
                continue
            self.devices.append(name)
            if "g920" in name.lower() or "logitech" in name.lower():
                auto_select = i  # auto-select common wheels

        if self.devices:
            self.device_combo.addItems(self.devices)
            self.device_combo.setCurrentIndex(auto_select)
            self.status_label.setText("Idle")
            self.status_label.setStyleSheet("color: #52525b;")
        else:
            self.device_combo.addItem("(no devices found)")
            self.status_label.setText("Idle  ·  no device detected")
            self.status_label.setStyleSheet("color: #52525b;")

    # ──────────────────────────── Stages ─────────────────────────────────────

    def _add_stage(self, label=None, pct=50, pct_editable=True, removable=True, btn_val=0, insert_before_last=False):
        if label is None:
            middle_count = sum(1 for s in self.stages if s["removable"])
            label = f"Partially engaged {middle_count + 1}" if middle_count > 0 else "Partially engaged"

        # Determine indicator color by stage type
        if not removable and not pct_editable:
            dot_color = "#818cf8"   # indigo — first (Disengaged)
        elif not removable and pct_editable:
            dot_color = "#34d399"   # emerald — last (Engaged)
        else:
            dot_color = "#a78bfa"   # violet — middle

        # ── Stage sub-card ────────────────────────────────────────────────
        row = QFrame()
        row.setObjectName("stageRow")
        row_lay = QHBoxLayout(row)
        row_lay.setContentsMargins(14, 10, 10, 10)
        row_lay.setSpacing(10)

        # Colored dot indicator
        indicator = QLabel("●")
        indicator.setStyleSheet(
            f"color: {dot_color}; font-size: 8px; background: transparent; border: none;"
        )
        indicator.setFixedWidth(10)
        row_lay.addWidget(indicator)

        # Stage name
        name_lbl = QLabel(label)
        name_lbl.setObjectName("stageName")
        name_lbl.setMinimumWidth(120)
        row_lay.addWidget(name_lbl)

        row_lay.addStretch()

        # Percentage
        pct_spin = QSpinBox()
        pct_spin.setRange(0, 100)
        pct_spin.setValue(pct)
        pct_spin.setSuffix(" %")
        pct_spin.setFixedWidth(64)
        pct_spin.setAlignment(Qt.AlignCenter)
        pct_spin.setEnabled(pct_editable)
        if not pct_editable:
            # Show fixed percentages as a styled pill label instead
            pct_spin.setVisible(False)
            pct_pill = QLabel(f"{pct} %")
            pct_pill.setObjectName("pctPill")
            pct_pill.setFixedWidth(64)
            pct_pill.setAlignment(Qt.AlignCenter)
            row_lay.addWidget(pct_pill)
        else:
            row_lay.addWidget(pct_spin)

        # Bind button
        bind_btn = BindButton(initial_btn=btn_val)
        row_lay.addWidget(bind_btn)

        # Remove button (middle stages only)
        remove_btn = None
        if removable:
            remove_btn = QPushButton("✕")
            remove_btn.setObjectName("removeStageBtn")
            remove_btn.setFixedSize(26, 34)
            row_lay.addWidget(remove_btn)

        stage_data = {
            "widget": row,
            "pct_spin": pct_spin,
            "bind_btn": bind_btn,
            "pct_editable": pct_editable,
            "removable": removable,
            "name_lbl": name_lbl,
            "remove_btn": remove_btn,
            "indicator": indicator,
            "dot_color": dot_color,
        }

        if insert_before_last and len(self.stages) >= 1:
            idx = len(self.stages) - 1
            self.stages.insert(idx, stage_data)
            self.stages_layout.insertWidget(idx, row)
        else:
            self.stages.append(stage_data)
            self.stages_layout.addWidget(row)

        if remove_btn:
            remove_btn.clicked.connect(lambda checked=False, sd=stage_data: self._remove_stage(sd))

    def _add_middle_stage(self):
        self._add_stage(label=None, pct=50, pct_editable=True, btn_val=0, insert_before_last=True)
        self._renumber_middle_stages()

    def _renumber_middle_stages(self):
        middle = [s for s in self.stages if s["removable"]]
        for i, s in enumerate(middle):
            if len(middle) > 1:
                s["name_lbl"].setText(f"Partially engaged {i + 1}")
            else:
                s["name_lbl"].setText("Partially engaged")

    def _remove_stage(self, stage_data):
        if stage_data in self.stages:
            self.stages.remove(stage_data)
            stage_data["widget"].setParent(None)
            stage_data["widget"].deleteLater()
            self._renumber_middle_stages()

    def _set_controls(self, enabled):
        for w in (self.device_combo, self.vjoy_spin,
                  self.axis_combo, self.rate_spin,
                  self.mode_combo, self.engage_speed_spin,
                  self.release_speed_spin):
            w.setEnabled(enabled)
        for s in self.stages:
            s["bind_btn"].setEnabled(enabled)
            if s["pct_editable"]:
                s["pct_spin"].setEnabled(enabled)
            if s["remove_btn"]:
                s["remove_btn"].setEnabled(enabled)
        self.add_stage_btn.setEnabled(enabled)

    # ──────────────────────────── Start / Stop ───────────────────────────────

    def _start(self):
        if not self.devices:
            QMessageBox.critical(self, "No device",
                                 "No joystick devices detected.\nConnect your controller and click ↻.")
            return

        idx = self.device_combo.currentIndex()
        vjoy_id = self.vjoy_spin.value()
        axis_key = self.axis_combo.currentText()
        axis = self.AXES[axis_key]
        rate = self.rate_spin.value()

        stage_list = []
        for s in self.stages:
            stage_list.append((s["bind_btn"].value(), s["pct_spin"].value() / 100.0))

        if not stage_list:
            QMessageBox.critical(self, "No stages", "Add at least one stage.")
            return

        try:
            self.joystick = pygame.joystick.Joystick(idx)
            self.joystick.init()
        except Exception as e:
            QMessageBox.critical(self, "Joystick error", str(e))
            return

        try:
            if self.vj is None or self.vj_id != vjoy_id:
                if self.vj is not None:
                    try:
                        self.vj.device.RelinquishVJD(self.vj_id)
                    except Exception:
                        pass
                self.vj = pyvjoy.VJoyDevice(vjoy_id)
                self.vj_id = vjoy_id
            self.vj.set_axis(axis, 0x0)
        except Exception as e:
            QMessageBox.critical(self, "vJoy error",
                                 f"Could not open vJoy device {vjoy_id}.\n{e}")
            return

        smooth = self.mode_combo.currentIndex() == 1
        engage_speed = 1000.0 / self.engage_speed_spin.value()
        release_speed = 1000.0 / self.release_speed_spin.value()

        self.running = True
        self._set_controls(False)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText(
            f"Running  ·  {self.devices[idx]}  →  vJoy {vjoy_id} {axis_key}")
        self.status_label.setStyleSheet("color: #34d399;")
        self.gauge.setStatus("READY", QColor("#52525b"))

        self.thread = threading.Thread(
            target=self._loop,
            args=(stage_list, axis, rate, smooth, engage_speed, release_speed),
            daemon=True,
        )
        self.thread.start()

    def _stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)
        if self.vj:
            try:
                self.vj.set_axis(self.AXES[self.axis_combo.currentText()], 0x0)
            except Exception:
                pass
        self._set_controls(True)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Idle")
        self.status_label.setStyleSheet("color: #52525b;")
        self._highlight_active_stage(-1)
        self._update_gauge(0)

    # ──────────────────────────── Loop ────────────────────────────────────────

    def _loop(self, stage_list, axis, rate, smooth=False, engage_speed=5.0, release_speed=3.0):
        clock = pygame.time.Clock()
        prev_pct = -1
        prev_stage_idx = -2  # force first emit
        current_pct = 0.0
        last_time = time.perf_counter()

        while self.running:
            pygame.event.pump()
            now = time.perf_counter()
            dt = now - last_time
            last_time = now

            # Check non-None stages first
            any_real_pressed = False
            target_pct = 0.0
            none_pct = -1.0
            active_stage_idx = -1
            none_stage_idx = -1
            for i, (btn, pct) in enumerate(stage_list):
                if btn == -1:
                    if pct > none_pct:
                        none_pct = pct
                        none_stage_idx = i
                elif self.joystick.get_button(btn):
                    any_real_pressed = True
                    if pct >= target_pct:
                        target_pct = pct
                        active_stage_idx = i
            # None stages activate when no real buttons are pressed
            if not any_real_pressed:
                target_pct = max(target_pct, max(none_pct, 0.0))
                active_stage_idx = none_stage_idx

            # Default to Disengaged (first stage) when nothing else is active
            if active_stage_idx == -1:
                active_stage_idx = 0

            if smooth:
                if target_pct > current_pct:
                    current_pct = min(target_pct, current_pct + engage_speed * dt)
                elif target_pct < current_pct:
                    current_pct = max(target_pct, current_pct - release_speed * dt)
                output_pct = current_pct
            else:
                output_pct = target_pct

            pct_int = int(output_pct * 100)
            axis_val = int(output_pct * 0x8000)
            if pct_int != prev_pct:
                self.vj.set_axis(axis, axis_val)
                prev_pct = pct_int
                self.signals.bar_update.emit(pct_int)

            if active_stage_idx != prev_stage_idx:
                prev_stage_idx = active_stage_idx
                self.signals.stage_highlight.emit(active_stage_idx)

            active_btns = []
            for btn, _ in stage_list:
                if btn == -1:
                    if not any_real_pressed:
                        active_btns.append("None")
                elif self.joystick.get_button(btn):
                    active_btns.append(btn)
            self.signals.debug_update.emit({
                "target_pct": round(target_pct * 100, 1),
                "output_pct": round(output_pct * 100, 1),
                "axis_val": axis_val,
                "active_buttons": active_btns,
                "dt_ms": round(dt * 1000, 2),
                "smooth": smooth,
                "engage_speed": round(engage_speed * 100),
                "release_speed": round(release_speed * 100),
                "rate": rate,
                "timestamp": now,
            })

            clock.tick(rate)

    def _highlight_active_stage(self, idx):
        """Set active stage border to its indicator color, reset others."""
        for i, s in enumerate(self.stages):
            widget = s["widget"]
            if i == idx:
                color = s["dot_color"]
                widget.setStyleSheet(
                    f"QFrame#stageRow {{"
                    f"  background-color: rgba(255, 255, 255, 5);"
                    f"  border: 1px solid {color};"
                    f"  border-radius: 10px;"
                    f"}}"
                )
            else:
                widget.setStyleSheet("")

    def _update_gauge(self, pct):
        self.gauge.setValue(pct)
        if pct > 0:
            self.gauge.setStatus("ENGAGED", QColor("#34d399"))
        elif self.running:
            self.gauge.setStatus("READY", QColor("#52525b"))
        else:
            self.gauge.setStatus("IDLE", QColor("#52525b"))

    def _forward_debug(self, data):
        if self.debug_viewer is not None:
            try:
                self.debug_viewer.update_data(data)
            except RuntimeError:
                self.debug_viewer = None

    # ──────────────────────────── Viewers ─────────────────────────────────────

    def _toggle_debug_viewer(self):
        if self.debug_viewer is not None:
            try:
                if self.debug_viewer.isVisible():
                    self.debug_viewer.close()
                    self.debug_viewer = None
                    return
            except RuntimeError:
                self.debug_viewer = None
        self.debug_viewer = DebugWindow(self)
        self.debug_viewer.show()

    def _toggle_input_viewer(self):
        if self.input_viewer is not None:
            try:
                if self.input_viewer.isVisible():
                    self.input_viewer.close()
                    self.input_viewer = None
                    return
            except RuntimeError:
                self.input_viewer = None

        if not self.devices:
            QMessageBox.critical(self, "No device", "No joystick devices detected.")
            return

        idx = self.device_combo.currentIndex()
        try:
            js = pygame.joystick.Joystick(idx)
            js.init()
        except Exception as e:
            QMessageBox.critical(self, "Joystick error", str(e))
            return

        self.input_viewer = InputViewer(self, js)
        self.input_viewer.show()

    # ──────────────────────────── Close ───────────────────────────────────────

    def closeEvent(self, event):
        self._save_config()
        for viewer in (self.input_viewer, self.debug_viewer):
            if viewer:
                try:
                    viewer.close()
                except RuntimeError:
                    pass
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)
        if self.vj is not None:
            try:
                self.vj.device.RelinquishVJD(self.vj_id)
            except Exception:
                pass
        pygame.quit()
        event.accept()


# ─────────────────────────── Graph Widget ────────────────────────────────────

class GraphWidget(QWidget):
    """Custom-painted rolling graph of handbrake output %."""

    HISTORY_SECONDS = 10

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(180)
        self._data: deque[tuple[float, float]] = deque()
        self._start_time = time.perf_counter()

    def append(self, timestamp: float, pct: float):
        self._data.append((timestamp, pct))
        cutoff = timestamp - self.HISTORY_SECONDS
        while self._data and self._data[0][0] < cutoff:
            self._data.popleft()

    def clear_data(self):
        self._data.clear()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        ml, mr, mt, mb = 40, 10, 10, 24
        gx, gy = ml, mt
        gw = w - ml - mr
        gh = h - mt - mb

        p.fillRect(self.rect(), QColor(0, 0, 0, 0))
        p.fillRect(gx, gy, gw, gh, QColor(8, 8, 14))

        label_font = QFont("Cascadia Code", 8)
        if not label_font.exactMatch():
            label_font = QFont("Consolas", 8)
        p.setFont(label_font)

        for pct in (0, 25, 50, 75, 100):
            y = gy + gh - int(pct / 100 * gh)
            p.setPen(QPen(QColor(255, 255, 255, 8), 1, Qt.DotLine))
            p.drawLine(gx, y, gx + gw, y)
            p.setPen(QColor("#3f3f46"))
            p.drawText(0, y - 6, ml - 4, 12, Qt.AlignRight | Qt.AlignVCenter, f"{pct}%")

        now = time.perf_counter()
        p.setPen(QColor("#3f3f46"))
        for sec in range(0, self.HISTORY_SECONDS + 1, 2):
            x = gx + int(sec / self.HISTORY_SECONDS * gw)
            label = f"-{self.HISTORY_SECONDS - sec}s" if sec < self.HISTORY_SECONDS else "0s"
            p.drawText(x - 16, gy + gh + 2, 32, 16, Qt.AlignHCenter | Qt.AlignTop, label)

        if len(self._data) >= 2:
            cutoff = now - self.HISTORY_SECONDS
            path = QPainterPath()
            first = True
            for ts, pct in self._data:
                t_norm = (ts - cutoff) / self.HISTORY_SECONDS
                x = gx + t_norm * gw
                y = gy + gh - (pct / 100 * gh)
                if first:
                    path.moveTo(x, y)
                    first = False
                else:
                    path.lineTo(x, y)

            p.setPen(QPen(QColor("#818cf8"), 2))
            p.drawPath(path)

            fill_path = QPainterPath(path)
            last_ts, _ = self._data[-1]
            first_ts, _ = self._data[0]
            x_last = gx + ((last_ts - cutoff) / self.HISTORY_SECONDS) * gw
            x_first = gx + ((first_ts - cutoff) / self.HISTORY_SECONDS) * gw
            fill_path.lineTo(x_last, gy + gh)
            fill_path.lineTo(x_first, gy + gh)
            fill_path.closeSubpath()
            grad = QLinearGradient(0, gy, 0, gy + gh)
            grad.setColorAt(0, QColor(129, 140, 248, 35))
            grad.setColorAt(1, QColor(129, 140, 248, 3))
            p.fillPath(fill_path, grad)

        p.setPen(QPen(QColor(255, 255, 255, 8), 1))
        p.drawRect(gx, gy, gw, gh)
        p.end()


# ─────────────────────────── Debug Window ────────────────────────────────────

class DebugWindow(QDialog):
    """Live debug information and activation graph."""

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Debug")
        self.setMinimumWidth(480)
        self.setMinimumHeight(520)

        central = QWidget()
        central.setObjectName("viewerCentral")
        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.addWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(18, 14, 18, 18)
        root.setSpacing(0)

        title = QLabel("Debug")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #fafafa;")
        root.addWidget(title)
        sub = QLabel("Live handbrake telemetry")
        sub.setStyleSheet("font-size: 11px; color: #3f3f46;")
        root.addWidget(sub)
        root.addSpacing(12)

        # ── Info card ──
        root.addWidget(self._header("TELEMETRY"))
        root.addSpacing(4)

        card = QFrame()
        card.setObjectName("card")
        info_lay = QVBoxLayout(card)
        info_lay.setContentsMargins(14, 10, 14, 10)
        info_lay.setSpacing(3)

        mono = "font-family: 'Cascadia Code', Consolas, monospace; font-size: 12px; color: #d4d4d8;"
        dim = "font-family: 'Cascadia Code', Consolas, monospace; font-size: 12px; color: #71717a;"

        self._labels = {}
        fields = [
            ("target_pct",  "Target %"),
            ("output_pct",  "Output %"),
            ("axis_val",    "Axis value"),
            ("active_btns", "Active btns"),
            ("mode",        "Mode"),
            ("rate",        "Poll rate"),
            ("dt_ms",       "Loop Δt"),
            ("engage_spd",  "Engage spd"),
            ("release_spd", "Release spd"),
        ]
        for key, display in fields:
            row = QHBoxLayout()
            name_lbl = QLabel(display)
            name_lbl.setStyleSheet(dim)
            name_lbl.setFixedWidth(110)
            row.addWidget(name_lbl)
            val_lbl = QLabel("—")
            val_lbl.setStyleSheet(mono)
            row.addWidget(val_lbl)
            row.addStretch()
            info_lay.addLayout(row)
            self._labels[key] = val_lbl

        root.addWidget(card)
        root.addSpacing(10)

        # ── Graph ──
        root.addWidget(self._header("ACTIVATION GRAPH"))
        root.addSpacing(4)

        graph_card = QFrame()
        graph_card.setObjectName("card")
        graph_lay = QVBoxLayout(graph_card)
        graph_lay.setContentsMargins(8, 8, 8, 8)

        self.graph = GraphWidget()
        graph_lay.addWidget(self.graph)
        root.addWidget(graph_card, 1)

        self._repaint_timer = QTimer(self)
        self._repaint_timer.timeout.connect(self.graph.update)
        self._repaint_timer.start(33)

    @staticmethod
    def _header(text):
        lbl = QLabel(text)
        lbl.setObjectName("sectionHeader")
        return lbl

    def update_data(self, d: dict):
        self._labels["target_pct"].setText(f"{d['target_pct']:.1f}%")
        self._labels["output_pct"].setText(f"{d['output_pct']:.1f}%")
        self._labels["axis_val"].setText(f"0x{d['axis_val']:04X}  ({d['axis_val']})")
        btns = d["active_buttons"]
        self._labels["active_btns"].setText(", ".join(str(b) for b in btns) if btns else "None")
        self._labels["mode"].setText("Smooth" if d["smooth"] else "Instant")
        self._labels["rate"].setText(f"{d['rate']} Hz")
        self._labels["dt_ms"].setText(f"{d['dt_ms']:.2f} ms")
        self._labels["engage_spd"].setText(f"{d['engage_speed']} %/s")
        self._labels["release_spd"].setText(f"{d['release_speed']} %/s")
        self.graph.append(d["timestamp"], d["output_pct"])

    def closeEvent(self, event):
        self._repaint_timer.stop()
        self.graph.clear_data()
        event.accept()


# ─────────────────────────── Input Viewer ────────────────────────────────────

class InputViewer(QDialog):

    def __init__(self, parent, joystick):
        super().__init__(parent)
        self.joystick = joystick
        self.setWindowTitle(f"Input Viewer — {joystick.get_name()}")
        self.setMinimumWidth(420)

        central = QWidget()
        central.setObjectName("viewerCentral")
        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.addWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(18, 14, 18, 18)
        root.setSpacing(0)

        title = QLabel("Input Viewer")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #fafafa;")
        root.addWidget(title)
        sub = QLabel(joystick.get_name())
        sub.setStyleSheet("font-size: 11px; color: #3f3f46;")
        root.addWidget(sub)
        root.addSpacing(12)

        num_axes = joystick.get_numaxes()
        num_buttons = joystick.get_numbuttons()
        num_hats = joystick.get_numhats()

        # Axes
        self.axis_bars = []
        self.axis_labels = []
        if num_axes > 0:
            root.addWidget(self._header("AXES"))
            root.addSpacing(4)
            card = QFrame()
            card.setObjectName("card")
            lay = QVBoxLayout(card)
            lay.setContentsMargins(14, 10, 14, 10)
            lay.setSpacing(5)

            for i in range(num_axes):
                row = QHBoxLayout()
                lbl = QLabel(f"Axis {i}")
                lbl.setObjectName("fieldLabel")
                lbl.setFixedWidth(48)
                row.addWidget(lbl)
                bar = QProgressBar()
                bar.setRange(0, 1000)
                bar.setValue(500)
                bar.setFixedHeight(10)
                bar.setStyleSheet("""
                    QProgressBar { background-color: rgba(255,255,255,4); border: 1px solid rgba(255,255,255,4);
                                   border-radius: 4px; min-height: 10px; max-height: 10px; color: transparent; }
                    QProgressBar::chunk { background-color: #818cf8; border-radius: 3px; }
                """)
                row.addWidget(bar, 1)
                self.axis_bars.append(bar)

                val_lbl = QLabel("+0.00")
                val_lbl.setObjectName("axisValue")
                val_lbl.setFixedWidth(44)
                val_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                row.addWidget(val_lbl)
                self.axis_labels.append(val_lbl)
                lay.addLayout(row)

            root.addWidget(card)
            root.addSpacing(8)

        # Buttons
        self.btn_dots = []
        if num_buttons > 0:
            root.addWidget(self._header("BUTTONS"))
            root.addSpacing(4)
            card = QFrame()
            card.setObjectName("card")
            grid_container = QVBoxLayout(card)
            grid_container.setContentsMargins(14, 10, 14, 10)
            grid = QGridLayout()
            grid.setSpacing(5)

            cols = min(num_buttons, 10)
            for i in range(num_buttons):
                r, c = divmod(i, cols)
                cell = QVBoxLayout()
                cell.setAlignment(Qt.AlignCenter)
                cell.setSpacing(1)

                dot = QLabel()
                dot.setFixedSize(20, 20)
                dot.setStyleSheet("background-color: rgba(255,255,255,12); border-radius: 10px;")
                dot.setAlignment(Qt.AlignCenter)
                cell.addWidget(dot, 0, Qt.AlignCenter)
                self.btn_dots.append(dot)

                num_lbl = QLabel(str(i))
                num_lbl.setObjectName("dotLabel")
                num_lbl.setAlignment(Qt.AlignCenter)
                cell.addWidget(num_lbl, 0, Qt.AlignCenter)
                grid.addLayout(cell, r, c)

            grid_container.addLayout(grid)
            root.addWidget(card)
            root.addSpacing(8)

        # Hats
        self.hat_labels = []
        if num_hats > 0:
            root.addWidget(self._header("HATS (D-PAD)"))
            root.addSpacing(4)
            card = QFrame()
            card.setObjectName("card")
            lay = QVBoxLayout(card)
            lay.setContentsMargins(14, 10, 14, 10)
            lay.setSpacing(4)

            for i in range(num_hats):
                row = QHBoxLayout()
                lbl = QLabel(f"Hat {i}")
                lbl.setObjectName("fieldLabel")
                row.addWidget(lbl)
                val_lbl = QLabel("(0, 0)")
                val_lbl.setObjectName("axisValue")
                row.addWidget(val_lbl)
                row.addStretch()
                self.hat_labels.append(val_lbl)
                lay.addLayout(row)

            root.addWidget(card)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._poll)
        self.timer.start(16)

    @staticmethod
    def _header(text):
        lbl = QLabel(text)
        lbl.setObjectName("sectionHeader")
        return lbl

    def _poll(self):
        try:
            pygame.event.pump()

            for i, (bar, lbl) in enumerate(zip(self.axis_bars, self.axis_labels)):
                raw = self.joystick.get_axis(i)
                bar.setValue(int((raw + 1.0) / 2.0 * 1000))
                lbl.setText(f"{raw:+.2f}")

            for i, dot in enumerate(self.btn_dots):
                pressed = self.joystick.get_button(i)
                if pressed:
                    dot.setStyleSheet("background-color: #818cf8; border-radius: 10px;")
                else:
                    dot.setStyleSheet("background-color: rgba(255,255,255,12); border-radius: 10px;")

            for i, lbl in enumerate(self.hat_labels):
                h = self.joystick.get_hat(i)
                lbl.setText(f"({h[0]:+d}, {h[1]:+d})")
        except Exception:
            pass

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()


# ─────────────────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = HandbrakeApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
