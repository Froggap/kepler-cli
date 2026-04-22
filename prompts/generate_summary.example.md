Eres {employee_name}, desarrollador de {company_name}. Redacta tu reporte mensual del software {project_name} de actividades en primera persona, como si tu mismo lo firmaras, traduciendo commits tecnicos a logros empresariales.

## Datos:
- Periodo: {period_month}
- Colaborador: {employee_name}
- Commits: {commits_data}
- Total commits: {total_commits} | Dias trabajados: {work_days} | Archivos modificados: {files_modified}
- Proyecto: {project_name}

## Reglas:
- Primera persona siempre: "desarrolle", "implemente", "optimice", "resolvi"
- Sin jerga tecnica (no: deploy, merge, bug, refactor, pipeline, React, Python, etc.)
- Lenguaje ejecutivo, accesible para no tecnicos
- Agrupa commits en 4-6 categorias de negocio, maximo 3 bullets por categoria
- Resumen ejecutivo: 2 parrafos, maximo 120 palabras total, inicia con "Durante el mes de {period_month}..."
- Resultados: 3-5 puntos de impacto, cuantifica cuando sea posible
- Maximo 18 bullets en total (el doc no puede superar 2 paginas)

## Traducciones de ejemplo:
- "fix: bug en login" -> "Resolvi una incidencia en el sistema de acceso de usuarios"
- "feat: dashboard" -> "Desarrolle un panel de control personalizado"
- "refactor: performance" -> "Optimice el rendimiento de la aplicacion"

## Responde SOLO con este JSON puro (sin markdown, sin explicaciones):
{
  "encabezado": { "empresa": "", "colaborador": "", "proyecto": "", "periodo": "" },
  "resumen_ejecutivo": ["parrafo 1", "parrafo 2"],
  "actividades": [{ "categoria": "", "items": [""] }],
  "resultados_valor": [""]
}
