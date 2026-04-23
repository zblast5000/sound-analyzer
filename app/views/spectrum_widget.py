from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget


class SpectrumWidget(pg.PlotWidget):
    """FFT spectrum plot with fully isolated ViewBox (zoom independent of waveform)."""

    def __init__(self, parent: QWidget | None = None):
        vb = pg.ViewBox(enableMenu=True)
        super().__init__(parent=parent, viewBox=vb)

        self.setLabel("bottom", "Frequência", units="Hz")
        self.setLabel("left", "Magnitude", units="dBFS")
        self.setTitle("Espectro FFT")
        self.showGrid(x=True, y=True, alpha=0.3)
        self.getViewBox().setMouseEnabled(x=True, y=True)
        self.getViewBox().enableAutoRange()

        self._curve = self.plot(pen=pg.mkPen(color="#4A9CC8", width=1))

    def plot_data(self, frequencies: np.ndarray, magnitude_db: np.ndarray) -> None:
        self._curve.setData(frequencies, magnitude_db)
        self.getViewBox().autoRange()

    def zoom_in(self) -> None:
        self.getViewBox().scaleBy((0.5, 1.0))

    def zoom_out(self) -> None:
        self.getViewBox().scaleBy((2.0, 1.0))

    def zoom_reset(self) -> None:
        self.getViewBox().autoRange()

    def apply_palette(self, palette: dict[str, str]) -> None:
        self.setBackground(palette["PLOT_BG"])
        self._curve.setPen(pg.mkPen(color=palette["PLOT_FG"], width=1))
        fg = palette["TEXT_PRIMARY"]
        for axis in ("bottom", "left"):
            ax = self.getAxis(axis)
            ax.setPen(pg.mkPen(color=fg))
            ax.setTextPen(pg.mkPen(color=fg))
