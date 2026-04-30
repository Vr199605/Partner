import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import locale

# Configuração da página
st.set_page_config(
    page_title="Assertif Corretora - Dashboard Financeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para visual moderno
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .section-header {
        font-size: 1.5rem;
        color: #1E3A5F;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def formatar_moeda(valor):
    """Formata valor para moeda brasileira"""
    try:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(valor)

def carregar_dados(uploaded_file):
    """Carrega e processa os dados do Excel"""
    dados = {}
    
    # Carregar todas as abas
    xl = pd.ExcelFile(uploaded_file)
    
    for sheet in xl.sheet_names:
        dados[sheet] = pd.read_excel(uploaded_file, sheet_name=sheet)
    
    return dados

def processar_dre(df):
    """Processa dados da DRE 2026"""
    # Encontrar a linha de cabeçalho (meses)
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    dre_data = {
        'meses': meses[:4],  # Dados disponíveis até Abril
        'receita_bruta': [],
        'impostos': [],
        'margem_contribuicao': [],
        'ebitda': [],
        'resultado_operacional': []
    }
    
    return dre_data

def criar_grafico_receita(df_assertif):
    """Cria gráfico de receita por mês"""
    df_assertif['MÊS'] = pd.to_datetime(df_assertif.iloc[:, 1], errors='coerce')
    
    # Agrupar por mês
    df_mensal = df_assertif.groupby(df_assertif['MÊS'].dt.strftime('%Y-%m')).agg({
        df_assertif.columns[12]: 'sum'  # Comissão Bruta
    }).reset_index()
    df_mensal.columns = ['Mês', 'Receita']
    
    fig = px.bar(
        df_mensal,
        x='Mês',
        y='Receita',
        title='📈 Receita Bruta por Mês',
        color='Receita',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=18,
        showlegend=False
    )
    
    return fig

def criar_grafico_seguradora(df_assertif):
    """Cria gráfico de pizza por seguradora"""
    col_seguradora = df_assertif.columns[4]  # Seguradora
    col_comissao = df_assertif.columns[12]  # Comissão Bruta
    
    df_seg = df_assertif.groupby(col_seguradora)[col_comissao].sum().reset_index()
    df_seg.columns = ['Seguradora', 'Comissão']
    df_seg = df_seg[df_seg['Comissão'] > 0].sort_values('Comissão', ascending=False)
    
    fig = px.pie(
        df_seg,
        values='Comissão',
        names='Seguradora',
        title='🏢 Distribuição por Seguradora',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=11),
        title_font_size=18
    )
    
    return fig

def criar_grafico_produto(df_assertif):
    """Cria gráfico de barras horizontais por produto"""
    col_produto = df_assertif.columns[10]  # Produto
    col_comissao = df_assertif.columns[12]  # Comissão Bruta
    
    df_prod = df_assertif.groupby(col_produto)[col_comissao].sum().reset_index()
    df_prod.columns = ['Produto', 'Comissão']
    df_prod = df_prod[df_prod['Comissão'] > 0].sort_values('Comissão', ascending=True)
    
    fig = px.bar(
        df_prod,
        x='Comissão',
        y='Produto',
        orientation='h',
        title='📦 Comissão por Produto',
        color='Comissão',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=11),
        title_font_size=18,
        showlegend=False,
        yaxis_title='',
        xaxis_title='Comissão (R$)'
    )
    
    return fig

def criar_grafico_originador(df_assertif):
    """Cria gráfico de barras por originador"""
    col_originador = df_assertif.columns[7]  # Originador
    col_comissao = df_assertif.columns[12]  # Comissão Bruta
    
    df_orig = df_assertif.groupby(col_originador)[col_comissao].sum().reset_index()
    df_orig.columns = ['Originador', 'Comissão']
    df_orig = df_orig[df_orig['Comissão'] > 0].sort_values('Comissão', ascending=False).head(10)
    
    fig = px.bar(
        df_orig,
        x='Originador',
        y='Comissão',
        title='👥 Top 10 Originadores',
        color='Comissão',
        color_continuous_scale='Purples'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=11),
        title_font_size=18,
        showlegend=False,
        xaxis_tickangle=-45
    )
    
    return fig

