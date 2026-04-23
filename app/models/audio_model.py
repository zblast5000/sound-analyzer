from __future__ import annotations

import numpy as np
from PySide6.QtCore import QObject, QThread, Signal


class _LoadWorker(QThread):
    finished = Signal(np.ndarray, int, str)  # samples, sample_rate, path
    failed = Signal(str)                      # error message

    def __init__(self, path: str, parent: QObject | None = None):
        super().__init__(parent)
        self._path = path

    def run(self) -> None:
        try:
            from app.utils.audio_loader import load_audio
            samples, sample_rate = load_audio(self._path)
            self.finished.emit(samples, sample_rate, self._path)
        except Exception as exc:
            self.failed.emit(str(exc))


class AudioModel(QObject):
    loading_started = Signal()
    loading_finished = Signal(np.ndarray, int, str)  # samples, sample_rate, path
    loading_failed = Signal(str)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.samples: np.ndarray | None = None
        self.sample_rate: int = 0
        self.file_path: str | None = None
        self._worker: _LoadWorker | None = None

    @property
    def duration_seconds(self) -> float:
        if self.samples is None or self.sample_rate == 0:
            return 0.0
        return self.samples.shape[1] / self.sample_rate

    @property
    def channel_count(self) -> int:
        if self.samples is None:
            return 0
        return self.samples.shape[0]

    def get_channel(self, index: int = 0) -> np.ndarray:
        if self.samples is None:
            return np.array([], dtype=np.float32)
        return self.samples[min(index, self.channel_count - 1)]

    def get_samples_for_range(self, t_start: float, t_end: float) -> np.ndarray:
        """Return samples (channels, N) for the given time range in seconds."""
        if self.samples is None or self.sample_rate == 0:
            return np.zeros((1, 0), dtype=np.float32)
        total = self.samples.shape[1]
        i0 = max(0, int(t_start * self.sample_rate))
        i1 = min(total, int(t_end * self.sample_rate))
        if i1 <= i0:
            return np.zeros((self.channel_count, 0), dtype=np.float32)
        return self.samples[:, i0:i1]

    def load_file(self, path: str) -> None:
        if self._worker and self._worker.isRunning():
            self._worker.quit()
            self._worker.wait()

        self.loading_started.emit()
        self._worker = _LoadWorker(path, self)
        self._worker.finished.connect(self._on_loaded)
        self._worker.failed.connect(self.loading_failed)
        self._worker.start()

    def _on_loaded(self, samples: np.ndarray, sample_rate: int, path: str) -> None:
        self.samples = samples
        self.sample_rate = sample_rate
        self.file_path = path
        self.loading_finished.emit(samples, sample_rate, path)
