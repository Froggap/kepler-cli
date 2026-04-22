import json
import os
from pathlib import Path

import keyring
from keyring.errors import KeyringError
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "kepler-cli"
CONFIG_DIR = Path.home() / ".kepler"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS = {
    "model": "gemini-2.5-flash",
    "output_path": str(Path.home() / "Documents"),
}


class Config:
    API_KEY_USERNAME = "gemini_api_key"

    @classmethod
    def _ensure_config_file(cls) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if not CONFIG_FILE.exists():
            CONFIG_FILE.write_text(
                json.dumps(DEFAULTS, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    @classmethod
    def _read(cls) -> dict:
        cls._ensure_config_file()
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))

    @classmethod
    def _write(cls, data: dict) -> None:
        cls._ensure_config_file()
        CONFIG_FILE.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @classmethod
    def _get_keyring_api_key(cls) -> str | None:
        try:
            return keyring.get_password(APP_NAME, cls.API_KEY_USERNAME)
        except KeyringError:
            return None

    @classmethod
    def get_api_key_source(cls) -> str | None:
        if cls._get_keyring_api_key():
            return "system"
        if os.getenv("GEMINI_API_KEY"):
            return "env"
        return None

    @classmethod
    def get_api_key(cls) -> str:
        key = cls._get_keyring_api_key() or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError(
                "GEMINI_API_KEY no configurada. Ejecuta: kepler config --set-key "
                "o define GEMINI_API_KEY en tu .env"
            )
        return key

    @classmethod
    def set_api_key(cls, key: str) -> None:
        normalized_key = key.strip()
        if not normalized_key:
            raise ValueError("La API key no puede estar vacia.")

        cls._ensure_config_file()
        try:
            keyring.set_password(APP_NAME, cls.API_KEY_USERNAME, normalized_key)
        except KeyringError as exc:
            raise RuntimeError(
                "No se pudo guardar la API key en el almacenamiento seguro del sistema."
            ) from exc

    @classmethod
    def delete_api_key(cls) -> None:
        try:
            keyring.delete_password(APP_NAME, cls.API_KEY_USERNAME)
        except KeyringError:
            return

    @classmethod
    def has_api_key(cls) -> bool:
        return bool(cls._get_keyring_api_key() or os.getenv("GEMINI_API_KEY"))

    @classmethod
    def get_model_name(cls) -> str:
        return cls._read().get("model") or os.getenv(
            "GEMINI_MODEL", DEFAULTS["model"]
        )

    @classmethod
    def set_model(cls, model: str) -> None:
        data = cls._read()
        data["model"] = model
        cls._write(data)

    @classmethod
    def get_output_path(cls) -> Path:
        return Path(cls._read().get("output_path", DEFAULTS["output_path"]))

    @classmethod
    def set_output_path(cls, path: str) -> None:
        resolved = Path(path).expanduser().resolve()
        data = cls._read()
        data["output_path"] = str(resolved)
        cls._write(data)

    @classmethod
    def get_commits_cache_path(cls) -> Path:
        cls._ensure_config_file()
        return CONFIG_DIR / "commits.json"

    @classmethod
    def all(cls) -> dict:
        data = cls._read()
        data["has_api_key"] = cls.has_api_key()
        data["api_key_source"] = cls.get_api_key_source()
        data["commits_cache_path"] = str(cls.get_commits_cache_path())
        return data
