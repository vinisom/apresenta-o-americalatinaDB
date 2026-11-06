
import re
import unicodedata
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from sqlalchemy import text
from database import conectar


# =====================================
# CONEXÃO E LEITURA - SQLITE
# =====================================

@st.cache_resource
def engine():
    return conectar()


@st.cache_data(ttl=600)
def read_view(schema, name):

    if not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", schema):
        raise ValueError("Schema inválido")

    if not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", name):
        raise ValueError("VIEW inválida")

    # SQLite: os resultados das VIEWs foram
    # exportados como tabelas, sem schema.
    sql = text(
        f'SELECT * FROM "{name}" LIMIT 5000'
    )

    return pd.read_sql(sql, engine())


def normalize(value):
    value = unicodedata.normalize(
        "NFKD", str(value)
    ).encode("ascii", "ignore").decode().lower()

    return re.sub(r"[^a-z0-9]+", "_", value).strip("_")


def find_col(df, names):
    mapping = {normalize(c): c for c in df.columns}

    for name in names:
        key = normalize(name)
        if key in mapping:
            return mapping[key]

    return None


# =====================================
# MÉTRICAS
# =====================================

METRICAS = {
    "Gols": ["gols", "goals"],
    "Assistências": ["assistencias", "assists"],
    "Gols + Assistências": [
        "gols_mais_assistencias",
        "gols_assistencias",
        "ga"
    ],
    "xG": ["xg"],
    "xA": ["xa"],
    "Finalizações": ["finalizacoes", "shots"],
    "Passes-chave": ["passes_chave", "key_passes"],
    "Grandes chances criadas": [
        "grandes_chances_criadas"
    ],
    "Desarmes": ["desarmes", "tackles"],
    "Interceptações": ["interceptacoes", "interceptions"],
    "Recuperações": [
        "recuperacoes",
        "recuperacoes_bola"
    ],
    "Cortes": ["cortes", "clearances"],
    "Duelos aéreos ganhos": [
        "duelos_aereos_ganhos"
    ],
    "Defesas": ["defesas", "saves"],
    "Jogos sem sofrer gols": [
        "clean_sheets",
        "jogos_sem_sofrer_gols"
    ],
    "Nota SofaScore": [
        "nota_sofascore",
        "nota"
    ],
    "Valor de mercado (€)": [
        "valor_mercado_eur",
        "market_value_eur"
    ],
    "Gols por 90": [
        "gols_por90",
        "gols_por_90"
    ],
    "Assistências por 90": [
        "assist_por90",
        "assistencias_por90"
    ],
    "Desarmes por 90": [
        "desarmes_por90",
        "desarmes_por_90"
    ]
}


def metricas_disponiveis(df):
    resultado = {}

    for label, nomes in METRICAS.items():
        coluna = find_col(df, nomes)

        if coluna:
            valores = pd.to_numeric(
                df[coluna], errors="coerce"
            )

            if valores.notna().any():
                resultado[label] = coluna

    return resultado


# =====================================
# ESTILO DOS GRÁFICOS
# =====================================

def estilizar(fig, altura=480):
    fig.update_layout(
        template="plotly_dark",
        height=altura,
        margin=dict(l=15, r=20, t=45, b=25),
        font=dict(size=13),
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        hovermode="closest"
    )

    return fig


def grafico_ranking(df, jogador, coluna, titulo):
    dados = df[[jogador, coluna]].copy()

    dados[coluna] = pd.to_numeric(
        dados[coluna], errors="coerce"
    )

    dados = (
        dados.dropna(subset=[coluna])
        .sort_values(coluna, ascending=False)
        .head(15)
        .sort_values(coluna)
    )

    if dados.empty:
        st.info("Sem dados para este gráfico.")
        return

    fig = px.bar(
        dados,
        x=coluna,
        y=jogador,
        orientation="h",
        color=coluna,
        color_continuous_scale="Teal",
        title=titulo,
        text=coluna
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        coloraxis_showscale=False,
        yaxis_title="",
        xaxis_title=titulo
    )

    st.plotly_chart(
        estilizar(fig, 560),
        use_container_width=True
    )


# =====================================
# COMPARAÇÃO ENTRE JOGADORES
# =====================================

