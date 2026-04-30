import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ======================== CONFIGURAÇÃO ========================
st.set_page_config(
    page_title="Assertif - Dashboard DRE",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================== CSS CUSTOMIZADO ========================
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A5F;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #667eea;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.4rem;
        color: #1E3A5F;
        border-left: 4px solid #667eea;
        padding-left: 10px;
        margin: 1.5rem 0 1rem 0;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ======================== FUNÇÕES AUXILIARES ========================
def formatar_moeda(valor):
    try:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(valor)

@st.cache_data
def carregar_dados(uploaded_file):
    return pd.read_excel(uploaded_file, sheet_name=None)

def criar_grafico_evolucao_mensal(dados_dre):
    meses = ['Jan', 'Fev', 'Mar', 'Abr']
    receita = [42263, 49513, 71946, 14350]
    resultado = [5133, 7667, 16690, 0]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=meses, y=receita, name='Receita Bruta', 
                             line=dict(color='#667eea', width=3), mode='lines+markers+text',
                             text=[formatar_moeda(v) for v in receita], textposition='top center'))
    fig.add_trace(go.Scatter(x=meses, y=resultado, name='Resultado', 
                             line=dict(color='#28a745', width=3), mode='lines+markers+text',
                             text=[formatar_moeda(v) for v in resultado], textposition='bottom center'))
    
    fig.update_layout(
        title='📈 Evolução Mensal - Receita vs Resultado',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        yaxis_title='Valor (R$)',
        height=400
    )
    return fig

def criar_grafico_trimestral():
    fig = go.Figure(data=[
        go.Bar(
            x=['1º Tri', '2º Tri', '3º Tri', '4º Tri'],
            y=[20439, 1159, 0, 0],
            marker_color=['#667eea', '#764ba2', '#a8a8a8', '#a8a8a8'],
            text=['R$ 20.439', 'R$ 1.159', '-', '-'],
            textposition='outside'
        )
    ])
    fig.update_layout(
        title='📅 Resultado Trimestral - Maldivas',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=350
    )
    return fig

def criar_grafico_share():
    fig = go.Figure(data=[go.Pie(
        labels=['Partner (65%)', 'Maldivas (35%)'],
        values=[19169, 10322],
        hole=.5,
        marker_colors=['#667eea', '#f5576c'],
        textinfo='label+value',
        texttemplate='%{label}<br>R$ %{value:,.0f}'
    )])
    fig.update_layout(
        title='🤝 Distribuição entre Sócios - YTD 2026',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        showlegend=False
    )
    return fig

def criar_grafico_seguradora(df):
    df_seg = df.groupby(df.columns[4])[df.columns[12]].sum().reset_index()
    df_seg.columns = ['Seguradora', 'Comissão']
    df_seg = df_seg[df_seg['Comissão'] > 0].sort_values('Comissão', ascending=False).head(10)
    
    fig = px.pie(df_seg, values='Comissão', names='Seguradora', title='🏢 Comissão por Seguradora',
                 hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400, showlegend=False)
    return fig

def criar_grafico_produto(df):
    df_prod = df.groupby(df.columns[10])[df.columns[12]].sum().reset_index()
    df_prod.columns = ['Produto', 'Comissão']
    df_prod = df_prod[df_prod['Comissão'] > 0].sort_values('Comissão', ascending=True)
    
    fig = px.bar(df_prod, x='Comissão', y='Produto', orientation='h',
                 title='📦 Comissão por Produto', color='Comissão',
                 color_continuous_scale='Blues')
    fig.update_layout(height=400, showlegend=False, yaxis_title='')
    return fig

def criar_grafico_originador(df):
    df_orig = df.groupby(df.columns[7])[df.columns[12]].sum().reset_index()
    df_orig.columns = ['Originador', 'Comissão']
    df_orig = df_orig[df_orig['Comissão'] > 0].sort_values('Comissão', ascending=False).head(8)
    
    fig = px.bar(df_orig, x='Originador', y='Comissão', title='👥 Top Originadores',
                 color='Comissão', color_continuous_scale='Purples',
                 text_auto='.2s')
    fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
    return fig

def criar_grafico_despesas(df):
    col_valor = df.columns[4]
    col_categoria = df.columns[5]
    
    df_clean = df.dropna(subset=[col_categoria, col_valor])
    df_desp = df_clean.groupby(col_categoria)[col_valor].sum().reset_index()
    df_desp.columns = ['Categoria', 'Valor']
    df_desp = df_desp[df_desp['Valor'] > 0].sort_values('Valor', ascending=False)
    
    fig = px.treemap(df_desp, path=['Categoria'], values='Valor',
                     title='💰 Despesas por Categoria',
                     color='Valor', color_continuous_scale='Reds')
    fig.update_layout(height=450)
    return fig

