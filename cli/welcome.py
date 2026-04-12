from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box
import subprocess
from pathlib import Path
from prompt_toolkit import PromptSession
import sys

console = Console()
permissions_granted = False
current_directory = Path.home()
ALLOWED_COMMANDS = {"dir", "ls", "cd", "tree", "type", "echo", "cls", "clear", "pwd"}


def _format_prompt_path(path: Path) -> str:
    """Formatea la ruta para mostrarla de forma compacta en el prompt."""
    try:
        home = Path.home().resolve()
        resolved = path.resolve()
        relative = resolved.relative_to(home)
        return "~" if str(relative) == "." else f"~\\{relative}"
    except ValueError:
        return str(path)


def _build_cli_prompt() -> str:
    """Construye el prompt interactivo del CLI."""
    return f"[Kepler] {_format_prompt_path(current_directory)} $ "


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
        "generate",
    )
    table.add_row("config", "Muestra la configuración actual del CLI", "config")
    table.add_row("version", "Muestra la versión de la herramienta", "version")
    table.add_row(
        "help", "Muestra ayuda detallada de un comando", "help"
    )

    console.print(table)


def show_cli_help():
    """Muestra ayuda general desde el menu interactivo."""
    cli_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    cli_table.add_column("Comando", style="bold green", width=12)
    cli_table.add_column("Descripción", style="white")

    cli_table.add_row(
        "generate",
        "Genera el reporte mensual en Word.\n"
        "[dim]Opciones:[/dim]\n"
        "  [yellow]--branch, -b[/yellow]   Rama específica a analizar\n"
        "  [yellow]--days, -d[/yellow]     Días hacia atrás a analizar [dim](default: 7)[/dim]\n"
        "  [yellow]--author, -a[/yellow]   Filtrar commits por autor\n"
        "  [yellow]--since, -s[/yellow]    Fecha inicio [dim](YYYY-MM-DD)[/dim]\n"
        "  [yellow]--until, -u[/yellow]    Fecha fin [dim](YYYY-MM-DD)[/dim]\n"
        "  [yellow]--detailed[/yellow]     Incluir análisis detallado con IA (Más adelante)\n"
        "  [yellow]--remote[/yellow]       Obtener commits desde remoto (Más adelante)"
    )
    cli_table.add_row("config",   "Muestra la configuración actual.")
    cli_table.add_row("version",  "Muestra la versión de la herramienta.")
    cli_table.add_row("help",     "Muestra esta ayuda.")
    cli_table.add_row("exit",     "Sale del CLI.")

    sys_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    sys_table.add_column("Comando", style="bold yellow", width=12)
    sys_table.add_column("Descripción", style="white")

    sys_table.add_row("cd <ruta>", "Navega a una carpeta.")
    sys_table.add_row("dir / ls",  "Lista archivos del directorio actual.")
    sys_table.add_row("tree",      "Muestra árbol de carpetas.")
    sys_table.add_row("pwd",       "Muestra la ruta actual.")
    sys_table.add_row("cls / clear","Limpia la pantalla.")

    console.print()
    console.print(Panel(
        cli_table,
        title="[bold cyan]⚡ Comandos Kepler[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print(Panel(
        sys_table,
        title="[bold yellow]🖥️  Comandos del sistema[/bold yellow]",
        border_style="yellow",
        padding=(1, 2),
    ))
    console.print(
        "[dim]  💡 Tip: Usa Ctrl+C dos veces para salir en cualquier momento.[/dim]\n"
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
        sys.exit(0)
        
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
      parts=cmd.split()
      extra_args = parts[1:]
      handle_menu_choice(base_cmd, extra_args)
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
    if base_cmd in ("cls", "clear"):
        console.clear()
        return
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


def handle_menu_choice(choice: str, extra_args: list = []):
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
            args=["generate", "--working-dir", str(current_directory)] + extra_args,
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

    _ctrl_c_count = 0
    while True:
        console.print()

        from config.config import Config

        if not Config.has_api_key():
            console.print(
                "[bold red]⚠️  API Key no configurada. Por favor, configura tu API Key para usar la herramienta.[/bold red]"
            )
            try:
                command = Prompt.ask(
                "¿Quieres configurar tu API Key ahora?",
                choices=["config", "version", "help", "generate"],
                default="config",)
            except KeyboardInterrupt:
                console.print("\n[dim]Usa 'exit' o cierra la terminal para salir.[/dim]")
                continue

        else:
            session = PromptSession()
            try:
                command = session.prompt(_build_cli_prompt())
                _ctrl_c_count = 0
            except KeyboardInterrupt:
                _ctrl_c_count += 1
                if _ctrl_c_count >= 2:
                    console.print("\n[bold cyan]👋 ¡Hasta luego![/bold cyan]")
                    break
                console.print("\n[dim]Presiona Ctrl+C de nuevo para salir.[/dim]")
                continue
            except EOFError:
                console.print("\n[bold cyan]👋 ¡Hasta luego![/bold cyan]")
                break
        if command.strip().lower() in ("exit", "quit", "q"):
            console.print("\n[bold cyan]👋 ¡Hasta luego![/bold cyan]")
            break
        execute_terminal_command(command)
        console.print()


if __name__ == "__main__":
    show_welcome_menu()
