import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
from typing import Optional
import subprocess
import json


app = typer.Typer(
    name="cli-kepler",
    help="A CLI tool for managing Kepler projects.",
    add_completion=False,
)

console = Console()

@app.command("generate")
def generate_content(
 
    branch: Optional[str] = typer.Option(
        None,
        "--branch",
        "-b",
        help="Rama específica a analizar (por defecto: rama actual)",
    ),
    days: Optional[int] = typer.Option(
        7,
        "--days",
        "-d",
        help="Número de días hacia atrás para analizar commits",
        min=1,
    ),
    author: Optional[str] = typer.Option(
        None,
        "--author",
        "-a",
        help="Filtrar commits por autor",
    ),
    detailed: bool = typer.Option(
        False,
        "--detailed",
        help="Incluir análisis detallado con IA",
    ),
    from_remote: bool = typer.Option(
        False,
        "--remote",
        help="Obtener commits desde repositorio remoto",
    ),
    since:Optional[str] = typer.Option(
        None,
        "--since", "-s",
        help="Fecha de inicio en formato YYYY-MM-DD (ej: 2025-02-01)",
    ),
    until:Optional[str] = typer.Option(
        None,
        "--until", "-u",
        help="Fecha de fin en formato YYYY-MM-DD (ej: 2025-02-28)",
    ),
    working_dir: Optional[Path] = typer.Option(
        None,
        "--working-dir",
        help="Directorio desde donde ejecutar los comandos git.",
        hidden=True,
    ),
):
    "Genera un reporte de commits."
    console.print(f"\n[bold cyan]Generando reporte de commits...[/bold cyan]\n")
    target_dir = working_dir or Path.cwd()

    try:
        result = subprocess.run(
            [
                "git",
                "log",
                '--pretty=format:{"hash":"%H","author":"%an","date":"%ad","message":"%s"},',
                "--date=iso",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            cwd=str(target_dir),
        )

        lines = result.stdout.strip()
        if lines.endswith(","):
            lines = lines[:-1]
            json_text = f"[{lines}]"
            data = json.loads(json_text)
        with open("commits.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error:[/bold red]\n{e.stderr}")

@app.command("config")
def show_config():
    """
    Muestra la configuración actual de la herramienta.
    """
    from utils.config import Config
    
    console.print("\n[bold cyan]⚙️  Configuración actual:[/bold cyan]")
    console.print(f"  🔑 API Key configurada: {'✅ Sí' if Config.has_api_key() else '❌ No'}")
    console.print(f"  📝 Modelo IA: {Config.get_model_name()}\n")


@app.command("version")
def show_version():
    """
    Muestra la versión de la herramienta.
    """
    console.print("\n[bold cyan]git-report-cli[/bold cyan] v1.0.0")
    console.print("Generador de reportes Git con IA\n")

@app.command("help")
def show_help(command: Optional[str] = typer.Argument(
    None,
    help="Comando específico para mostrar su ayuda (ej: 'generate')",
)):
    """
    Muestra ayuda detallada de un comando específico.
    """
    if command:
        print(f"\n[bold cyan]Ayuda para comando: {command}[/bold cyan]\n")
        print("Primero deberias navegar por los directorios y generar el reporte. Puedes usar comandos de terminal")
        print("[bold] generate [/bold] - Este generará el reporte de commits y a su vez generará un archivo")
        print("[bold] config [/bold] - Este comando muestra la configuración actual del CLI, incluyendo si la API Key está configurada y el modelo de IA en uso.")
        print("[bold] version [/bold] - Este comando muestra la versión actual de la herramienta.")
        print("[bold] help [/bold] - Este comando muestra ayuda detallada de un comando específico. Puedes usarlo para obtener información sobre cómo usar otros comandos, por ejemplo: 'kepler help generate' para obtener ayuda sobre el comando generate.")



if __name__ == "__main__":
    app()    
