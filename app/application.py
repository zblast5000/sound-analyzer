from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from app.utils.resource_path import resource_path


class Application(QApplication):
    def __init__(self, argv: list[str]):
        super().__init__(argv)
        self.setApplicationName("Sound Analyzer")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("Territorio")

        icon_path = resource_path("app/resources/icons/app_icon.png")
        self.setWindowIcon(QIcon(icon_path))
