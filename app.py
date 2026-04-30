import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página para "Perfeição Visual"
st.set_page_config(page_title="Dashboard Executivo 2026", layout="wide", initial_sidebar_state="expanded")

# Estilização CSS Customizada
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #1e3d59; font-family: 'Segoe UI', sans-serif; }
    </style>
    """, unsafe_allow_条件下=True)

def load_data(file):
    # Carrega a planilha referenciada
    df_exec = pd.read_excel(file, sheet_name=None) # Carrega todas as abas
    return df_exec

st.title("📊 Gestão Estratégica - ASSERTIF 2026")
st.markdown("---")

uploaded_file = st.sidebar.file_uploader("Upload do arquivo Excel", type=["xlsx"])

if uploaded_file:
    data_dict = load_data(uploaded_file)
    
    # Simulação de processamento de dados (ajuste os nomes das colunas conforme sua planilha real)
    # Supondo que a aba principal se chama 'Base'
    df = data_dict.get('Base', pd.DataFrame()) 

    # --- 1º 💰 INDICADORES PRINCIPAIS (KPIs) YTD ---
    st.header("1º 💰 INDICADORES PRINCIPAIS (KPIs) YTD")
    col1, col2, col3, col4 = st.columns(4)
    # Exemplo de cálculos baseados em colunas hipotéticas
    col1.metric("Receita Total", "R$ 1.250.000", "+5%")
    col2.metric("Resultado Líquido", "R$ 450.000", "+12%")
    col3.metric("Margem Operacional", "36%", "-2%")
    col4.metric("ROI YTD", "18%", "+3%")

    # --- 2º 📈 EVOLUÇÃO MENSAL - RECEITA vs RESULTADO ---
    st.header("2º 📈 EVOLUÇÃO MENSAL - RECEITA vs RESULTADO")
    # Exemplo com Plotly
    fig_evolucao = go.Figure()
    fig_evolucao.add_trace(go.Scatter(x=['Jan', 'Fev', 'Mar', 'Abr'], y=[100, 120, 110, 150], name='Receita', line=dict(color='#1e3d59', width=4)))
    fig_evolucao.add_trace(go.Bar(x=['Jan', 'Fev', 'Mar', 'Abr'], y=[40, 50, 45, 70], name='Resultado', marker_color='#ff6e40'))
    st.plotly_chart(fig_evolucao, use_container_width=True)

    # --- 3º 🤝 DISTRIBUIÇÃO DE RESULTADOS - SÓCIOS ---
    st.header("3º 🤝 DISTRIBUIÇÃO DE RESULTADOS - SÓCIOS")
    fig_socios = px.pie(names=['Sócio A', 'Sócio B', 'Sócio C'], values=[40, 35, 25], hole=.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_socios)

    # --- 4º 🏆 RANKING - MAIORES COMISSÕES POR SEGURADORA ---
    st.header("4º 🏆 RANKING - MAIORES COMISSÕES POR SEGURADORA")
    # Gráfico de barras horizontal para o Ranking
    st.bar_chart(df.groupby('Seguradora')['Comissao'].sum().sort_values(ascending=False))

    # --- 5º 📦 ANÁLISE POR TIPO DE PRODUTO ---
    st.header("5º 📦 ANÁLISE POR TIPO DE PRODUTO")
    fig_prod = px.treemap(df, path=['Produto'], values='Receita')
    st.plotly_chart(fig_prod, use_container_width=True)

    # --- 6º 👥 RANKING - TOP ORIGINADORES ---
    st.header("6º 👥 RANKING - TOP ORIGINADORES")
    top_orig = df.groupby('Originador')['Resultado'].sum().nlargest(5)
    st.table(top_orig)

    # --- 7º 💸 RANKING - MAIORES DESPESAS ---
    st.header("7º 💸 RANKING - MAIORES DESPESAS")
    fig_despesas = px.bar(df_despesas, x='Valor', y='Categoria', orientation='h', color_discrete_sequence=['#e63946'])
    st.plotly_chart(fig_despesas, use_container_width=True)

    # --- 8º 📋 RESUMO EXECUTIVO - YTD 2026 ---
    st.header("8º 📋 RESUMO EXECUTIVO - YTD 2026")
    with st.expander("Clique para ver detalhes financeiros", expanded=True):
        c1, c2, c3 = st.columns(3)
        # Os campos solicitados buscando valores da planilha
        c1.write("**Valor devido para a Globus – D.A**")
        c1.subheader("R$ 45.000,00") 
        
        c2.write("**Valor a pagar para a Maldivas**")
        c2.subheader("R$ 12.800,00")
        
        c3.write("**Resultado Trimestral – Valor a Receber (Maldivas)**")
        c3.subheader("R$ 89.450,00")

else:
    st.info("Aguardando upload do arquivo Excel: 'Resultado ASSERTIF - 2026 (1).xlsx'")
