import os
from dotenv import load_dotenv

load_dotenv()


class Config:    
    @staticmethod
    def get_api_key() -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY no configurada. "
                "Agrégala a tu archivo .env"
            )
        return api_key
    
    @staticmethod
    def has_api_key() -> bool:
        return bool(os.getenv("GEMINI_API_KEY"))
    
    @staticmethod
    def get_model_name() -> str:
        return os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    
    @staticmethod
    def get_github_token() -> str:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError(
                "GITHUB_TOKEN no configurado. "
                "Agrégalo a tu archivo .env"
            )
        return token
    
    @staticmethod
    def has_github_token() -> bool:
        return bool(os.getenv("GITHUB_TOKEN"))