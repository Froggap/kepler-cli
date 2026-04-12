import sys
from cli.commands import app
from cli.welcome import show_welcome_menu

if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            show_welcome_menu()
        else:
            app()
    except KeyboardInterrupt:
        print("\n [Kepler]👋 ¡Hasta luego!")