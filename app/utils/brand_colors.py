# Color palettes extracted from "territorio marca.pdf" (vector shapes analysis).
#
# Brand primaries:
#   #15A249 — brand green (main accent, all pages)
#   #21C55E — brand green light (hover/highlight)
#   #0F1A0F — near-black green (dark backgrounds)
#   #F7F9F7 — near-white green (light backgrounds)

LIGHT_THEME: dict[str, str] = {
    "BG_PRIMARY":     "#F7F9F7",  # brand near-white
    "BG_SECONDARY":   "#ECF7EC",  # very light green
    "ACCENT":         "#15A249",  # brand primary green
    "ACCENT_HOVER":   "#0F1A0F",  # dark on hover (light bg)
    "TEXT_PRIMARY":   "#0F1A0F",  # brand near-black
    "TEXT_SECONDARY": "#495E49",  # mid green
    "PLOT_BG":        "#FFFFFF",
    "PLOT_FG":        "#15A249",  # signal line: brand green
    "GRID":           "#D3ECDA",
    "BORDER":         "#E1EBE1",
}

DARK_THEME: dict[str, str] = {
    "BG_PRIMARY":     "#0F1A0F",  # brand near-black green
    "BG_SECONDARY":   "#1A2D1A",  # dark green secondary
    "ACCENT":         "#15A249",  # brand primary green
    "ACCENT_HOVER":   "#21C55E",  # brand green light on hover
    "TEXT_PRIMARY":   "#F7F9F7",  # brand near-white
    "TEXT_SECONDARY": "#E1EBE1",  # light green-grey
    "PLOT_BG":        "#111A11",  # slightly lighter than BG_PRIMARY
    "PLOT_FG":        "#21C55E",  # signal line: bright green
    "GRID":           "#1A2D1A",
    "BORDER":         "#1A2D1A",
}
