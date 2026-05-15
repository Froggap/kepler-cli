import shutil
from pathlib import Path
from config.config_impl import Config, CONFIG_DIR

def _remove_file(path: Path) -> None:
    try:
        if path.exists():
            path.unlink()
    except Exception:
        pass


def _remove_dir(path: Path) -> None:
    try:
        if path.exists():
            shutil.rmtree(path)
    except Exception:
        pass



def handle_uninstall() -> None:
    try:
        Config.delete_api_key()
        _remove_file(Config.get_commits_cache_path())
        _remove_dir(CONFIG_DIR)
    except Exception:
        pass

