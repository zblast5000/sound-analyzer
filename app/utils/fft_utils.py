import numpy as np
from scipy import signal, fft as scipy_fft


WINDOW_FUNCTIONS = {
    "hann":     signal.windows.hann,
    "blackman": signal.windows.blackman,
    "flattop":  signal.windows.flattop,
    "hamming":  signal.windows.hamming,
}


def compute_fft(
    samples: np.ndarray,
    sample_rate: int,
    fft_size: int = 4096,
    window_name: str = "hann",
) -> tuple[np.ndarray, np.ndarray]:
    """Return (frequencies_hz, magnitude_db) for the given mono samples."""
    n = min(fft_size, len(samples))
    chunk = samples[:n].copy()

    win_fn = WINDOW_FUNCTIONS.get(window_name, signal.windows.hann)
    window = win_fn(n)
    windowed = chunk * window

    spectrum = scipy_fft.rfft(windowed, n=fft_size, workers=-1)
    magnitude = np.abs(spectrum)

    # Avoid log(0)
    magnitude = np.where(magnitude == 0, 1e-12, magnitude)
    magnitude_db = 20 * np.log10(magnitude / magnitude.max())

    frequencies = scipy_fft.rfftfreq(fft_size, d=1.0 / sample_rate)
    return frequencies, magnitude_db


def downsample_for_display(
    x: np.ndarray, y: np.ndarray, max_points: int = 10_000
) -> tuple[np.ndarray, np.ndarray]:
    """Reduce array length for rendering without distorting the envelope."""
    if len(x) <= max_points:
        return x, y
    step = len(x) // max_points
    return x[::step], y[::step]
