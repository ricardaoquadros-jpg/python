"""
==============================================================================
DASHBOARD DE SUPORTE DE TI - STREAMLIT
==============================================================================
Autor: [Seu Nome]
Data: Dezembro 2024
Descrição: Dashboard interativo para visualização de métricas de suporte de TI

Para executar:
    streamlit run dashboard.py

O que você vai aprender:
- Como criar dashboards com Streamlit
- Visualização de dados com gráficos
- Interface web com Python puro
==============================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
# st.set_page_config() define as configurações gerais do dashboard
# Deve ser a primeira chamada do Streamlit no script

st.set_page_config(
    page_title="Dashboard TI",  # Título da aba do navegador
    page_icon="📊",             # Ícone da aba
    layout="wide",              # Layout expandido (usa toda a tela)
    initial_sidebar_state="expanded"  # Sidebar aberta por padrão
)

# ==============================================================================
# ESTILO CSS CUSTOMIZADO
# ==============================================================================
# Podemos injetar CSS para personalizar a aparência

st.markdown("""
<style>
    /* Cards de métricas */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Título principal */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Subtítulos */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        border-left: 4px solid #667eea;
        padding-left: 15px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# FUNÇÕES DE CARREGAMENTO E TRATAMENTO
# ==============================================================================

@st.cache_data  # Cache para não recarregar dados a cada interação
def carregar_dados():
    """
    Carrega e trata os dados do CSV.
    
    @st.cache_data é um decorador que cacheia os dados.
    Isso significa que a função só roda uma vez, depois usa o cache.
    Melhora muito a performance do dashboard!
    """
    df = pd.read_csv('chamados_ti.csv')
    
    # Tratamento de datas
    df['data_abertura'] = pd.to_datetime(df['data_abertura'])
    df['data_fechamento'] = pd.to_datetime(df['data_fechamento'], errors='coerce')
    
    # Cálculo do tempo de atendimento
    df['tempo_atendimento_horas'] = (
        (df['data_fechamento'] - df['data_abertura'])
        .dt.total_seconds() / 3600
    ).round(2)
    
    return df


def calcular_metricas(df):
    """Calcula as métricas principais do dashboard."""
    return {
        'total': len(df),
        'abertos': len(df[df['status'] == 'Aberto']),
        'em_andamento': len(df[df['status'] == 'Em Andamento']),
        'fechados': len(df[df['status'] == 'Fechado']),
        'tempo_medio': df['tempo_atendimento_horas'].mean(),
        'criticos': len(df[df['prioridade'] == 'Critica'])
    }


# ==============================================================================
# CARREGAMENTO DOS DADOS
# ==============================================================================

df = carregar_dados()
metricas = calcular_metricas(df)

# ==============================================================================
# SIDEBAR - FILTROS
# ==============================================================================

st.sidebar.markdown("## 🔧 Filtros")

# Filtro de Status
status_options = ['Todos'] + list(df['status'].unique())
status_selecionado = st.sidebar.selectbox('Status', status_options)

# Filtro de Tipo de Chamado
tipo_options = ['Todos'] + list(df['tipo_chamado'].unique())
tipo_selecionado = st.sidebar.selectbox('Tipo de Chamado', tipo_options)

# Filtro de Setor
setor_options = ['Todos'] + list(df['setor'].unique())
setor_selecionado = st.sidebar.selectbox('Setor', setor_options)

# Filtro de Prioridade
prioridade_options = ['Todos'] + list(df['prioridade'].unique())
prioridade_selecionada = st.sidebar.selectbox('Prioridade', prioridade_options)

# Aplicar filtros
df_filtrado = df.copy()

if status_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['status'] == status_selecionado]
if tipo_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['tipo_chamado'] == tipo_selecionado]
if setor_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['setor'] == setor_selecionado]
if prioridade_selecionada != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['prioridade'] == prioridade_selecionada]

# Recalcular métricas com filtros
metricas_filtradas = calcular_metricas(df_filtrado)

# Informação da sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(f"📊 **Chamados exibidos:** {len(df_filtrado)}")
st.sidebar.markdown(f"📅 **Período:** Jan-Mar 2024")

# ==============================================================================
# CONTEÚDO PRINCIPAL
# ==============================================================================

# Título
st.markdown('<h1 class="main-title">📊 Dashboard de Suporte de TI</h1>', unsafe_allow_html=True)

