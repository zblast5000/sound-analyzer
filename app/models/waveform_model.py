from __future__ import annotations

import numpy as np
from PySide6.QtCore import QObject, Signal


class WaveformModel(QObject):
    waveform_ready = Signal(np.ndarray, np.ndarray)  # time_axis, amplitude

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.time_axis: np.ndarray | None = None
        self.amplitude: np.ndarray | None = None

    def prepare(self, samples: np.ndarray, sample_rate: int) -> None:
        mono = samples.mean(axis=0) if samples.ndim > 1 else samples
        n = len(mono)
        time_axis = np.linspace(0, n / sample_rate, num=n, endpoint=False)
        self.time_axis = time_axis
        self.amplitude = mono
        self.waveform_ready.emit(time_axis, mono)

    def get_downsampled(
        self, max_points: int = 10_000
    ) -> tuple[np.ndarray, np.ndarray]:
        from app.utils.fft_utils import downsample_for_display
        if self.time_axis is None or self.amplitude is None:
            return np.array([]), np.array([])
        return downsample_for_display(self.time_axis, self.amplitude, max_points)
