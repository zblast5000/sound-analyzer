================================================================================
                           SOUND ANALYZER
              Visualizador de Espectros de Áudio
================================================================================

DESCRIÇÃO
---------
Sound Analyzer é um aplicativo desktop desenvolvido em Python para análise
visual de arquivos de áudio. Ele exibe a forma de onda no domínio do tempo
e o espectro de frequências via FFT (Transformada Rápida de Fourier),
permitindo a inspeção detalhada de qualquer trecho do áudio.


FUNCIONALIDADES
---------------

  Visualização de Áudio
  • Suporte a arquivos .wav e .m4a (AAC)
  • Exibição da forma de onda completa com eixo de tempo em segundos
  • Exibição do espectro FFT em dBFS com eixo de frequência em Hz
  • Downsampling automático para renderização fluida de arquivos longos

  Seleção de Trecho para Análise FFT
  • Região de seleção interativa (verde) sobre a forma de onda
  • Arraste as bordas da região para selecionar qualquer intervalo de tempo
  • O espectro FFT é recalculado automaticamente refletindo apenas
    as amostras do trecho selecionado
  • Barra de status exibe o intervalo selecionado em tempo real

  Zoom Independente
  • Zoom e pan via mouse (scroll/arrastar) em cada gráfico separadamente
  • Zoom no gráfico de forma de onda NÃO afeta o gráfico FFT e vice-versa
  • Botões dedicados na barra de ferramentas: Zoom +, Zoom -, Reset
    para cada gráfico individualmente

  Tema Claro / Escuro
  • Dois temas completos: Escuro (padrão) e Claro
  • Alternância via menu Visualização → Alternar tema ou atalho Ctrl+T
  • Cores baseadas na identidade visual da marca (verde primário #15A249)
  • Cores dos gráficos também se adaptam ao tema ativo

  Interface
  • Splash screen animada na inicialização
  • Barra de menu: Arquivo, Visualização, Ajuda
  • Barra de ferramentas com ícones para ações frequentes
  • Barra de status com informações do arquivo: nome, taxa de amostragem,
    duração e número de canais
  • Layout com divisor ajustável entre os dois gráficos
  • Diálogos: Sobre o programa, Preferências

  Configurações (Preferências)
  • Escolha da função de janelamento FFT: Hann, Blackman, Flat Top, Hamming
  • Tamanho da FFT configurável: 1024, 2048, 4096 (padrão) ou 8192 pontos


REQUISITOS DO SISTEMA
---------------------
  • Windows 10 ou superior
  • Python 3.10 ou superior
  • virtualenv (instalado via pip)
  • Conexão à internet apenas para instalação das dependências


INSTALAÇÃO
----------
  1. Clone o repositório ou extraia os arquivos do projeto

  2. Instale o virtualenv (caso não tenha):
       pip install virtualenv

  3. Crie e ative o ambiente virtual:
       virtualenv .venv
       .venv\Scripts\activate

  4. Instale as dependências:
       pip install -r requirements.txt

  Obs.: Não é necessário instalar o ffmpeg no sistema operacional.
  O suporte a .m4a utiliza a biblioteca PyAV, que já inclui o ffmpeg
  internamente (instalado automaticamente com o pip).


COMO USAR
---------
  1. Ative o ambiente virtual:
       .venv\Scripts\activate

  2. Execute o aplicativo:
       python main.py

  3. Clique em "Abrir arquivo..." (Ctrl+O) e selecione um arquivo .wav ou .m4a

  4. A forma de onda e o espectro FFT serão exibidos automaticamente

  5. Para analisar um trecho específico:
       - Arraste as bordas da região verde na forma de onda
       - O espectro FFT atualiza automaticamente

  6. Para alterar o tema: menu Visualização → Alternar tema (Ctrl+T)

  7. Para fazer zoom:
       - Scroll do mouse sobre qualquer gráfico
       - Ou use os botões Zoom +/- na barra de ferramentas


ATALHOS DE TECLADO
------------------
  Ctrl+O    Abrir arquivo de áudio
  Ctrl+T    Alternar tema claro/escuro
  Ctrl+Q    Sair do aplicativo


ARQUITETURA TÉCNICA
-------------------
  Padrão:    MVC (Model-View-Controller)
  Interface: PySide6 com layouts em arquivos .ui (editáveis no Qt Designer)
  Plots:     pyqtgraph (renderização nativa Qt, ViewBox independente por gráfico)
  FFT:       scipy.fft com suporte multithreaded (pocketfft)
  Áudio .wav: soundfile (libsndfile)
  Áudio .m4a: PyAV (ffmpeg embutido, sem dependência de sistema)

  Padrões de projeto utilizados:
    • Observer   — Qt Signals/Slots entre model e view
    • Strategy   — seleção de loader por extensão de arquivo
    • Singleton  — ThemeManager com instância global
    • Factory    — criação centralizada dos modelos
    • Template Method — pipeline FFT (window → fft → dBFS → notify)


ESTRUTURA DO PROJETO
--------------------
  main.py                      Ponto de entrada do aplicativo
  requirements.txt             Dependências Python
  app/
    models/                    Camada de dados (AudioModel, FFTModel, WaveformModel)
    views/                     Camada de interface (widgets, tema, splash)
    controllers/               Camada de controle (lógica de negócio)
    ui/                        Arquivos .ui editáveis no Qt Designer
    resources/
      themes/                  Folhas de estilo QSS (dark.qss, light.qss)
      icons/                   Ícones SVG e PNG
      splash/                  Imagem da splash screen
    utils/                     Utilitários (loader de áudio, FFT, cores da marca)
  tests/                       Testes automatizados


DEPENDÊNCIAS
------------
  PySide6        Interface gráfica Qt
  pyqtgraph      Gráficos interativos de alta performance
  av (PyAV)      Decodificação de .m4a (ffmpeg embutido)
  soundfile      Decodificação de .wav
  numpy          Computação numérica
  scipy          FFT multithreaded e funções de janelamento


REPOSITÓRIO
-----------
  https://github.com/zblast5000/sound-analyzer


================================================================================
