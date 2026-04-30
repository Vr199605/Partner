# =============================================================================
# 🚀 ASSERTIF CORRETORA - DASHBOARD HIGH-CONTRAST (FOCO EM LEITURA)
# =============================================================================

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import display, HTML
import warnings

# Silenciar avisos irrelevantes
warnings.filterwarnings('ignore')

# -----------------------------------------------------------------------------
# 🎨 DEFINIÇÃO DE ESTILO E CORES (Enterprise Clean)
# -----------------------------------------------------------------------------
STYLE = {
    'bg_card': '#FFFFFF',
    'text_main': '#1A1A1B',
    'text_sub': '#4A4A4A',
    'accent_blue': '#0056b3',
    'accent_green': '#198754',
    'accent_red': '#d00000',
    'border_light': '#E0E0E0',
    'font_family': 'Segoe UI, Helvetica, Arial, sans-serif'
}

def formatar_moeda(valor):
    """Formata valores numéricos para o padrão monetário brasileiro."""
    if pd.isna(valor) or valor == 0: return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# -----------------------------------------------------------------------------
# 🏗️ ESTRUTURA CSS PARA O LAYOUT (Injetado no Notebook)
# -----------------------------------------------------------------------------
css_estilo = f"""
<style>
    body {{ font-family: {STYLE['font_family']}; background-color: #F8F9FA; }}
    .dashboard-wrapper {{ padding: 20px; background: white; }}
    .kpi-container {{
        display: flex; flex-wrap: wrap; justify-content: space-between; gap: 15px; margin: 20px 0;
    }}
    .kpi-card {{
        background: white; border: 1px solid {STYLE['border_light']}; border-radius: 8px;
        padding: 20px; flex: 1; min-width: 200px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: left; border-top: 5px solid {STYLE['accent_blue']};
    }}
    .kpi-title {{ color: {STYLE['text_sub']}; font-size: 0.85rem; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }}
    .kpi-value {{ color: {STYLE['text_main']}; font-size: 1.8rem; font-weight: 800; margin: 5px 0; }}
    .section-header {{
        background: #f1f3f5; padding: 12px 15px; border-radius: 4px; 
        color: {STYLE['text_main']}; font-weight: bold; border-left: 6px solid {STYLE['accent_blue']};
        margin-top: 30px; margin-bottom: 15px; font-size: 1.1rem;
    }}
</style>
"""
display(HTML(css_estilo))

# -----------------------------------------------------------------------------
# 💎 CABEÇALHO E INDICADORES (KPIs)
# -----------------------------------------------------------------------------
display(HTML(f"""
<div style="text-align: center; padding: 20px; border-bottom: 2px solid #EEE; background: white;">
    <h1 style="color: {STYLE['text_main']}; margin: 0;">📊 Relatório Executivo Assertif</h1>
    <p style="color: {STYLE['text_sub']}; font-size: 1.1rem;">Consolidado Financeiro | Gestão de Dados 2026</p>
</div>
"""))

# Simulação de valores para exibição imediata
# (Substitua por suas variáveis de faturamento reais)
kpis_html = f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-title">Faturamento Acumulado (YTD)</div>
        <div class="kpi-value">{formatar_moeda(178072.00)}</div>
        <div style="color: {STYLE['accent_green']}; font-weight: bold;">↑ Receita Consolidada</div>
    </div>
    <div class="kpi-card" style="border-top-color: {STYLE['accent_green']};">
        <div class="kpi-title">Resultado Líquido</div>
        <div class="kpi-value" style="color: {STYLE['accent_green']};">{formatar_moeda(29490.00)}</div>
        <div style="color: {STYLE['text_sub']}; font-weight: bold;">Margem Líquida: 16.5%</div>
    </div>
    <div class="kpi-card" style="border-top-color: #6f42c1;">
        <div class="kpi-title">Ponto de Equilíbrio</div>
        <div class="kpi-value">{formatar_moeda(148582.00)}</div>
        <div style="color: {STYLE['text_sub']};">Cobertura de Custos Fixos</div>
    </div>
