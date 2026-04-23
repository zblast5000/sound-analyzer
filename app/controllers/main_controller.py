from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication

from app.models.audio_model import AudioModel
from app.models.fft_model import FFTModel
from app.models.waveform_model import WaveformModel
from app.views.main_window import MainWindow
from app.views.theme_manager import ThemeManager
from app.controllers.audio_controller import AudioController
from app.controllers.plot_controller import PlotController


class ModelFactory:
    @staticmethod
    def create_all(parent: QObject | None = None) -> tuple[AudioModel, FFTModel, WaveformModel]:
        return (
            AudioModel(parent),
            FFTModel(parent),
            WaveformModel(parent),
        )


class MainController(QObject):
    def __init__(
        self,
        main_window: MainWindow,
        app: QApplication,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self._win = main_window
        self._app = app

        audio_model, fft_model, waveform_model = ModelFactory.create_all(self)

        self._audio_ctrl = AudioController(
            audio_model, fft_model, waveform_model, main_window, self
        )
        self._plot_ctrl = PlotController(
            main_window.waveform_widget,
            main_window.spectrum_widget,
            main_window,
            self,
        )

        self._theme_mgr = ThemeManager()
        self._theme_mgr.theme_changed.connect(self._on_theme_changed)
        main_window.action_toggle_theme.triggered.connect(
            lambda: self._theme_mgr.toggle(self._app)
        )

    def _on_theme_changed(self, name: str, palette: dict) -> None:
        self._win.waveform_widget.apply_palette(palette)
        self._win.spectrum_widget.apply_palette(palette)
