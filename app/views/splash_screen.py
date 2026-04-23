from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap, QFont
from PySide6.QtWidgets import QSplashScreen

from app.utils.resource_path import resource_path


class SplashScreen(QSplashScreen):
    def __init__(self) -> None:
        splash_path = resource_path("app/resources/splash/splash.png")

        if Path(splash_path).exists():
            pixmap = QPixmap(splash_path)
            pixmap = pixmap.scaled(
                600, 400,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        else:
            # Fallback: plain colored rectangle until splash image is added
            pixmap = QPixmap(600, 400)
            pixmap.fill(QColor("#1C1C1E"))

        super().__init__(pixmap, Qt.WindowType.WindowStaysOnTopHint)

    def show_message(self, msg: str) -> None:
        font = QFont("Segoe UI", 10)
        self.setFont(font)
        self.showMessage(
            msg,
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
            QColor("#AAAAAA"),
        )
