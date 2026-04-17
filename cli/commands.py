import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
from typing import Optional
import subprocess
import json
import re
from cli.app_info import APP_DESCRIPTION, APP_NAME, VERSION

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
    since: Optional[str] = typer.Option(
        None,
        "--since",
        "-s",
        help="Fecha de inicio en formato YYYY-MM-DD (ej: 2025-02-01)",
    ),
    until: Optional[str] = typer.Option(
        None,
        "--until",
        "-u",
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
    root = Path(__file__).parent.parent

    console.print("[bold]🔍 Filtros aplicados:[/bold]")
    console.print(f"  - Rama:   [green]{branch or 'Actual'}[/green]")
    console.print(f"  - Autor:  [green]{author or 'Cualquiera'}[/green]")
    console.print(f"  - Desde:  [green]{since or f'últimos {days} días'}[/green]")
    console.print(f"  - Hasta:  [green]{until or 'hoy'}[/green]")
    console.print(f"  - Dir:    [green]{target_dir}[/green]\n")

    try:
        git_cmd = [
            "git",
            "log",
            "--pretty=format:%H%x00%an%x00%ad%x00%s%x01",
            "--date=iso",
        ]
        if branch:
            git_cmd.append(branch)
        if author:
            git_cmd += [f"--author={author}"]
        if since:
            git_cmd += [f"--since={since}"]
        if until:
            git_cmd += [f"--until={until}"]
        if not since and not until:
            git_cmd += [f"--since={days} days ago"]

        # console.print(f"[dim]🛠  git cmd: {' '.join(git_cmd)}[/dim]\n")
        with Progress(
            SpinnerColumn(style="cyan"),
            TextColumn("[bold cyan]Obteniendo commits desde Git...[/bold cyan]"),
            transient=True,
            console=console,
        ) as progress:
            progress.add_task("git", total=None)
            result = subprocess.run(
                git_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                cwd=str(target_dir),
            )

        lines = result.stdout.strip()
        if not lines:
            console.print(
                "[yellow]⚠️  No se encontraron commits con los filtros aplicados.[/yellow]"
            )
            return

        # Parseo seguro: separadores nulos en lugar de JSON crudo
        records = [r for r in lines.split("\x01") if r.strip()]
        data = []
        for record in records:
            parts = record.strip().split("\x00")
            if len(parts) == 4:
                data.append(
                    {
                        "hash": parts[0].strip(),
                        "author": parts[1].strip(),
                        "date": parts[2].strip(),
                        "message": parts[3].strip(),
                    }
                )

        if not data:
            console.print(
                "[yellow]⚠️  No se encontraron commits válidos tras parsear.[/yellow]"
            )
            return

        output_path = root / "commits.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        console.print(
            f"[bold green]✅ {len(data)} commits guardados en:[/bold green] [cyan]{output_path}[/cyan]"
        )
        from service.ai_service import AIReportService
        from utils.date_util import  resolve_period
        from config.prompt_config import ReportConfig
        from utils.git_util import get_project_name

        service = AIReportService()
        project_name = get_project_name(target_dir)

        month, year = resolve_period(since=since, until=until, days=days)
        with Progress(
            SpinnerColumn(style="magenta"),
            TextColumn("[bold magenta][Kepler]: Generando análisis con IA...[/bold magenta]"),
            transient=True,
            console=console,
        ) as progress:
            progress.add_task("ai", total=None)
            report_data = service.generate_report(
                commits=data,
                company_name=ReportConfig.COMPANY_NAME,
                employee_name= author or ReportConfig.EMPLOYEE_NAME,
                month=month,
                year=year,
                project_name=project_name or ReportConfig.PROJECT_NAME,
            )

        if isinstance(report_data, str):   
            clean = re.sub(r"```json|```", "", report_data).strip() 
            report_data = json.loads(clean)
        md_path = root / f"reporte_{month}_{year}.docx"
        # from utils.write_markdown import _write_markdown
        from service.word_service import WordService
        with Progress(
            SpinnerColumn(style="green"),
            TextColumn("[bold green]Construyendo documento markdown...[/bold green]"),
            transient=True,
            console=console,
        ) as progress:
            # progress.add_task("markdown", total=None)
            # _write_markdown(report_data, md_path
            WordService(report_data).build().save(str(md_path))
        console.print(
            f"[bold green]✅ Reporte generado en:[/bold green] [cyan]{md_path}[/cyan]"
        )

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Error ejecutando git:[/bold red]\n{e.stderr}")
    except json.JSONDecodeError as e:
        console.print(f"[bold red]❌ Error parseando commits:[/bold red]\n{e}")
    except RuntimeError as e:
        console.print(f"[bold red]❌ Error generando el reporte con IA:[/bold red]\n{e}")
    


@app.command("config")
def show_config():
    """
    Muestra la configuración actual de la herramienta.
    """
    from config.config import Config

    console.print("\n[bold cyan]⚙️  Configuración actual:[/bold cyan]")
    console.print(
        f"  🔑 API Key configurada: {'✅ Sí' if Config.has_api_key() else '❌ No'}"
    )
    console.print(f"  📝 Modelo IA: {Config.get_model_name()}\n")


@app.command("version")
def show_version():
    """
    Muestra la versión de la herramienta.
    """
    console.print(f"\n[bold cyan]{APP_NAME}[/bold cyan] v{VERSION}")
    console.print(f"{APP_DESCRIPTION}\n")


@app.command("help")
def show_help(
    command: Optional[str] = typer.Argument(
        None,
        help="Comando específico para mostrar su ayuda (ej: 'generate')",
    )
):
    """
    Muestra ayuda detallada de un comando específico.
    """
    if command:
        print(f"\n[bold cyan]Ayuda para comando: {command}[/bold cyan]\n")
        print(
            "Primero deberias navegar por los directorios y generar el reporte. Puedes usar comandos de terminal"
        )
        print(
            "[bold] generate [/bold] - Este generará el reporte de commits y a su vez generará un archivo"
        )
        print(
            "[bold] config [/bold] - Este comando muestra la configuración actual del CLI, incluyendo si la API Key está configurada y el modelo de IA en uso."
        )
        print(
            "[bold] version [/bold] - Este comando muestra la versión actual de la herramienta."
        )
        print(
            "[bold] help [/bold] - Este comando muestra ayuda detallada de un comando específico. Puedes usarlo para obtener información sobre cómo usar otros comandos, por ejemplo: 'kepler help generate' para obtener ayuda sobre el comando generate."
        )


if __name__ == "__main__":
    app()
