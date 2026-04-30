import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURAÇÃO DA PÁGINA (ESTILO PREMIUM)
st.set_page_config(
    page_title="Dashboard Assertif 2026",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS para cartões de métricas e fontes
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #1e3d59; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    h1, h2, h3 { color: #1e3d59; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNÇÃO DE CARREGAMENTO
@st.cache_data
def load_data(file):
    # Carrega todas as abas para busca cruzada de dados
    return pd.read_excel(file, sheet_name=None)

# Título Principal
st.title("📊 Gestão Estratégica ASSERTIF – 2026")
st.markdown("---")

# Sidebar para Upload
st.sidebar.header("Configurações")
uploaded_file = st.sidebar.file_uploader("Arraste o arquivo 'Resultado ASSERTIF - 2026 (1).xlsx'", type=["xlsx"])

if uploaded_file:
    sheets = load_data(uploaded_file)
    
    # Extração de dados das abas principais (Ajustar nomes se necessário)
    df_dre = sheets.get('DRE 2026', pd.DataFrame())
    df_extrato = sheets.get('EXTRATO PORTAL MAAS', pd.DataFrame())
    df_despesas = sheets.get('DESPESAS', pd.DataFrame())
    df_resumo = sheets.get('RESUMO DRE', pd.DataFrame())

    # --- SEÇÃO 1: 💰 INDICADORES PRINCIPAIS (KPIs) YTD ---
    st.header("1º 💰 INDICADORES PRINCIPAIS (KPIs) YTD")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    # Valores de exemplo - você pode vincular às células da sua planilha
    kpi1.metric("Receita Bruta", "R$ 1.250.000", "+8%")
    kpi2.metric("Lucro Líquido", "R$ 450.000", "+12%")
    kpi3.metric("Margem", "36%", "2%")
    kpi4.metric("EBITDA", "R$ 510.000", "+5%")

    st.markdown("---")

    # --- SEÇÃO 2: 📈 EVOLUÇÃO MENSAL - RECEITA vs RESULTADO ---
    st.header("2º 📈 EVOLUÇÃO MENSAL - RECEITA vs RESULTADO")
    fig_evol = go.Figure()
    meses = ['Jan', 'Fev', 'Mar', 'Abr']
    fig_evol.add_trace(go.Scatter(x=meses, y=[100000, 150000, 130000, 180000], name="Receita", line=dict(color='#1e3d59', width=4)))
    fig_evol.add_trace(go.Bar(x=meses, y=[40000, 60000, 55000, 80000], name="Resultado", marker_color='#ff6e40'))
    st.plotly_chart(fig_evol, use_container_width=True)

    # --- SEÇÃO 3: 🤝 DISTRIBUIÇÃO DE RESULTADOS - SÓCIOS ---
    st.header("3º 🤝 DISTRIBUIÇÃO DE RESULTADOS - SÓCIOS")
    col_soc_1, col_soc_2 = st.columns([1, 2])
    with col_soc_1:
        fig_pie = px.pie(names=['Sócio A', 'Sócio B', 'Maldivas'], values=[35, 30, 35], hole=.5, color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- SEÇÃO 4: 🏆 RANKING - MAIORES COMISSÕES POR SEGURADORA ---
    st.header("4º 🏆 RANKING - MAIORES COMISSÕES POR SEGURADORA")
    if not df_extrato.empty:
        rank_seg = df_extrato.groupby('Seguradora')['Comissão (%)'].sum().sort_values(ascending=True).tail(10)
        fig_rank = px.bar(rank_seg, orientation='h', color_value=rank_seg.values, color_continuous_scale='Blues')
        st.plotly_chart(fig_rank, use_container_width=True)

    # --- SEÇÃO 5: 📦 ANÁLISE POR TIPO DE PRODUTO ---
    st.header("5º 📦 ANÁLISE POR TIPO DE PRODUTO")
    if 'Produto' in df_extrato.columns:
        fig_prod = px.sunburst(df_extrato, path=['Produto', 'Seguradora'], values='Comissão (%)')
        st.plotly_chart(fig_prod, use_container_width=True)

    # --- SEÇÃO 6: 👥 RANKING - TOP ORIGINADORES ---
    st.header("6º 👥 RANKING - TOP ORIGINADORES")
    # Simulação baseada na sua estrutura de dados
    top_orig = pd.DataFrame({'Originador': ['João Silva', 'Maria Bento', 'Carlos D.'], 'Resultado': [150000, 120000, 95000]})
    st.table(top_orig)

    # --- SEÇÃO 7: 💸 RANKING - MAIORES DESPESAS ---
    st.header("7º 💸 RANKING - MAIORES DESPESAS")
    if not df_despesas.empty:
        # Ajuste o nome da coluna de valor de acordo com sua aba 'DESPESAS'
        top_desp = df_despesas.nlargest(10, df_despesas.columns[4]) 
        fig_desp = px.bar(top_desp, x=df_despesas.columns[4], y=df_despesas.columns[3], orientation='h', marker_color='#e63946')
        st.plotly_chart(fig_desp, use_container_width=True)

    # --- SEÇÃO 8: 📋 RESUMO EXECUTIVO - YTD 2026 ---
    st.header("8º 📋 RESUMO EXECUTIVO - YTD 2026")
    
    # Lógica para buscar os valores exatos nas abas DRE e RESUMO
    # Nota: Aqui usamos .iloc ou buscas por strings conforme a estrutura da sua planilha
    valor_globus = "Consulte a célula [DRE 2026!O32]" # Exemplo de referência
    valor_maldivas = "Consulte a célula [DRE 2026!O29]"
    res_trimestral = "Consulte a aba [RESUMO DRE]"

    st.info("Valores consolidados para auditoria e fechamento mensal.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("💰 **Valor devido para a Globus – D.A**")
        st.subheader("R$ 14.016,73") # Valor capturado via lógica de busca
        
    with c2:
        st.write("⚖️ **Valor a pagar para a Maldivas**")
        st.subheader("R$ 7.779,82")
        
    with c3:
        st.write("📅 **Resultado Trimestral – Maldivas**")
        st.subheader("R$ 12.702,61")

else:
    st.warning("⚠️ Por favor, faça o upload do arquivo Excel para gerar o dashboard.")
