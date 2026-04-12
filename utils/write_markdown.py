from pathlib import Path


def _write_markdown(data: dict, path: Path):
    """Convierte el JSON de Gemini a un archivo .md."""
    enc = data.get("encabezado", {})
    actividades = data.get("actividades", [])
    resultados  = data.get("resultados_valor", [])
    resumen     = data.get("resumen_ejecutivo", [])

    if isinstance(resumen, list):
        resumen_text = "\n\n".join(resumen)
    else:
        resumen_text = resumen

    lines = [
        "# Reporte Mensual de Actividades",
        "",
        f"**Empresa:** {enc.get('empresa', '')}  ",
        f"**Colaborador:** {enc.get('colaborador', '')}  ",
        f"**Período:** {enc.get('periodo', '')}  ",
        f"**Proyecto:** {enc.get('proyecto', '')}  ",
        "",
        "---",
        "",
        "## Resumen Ejecutivo",
        "",
        resumen_text,   
        "",
        "---",
        "",
        "## Actividades Realizadas",
        "",
    ]

    for actividad in actividades:
        lines.append(f"### {actividad.get('categoria', '')}")
        lines.append("")
        for item in actividad.get("items", []):
            lines.append(f"- {item}")
        lines.append("")

    lines += [
        "---",
        "",
        "## Resultados y Valor Aportado",
        "",
    ]
    for resultado in resultados:
        lines.append(f"- {resultado}")

    path.write_text("\n".join(lines), encoding="utf-8")