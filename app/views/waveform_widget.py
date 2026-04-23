from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget


class WaveformWidget(pg.PlotWidget):
    """Waveform plot with fully isolated ViewBox (zoom independent of FFT).

    Emits region_changed(t_start, t_end) whenever the user moves the
    selection region; consumers should recompute the FFT for that slice.
    """

    region_changed = Signal(float, float)  # t_start, t_end (seconds)

    def __init__(self, parent: QWidget | None = None):
        vb = pg.ViewBox(enableMenu=True)
        super().__init__(parent=parent, viewBox=vb)

        self.setLabel("bottom", "Tempo", units="s")
        self.setLabel("left", "Amplitude")
        self.setTitle("Forma de Onda")
        self.showGrid(x=True, y=True, alpha=0.3)
        self.getViewBox().setMouseEnabled(x=True, y=True)
        self.getViewBox().enableAutoRange()

        self._curve = self.plot(pen=pg.mkPen(color="#21C55E", width=1))

        # Selection region — hidden until data is loaded
        self._region = pg.LinearRegionItem(
            values=[0, 1],
            brush=pg.mkBrush(QColor(21, 162, 73, 45)),   # brand green, translucent
            pen=pg.mkPen(color="#15A249", width=1),
            movable=True,
            swapMode="push",
        )
        self._region.setZValue(10)
        self._region.hide()
        self.addItem(self._region)
        self._region.sigRegionChanged.connect(self._on_region_changed)

    # --- Data ---

    def plot_data(self, time_axis: np.ndarray, amplitude: np.ndarray) -> None:
        self._curve.setData(time_axis, amplitude)
        if len(time_axis) > 0:
            self._init_region(float(time_axis[0]), float(time_axis[-1]))
        self.getViewBox().autoRange()

    def _init_region(self, t_start: float, t_end: float) -> None:
        """Place the selection region across the full waveform on first load."""
        # Block signal to avoid premature FFT recompute during init
        self._region.blockSignals(True)
        self._region.setRegion([t_start, t_end])
        self._region.blockSignals(False)
        self._region.show()

    def get_region(self) -> tuple[float, float]:
        return tuple(self._region.getRegion())  # type: ignore[return-value]

    # --- Zoom ---

    def zoom_in(self) -> None:
        self.getViewBox().scaleBy((0.5, 1.0))

    def zoom_out(self) -> None:
        self.getViewBox().scaleBy((2.0, 1.0))

    def zoom_reset(self) -> None:
        self.getViewBox().autoRange()

    # --- Theme ---

    def apply_palette(self, palette: dict[str, str]) -> None:
        self.setBackground(palette["PLOT_BG"])
        self._curve.setPen(pg.mkPen(color=palette["PLOT_FG"], width=1))
        accent = QColor(palette["ACCENT"])
        accent.setAlpha(45)
        self._region.setBrush(pg.mkBrush(accent))
        self._region.setPen(pg.mkPen(color=palette["ACCENT"], width=1))
        fg = palette["TEXT_PRIMARY"]
        for axis in ("bottom", "left"):
            ax = self.getAxis(axis)
            ax.setPen(pg.mkPen(color=fg))
            ax.setTextPen(pg.mkPen(color=fg))

    # --- Internal ---

    def _on_region_changed(self) -> None:
        t_start, t_end = self._region.getRegion()
        if t_end > t_start:
            self.region_changed.emit(t_start, t_end)