def comparar_jogadores(df, jogador, metricas):

    jogadores = sorted(
        df[jogador].dropna().astype(str).unique()
    )

    if len(jogadores) < 2:
        st.info("É necessário ter dois jogadores.")
        return

    selecionados = st.multiselect(
        "Selecione dois jogadores",
        jogadores,
        max_selections=2
    )

    if len(selecionados) != 2:
        st.info("Selecione dois jogadores para comparar.")
        return

    dados = df[
        df[jogador].astype(str).isin(selecionados)
    ].copy()

    metricas_comparacao = {
        k: v for k, v in metricas.items()
        if "mercado" not in k.lower()
    }

    escolhidas = st.multiselect(
        "Métricas da comparação",
        list(metricas_comparacao),
        default=list(metricas_comparacao)[:5],
        max_selections=6
    )

    if not escolhidas:
        return

    # Agregar registros repetidos por jogador
    colunas = [
        metricas_comparacao[m]
        for m in escolhidas
    ]

    for coluna in colunas:
        dados[coluna] = pd.to_numeric(
            dados[coluna], errors="coerce"
        )

    dados = dados.groupby(
        jogador, as_index=False
    )[list(dict.fromkeys(colunas))].mean()

    # Gráfico de barras agrupadas
    fig = go.Figure()

    for nome in selecionados:
        linha = dados[dados[jogador] == nome]

        if linha.empty:
            continue

        valores = [
            linha[metricas_comparacao[m]].iloc[0]
            for m in escolhidas
        ]

        fig.add_trace(go.Bar(
            name=nome,
            x=escolhidas,
            y=valores,
            text=[
                f"{v:.2f}" if pd.notna(v) else ""
                for v in valores
            ]
        ))

    fig.update_layout(
        title="Comparação direta",
        barmode="group",
        xaxis_title="Métricas",
        yaxis_title="Valor"
    )

    st.plotly_chart(
        estilizar(fig),
        use_container_width=True
    )

    st.caption(
        "Compare métricas com a mesma unidade. "
        "Os valores apresentados são médias quando "
        "há registros repetidos do mesmo jogador."
    )

    # Radar normalizado de 0 a 100
    if len(escolhidas) >= 3:
        fig_radar = go.Figure()

        for nome in selecionados:
            linha = dados[dados[jogador] == nome]

            if linha.empty:
                continue

            valores = []

            for metrica in escolhidas:
                coluna = metricas_comparacao[metrica]

                referencia = pd.to_numeric(
                    df[coluna], errors="coerce"
                ).dropna()

                valor = linha[coluna].iloc[0]

                if referencia.empty or pd.isna(valor):
                    valores.append(0)
                else:
                    valores.append(
                        round(
                            100 * (referencia <= valor).mean(),
                            1
                        )
                    )

            fig_radar.add_trace(go.Scatterpolar(
                r=valores + [valores[0]],
                theta=escolhidas + [escolhidas[0]],
                fill="toself",
                name=nome
            ))

        fig_radar.update_layout(
            title="Perfil comparativo (percentis)",
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            )
        )

        st.plotly_chart(
            estilizar(fig_radar, 550),
            use_container_width=True
        )

        st.caption(
            "Percentis calculados dentro da VIEW "
            "selecionada. Valores maiores representam "
            "percentis mais altos, não necessariamente "
            "melhor desempenho em todas as métricas."
        )


# =====================================
# DASHBOARD PRINCIPAL
# =====================================

