from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFileDialog, QMainWindow

from app.utils.resource_path import resource_path
from app.views.waveform_widget import WaveformWidget
from app.views.spectrum_widget import SpectrumWidget


class MainWindow(QObject):
    """Wraps the QMainWindow loaded from main_window.ui."""

    file_open_requested = Signal(str)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._load_ui()
        self._connect_actions()

    def _load_ui(self) -> None:
        loader = QUiLoader()
        loader.registerCustomWidget(WaveformWidget)
        loader.registerCustomWidget(SpectrumWidget)
        ui_path = resource_path("app/ui/main_window.ui")
        self._ui: QMainWindow = loader.load(ui_path)

    def _connect_actions(self) -> None:
        self._ui.actionOpen.triggered.connect(self._on_open_triggered)
        self._ui.actionExit.triggered.connect(self._ui.close)
        self._ui.actionAbout.triggered.connect(self._show_about)

    # --- Public interface ---

    @property
    def qt_window(self) -> QMainWindow:
        """The actual QMainWindow — use for splash.finish() and show()."""
        return self._ui

    def show(self) -> None:
        self._ui.show()

    @property
    def waveform_widget(self) -> WaveformWidget:
        return self._ui.waveformWidget

    @property
    def spectrum_widget(self) -> SpectrumWidget:
        return self._ui.spectrumWidget

    @property
    def action_wave_zoom_in(self):
        return self._ui.actionWaveZoomIn

    @property
    def action_wave_zoom_out(self):
        return self._ui.actionWaveZoomOut

    @property
    def action_wave_zoom_reset(self):
        return self._ui.actionWaveZoomReset

    @property
    def action_fft_zoom_in(self):
        return self._ui.actionFFTZoomIn

    @property
    def action_fft_zoom_out(self):
        return self._ui.actionFFTZoomOut

    @property
    def action_fft_zoom_reset(self):
        return self._ui.actionFFTZoomReset

    @property
    def action_toggle_theme(self):
        return self._ui.actionToggleTheme

    def set_status(self, message: str) -> None:
        self._ui.statusBar().showMessage(message)

    def set_file_loaded(
        self, path: str, sample_rate: int, duration: float, channels: int
    ) -> None:
        name = Path(path).name
        self.set_status(
            f"{name}  |  {sample_rate} Hz  |  {duration:.2f} s  |  {channels} canal(is)"
        )
        for action in (
            self._ui.actionWaveZoomIn, self._ui.actionWaveZoomOut,
            self._ui.actionWaveZoomReset, self._ui.actionFFTZoomIn,
            self._ui.actionFFTZoomOut, self._ui.actionFFTZoomReset,
        ):
            action.setEnabled(True)

    def _on_open_triggered(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self._ui,
            "Abrir arquivo de áudio",
            "",
            "Áudio (*.wav *.m4a *.mp4);;Todos os arquivos (*)",
        )
        if path:
            self.file_open_requested.emit(path)

    def _show_about(self) -> None:
        loader = QUiLoader()
        ui_path = resource_path("app/ui/about_dialog.ui")
        dialog = loader.load(ui_path, self._ui)
        dialog.exec()
