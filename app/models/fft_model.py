from __future__ import annotations

import numpy as np
from PySide6.QtCore import QObject, Signal


class FFTModel(QObject):
    fft_ready = Signal(np.ndarray, np.ndarray)  # frequencies, magnitude_db

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.fft_size: int = 4096
        self.window_name: str = "hann"
        self.frequencies: np.ndarray | None = None
        self.magnitude_db: np.ndarray | None = None

    def set_fft_size(self, n: int) -> None:
        self.fft_size = n

    def set_window(self, name: str) -> None:
        self.window_name = name

    def compute(self, samples: np.ndarray, sample_rate: int) -> None:
        """Pipeline: window → fft → db → notify."""
        mono = self._to_mono(samples)
        freq, mag_db = self._run_fft(mono, sample_rate)
        self.frequencies = freq
        self.magnitude_db = mag_db
        self.fft_ready.emit(freq, mag_db)

    def _to_mono(self, samples: np.ndarray) -> np.ndarray:
        if samples.ndim == 1:
            return samples
        return samples.mean(axis=0)

    def _run_fft(
        self, mono: np.ndarray, sample_rate: int
    ) -> tuple[np.ndarray, np.ndarray]:
        from app.utils.fft_utils import compute_fft
        return compute_fft(mono, sample_rate, self.fft_size, self.window_name)