</div>
"""
display(HTML(kpis_html))

# -----------------------------------------------------------------------------
# 📈 VISUALIZAÇÃO GRÁFICA (Plotly High-Contrast)
# -----------------------------------------------------------------------------
display(HTML('<div class="section-header">ANÁLISE DE EVOLUÇÃO MENSAL</div>'))

# Dados de exemplo para o gráfico
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril']
receita = [42263, 49513, 71946, 14350]
lucro = [5133, 7667, 16690, 2400]

fig = make_subplots(rows=1, cols=2, subplot_titles=("Receita Bruta", "Lucro Líquido"), horizontal_spacing=0.12)

# Gráfico de Barras - Receita
fig.add_trace(go.Bar(
    x=meses, y=receita, name="Receita",
    marker_color=STYLE['accent_blue'],
    text=[f"R$ {v/1000:.1f}k" for v in receita], textposition='auto',
), row=1, col=1)

# Gráfico de Linha - Lucro
fig.add_trace(go.Scatter(
    x=meses, y=lucro, name="Lucro",
    mode='lines+markers+text', 
    line=dict(color=STYLE['accent_green'], width=4),
    marker=dict(size=10, symbol='diamond'),
    text=[f"R$ {v/1000:.1f}k" for v in lucro], textposition='top center'
), row=1, col=2)

fig.update_layout(
    height=450, plot_bgcolor='white', paper_bgcolor='white',
    font=dict(family=STYLE['font_family'], size=13, color=STYLE['text_main']),
    margin=dict(l=40, r=40, t=60, b=40), showlegend=False
)

# Estilização dos eixos para clareza
fig.update_xaxes(showline=True, linewidth=1, linecolor='#CCC', gridcolor='#F2F2F2')
fig.update_yaxes(showline=True, linewidth=1, linecolor='#CCC', gridcolor='#F2F2F2')

fig.show()

# -----------------------------------------------------------------------------
# 📋 TABELA FINANCEIRA (Detalhamento)
# -----------------------------------------------------------------------------
display(HTML('<div class="section-header">DEMONSTRATIVO DE RESULTADOS SINTÉTICO</div>'))

tabela_html = f"""
<table style="width:100%; border-collapse: collapse; font-family: {STYLE['font_family']}; background: white; margin-bottom: 50px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
    <thead>
        <tr style="background: {STYLE['text_main']}; color: white; text-align: left;">
            <th style="padding: 15px; border: 1px solid #ddd;">GRUPO DE CONTA</th>
            <th style="padding: 15px; border: 1px solid #ddd; text-align: right;">VALOR ACUMULADO</th>
            <th style="padding: 15px; border: 1px solid #ddd; text-align: center;">% SOBRE RECEITA</th>
        </tr>
    </thead>
    <tbody>
        <tr style="background: #FDFDFD;">
            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">(+) FATURAMENTO BRUTO</td>
            <td style="padding: 12px; border: 1px solid #ddd; text-align: right; font-weight: bold;">{formatar_moeda(178072)}</td>
            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">100%</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #ddd; color: {STYLE['accent_red']};">(-) Custos Operacionais / Variáveis</td>
            <td style="padding: 12px; border: 1px solid #ddd; text-align: right; color: {STYLE['accent_red']};">({formatar_moeda(117592)})</td>
            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">-66.0%</td>
        </tr>
        <tr style="background: #F1F8E9;">
            <td style="padding: 15px; border: 1px solid #ddd; font-weight: bold; font-size: 1.1rem; color: {STYLE['accent_green']};">(=) MARGEM LÍQUIDA FINAL</td>
            <td style="padding: 15px; border: 1px solid #ddd; text-align: right; font-weight: bold; font-size: 1.1rem; color: {STYLE['accent_green']};">{formatar_moeda(29490)}</td>
            <td style="padding: 15px; border: 1px solid #ddd; text-align: center; font-weight: bold; color: {STYLE['accent_green']};">16.5%</td>
        </tr>
    </tbody>
</table>
"""
display(HTML(tabela_html))
