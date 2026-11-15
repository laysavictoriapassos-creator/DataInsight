import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="DataInsight",
    page_icon="📊",
    layout="wide"
)

# Visual
st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: #F8FAFC;
}
h1, h2, h3, p, label {
    color: #F8FAFC !important;
}
div[data-testid="stMetric"] {
    background: #1E293B;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.title("📊 DataInsight")
st.caption("PLATAFORMA INTELIGENTE DE ANÁLISE DE DADOS")
st.markdown("---")

st.subheader("Seu painel de dados")
st.write("Envie uma planilha e transforme números em informações.")

arquivo = st.file_uploader(
    "📁 Envie sua planilha",
    type=["csv", "xlsx"]
)

if arquivo is not None:
    try:
        if arquivo.name.endswith(".csv"):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)

        st.success("Planilha carregada com sucesso!")

        st.subheader("Visão geral")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total de linhas", df.shape[0])

        with col2:
            st.metric("Total de colunas", df.shape[1])

        with col3:
            st.metric(
                "Valores vazios",
                int(df.isna().sum().sum())
            )

        st.markdown("---")

        st.subheader("📋 Dados da planilha")
        st.dataframe(df, use_container_width=True)

        colunas_numericas = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if colunas_numericas:
            st.markdown("---")
            st.subheader("📈 Análise visual")

            coluna = st.selectbox(
                "Escolha uma coluna para analisar",
                colunas_numericas
            )

            fig = px.histogram(
                df,
                x=coluna,
                title=f"Distribuição de {coluna}",
                template="plotly_dark",
                color_discrete_sequence=["#8B5CF6"]
            )

            fig.update_layout(
                paper_bgcolor="#101827",
                plot_bgcolor="#1E293B",
                font_color="#F8FAFC"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.subheader("📊 Estatísticas")
            relatorio = df[colunas_numericas].describe().round(2)

            st.dataframe(
                relatorio,
                use_container_width=True
            )

            st.download_button(
                label="⬇️ Baixar relatório",
                data=relatorio.to_csv().encode("utf-8"),
                file_name="relatorio_datainsight.csv",
                mime="text/csv"
            )
            st.dataframe(
                df[colunas_numericas].describe(),
                use_container_width=True
            )

        else:
            st.info("Não existem colunas numéricas nesta planilha.")

    except Exception as erro:
        st.error(f"Erro ao ler arquivo: {erro}")

else:
    st.info("👆 Envie um arquivo para começar sua análise.")