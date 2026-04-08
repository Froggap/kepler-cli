from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box
import subprocess
from pathlib import Path

console = Console()
permissions_granted = False
current_directory = Path.home()
ALLOWED_COMMANDS = {"dir", "ls", "cd", "tree", "type", "echo", "cls", "clear", "pwd"}


def show_banner():
    """Muestra el banner de bienvenida."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ██╗  ██╗███████╗██████╗ ██╗     ███████╗██████╗        ║
    ║   ██║ ██╔╝██╔════╝██╔══██╗██║     ██╔════╝██╔══██╗       ║
    ║   █████╔╝ █████╗  ██████╔╝██║     █████╗  ██████╔╝       ║
    ║   ██╔═██╗ ██╔══╝  ██╔═══╝ ██║     ██╔══╝  ██╔══██╗       ║
    ║   ██║  ██╗███████╗██║     ███████╗███████╗██║  ██║       ║
    ║   ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝       ║
    ║                                                           ║
    ║          Generador de Reportes Mensuales con IA          ║
    ║                      v1.0.0                               ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")
    console.print(
        "\n[dim]Transform your Git commits into professional monthly reports[/dim]\n"
    )


def show_commands_table():
    """Muestra tabla de comandos disponibles."""
    table = Table(
        title="📋 Comandos Disponibles",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        title_style="bold cyan",
    )

    table.add_column("Comando", style="green", width=15)
    table.add_column("Descripción", style="white", width=50)
    table.add_column("Ejemplo", style="yellow", width=35)

    table.add_row(
        "generate",
        "Genera un reporte mensual de actividades en Word",
        "kepler generate",
    )
    table.add_row("config", "Muestra la configuración actual del CLI", "kepler config")
    table.add_row("version", "Muestra la versión de la herramienta", "kepler version")
    table.add_row(
        "help", "Muestra ayuda detallada de un comando", "kepler generate --help"
    )

    console.print(table)


def show_cli_help():
    """Muestra ayuda general desde el menu interactivo."""
    console.print("\n[bold cyan]Ayuda de Kepler[/bold cyan]\n")
    console.print(
        "Puedes ejecutar los comandos del CLI o algunos comandos seguros del sistema "
        "desde este menu interactivo.\n"
    )
    console.print("[bold]generate[/bold] - Genera el reporte mensual.")
    console.print("[bold]config[/bold] - Muestra la configuracion actual.")
    console.print("[bold]version[/bold] - Muestra la version de la herramienta.")
    console.print(
        "[bold]help[/bold] - Muestra esta ayuda general del menu de bienvenida."
    )
    console.print(
        "\n[dim]Comandos de sistema permitidos:[/dim] "
        + ", ".join(sorted(ALLOWED_COMMANDS))
    )


def request_permissions():
    """Solicita permisos al usuario para ejecutar comandos del sistema."""
    global permissions_granted

    if permissions_granted:
        return True
    console.print()
    console.print(
        Panel.fit(
            "[bold yellow]⚠️  Permiso de acceso al sistema[/bold yellow]\n\n"
            "Esta herramienta necesita ejecutar comandos en tu PC para:\n\n"
            "  [cyan]•[/cyan] Listar carpetas y archivos  ([green]dir[/green], [green]ls[/green], [green]tree[/green])\n"
            "  [cyan]•[/cyan] Navegar entre directorios   ([green]cd[/green])\n"
            "  [cyan]•[/cyan] Ver contenido de archivos   ([green]type[/green])\n\n"
            "[dim]Solo se ejecutarán comandos de lectura. No se modificará ningún archivo.[/dim]",
            border_style="yellow",
            title="🔒 Permisos requeridos",
        )
    )
    console.print()
    response = Prompt.ask(
        "[bold] ¿Deseas permitir el acceso a tu sistema de archivos? [/bold]",
        choices=["yes", "no"],
        default="no",
    )

    if response == "yes":
        permissions_granted = True
        console.print(
            "[bold green]✅ Permisos concedidos. Ya puedes navegar tu sistema.[/bold green]"
        )
    else:
        console.print(
            "[bold red]❌ Permisos denegados. No podrás usar las funciones de navegación.[/bold red]"
        )
    console.print()
    return response


def is_safe_command(cmd: str) -> bool:
    """Verifica si un comando es seguro de ejecutar."""
    base = cmd.strip().split()[0].lower().rstrip(".exe")
    return base in ALLOWED_COMMANDS


def execute_terminal_command(cmd: str):
    """Ejecuta un comando del sistema de forma segura."""
    global current_directory
    cmd = cmd.strip()
    if not cmd:
        return

    parts = cmd.split(maxsplit=1)
    base_cmd = parts[0].lower()
    if base_cmd in ["config", "version", "help", "generate"]:
      handle_menu_choice(base_cmd)
      return

    if base_cmd == "cd":
        if len(parts) < 2 or parts[1].strip() in ("~", ""):
            current_directory = Path.home()
            console.print(f"[cyan]📂 {current_directory}[/cyan]")
            return

        destino = parts[1].strip().strip('"')

        if destino == "..":
            new = current_directory.parent
        elif Path(destino).is_absolute():
            new = Path(destino)
        else:
            new = current_directory / destino

        new = new.resolve()

        if not new.exists():
            console.print(f"[bold red]❌ La ruta no existe:[/bold red] {new}")
        elif not new.is_dir():
            console.print(f"[bold red]❌ No es una carpeta:[/bold red] {new}")
        else:
            current_directory = new
            console.print(f"[cyan]📂 {current_directory}[/cyan]")
            result = subprocess.run(
                "dir",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(current_directory),
            )
            output = result.stdout.decode("latin-1", errors="replace")
            console.print(f"[dim]{output}[/dim]")
        return

    if base_cmd in ("pwd", "cd"):
        console.print(f"[cyan]📂 {current_directory}[/cyan]")
        return
    if not request_permissions():
        console.print("[yellow]Comando cancelado. Sin permisos del sistema.[/yellow]")
        return
    if not is_safe_command(cmd):
        console.print(
            f"[bold red]⛔ Comando no permitido:[/bold red] [yellow]{base_cmd}[/yellow]\n"
            f"[dim]Comandos disponibles: {', '.join(sorted(ALLOWED_COMMANDS))}[/dim]"
        )
        return
    if base_cmd == "ls":
        command = "dir " + (parts[1] if len(parts) > 1 else "")
    if base_cmd == "clear":
        command = "cls"
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(current_directory),
        )
        salida = result.stdout.decode("latin-1", errors="replace")
        console.print(f"[dim]{salida}[/dim]")

    except subprocess.CalledProcessError as e:
        error = e.stderr.decode("latin-1", errors="replace")
        console.print(f"[bold red]❌ Error:[/bold red]\n{error}")


def handle_menu_choice(choice: str):
    """Maneja la elección del usuario."""
    from cli.commands import app
    

    console.print(f"\n[bold cyan]Ejecutando comando: {choice}[/bold cyan]\n")

    if choice == "config":
        app(prog_name="kepler", args=["config"], standalone_mode=False)
    elif choice == "version":
        app(prog_name="kepler", args=["version"], standalone_mode=False)
    elif choice == "help":
        show_cli_help()
    elif choice == "generate":
        app(
            prog_name="kepler",
            args=["generate", "--working-dir", str(current_directory)],
            standalone_mode=False,
        )


def show_welcome_menu():
    """Muestra el menú de bienvenida completo."""
    console.clear()

    # Banner
    show_banner()

    # Tabla de comandos
    show_commands_table()
    console.print()

    console.print()

    # Menú interactivo
    while True:
        console.print()

        from utils.config import Config

        if not Config.has_api_key():
            console.print(
                "[bold red]⚠️  API Key no configurada. Por favor, configura tu API Key para usar la herramienta.[/bold red]"
            )
            command = Prompt.ask(
                "¿Quieres configurar tu API Key ahora?",
                choices=["config", "version", "help", "generate"],
                default="config",
            )
        else:
            session = PromptSession()
            command = session.prompt(f"[{current_directory}] $ ")

        execute_terminal_command(command)
        console.print()


if __name__ == "__main__":
    show_welcome_menu()
