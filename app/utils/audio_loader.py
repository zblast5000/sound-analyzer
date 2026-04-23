from __future__ import annotations

from pathlib import Path
from typing import Protocol

import numpy as np


class AudioLoaderStrategy(Protocol):
    def load(self, path: str) -> tuple[np.ndarray, int]:
        """Return (samples float32 shape (channels, samples), sample_rate)."""
        ...


class WavLoader:
    def load(self, path: str) -> tuple[np.ndarray, int]:
        import soundfile as sf
        data, sample_rate = sf.read(path, dtype="float32", always_2d=True)
        # soundfile returns (samples, channels) — transpose to (channels, samples)
        return data.T, sample_rate


class M4aLoader:
    def load(self, path: str) -> tuple[np.ndarray, int]:
        import av
        container = av.open(path)
        audio_stream = next(s for s in container.streams if s.type == "audio")
        sample_rate = audio_stream.sample_rate
        channel_layout = audio_stream.layout.name
        channels = len(audio_stream.layout.channels)

        frames: list[np.ndarray] = []
        for frame in container.decode(audio_stream):
            arr = frame.to_ndarray()  # shape varies by format
            if arr.dtype != np.float32:
                arr = arr.astype(np.float32) / 32768.0
            # Ensure shape is (channels, samples)
            if arr.ndim == 1:
                arr = arr[np.newaxis, :]
            frames.append(arr)

        container.close()

        if not frames:
            return np.zeros((channels, 0), dtype=np.float32), sample_rate

        return np.concatenate(frames, axis=1), sample_rate


_LOADERS: dict[str, type] = {
    ".wav":  WavLoader,
    ".m4a":  M4aLoader,
    ".mp4":  M4aLoader,
}


def get_loader(path: str) -> AudioLoaderStrategy:
    ext = Path(path).suffix.lower()
    loader_cls = _LOADERS.get(ext)
    if loader_cls is None:
        supported = ", ".join(_LOADERS.keys())
        raise ValueError(f"Formato não suportado: '{ext}'. Suportados: {supported}")
    return loader_cls()


def load_audio(path: str) -> tuple[np.ndarray, int]:
    """Convenience wrapper: returns (samples float32 (channels, N), sample_rate)."""
    return get_loader(path).load(path)
