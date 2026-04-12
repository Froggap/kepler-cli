import subprocess
from pathlib import Path

def get_project_name(target_dir:Path)-> str:
    """Obtiene el nombre del proyecto"""
    try:
        result=subprocess.run(
            ["git", "remote", "get-url", "origin"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(target_dir),
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            name = url.rstrip(".git").split("/")[-1]
            return name
    except Exception:
        pass
    return target_dir.name