# Subtítulo
st.markdown(
    '<p style="text-align: center; color: #666; margin-bottom: 30px;">'
    'Análise de chamados técnicos | Período: Janeiro a Março de 2024</p>',
    unsafe_allow_html=True
)

# ==============================================================================
# CARDS DE MÉTRICAS
# ==============================================================================

st.markdown('<p class="section-title">📈 Métricas Principais</p>', unsafe_allow_html=True)

# Criando 6 colunas para os cards
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        label="📋 Total",
        value=metricas_filtradas['total'],
        delta=None
    )

with col2:
    st.metric(
        label="🔴 Abertos",
        value=metricas_filtradas['abertos'],
        delta=f"{(metricas_filtradas['abertos']/metricas_filtradas['total']*100):.0f}%" if metricas_filtradas['total'] > 0 else "0%"
    )

with col3:
    st.metric(
        label="🟡 Em Andamento",
        value=metricas_filtradas['em_andamento'],
        delta=f"{(metricas_filtradas['em_andamento']/metricas_filtradas['total']*100):.0f}%" if metricas_filtradas['total'] > 0 else "0%"
    )

with col4:
    st.metric(
        label="🟢 Fechados",
        value=metricas_filtradas['fechados'],
        delta=f"{(metricas_filtradas['fechados']/metricas_filtradas['total']*100):.0f}%" if metricas_filtradas['total'] > 0 else "0%"
    )

with col5:
    tempo_medio_display = f"{metricas_filtradas['tempo_medio']:.1f}h" if pd.notna(metricas_filtradas['tempo_medio']) else "N/A"
    st.metric(
        label="⏱️ Tempo Médio",
        value=tempo_medio_display
    )

with col6:
    st.metric(
        label="🚨 Críticos",
        value=metricas_filtradas['criticos'],
        delta="Atenção!" if metricas_filtradas['criticos'] > 0 else None,
        delta_color="inverse"
    )

st.markdown("---")

# ==============================================================================
# GRÁFICOS - LINHA 1
# ==============================================================================

st.markdown('<p class="section-title">📊 Análise por Categoria</p>', unsafe_allow_html=True)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Gráfico de Pizza - Chamados por Status
    df_status = df_filtrado['status'].value_counts().reset_index()
    df_status.columns = ['Status', 'Quantidade']
    
    fig_status = px.pie(
        df_status,
        values='Quantidade',
        names='Status',
        title='Chamados por Status',
        color='Status',
        color_discrete_map={
            'Fechado': '#2ecc71',
            'Em Andamento': '#f1c40f',
            'Aberto': '#e74c3c'
        },
        hole=0.4  # Donut chart
    )
    fig_status.update_layout(
        font=dict(family="Arial", size=12),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )
    st.plotly_chart(fig_status, use_container_width=True)

with col_chart2:
    # Gráfico de Barras - Chamados por Tipo
    df_tipo = df_filtrado['tipo_chamado'].value_counts().reset_index()
    df_tipo.columns = ['Tipo', 'Quantidade']
    
    fig_tipo = px.bar(
        df_tipo,
        x='Tipo',
        y='Quantidade',
        title='Chamados por Tipo',
        color='Quantidade',
        color_continuous_scale='Viridis'
    )
    fig_tipo.update_layout(
        xaxis_title="Tipo de Chamado",
        yaxis_title="Quantidade",
        showlegend=False
    )
    st.plotly_chart(fig_tipo, use_container_width=True)

# ==============================================================================
# GRÁFICOS - LINHA 2
# ==============================================================================

col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    # Gráfico de Barras Horizontais - Chamados por Setor
    df_setor = df_filtrado['setor'].value_counts().reset_index()
    df_setor.columns = ['Setor', 'Quantidade']
    
    fig_setor = px.bar(
        df_setor,
        y='Setor',
        x='Quantidade',
        title='Chamados por Setor',
        orientation='h',
        color='Quantidade',
        color_continuous_scale='Plasma'
    )
    fig_setor.update_layout(
        yaxis_title="",
        xaxis_title="Quantidade de Chamados",
        showlegend=False
    )
    st.plotly_chart(fig_setor, use_container_width=True)

