
import pandas as pd
from sqlalchemy import create_engine, text
from database import conectar

# Conexão com seu SQL Server
origem = conectar()

# Banco portátil SQLite
destino = create_engine("sqlite:///americaLatinaDB.db")

# Localizar todas as VIEWs do banco
with origem.connect() as conexao:
    views = pd.read_sql(
        text("""
            SELECT TABLE_SCHEMA, TABLE_NAME
            FROM INFORMATION_SCHEMA.VIEWS
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """),
        conexao
    )

# Exportar resultados das VIEWs
for _, view in views.iterrows():
    esquema = view["TABLE_SCHEMA"]
    nome = view["TABLE_NAME"]

    print(f"Exportando: {esquema}.{nome}")

    try:
        consulta = text(
            f"SELECT * FROM [{esquema}].[{nome}]"
        )

        with origem.connect() as conexao:
            dados = pd.read_sql(consulta, conexao)

        dados.to_sql(
            nome,
            destino,
            if_exists="replace",
            index=False
        )

        print(f"OK: {len(dados)} registros")

    except Exception as erro:
        print(f"ERRO em {nome}: {erro}")

print("Exportação finalizada!")
