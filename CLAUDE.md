# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto

Aplicativo desktop Python para visualização de espectros de áudio (.wav e .m4a). Dois gráficos independentes: forma de onda (tempo) e espectro FFT, com zoom independente por gráfico. Arquitetura MVC, PySide6, tema claro/escuro e identidade visual do arquivo `territorio marca.pdf`.

## Ambiente Virtual

```bash
# Criar (primeira vez)
pip install virtualenv
virtualenv .venv

# Ativar (Windows)
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar o app
python main.py

# Rodar testes
pytest tests/
```

O app deve ser sempre executado com o `.venv` ativado.

## Arquitetura

```
Sound Analyzer/
├── main.py                  # Entry point: QApplication, SplashScreen, MainController
├── requirements.txt
├── app/
│   ├── application.py       # QApplication subclass
│   ├── models/              # MVC — Model (QObject + Signals, sem imports de UI)
│   │   ├── audio_model.py   # Carregamento de arquivo em QThread, emite loading_finished
│   │   ├── fft_model.py     # Cálculo FFT via scipy, emite fft_ready
│   │   └── waveform_model.py# Preparação eixo de tempo + downsampling, emite waveform_ready
│   ├── views/               # MVC — View (widgets Qt, sem lógica de negócio)
│   │   ├── main_window.py   # Carrega main_window.ui via QUiLoader, expõe signals
│   │   ├── waveform_widget.py  # pg.PlotWidget com ViewBox isolado (zoom independente)
│   │   ├── spectrum_widget.py  # pg.PlotWidget com ViewBox isolado (zoom independente)
│   │   ├── splash_screen.py    # QSplashScreen
│   │   └── theme_manager.py    # Singleton — aplica QSS + atualiza cores pyqtgraph
│   ├── controllers/         # MVC — Controller (conecta signals model ↔ view)
│   │   ├── main_controller.py  # Raiz: instancia modelos e sub-controllers
│   │   ├── audio_controller.py # file_open_requested → AudioModel.load_file (QThread)
│   │   └── plot_controller.py  # Gerencia zoom reset dos dois gráficos
│   ├── ui/                  # Arquivos Qt Designer (.ui) — editáveis externamente
│   │   ├── main_window.ui
│   │   ├── about_dialog.ui
│   │   └── preferences_dialog.ui
│   ├── resources/
│   │   ├── icons/           # SVG/PNG: app_icon, open_file, zoom_in/out/reset, theme
│   │   ├── splash/splash.png
│   │   └── themes/
│   │       ├── light.qss    # Template QSS com placeholders {BG_PRIMARY} etc.
│   │       └── dark.qss
│   └── utils/
│       ├── audio_loader.py  # Strategy: WavLoader (soundfile) / M4aLoader (PyAV)
│       ├── fft_utils.py     # Helpers FFT e funções de janela (scipy)
│       ├── brand_colors.py  # Paletas LIGHT_THEME / DARK_THEME extraídas do PDF
│       └── resource_path.py # Resolve caminhos em dev e bundle
└── tests/
```

## Padrões de Projeto

| Padrão | Onde |
|--------|------|
| Observer | Qt Signals/Slots — toda comunicação model → view/controller |
| Strategy | `audio_loader.py`: `WavLoader` / `M4aLoader` selecionados por extensão |
| Singleton | `ThemeManager` — instância global acessível a todos os widgets |
| Factory | `ModelFactory` em `main_controller.py` — cria os três modelos |
| Template Method | `FFTModel.compute()`: pipeline _window → _fft → _db → _notify |
| Command | `QAction` para zoom reset (habilitado/desabilitado conforme estado) |

## Zoom Independente

Cada `PlotWidget` tem seu próprio `ViewBox` — nunca compartilhado ou vinculado ao outro gráfico. Zoom no waveform não afeta o FFT e vice-versa.

## Tema Claro/Escuro

- QSS usa templates com `{BG_PRIMARY}`, `{ACCENT}`, etc. preenchidos via `brand_colors.py`
- `ThemeManager.apply_theme()` aplica QSS via `app.setStyleSheet()`
- Cores dos plots pyqtgraph são atualizadas via API (pyqtgraph ignora QSS para o canvas)

## Bibliotecas Principais

- `PySide6` — UI framework
- `soundfile` — decodificação .wav
- `av` (PyAV) — decodificação .m4a (ffmpeg embutido no wheel, sem instalação no sistema)
- `scipy` — FFT multithreaded (pocketfft)
- `pyqtgraph` — plots interativos nativos Qt com zoom/pan por ViewBox