def criar_grafico_despesas(df_despesas):
    """Cria gráfico de despesas por categoria"""
    col_valor = df_despesas.columns[4]  # Valor
    col_categoria = df_despesas.columns[5]  # Categoria
    
    df_desp = df_despesas.groupby(col_categoria)[col_valor].sum().reset_index()
    df_desp.columns = ['Categoria', 'Valor']
    df_desp = df_desp[df_desp['Valor'] > 0].sort_values('Valor', ascending=False)
    
    fig = px.treemap(
        df_desp,
        path=['Categoria'],
        values='Valor',
        title='💰 Despesas por Categoria',
        color='Valor',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        font=dict(size=12),
        title_font_size=18
    )
    
    return fig

def criar_gauge_margem(margem):
    """Cria gráfico gauge para margem de lucro"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=margem,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Margem de Lucro", 'font': {'size': 18}},
        number={'suffix': '%', 'font': {'size': 36}},
        gauge={
            'axis': {'range': [None, 50], 'tickwidth': 1},
            'bar': {'color': "#667eea"},
            'bgcolor': "white",
            'borderwidth': 2,
            'steps': [
                {'range': [0, 10], 'color': '#ffcccc'},
                {'range': [10, 20], 'color': '#ffffcc'},
                {'range': [20, 50], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 15
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#1E3A5F"),
        height=300
    )
    
    return fig

def criar_grafico_trimestral(valores):
    """Cria gráfico de resultado trimestral"""
    trimestres = ['1º Tri', '2º Tri', '3º Tri', '4º Tri']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=trimestres,
        y=valores,
        marker_color=['#667eea', '#764ba2', '#f093fb', '#f5576c'],
        text=[formatar_moeda(v) for v in valores],
        textposition='outside'
    ))
    
    fig.update_layout(
        title='📅 Resultado Trimestral - Maldivas',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=18,
        yaxis_title='Valor (R$)',
        showlegend=False
    )
    
    return fig

def criar_grafico_share(partner, maldivas):
    """Cria gráfico de share entre sócios"""
    fig = go.Figure(data=[go.Pie(
        labels=['Partner', 'Maldivas'],
        values=[partner, maldivas],
        hole=.5,
        marker_colors=['#667eea', '#f5576c']
    )])
    
    fig.update_layout(
        title='🤝 Share de Distribuição',
        annotations=[dict(text='Share', x=0.5, y=0.5, font_size=20, showarrow=False)],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=18
    )
    
    return fig

# ==================== INTERFACE PRINCIPAL ====================

st.markdown('<h1 class="main-header">📊 Assertif Corretora - Dashboard Financeiro</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/combo-chart.png", width=80)
    st.markdown("### 📁 Upload da Planilha")
    
    uploaded_file = st.file_uploader(
        "Selecione o arquivo Excel",
        type=['xlsx', 'xls'],
        help="Faça upload da planilha DRE da Assertif"
    )
    
    st.markdown("---")
    
    if uploaded_file:
        st.success("✅ Arquivo carregado!")
        
        # Menu de navegação
        pagina = st.radio(
            "📌 Navegação",
            ["🏠 Visão Geral", "📈 Receitas", "💸 Despesas", "📊 Análise Detalhada"],
            index=0
        )
    else:
        st.info("👆 Faça upload da planilha para começar")
        pagina = None

# Conteúdo principal
if uploaded_file:
    # Carregar dados
    dados = carregar_dados(uploaded_file)
    
    # ==================== VISÃO GERAL ====================
    if pagina == "🏠 Visão Geral":
        st.markdown('<h2 class="section-header">📋 Resumo Executivo</h2>', unsafe_allow_html=True)
        
        # KPIs principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💰 Faturamento Total (YTD)",
                value="R$ 178.072",
                delta="↑ 12%"
            )
        
        with col2:
            st.metric(
                label="📈 Lucro Líquido",
                value="R$ 29.490",
                delta="↑ 8%"
            )
        
        with col3:
            st.metric(
                label="📊 Margem de Lucro",
                value="17%",
                delta="↑ 2%"
            )
        
        with col4:
            st.metric(
                label="🎯 Status",
                value="LUCRO",
                delta="Positivo"
            )
        
        st.markdown("---")
        
        # Gráficos principais
        col1, col2 = st.columns(2)
        
        with col1:
            # Resultado trimestral
            valores_trim = [20439, 1159, 0, 0]
            fig_trim = criar_grafico_trimestral(valores_trim)
            st.plotly_chart(fig_trim, use_container_width=True)
        
        with col2:
            # Share entre sócios
            fig_share = criar_grafico_share(65, 35)
            st.plotly_chart(fig_share, use_container_width=True)
        
        # Tabela de distribuição
        st.markdown('<h3 class="section-header">📊 Distribuição YTD 2026</h3>', unsafe_allow_html=True)
        
        df_dist = pd.DataFrame({
            'Sócio': ['Partner', 'Maldivas', '**Total 2026**'],
            'Valor (R$)': ['R$ 19.169', 'R$ 10.322', '**R$ 29.490**'],
            'Share (%)': ['65%', '35%', '100%']
        })
        
        st.dataframe(df_dist, use_container_width=True, hide_index=True)
        
        # Gauge de margem
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            fig_gauge = criar_gauge_margem(17)
            st.plotly_chart(fig_gauge, use_container_width=True)
    
    # ==================== RECEITAS ====================
    elif pagina == "📈 Receitas":
        st.markdown('<h2 class="section-header">📈 Análise de Receitas</h2>', unsafe_allow_html=True)
        
        if 'ASSERTIF DIRETO' in dados:
            df_assertif = dados['ASSERTIF DIRETO']
            
            # Filtros
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Filtro por mês
                meses_disponiveis = df_assertif.iloc[:, 1].dropna().unique()
                mes_selecionado = st.multiselect("📅 Filtrar por Mês", meses_disponiveis)
            
            with col2:
                # Filtro por seguradora
                seguradoras = df_assertif.iloc[:, 4].dropna().unique()
                seg_selecionada = st.multiselect("🏢 Filtrar por Seguradora", seguradoras)
            
            with col3:
                # Filtro por área de negócio
                areas = df_assertif.iloc[:, 5].dropna().unique()
                area_selecionada = st.multiselect("📁 Filtrar por Área", areas)
            
            st.markdown("---")
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                fig_receita = criar_grafico_receita(df_assertif)
                st.plotly_chart(fig_receita, use_container_width=True)
            
            with col2:
                fig_seg = criar_grafico_seguradora(df_assertif)
                st.plotly_chart(fig_seg, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_prod = criar_grafico_produto(df_assertif)
                st.plotly_chart(fig_prod, use_container_width=True)
            
            with col2:
                fig_orig = criar_grafico_originador(df_assertif)
                st.plotly_chart(fig_orig, use_container_width=True)
            
            # Tabela detalhada
            st.markdown('<h3 class="section-header">📋 Detalhamento de Comissões</h3>', unsafe_allow_html=True)
            
            with st.expander("📊 Ver tabela completa"):
                st.dataframe(df_assertif, use_container_width=True)
    
    # ==================== DESPESAS ====================
    elif pagina == "💸 Despesas":
        st.markdown('<h2 class="section-header">💸 Análise de Despesas</h2>', unsafe_allow_html=True)
        
        if 'DESPESAS' in dados:
            df_despesas = dados['DESPESAS']
            
            # KPIs de despesas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_despesas = df_despesas.iloc[:, 4].sum() if len(df_despesas) > 0 else 0
                st.metric("💰 Total de Despesas", formatar_moeda(total_despesas))
            
            with col2:
                qtd_lancamentos = len(df_despesas)
                st.metric("📝 Qtd. Lançamentos", qtd_lancamentos)
            
            with col3:
                media = total_despesas / qtd_lancamentos if qtd_lancamentos > 0 else 0
                st.metric("📊 Média por Lançamento", formatar_moeda(media))
            
            st.markdown("---")
            
            # Gráfico treemap de despesas
            fig_desp = criar_grafico_despesas(df_despesas)
            st.plotly_chart(fig_desp, use_container_width=True)
            
            # Tabela de despesas
            st.markdown('<h3 class="section-header">📋 Detalhamento de Despesas</h3>', unsafe_allow_html=True)
            
            with st.expander("📊 Ver tabela completa"):
                st.dataframe(df_despesas, use_container_width=True)
    
    # ==================== ANÁLISE DETALHADA ====================
    elif pagina == "📊 Análise Detalhada":
        st.markdown('<h2 class="section-header">📊 Análise Detalhada DRE</h2>', unsafe_allow_html=True)
        
        if 'DRE 2026' in dados:
            df_dre = dados['DRE 2026']
            
            # Exibir estrutura da DRE
            st.markdown("### 📑 Demonstração do Resultado do Exercício - 2026")
            
            # Criar visualização da DRE
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'YTD']
            
            dre_resumo = {
                'Descrição': [
                    'RECEITA BRUTA TOTAL',
                    'IMPOSTOS DIRETOS',
                    'CUSTO OPERACIONAL (D.A)',
                    'REBATE AAI',
                    'MARGEM DE CONTRIBUIÇÃO',
                    'DESPESAS',
                    'EBITDA SOCIETÁRIO',
                    'RESULTADO OPERACIONAL'
                ],
                'Jan': ['42.263', '(7.366)', '(3.619)', '(11.648)', '20.373', '(9.836)', '5.133', '5.133'],
                'Fev': ['49.513', '(8.630)', '(4.097)', '(14.087)', '22.732', '(9.294)', '7.667', '7.667'],
                'Mar': ['71.946', '(12.492)', '(5.918)', '(21.024)', '32.237', '(9.975)', '16.491', '16.690'],
                'Abr': ['14.350', '(2.501)', '(1.185)', '(3.888)', '6.803', '-', '-', '-'],
                'YTD': ['178.072', '(30.990)', '(14.820)', '(50.646)', '82.144', '(29.104)', '36.094', '29.490']
            }
            
            df_dre_resumo = pd.DataFrame(dre_resumo)
            
            st.dataframe(
                df_dre_resumo,
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("---")
            
            # Gráfico de evolução mensal
            fig_evolucao = go.Figure()
            
            fig_evolucao.add_trace(go.Scatter(
                x=['Jan', 'Fev', 'Mar', 'Abr'],
                y=[42263, 49513, 71946, 14350],
                name='Receita Bruta',
                line=dict(color='#667eea', width=3),
                mode='lines+markers'
            ))
            
            fig_evolucao.add_trace(go.Scatter(
                x=['Jan', 'Fev', 'Mar', 'Abr'],
                y=[5133, 7667, 16690, 0],
                name='Resultado Operacional',
                line=dict(color='#28a745', width=3),
                mode='lines+markers'
            ))
            
            fig_evolucao.update_layout(
                title='📈 Evolução Mensal - Receita vs Resultado',
                xaxis_title='Mês',
                yaxis_title='Valor (R$)',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=1.02),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_evolucao, use_container_width=True)
            
            # Inputs e parâmetros
            st.markdown('<h3 class="section-header">⚙️ Parâmetros do Modelo</h3>', unsafe_allow_html=True)
            
            if 'INPUTS' in dados:
                df_inputs = dados['INPUTS']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📊 Alíquotas de Impostos")
                    impostos = pd.DataFrame({
                        'Imposto': ['ISS', 'PIS', 'COFINS', 'IRPJ', 'CSLL'],
                        'Alíquota': ['5,00%', '0,65%', '3,00%', '4,80%', '6,08%']
                    })
                    st.dataframe(impostos, hide_index=True, use_container_width=True)
                
                with col2:
                    st.markdown("#### 🤝 Share de Distribuição")
                    share = pd.DataFrame({
                        'Sócio': ['Partner', 'Maldivas'],
                        'Participação': ['65%', '35%']
                    })
                    st.dataframe(share, hide_index=True, use_container_width=True)

else:
    # Tela de boas-vindas
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <img src="https://img.icons8.com/fluency/128/000000/upload-to-cloud.png" width="128">
        <h2 style="color: #1E3A5F; margin-top: 1rem;">Bem-vindo ao Dashboard Assertif</h2>
        <p style="color: #666; font-size: 1.1rem;">
            Faça upload da sua planilha Excel no menu lateral para começar a análise.
        </p>
        <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; margin-top: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
            <h4 style="color: #1E3A5F;">📋 Funcionalidades disponíveis:</h4>
            <ul style="text-align: left; color: #666;">
                <li>📊 Visão geral com KPIs principais</li>
                <li>📈 Análise detalhada de receitas por seguradora e produto</li>
                <li>💸 Controle de despesas por categoria</li>
                <li>📅 Resultado trimestral e distribuição entre sócios</li>
                <li>⚙️ Visualização dos parâmetros do modelo</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>🚀 Dashboard desenvolvido para Assertif Corretora | Streamlit + Plotly</p>",
    unsafe_allow_html=True
)