def criar_gauge_margem(margem):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=margem,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Margem de Lucro", 'font': {'size': 16}},
        number={'suffix': '%', 'font': {'size': 32, 'color': '#1E3A5F'}},
        gauge={
            'axis': {'range': [0, 30], 'tickwidth': 1},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 10], 'color': '#ffcccc'},
                {'range': [10, 20], 'color': '#ffffcc'},
                {'range': [20, 30], 'color': '#ccffcc'}
            ],
            'threshold': {'line': {'color': "green", 'width': 4}, 'thickness': 0.75, 'value': 17}
        }
    ))
    fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)')
    return fig

# ======================== INTERFACE PRINCIPAL ========================
st.markdown('<h1 class="main-header">📊 Assertif Corretora - Dashboard Financeiro</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=70)
    st.markdown("### 📁 Upload do Arquivo")
    
    uploaded_file = st.file_uploader("Selecione a planilha Excel", type=['xlsx', 'xls'])
    
    if uploaded_file:
        st.success("✅ Arquivo carregado!")
        st.markdown("---")
        pagina = st.radio("📌 Navegação", 
                          ["🏠 Visão Geral", "📈 Receitas", "💸 Despesas", "📊 DRE Detalhado"],
                          index=0)
    else:
        pagina = None
        st.info("👆 Faça upload para começar")

# ======================== CONTEÚDO ========================
if uploaded_file:
    dados = carregar_dados(uploaded_file)
    
    # ===== VISÃO GERAL =====
    if pagina == "🏠 Visão Geral":
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Faturamento YTD", "R$ 178.072", "Jan-Abr")
        with col2:
            st.metric("📈 Lucro Líquido", "R$ 29.490", "+17%")
        with col3:
            st.metric("📊 Margem", "17%", "Lucro")
        with col4:
            st.metric("🎯 Status", "LUCRO", "Positivo")
        
        st.markdown("---")
        
        # Gráficos principais
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(criar_grafico_trimestral(), use_container_width=True)
        with col2:
            st.plotly_chart(criar_grafico_share(), use_container_width=True)
        
        # Evolução mensal
        st.plotly_chart(criar_grafico_evolucao_mensal(dados), use_container_width=True)
        
        # Gauge + Tabela
        col1, col2 = st.columns([1, 2])
        with col1:
            st.plotly_chart(criar_gauge_margem(17), use_container_width=True)
        with col2:
            st.markdown('<h3 class="section-header">💵 Distribuição YTD 2026</h3>', unsafe_allow_html=True)
            df_dist = pd.DataFrame({
                'Sócio': ['Partner', 'Maldivas', '**TOTAL**'],
                'Share': ['65%', '35%', '100%'],
                'Valor': ['R$ 19.169', 'R$ 10.322', '**R$ 29.490**']
            })
            st.dataframe(df_dist, use_container_width=True, hide_index=True)
    
    # ===== RECEITAS =====
    elif pagina == "📈 Receitas":
        st.markdown('<h2 class="section-header">📈 Análise de Receitas</h2>', unsafe_allow_html=True)
        
        if 'ASSERTIF DIRETO' in dados:
            df = dados['ASSERTIF DIRETO']
            
            # Filtros
            col1, col2 = st.columns(2)
            with col1:
                seguradoras = df.iloc[:, 4].dropna().unique().tolist()
                seg_sel = st.multiselect("🏢 Filtrar Seguradora", seguradoras)
            with col2:
                produtos = df.iloc[:, 10].dropna().unique().tolist()
                prod_sel = st.multiselect("📦 Filtrar Produto", produtos)
            
            # Aplicar filtros
            df_filtered = df.copy()
            if seg_sel:
                df_filtered = df_filtered[df_filtered.iloc[:, 4].isin(seg_sel)]
            if prod_sel:
                df_filtered = df_filtered[df_filtered.iloc[:, 10].isin(prod_sel)]
            
            # KPIs
            total_comissao = df_filtered.iloc[:, 12].sum()
            qtd_registros = len(df_filtered)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Total Comissões", formatar_moeda(total_comissao))
            with col2:
                st.metric("📝 Registros", qtd_registros)
            with col3:
                st.metric("📊 Ticket Médio", formatar_moeda(total_comissao / qtd_registros if qtd_registros > 0 else 0))
            
            st.markdown("---")
            
            # Gráficos
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(criar_grafico_seguradora(df_filtered), use_container_width=True)
            with col2:
                st.plotly_chart(criar_grafico_produto(df_filtered), use_container_width=True)
            
            st.plotly_chart(criar_grafico_originador(df_filtered), use_container_width=True)
            
            # Tabela
            with st.expander("📋 Ver Dados Completos"):
                st.dataframe(df_filtered, use_container_width=True, height=400)
    
    # ===== DESPESAS =====
    elif pagina == "💸 Despesas":
        st.markdown('<h2 class="section-header">💸 Análise de Despesas</h2>', unsafe_allow_html=True)
        
        if 'DESPESAS' in dados:
            df = dados['DESPESAS'].dropna(how='all')
            
            total = df.iloc[:, 4].sum()
            qtd = len(df)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Total Despesas", formatar_moeda(total))
            with col2:
                st.metric("📝 Lançamentos", qtd)
            with col3:
                st.metric("📊 Média", formatar_moeda(total / qtd if qtd > 0 else 0))
            
            st.markdown("---")
            st.plotly_chart(criar_grafico_despesas(df), use_container_width=True)
            
            with st.expander("📋 Ver Dados Completos"):
                st.dataframe(df, use_container_width=True, height=400)
    
    # ===== DRE DETALHADO =====
    elif pagina == "📊 DRE Detalhado":
        st.markdown('<h2 class="section-header">📊 DRE 2026 - Detalhado</h2>', unsafe_allow_html=True)
        
        # Tabela DRE formatada
        dre_data = {
            'Descrição': [
                'RECEITA BRUTA TOTAL', 'IMPOSTOS DIRETOS', 'CUSTO OPERACIONAL (D.A)',
                'REBATE AAI', '(=) MARGEM DE CONTRIBUIÇÃO', 'DESPESAS',
                'EBITDA SOCIETÁRIO', 'RESULTADO OPERACIONAL'
            ],
            'Jan': ['42.263', '(7.366)', '(3.619)', '(11.648)', '20.373', '(9.836)', '5.133', '5.133'],
            'Fev': ['49.513', '(8.630)', '(4.097)', '(14.087)', '22.732', '(9.294)', '7.667', '7.667'],
            'Mar': ['71.946', '(12.492)', '(5.918)', '(21.024)', '32.237', '(9.975)', '16.491', '16.690'],
            'Abr': ['14.350', '(2.501)', '(1.185)', '(3.888)', '6.803', '-', '-', '-'],
            'YTD': ['178.072', '(30.990)', '(14.820)', '(50.646)', '82.144', '(29.104)', '36.094', '29.490']
        }
        
        df_dre = pd.DataFrame(dre_data)
        st.dataframe(df_dre, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.plotly_chart(criar_grafico_evolucao_mensal(dados), use_container_width=True)
        
        # Parâmetros
        st.markdown('<h3 class="section-header">⚙️ Parâmetros do Modelo</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📊 Alíquotas de Impostos**")
            impostos = pd.DataFrame({
                'Imposto': ['ISS', 'PIS', 'COFINS', 'IRPJ', 'CSLL'],
                'Alíquota': ['5,00%', '0,65%', '3,00%', '4,80%', '6,08%']
            })
            st.dataframe(impostos, hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("**🤝 Share de Distribuição**")
            share = pd.DataFrame({
                'Sócio': ['Partner', 'Maldivas'],
                'Participação': ['65%', '35%']
            })
            st.dataframe(share, hide_index=True, use_container_width=True)

else:
    # Tela de boas-vindas
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <img src="https://img.icons8.com/fluency/128/cloud-upload.png" width="100">
        <h2 style="color: #1E3A5F; margin-top: 1rem;">Bem-vindo ao Dashboard Assertif</h2>
        <p style="color: #666; font-size: 1.1rem;">
            Faça upload da planilha Excel no menu lateral para visualizar os dashboards.
        </p>
    </div>
    
    <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; max-width: 700px; margin: 2rem auto;">
        <h4 style="color: #1E3A5F;">📋 Funcionalidades:</h4>
        <ul style="color: #666; line-height: 2;">
            <li>🏠 <b>Visão Geral</b> - KPIs, resultado trimestral, distribuição</li>
            <li>📈 <b>Receitas</b> - Análise por seguradora, produto, originador</li>
            <li>💸 <b>Despesas</b> - Treemap de categorias</li>
            <li>📊 <b>DRE Detalhado</b> - Estrutura completa da DRE</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>📊 Assertif Corretora - Dashboard Financeiro | Streamlit + Plotly</p>", unsafe_allow_html=True)