with col_chart4:
    # Gráfico de Pizza - Chamados por Prioridade
    df_prioridade = df_filtrado['prioridade'].value_counts().reset_index()
    df_prioridade.columns = ['Prioridade', 'Quantidade']
    
    fig_prioridade = px.pie(
        df_prioridade,
        values='Quantidade',
        names='Prioridade',
        title='Chamados por Prioridade',
        color='Prioridade',
        color_discrete_map={
            'Baixa': '#3498db',
            'Media': '#2ecc71',
            'Alta': '#f39c12',
            'Critica': '#e74c3c'
        }
    )
    fig_prioridade.update_layout(
        font=dict(family="Arial", size=12),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )
    st.plotly_chart(fig_prioridade, use_container_width=True)

st.markdown("---")

# ==============================================================================
# GRÁFICO DE TEMPO MÉDIO POR PRIORIDADE
# ==============================================================================

st.markdown('<p class="section-title">⏱️ Análise de Tempo de Atendimento</p>', unsafe_allow_html=True)

col_tempo1, col_tempo2 = st.columns(2)

with col_tempo1:
    # Tempo médio por prioridade
    df_tempo_prioridade = df_filtrado.groupby('prioridade')['tempo_atendimento_horas'].mean().reset_index()
    df_tempo_prioridade.columns = ['Prioridade', 'Tempo Médio (h)']
    df_tempo_prioridade = df_tempo_prioridade.dropna()
    
    # Ordenar por tempo
    ordem_prioridade = ['Critica', 'Alta', 'Media', 'Baixa']
    df_tempo_prioridade['Prioridade'] = pd.Categorical(
        df_tempo_prioridade['Prioridade'], 
        categories=ordem_prioridade, 
        ordered=True
    )
    df_tempo_prioridade = df_tempo_prioridade.sort_values('Prioridade')
    
    fig_tempo = px.bar(
        df_tempo_prioridade,
        x='Prioridade',
        y='Tempo Médio (h)',
        title='Tempo Médio de Atendimento por Prioridade',
        color='Prioridade',
        color_discrete_map={
            'Baixa': '#3498db',
            'Media': '#2ecc71',
            'Alta': '#f39c12',
            'Critica': '#e74c3c'
        }
    )
    fig_tempo.update_layout(showlegend=False)
    st.plotly_chart(fig_tempo, use_container_width=True)

with col_tempo2:
    # Performance por Responsável
    df_responsavel = df_filtrado.groupby('responsavel').agg({
        'id_chamado': 'count',
        'tempo_atendimento_horas': 'mean'
    }).reset_index()
    df_responsavel.columns = ['Responsável', 'Total Chamados', 'Tempo Médio (h)']
    df_responsavel = df_responsavel.dropna()
    
    fig_responsavel = px.bar(
        df_responsavel,
        x='Responsável',
        y='Total Chamados',
        title='Chamados por Responsável',
        color='Tempo Médio (h)',
        color_continuous_scale='RdYlGn_r'  # Verde = rápido, Vermelho = lento
    )
    fig_responsavel.update_layout(
        xaxis_title="",
        yaxis_title="Quantidade de Chamados"
    )
    st.plotly_chart(fig_responsavel, use_container_width=True)

st.markdown("---")

# ==============================================================================
# TABELA DE DADOS
# ==============================================================================

st.markdown('<p class="section-title">📋 Dados Detalhados</p>', unsafe_allow_html=True)

# Checkbox para mostrar/esconder tabela
if st.checkbox('Mostrar tabela de dados', value=False):
    # Seletor de colunas
    colunas_disponiveis = df_filtrado.columns.tolist()
    colunas_selecionadas = st.multiselect(
        'Selecione as colunas:',
        colunas_disponiveis,
        default=['id_chamado', 'data_abertura', 'status', 'tipo_chamado', 'setor', 'prioridade', 'responsavel']
    )
    
    if colunas_selecionadas:
        st.dataframe(
            df_filtrado[colunas_selecionadas].sort_values('data_abertura', ascending=False),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("Selecione pelo menos uma coluna para exibir.")

# ==============================================================================
# RODAPÉ
# ==============================================================================

st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #888; font-size: 0.9rem;">'
    '📊 Dashboard de Suporte de TI | Desenvolvido com Streamlit e Python<br>'
    f'Última atualização: {datetime.now().strftime("%d/%m/%Y %H:%M")}'
    '</p>',
    unsafe_allow_html=True
)
