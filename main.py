import sys

from app.application import Application
from app.views.splash_screen import SplashScreen
from app.views.theme_manager import ThemeManager
from app.views.main_window import MainWindow
from app.controllers.main_controller import MainController


def main() -> None:
    app = Application(sys.argv)

    splash = SplashScreen()
    splash.show()
    app.processEvents()

    splash.show_message("Inicializando tema...")
    app.processEvents()
    theme_mgr = ThemeManager()
    theme_mgr.apply_theme("dark", app)

    splash.show_message("Carregando interface...")
    app.processEvents()
    window = MainWindow()

    splash.show_message("Conectando componentes...")
    app.processEvents()
    MainController(window, app)

    window.show()
    splash.finish(window.qt_window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
