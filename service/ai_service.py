import json
import time
from pathlib import Path
from typing import Dict, List, Optional

from google import genai
from google.genai import errors, types
from datetime import datetime
from config.config import Config


class AIReportService:
    """Servicio para generar reportes mensuales usando Gemini."""

    PROMPT_PATH = Path("prompts/generate_summary.md")
    MAX_RETRIES = 5
    INITIAL_BACKOFF_SECONDS = 2

    def __init__(self):
        self.client = genai.Client(api_key=Config.get_api_key())
        self.model_name = Config.get_model_name()

    def generate_report(
        self,
        commits: List[Dict],
        company_name: str = "Empresa",
        employee_name: str = "Colaborador",
        month: Optional[int] = None,
        year: Optional[int] = None,
        project_name: Optional[str] = None,
    ) -> Dict:
        month = month or datetime.now().month
        year = year or datetime.now().year

        from utils.date_util import _format_period

        period_month   = _format_period(month, year)
        commits_data   = self._format_commits(commits)
        work_days      = self._count_work_days(commits)
        files_modified = self._count_files(commits)

        prompt = self._load_prompt(
            company_name   = company_name,
            employee_name  = employee_name,
            period_month   = period_month,
            commits_data   = commits_data,
            total_commits  = len(commits),
            work_days      = work_days,
            files_modified = files_modified,
            project_name   = project_name,
        )

        response = self._generate_with_retry(prompt)
        return self._parse_response(response.text)

    def _generate_with_retry(self, prompt: str):
        last_error = None

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                return self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.3,
                    ),
                )
            except errors.ServerError as exc:
                last_error = exc
                if attempt == self.MAX_RETRIES:
                    break
                backoff = self.INITIAL_BACKOFF_SECONDS * (2 ** (attempt - 1))
                time.sleep(backoff)

        raise RuntimeError(
            "Gemini esta temporalmente saturado y no pudo generar el reporte "
            f"despues de {self.MAX_RETRIES} intentos. Intenta nuevamente en unos minutos."
        ) from last_error

    def _load_prompt(self, **kwargs) -> str:
        if not self.PROMPT_PATH.exists():
            raise FileNotFoundError(f"No se encontró el prompt en: {self.PROMPT_PATH}")
        template = self.PROMPT_PATH.read_text(encoding="utf-8")
    
        for key, value in kwargs.items():
            template = template.replace("{" + key + "}", str(value))

        return template

    def _format_commits(self, commits: List[Dict]) -> str:
        if not commits:
            return "No se encontraron commits en el período."
        lines = []
        for commit in commits:
            date      = commit.get("date", "")[:10]
            author    = commit.get("author", "")
            message   = commit.get("message", "").split("\n")[0]
            files     = commit.get("files", [])
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
        clean = raw.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        clean = clean.strip().rstrip("```").strip()
        return json.loads(clean)