def run(country, schema, view_names):

    st.set_page_config(
        page_title=f"América Latina DB | {country}",
        page_icon="⚽",
        layout="wide"
    )

    st.title(f"América Latina DB — {country}")

    st.caption(
        "Análise de desempenho, mercado e scouting | 2025"
    )

    # MENU LATERAL
    st.sidebar.title("Navegação")

    views = sorted(view_names)

    view = st.sidebar.selectbox(
        "Selecione a análise",
        views,
        format_func=lambda x: (
            x.replace("vw_", "")
            .replace("_2025_", " | ")
            .replace("_", " ")
            .title()
        )
    )

    st.sidebar.caption(
        f"{len(views)} VIEWs disponíveis"
    )

    try:
        df = read_view(schema, view)

    except Exception as erro:
        st.error(f"Erro ao consultar a VIEW: {erro}")
        st.stop()

    st.subheader(view)

    if df.empty:
        st.warning("A VIEW não retornou registros.")
        st.stop()

    # IDENTIFICAR COLUNAS
    jogador = find_col(
        df, ["nome_jogador", "jogador", "player_name"]
    )

    clube = find_col(
        df, ["nome_clube", "clube", "team_name"]
    )

    posicao = find_col(
        df, ["posicao", "posição", "position"]
    )

    mercado = find_col(
        df, ["valor_mercado_eur", "market_value_eur"]
    )

    minutos = find_col(
        df, ["minutos_jogados", "minutos"]
    )

    metricas = metricas_disponiveis(df)

    # FILTROS
    if clube:
        clubes = st.sidebar.multiselect(
            "Clubes",
            sorted(
                df[clube].dropna().astype(str).unique()
            )
        )

        if clubes:
            df = df[
                df[clube].astype(str).isin(clubes)
            ]

    if posicao:
        posicoes = st.sidebar.multiselect(
            "Posições",
            sorted(
                df[posicao].dropna().astype(str).unique()
            )
        )

        if posicoes:
            df = df[
                df[posicao].astype(str).isin(posicoes)
            ]

    if jogador:
        busca = st.sidebar.text_input(
            "Buscar jogador"
        )

        if busca:
            df = df[
                df[jogador].astype(str).str.contains(
                    busca,
                    case=False,
                    regex=False,
                    na=False
                )
            ]

    # INDICADORES
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Jogadores / Registros",
        len(df)
    )

    c2.metric(
        "Clubes",
        df[clube].nunique() if clube else "-"
    )

    c3.metric(
        "Posições",
        df[posicao].nunique() if posicao else "-"
    )

    if mercado:
        total = pd.to_numeric(
            df[mercado], errors="coerce"
        ).sum()

        c4.metric(
            "Valor de mercado",
            f"€ {total / 1_000_000:,.1f} mi"
        )
    else:
        c4.metric(
            "Métricas",
            len(metricas)
        )

    st.divider()

    abas = st.tabs([
        "Rankings",
        "Comparações",
        "Mercado",
        "Dados completos"
    ])

    # =====================================
    # ABA 1 - RANKINGS
    # =====================================

    with abas[0]:
        st.header("Rankings de desempenho")

        if jogador and metricas:
            metrica = st.selectbox(
                "Escolha a métrica",
                list(metricas),
                key="ranking"
            )

            grafico_ranking(
                df,
                jogador,
                metricas[metrica],
                metrica
            )

            if minutos and "por 90" in metrica.lower():
                st.warning(
                    "Métricas por 90 podem ser distorcidas "
                    "quando o jogador possui poucos minutos."
                )
        else:
            st.info(
                "Esta VIEW não possui colunas suficientes "
                "para gerar rankings."
            )

    # =====================================
    # ABA 2 - COMPARAÇÕES
    # =====================================

    with abas[1]:
        st.header("Comparação de jogadores")

        if jogador and metricas:
            comparar_jogadores(
                df, jogador, metricas
            )
        else:
            st.info(
                "Comparação indisponível para esta VIEW."
            )

    # =====================================
    # ABA 3 - MERCADO
    # =====================================

    with abas[2]:
        st.header("Análise de mercado")

        if jogador and mercado:
            grafico_ranking(
                df,
                jogador,
                mercado,
                "Valor de mercado (€)"
            )

            outras = {
                k: v for k, v in metricas.items()
                if "mercado" not in k.lower()
            }

            if outras:
                metrica = st.selectbox(
                    "Comparar valor de mercado com",
                    list(outras),
                    key="mercado"
                )

                coluna = outras[metrica]

                dados = df[
                    [jogador, mercado, coluna]
                ].copy()

                dados[mercado] = pd.to_numeric(
                    dados[mercado], errors="coerce"
                )

                dados[coluna] = pd.to_numeric(
                    dados[coluna], errors="coerce"
                )

                dados = dados.dropna(
                    subset=[mercado, coluna]
                )

                if not dados.empty:
                    fig = px.scatter(
                        dados,
                        x=mercado,
                        y=coluna,
                        hover_name=jogador,
                        title=(
                            f"Valor de mercado x {metrica}"
                        ),
                        labels={
                            mercado: "Valor de mercado (€)",
                            coluna: metrica
                        }
                    )

                    st.plotly_chart(
                        estilizar(fig),
                        use_container_width=True
                    )
        else:
            st.info(
                "Esta VIEW não possui dados suficientes "
                "de mercado."
            )

    # =====================================
    # ABA 4 - DADOS COMPLETOS
    # =====================================

    with abas[3]:
        st.header("Dados completos da VIEW")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=550
        )

        st.caption(
            "Até 5.000 registros carregados por VIEW."
        )

        st.download_button(
            "Baixar CSV",
            df.to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name=f"{view}.csv",
            mime="text/csv"
        )
