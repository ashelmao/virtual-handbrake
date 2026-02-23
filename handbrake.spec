# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Virtual Handbrake — single-file exe

import os

block_cipher = None
here = os.path.abspath(SPECPATH)

a = Analysis(
    [os.path.join(here, 'handbrake_ui.py')],
    pathex=[here],
    binaries=[],
    datas=[
        # Ship the default config beside the exe at runtime
        (os.path.join(here, 'config.json'), '.'),
    ],
    hiddenimports=[
        'config',
        'pyvjoy',
        'pygame',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VirtualHandbrake',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # windowed app, no terminal
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
