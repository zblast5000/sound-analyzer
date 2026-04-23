from __future__ import annotations

from PySide6.QtCore import QObject

from app.views.waveform_widget import WaveformWidget
from app.views.spectrum_widget import SpectrumWidget


class PlotController(QObject):
    def __init__(
        self,
        waveform_widget: WaveformWidget,
        spectrum_widget: SpectrumWidget,
        main_window,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self._ww = waveform_widget
        self._sw = spectrum_widget
        self._win = main_window
        self._connect()

    def _connect(self) -> None:
        self._win.action_wave_zoom_in.triggered.connect(self._ww.zoom_in)
        self._win.action_wave_zoom_out.triggered.connect(self._ww.zoom_out)
        self._win.action_wave_zoom_reset.triggered.connect(self._ww.zoom_reset)

        self._win.action_fft_zoom_in.triggered.connect(self._sw.zoom_in)
        self._win.action_fft_zoom_out.triggered.connect(self._sw.zoom_out)
        self._win.action_fft_zoom_reset.triggered.connect(self._sw.zoom_reset)
