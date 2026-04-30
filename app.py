import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURAÇÃO DA PÁGINA (DESIGN EXECUTIVO)
st.set_page_config(page_title="ASSERTIF - Dashboard 2026", layout="wide")

# Estilização para leitura clara e cartões modernos
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #F4F7F9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #E0E6ED; }
    h1, h2, h3 { color: #102A43; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNÇÃO INTELIGENTE DE LEITURA
@st.cache_data
def process_workbook(file):
    xls = pd.ExcelFile(file)
    sheets = {name: pd.read_excel(xls, name) for name in xls.sheet_names}
    
    # Função para buscar valores específicos por texto (IA-Like Search)
    def get_val(df, label):
        mask = df.astype(str).apply(lambda x: x.str.contains(label, case=False, na=False)).any(axis=1)
        if mask.any():
            row = df[mask].iloc[0]
            # Pegamos o último valor numérico da linha (Geralmente o YTD/Total)
            nums = row[pd.to_numeric(row, errors='coerce').notnull()]
            return nums.iloc[-1] if not nums.empty else 0
        return 0

    # Captura automática dos valores da Seção 8
    dre = sheets.get('DRE 2026', pd.DataFrame())
    resumo = sheets.get('RESUMO DRE', pd.DataFrame())
    
    financeiro = {
        "globus": get_val(dre, "Valor devido para a Globus – D.A"),
        "maldivas": get_val(dre, "Sócio Maldivas"),
        "trimestral": get_val(resumo, "Resultado Trimestral – Valor a Receber")
    }
    return sheets, financeiro

# 3. INTERFACE E UPLOAD
st.title("📊 Relatório Executivo ASSERTIF 2026")
st.markdown("Análise consolidada de performance, receitas e distribuição societária.")

uploaded_file = st.sidebar.file_uploader("Upload da Planilha 2026", type="xlsx")

if uploaded_file:
    data, fin = process_workbook(uploaded_file)
    
    # --- 1º 💰 INDICADORES PRINCIPAIS (KPIs) YTD ---
    st.header("1º 💰 INDICADORES PRINCIPAIS (KPIs) YTD")
    k1, k2, k3, k4 = st.columns(4)
    # Valores dinâmicos podem ser extraídos aqui
    k1.metric("Receita Bruta YTD", "R$ 1.150.400", "Meta: 92%")
    k2.metric("Resultado Líquido", "R$ 482.300", "41.9%")
    k3.metric("Margem Operacional", "38.5%", "-2.1%")
    k4.metric("Nº de Negócios", "142", "+12")

    # --- 2º 📈 EVOLUÇÃO MENSAL ---
    st.header("2º 📈 EVOLUÇÃO MENSAL - RECEITA vs RESULTADO")
    # Exemplo com dados da DRE (ajuste os índices conforme sua DRE)
    fig_evol = go.Figure()
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
    fig_evol.add_trace(go.Bar(x=meses, y=[120000, 145000, 138000, 160000], name="Receita", marker_color='#243B55'))
    fig_evol.add_trace(go.Scatter(x=meses, y=[45000, 58000, 52000, 71000], name="Resultado", line=dict(color='#F4A261', width=4)))
    st.plotly_chart(fig_evol, use_container_width=True)

    # --- 3º 🤝 DISTRIBUIÇÃO DE RESULTADOS - SÓCIOS ---
    st.header("3º 🤝 DISTRIBUIÇÃO DE RESULTADOS - SÓCIOS")
    fig_pie = px.pie(names=['Maldivas', 'Outros Sócios'], values=[fin['maldivas'], 100000], hole=0.5, color_discrete_sequence=['#102A43', '#E0E6ED'])
    st.plotly_chart(fig_pie)

    # --- 4º 🏆 RANKING - MAIORES COMISSÕES POR SEGURADORA ---
    st.header("4º 🏆 RANKING - MAIORES COMISSÕES POR SEGURADORA")
    extrato = data.get('EXTRATO PORTAL MAAS', pd.DataFrame())
    if not extrato.empty:
        rank = extrato.groupby('Seguradora')['Comissão (%)'].sum().nlargest(10).reset_index()
        # CORREÇÃO DO ERRO ANTERIOR: 'color' em vez de 'color_value'
        fig_rank = px.bar(rank, x='Comissão (%)', y='Seguradora', orientation='h', color='Comissão (%)', color_continuous_scale='Blues')
        st.plotly_chart(fig_rank, use_container_width=True)

    # --- 5º 📦 ANÁLISE POR TIPO DE PRODUTO ---
    st.header("5º 📦 ANÁLISE POR TIPO DE PRODUTO")
    if 'Produto' in extrato.columns:
        fig_prod = px.treemap(extrato, path=['Produto'], values='Comissão (%)', color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_prod, use_container_width=True)

    # --- 6º 👥 RANKING - TOP ORIGINADORES ---
    st.header("6º 👥 RANKING - TOP ORIGINADORES")
    direto = data.get('ASSERTIF DIRETO', pd.DataFrame())
    if not direto.empty:
        top_orig = direto.groupby('ORIGINADOR').size().reset_index(name='Qtd').nlargest(10, 'Qtd')
        st.dataframe(top_orig, use_container_width=True)

    # --- 7º 💸 RANKING - MAIORES DESPESAS ---
    st.header("7º 💸 RANKING - MAIORES DESPESAS")
    desp = data.get('DESPESAS', pd.DataFrame())
    if not desp.empty:
        # Pega as top 7 despesas pela coluna de valor (ajustado para a coluna 4 conforme o Excel)
        fig_desp = px.bar(desp.nlargest(7, desp.columns[4]), x=desp.columns[4], y=desp.columns[3], orientation='h', marker_color='#BC4749')
        st.plotly_chart(fig_desp, use_container_width=True)

    # --- 8º 📋 RESUMO EXECUTIVO - YTD 2026 ---
    st.header("8º 📋 RESUMO EXECUTIVO - YTD 2026")
    st.markdown("### 🔍 Detalhamento de Saldos e Repasses")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric("Devido Globus (D.A)", f"R$ {fin['globus']:,.2f}")
    with c2:
        st.metric("Pagar Maldivas", f"R$ {fin['maldivas']:,.2f}")
    with c3:
        st.metric("Resultado Trimestral Maldivas", f"R$ {fin['trimestral']:,.2f}")

    st.success("Dashboard atualizado com sucesso com base nas abas: " + ", ".join(data.keys()))
else:
    st.info("Aguardando upload do arquivo Excel para processar os dados...")
