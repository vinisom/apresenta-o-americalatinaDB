
from sqlalchemy import create_engine
from pathlib import Path

def conectar():
    caminho = Path(__file__).resolve().parent / "americaLatinaDB.db"

    if not caminho.is_file():
        raise FileNotFoundError(
            f"Banco SQLite não encontrado: {caminho}"
        )

    return create_engine(f"sqlite:///{caminho.as_posix()}")
