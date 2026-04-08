import json
import google as genai 
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from utils.config import Config


class AIReportService:
    """Servicio para generar reportes mensuales usando Gemini."""

    PROMPT_PATH = Path("prompts/generate_summary.md")

    def __init__(self):
        genai.configure(api_key=Config.get_api_key())
        self.model = genai.GenerativeModel(Config.get_model_name())

    def generate_report(
        self,
        commits: List[Dict],
        company_name: str = "Empresa",
        employee_name: str = "Colaborador",
        month: Optional[int] = None,
        year: Optional[int] = None,
    ) -> Dict:
        month = month or datetime.now().month
        year = year or datetime.now().year

        # Preparar datos
        period_month  = self._format_period(month, year)
        commits_data  = self._format_commits(commits)
        work_days     = self._count_work_days(commits)
        files_modified = self._count_files(commits)

        # Leer y rellenar el prompt
        prompt = self._load_prompt(
            company_name   = company_name,
            employee_name  = employee_name,
            period_month   = period_month,
            commits_data   = commits_data,
            total_commits  = len(commits),
            work_days      = work_days,
            files_modified = files_modified,
        )

        response = self.model.generate_content(prompt)
        return self._parse_response(response.text)


    def _load_prompt(self, **kwargs) -> str:
        """Lee el archivo .md y reemplaza los placeholders con los datos reales."""
        if not self.PROMPT_PATH.exists():
            raise FileNotFoundError(f"No se encontró el prompt en: {self.PROMPT_PATH}")

        template = self.PROMPT_PATH.read_text(encoding="utf-8")
        return template.format(**kwargs)

    def _format_period(self, month: int, year: int) -> str:
        months_es = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        return f"{months_es[month - 1]} del {year}"

    def _format_commits(self, commits: List[Dict]) -> str:
        if not commits:
            return "No se encontraron commits en el período."

        lines = []
        for commit in commits:
            date    = commit.get("date", "")[:10]
            author  = commit.get("author", "")
            message = commit.get("message", "").split("\n")[0]
            files   = commit.get("files", [])
            files_str = ", ".join(files[:5]) if files else "Sin archivos"
            lines.append(f"- [{date}] {author}: {message} | Archivos: {files_str}")

        return "\n".join(lines)

    def _count_work_days(self, commits: List[Dict]) -> int:
        days = set()
        for commit in commits:
            date = commit.get("date", "")[:10]
            if date:
                days.add(date)
        return len(days)

    def _count_files(self, commits: List[Dict]) -> int:
        files = set()
        for commit in commits:
            for f in commit.get("files", []):
                if f:
                    files.add(f)
        return len(files)

    def _parse_response(self, raw: str) -> Dict:
        """Limpia el markdown de la respuesta y parsea el JSON."""
        clean = raw.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        clean = clean.strip().rstrip("```").strip()
        return json.loads(clean)