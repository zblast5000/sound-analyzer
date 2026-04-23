from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

from app.utils.brand_colors import DARK_THEME, LIGHT_THEME
from app.utils.resource_path import resource_path


class ThemeManager(QObject):
    theme_changed = Signal(str, dict)  # theme_name, palette dict

    _instance: "ThemeManager | None" = None

    def __new__(cls, parent: QObject | None = None) -> "ThemeManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent: QObject | None = None):
        if hasattr(self, "_initialized"):
            return
        super().__init__(parent)
        self._current_name: str = "dark"
        self._current_palette: dict[str, str] = DARK_THEME
        self._initialized = True

    @property
    def current_name(self) -> str:
        return self._current_name

    @property
    def current_palette(self) -> dict[str, str]:
        return self._current_palette

    def apply_theme(self, name: str, app: QApplication) -> None:
        palette = DARK_THEME if name == "dark" else LIGHT_THEME
        qss_path = resource_path(f"app/resources/themes/{name}.qss")
        try:
            template = Path(qss_path).read_text(encoding="utf-8")
            stylesheet = template.format(**palette)
        except FileNotFoundError:
            stylesheet = ""

        app.setStyleSheet(stylesheet)
        self._current_name = name
        self._current_palette = palette
        self.theme_changed.emit(name, palette)

    def toggle(self, app: QApplication) -> None:
        new_name = "light" if self._current_name == "dark" else "dark"
        self.apply_theme(new_name, app)
