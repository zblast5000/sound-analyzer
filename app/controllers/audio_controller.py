from __future__ import annotations

import numpy as np
from PySide6.QtCore import QObject

from app.models.audio_model import AudioModel
from app.models.fft_model import FFTModel
from app.models.waveform_model import WaveformModel
from app.views.main_window import MainWindow


class AudioController(QObject):
    def __init__(
        self,
        audio_model: AudioModel,
        fft_model: FFTModel,
        waveform_model: WaveformModel,
        main_window: MainWindow,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self._audio = audio_model
        self._fft = fft_model
        self._waveform = waveform_model
        self._win = main_window
        self._connect()

    def _connect(self) -> None:
        self._win.file_open_requested.connect(self._audio.load_file)
        self._audio.loading_started.connect(self._on_loading_started)
        self._audio.loading_finished.connect(self._on_audio_loaded)
        self._audio.loading_failed.connect(self._on_loading_failed)

        self._waveform.waveform_ready.connect(self._on_waveform_ready)
        self._fft.fft_ready.connect(self._on_fft_ready)

        self._win.waveform_widget.region_changed.connect(self._on_region_changed)

    def _on_loading_started(self) -> None:
        self._win.set_status("Carregando arquivo...")

    def _on_audio_loaded(
        self, samples: np.ndarray, sample_rate: int, path: str
    ) -> None:
        self._win.set_file_loaded(
            path, sample_rate,
            self._audio.duration_seconds,
            self._audio.channel_count,
        )
        self._waveform.prepare(samples, sample_rate)
        self._fft.compute(samples, sample_rate)

    def _on_loading_failed(self, error: str) -> None:
        self._win.set_status(f"Erro ao carregar arquivo: {error}")

    def _on_waveform_ready(
        self, time_axis: np.ndarray, amplitude: np.ndarray
    ) -> None:
        x, y = self._waveform.get_downsampled()
        self._win.waveform_widget.plot_data(x, y)

    def _on_fft_ready(
        self, frequencies: np.ndarray, magnitude_db: np.ndarray
    ) -> None:
        self._win.spectrum_widget.plot_data(frequencies, magnitude_db)

    def _on_region_changed(self, t_start: float, t_end: float) -> None:
        samples = self._audio.get_samples_for_range(t_start, t_end)
        if samples.shape[1] > 0:
            self._fft.compute(samples, self._audio.sample_rate)
            duration = t_end - t_start
            self._win.set_status(
                f"Seleção: {t_start:.3f}s — {t_end:.3f}s  ({duration:.3f}s)"
            )
