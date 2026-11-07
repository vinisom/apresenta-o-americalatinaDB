import streamlit as st

st.set_page_config(
    page_title="América Latina DB",
    page_icon="⚽",
    layout="wide"
)

st.title("América Latina DB")
st.caption("Análise de desempenho, mercado e scouting | 2025")

st.markdown(
    """
    Projeto de análise de dados aplicado ao futebol sul-americano,
    integrando desempenho esportivo e valor de mercado dos jogadores.

    Selecione um país abaixo para abrir o dashboard correspondente.
    """
)

st.divider()

paises = [
    {
        "nome": "Argentina",
        "bandeira": "🇦🇷",
        "pagina": "pages/1_Argentina.py",
        "descricao": "Análises da Liga Argentina 2025.",
    },
    {
        "nome": "Bolívia",
        "bandeira": "🇧🇴",
        "pagina": "pages/2_Bolivia.py",
        "descricao": "Análises da Liga Boliviana 2025.",
    },
    {
        "nome": "Brasil",
        "bandeira": "🇧🇷",
        "pagina": "pages/3_Brasil.py",
        "descricao": "Análises do Campeonato Brasileiro 2025.",
    },
]

colunas = st.columns(len(paises))

for coluna, pais in zip(colunas, paises):
    with coluna:
        with st.container(border=True):
            st.markdown(f"### {pais['bandeira']} {pais['nome']}")
            st.write(pais["descricao"])
            st.page_link(
                pais["pagina"],
                label=f"Abrir {pais['nome']}",
                icon="➡️",
            )

st.divider()
st.caption(
    "Você também pode navegar entre os países pelo menu lateral, a qualquer momento."
)
