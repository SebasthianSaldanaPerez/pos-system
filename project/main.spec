# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all
import os

block_cipher = None

# =========================
# PySide6 (CRÍTICO)
# =========================
datas, binaries, hiddenimports = collect_all("PySide6")

# =========================
# Assets del proyecto
# =========================
project_assets = [
    ("ui/assets", "ui/assets"),
    (".env", "."),
]

# =========================
# SPEC
# =========================
a = Analysis(
    ["main.py"],
    pathex=[os.getcwd()],
    binaries=binaries,
    datas=datas + project_assets,
    hiddenimports=hiddenimports + [
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "PySide6.QtNetwork",
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
    name="main",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,   # GUI app
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ui/assets/main_icon.ico',
)