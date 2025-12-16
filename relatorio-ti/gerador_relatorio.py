"""
==============================================================================
GERADOR DE RELATÓRIO DE SUPORTE DE TI
==============================================================================
Autor: [Seu Nome]
Data: Dezembro 2024
Descrição: Script Python para automatizar a geração de relatórios de suporte
           de TI a partir de uma base de chamados em CSV.

O QUE VOCÊ VAI APRENDER NESTE SCRIPT:
- Como ler arquivos CSV com Pandas
- O que é um DataFrame e como manipulá-lo
- Como tratar dados (datas, valores nulos)
- Como calcular métricas de negócio
- Como exportar dados para Excel com múltiplas abas
==============================================================================
"""

# ==============================================================================
# ETAPA 3: IMPORTAÇÃO DE BIBLIOTECAS
# ==============================================================================
# 
# O que é uma biblioteca?
# Uma biblioteca é um conjunto de código pronto que podemos reutilizar.
# Em vez de escrever tudo do zero, usamos bibliotecas para tarefas comuns.
#
# Pandas: Biblioteca principal para análise de dados em Python
# - Lê arquivos CSV, Excel, JSON, etc.
# - Cria estruturas chamadas DataFrames (como uma tabela do Excel)
# - Permite filtrar, agrupar e calcular dados facilmente

import pandas as pd  # 'pd' é um apelido (alias) para facilitar a digitação

# ==============================================================================
# ETAPA 3: LEITURA DOS DADOS
# ==============================================================================
#
# O que estamos fazendo: Carregando os dados do arquivo CSV para a memória
# Por que: Precisamos dos dados na memória do Python para manipulá-los
# O que você aprende: Como usar pd.read_csv() para ler arquivos

def carregar_dados(caminho_arquivo):
    """
    Função para carregar dados de um arquivo CSV.
    
    Parâmetros:
        caminho_arquivo (str): Caminho para o arquivo CSV
        
    Retorna:
        DataFrame: Tabela com os dados do arquivo
        
    O que é um DataFrame?
    - É como uma planilha do Excel dentro do Python
    - Tem linhas (cada chamado) e colunas (informações do chamado)
    - Permite operações como filtros, somas, médias, etc.
    """
    print("📂 Carregando dados do arquivo CSV...")
    
    # pd.read_csv() lê o arquivo e cria um DataFrame
    # O arquivo precisa estar no mesmo diretório do script
    # ou você precisa passar o caminho completo
    df = pd.read_csv(caminho_arquivo)
    
    print(f"✅ Dados carregados com sucesso!")
    print(f"   Total de registros: {len(df)}")  # len() conta as linhas
    print(f"   Total de colunas: {len(df.columns)}")  # df.columns lista as colunas
    
    return df


def inspecionar_dados(df):
    """
    Função para inspecionar os dados carregados.
    
    O que estamos fazendo: Verificando a estrutura e qualidade dos dados
    Por que: Antes de trabalhar com dados, precisamos entendê-los
    O que você aprende: Métodos de inspeção do Pandas
    
    Métodos úteis:
    - head(): Mostra as primeiras 5 linhas
    - info(): Mostra tipos de dados e valores nulos
    - describe(): Mostra estatísticas numéricas
    """
    print("\n" + "="*60)
    print("📊 INSPEÇÃO DOS DADOS")
    print("="*60)
    
    # head() - Primeiras linhas
    # Por que usar: Para ter uma visão rápida do formato dos dados
    print("\n🔍 Primeiras 5 linhas (head):")
    print(df.head())
    
    # info() - Informações sobre o DataFrame
    # Por que usar: Para ver tipos de dados e identificar valores nulos
    print("\n📋 Informações do DataFrame (info):")
    print(df.info())
    
    # describe() - Estatísticas
    # Por que usar: Para ter uma visão estatística rápida dos números
    # Nota: Só funciona bem com colunas numéricas
    print("\n📈 Estatísticas descritivas (describe):")
    print(df.describe())


# ==============================================================================
# ETAPA 4: TRATAMENTO DE DADOS
# ==============================================================================
#
# O que estamos fazendo: Preparando os dados para análise
# Por que: Dados "brutos" geralmente precisam de limpeza e transformação
# O que você aprende: Conversão de tipos, criação de colunas, tratamento de nulos

def tratar_dados(df):
    """
    Função para tratar e limpar os dados.
    
    Tratamentos aplicados:
    1. Conversão de datas (string → datetime)
    2. Criação da coluna de tempo de atendimento
    3. Tratamento de valores nulos
    4. Padronização de texto
    """
    print("\n" + "="*60)
    print("🔧 TRATAMENTO DE DADOS")
    print("="*60)
    
    # Criar uma cópia para não modificar o original
    # Boa prática: sempre trabalhe em cópias dos dados
    df_tratado = df.copy()
    
    # -------------------------------------------------------------------------
    # TRATAMENTO 1: Conversão de Datas
    # -------------------------------------------------------------------------
    # O que: Converter strings de data para tipo datetime do Python
    # Por que: Para fazer cálculos com datas (diferença de dias, horas, etc.)
    # Como: pd.to_datetime() converte automaticamente
    
    print("\n📅 Convertendo colunas de data...")
    
    # Convertendo data_abertura
    # O Pandas reconhece automaticamente o formato "AAAA-MM-DD HH:MM:SS"
    df_tratado['data_abertura'] = pd.to_datetime(df_tratado['data_abertura'])
    
    # Convertendo data_fechamento
    # errors='coerce': Se encontrar valor inválido, coloca NaT (Not a Time)
    # Por que usamos coerce: Chamados abertos não têm data de fechamento (vazio)
    df_tratado['data_fechamento'] = pd.to_datetime(
        df_tratado['data_fechamento'], 
        errors='coerce'  # Valores vazios viram NaT (nulo para datas)
    )
    
    print("   ✅ Colunas de data convertidas")
    
    # -------------------------------------------------------------------------
    # TRATAMENTO 2: Criação da Coluna de Tempo de Atendimento
    # -------------------------------------------------------------------------
    # O que: Calcular quanto tempo cada chamado levou para ser resolvido
    # Por que: Esta é uma métrica importante (SLA, eficiência da equipe)
    # Como: Subtrair data_fechamento - data_abertura
    
    print("\n⏱️ Calculando tempo de atendimento...")
    
    # A subtração de datas cria um objeto Timedelta
    # .dt.total_seconds() converte para segundos
    # / 3600 converte para horas
    df_tratado['tempo_atendimento_horas'] = (
        (df_tratado['data_fechamento'] - df_tratado['data_abertura'])
        .dt.total_seconds() / 3600  # Convertendo segundos para horas
    )
    
    # Arredondando para 2 casas decimais para melhor visualização
    df_tratado['tempo_atendimento_horas'] = df_tratado['tempo_atendimento_horas'].round(2)
    
    print("   ✅ Coluna 'tempo_atendimento_horas' criada")
    
    # -------------------------------------------------------------------------
    # TRATAMENTO 3: Tratamento de Valores Nulos
    # -------------------------------------------------------------------------
    # O que: Identificar e documentar onde há valores faltantes
    # Por que: Valores nulos podem causar erros ou distorcer métricas
    # Observação: Para chamados abertos, tempo_atendimento será NaN (nulo)
    #             Isso é ESPERADO, não é um erro!
    
    print("\n🔍 Verificando valores nulos...")
    
    # isnull().sum() conta quantos valores nulos em cada coluna
    nulos = df_tratado.isnull().sum()
    print("   Valores nulos por coluna:")
    print(nulos[nulos > 0].to_string() if nulos.sum() > 0 else "   Nenhum valor nulo encontrado")
    
    # -------------------------------------------------------------------------
    # TRATAMENTO 4: Padronização de Texto (Status)
    # -------------------------------------------------------------------------
    # O que: Garantir que os valores de texto estejam padronizados
    # Por que: "aberto", "Aberto" e "ABERTO" devem ser tratados como iguais
    # Como: Usando .str.strip() para remover espaços extras
    
    print("\n📝 Padronizando texto...")
    
    # .str.strip() remove espaços no início e fim
    df_tratado['status'] = df_tratado['status'].str.strip()
    df_tratado['tipo_chamado'] = df_tratado['tipo_chamado'].str.strip()
    df_tratado['setor'] = df_tratado['setor'].str.strip()
    df_tratado['prioridade'] = df_tratado['prioridade'].str.strip()
    df_tratado['responsavel'] = df_tratado['responsavel'].str.strip()
    
    print("   ✅ Colunas de texto padronizadas")
    
    print("\n✅ Tratamento de dados concluído!")
    
    return df_tratado


# ==============================================================================
# ETAPA 5: CÁLCULO DE MÉTRICAS
# ==============================================================================
#
# O que estamos fazendo: Calculando indicadores de desempenho (KPIs)
# Por que: Métricas permitem avaliar a performance e tomar decisões
# O que você aprende: Agregações, agrupamentos e estatísticas com Pandas

def calcular_metricas(df):
    """
    Função para calcular métricas do relatório.
    
    Métricas calculadas:
    1. Total de chamados
    2. Chamados por status
    3. Chamados por tipo
    4. Tempo médio de atendimento
    5. Chamados por setor
    6. Chamados por prioridade
    7. Chamados por responsável
    """
    print("\n" + "="*60)
    print("📊 CÁLCULO DE MÉTRICAS")
    print("="*60)
    
    # Dicionário para armazenar todas as métricas
    # Usamos dicionário para organizar os resultados
    metricas = {}
    
    # -------------------------------------------------------------------------
    # MÉTRICA 1: Total de Chamados
    # -------------------------------------------------------------------------
    # O que: Contar quantos chamados existem no total
    # Por que: É o número mais básico e importante
    # Como: len() conta o número de linhas
    
    total_chamados = len(df)
    metricas['total_chamados'] = total_chamados
    print(f"\n📌 Total de chamados: {total_chamados}")
    
    # -------------------------------------------------------------------------
    # MÉTRICA 2: Chamados por Status
    # -------------------------------------------------------------------------
    # O que: Contar quantos chamados em cada status (Aberto, Em Andamento, Fechado)
    # Por que: Para saber a carga de trabalho atual
    # Como: value_counts() conta valores únicos
    
    por_status = df['status'].value_counts()
    metricas['por_status'] = por_status
    print(f"\n📌 Chamados por Status:")
    for status, quantidade in por_status.items():
        percentual = (quantidade / total_chamados) * 100
        print(f"   • {status}: {quantidade} ({percentual:.1f}%)")
    
    # -------------------------------------------------------------------------
    # MÉTRICA 3: Chamados por Tipo
    # -------------------------------------------------------------------------
    # O que: Contar chamados de cada categoria (Hardware, Software, Rede, Acesso)
    # Por que: Para identificar qual tipo de problema é mais comum
    # Como: value_counts() novamente
    
    por_tipo = df['tipo_chamado'].value_counts()
    metricas['por_tipo'] = por_tipo
    print(f"\n📌 Chamados por Tipo:")
    for tipo, quantidade in por_tipo.items():
        percentual = (quantidade / total_chamados) * 100
        print(f"   • {tipo}: {quantidade} ({percentual:.1f}%)")
    
    # -------------------------------------------------------------------------
    # MÉTRICA 4: Tempo Médio de Atendimento
    # -------------------------------------------------------------------------
    # O que: Calcular a média de tempo para resolver chamados
    # Por que: Indicador de eficiência (SLA)
    # Como: .mean() calcula a média, ignorando valores NaN automaticamente
    
    # Filtrando apenas chamados fechados (que têm tempo de atendimento)
    tempo_medio = df['tempo_atendimento_horas'].mean()
    tempo_min = df['tempo_atendimento_horas'].min()
    tempo_max = df['tempo_atendimento_horas'].max()
    
    metricas['tempo_medio'] = tempo_medio
    metricas['tempo_min'] = tempo_min
    metricas['tempo_max'] = tempo_max
    
    print(f"\n📌 Tempo de Atendimento (apenas chamados fechados):")
    print(f"   • Médio: {tempo_medio:.2f} horas")
    print(f"   • Mínimo: {tempo_min:.2f} horas")
    print(f"   • Máximo: {tempo_max:.2f} horas")
    
    # -------------------------------------------------------------------------
    # MÉTRICA 5: Chamados por Setor
    # -------------------------------------------------------------------------
    # O que: Contar chamados de cada departamento
    # Por que: Identificar quais setores mais demandam suporte
    # Como: value_counts() + sort_values() para ordenar
    
    por_setor = df['setor'].value_counts()
    metricas['por_setor'] = por_setor
    print(f"\n📌 Chamados por Setor:")
    for setor, quantidade in por_setor.items():
        percentual = (quantidade / total_chamados) * 100
        print(f"   • {setor}: {quantidade} ({percentual:.1f}%)")
    
    # -------------------------------------------------------------------------
    # MÉTRICA 6: Chamados por Prioridade
    # -------------------------------------------------------------------------
    # O que: Distribuição por urgência
    # Por que: Para entender a criticidade média dos chamados
    
    por_prioridade = df['prioridade'].value_counts()
    metricas['por_prioridade'] = por_prioridade
    print(f"\n📌 Chamados por Prioridade:")
    for prioridade, quantidade in por_prioridade.items():
        percentual = (quantidade / total_chamados) * 100
        print(f"   • {prioridade}: {quantidade} ({percentual:.1f}%)")
    
    # -------------------------------------------------------------------------
    # MÉTRICA 7: Chamados por Responsável
    # -------------------------------------------------------------------------
    # O que: Carga de trabalho por técnico
    # Por que: Para balancear a equipe
    
    por_responsavel = df['responsavel'].value_counts()
    metricas['por_responsavel'] = por_responsavel
    print(f"\n📌 Chamados por Responsável:")
    for responsavel, quantidade in por_responsavel.items():
        percentual = (quantidade / total_chamados) * 100
        print(f"   • {responsavel}: {quantidade} ({percentual:.1f}%)")
    
    # -------------------------------------------------------------------------
    # MÉTRICA 8: Tempo Médio por Prioridade
    # -------------------------------------------------------------------------
    # O que: Tempo de atendimento agrupado por prioridade
    # Por que: Chamados críticos devem ser resolvidos mais rápido
    # Como: groupby() + mean() para calcular média por grupo
    
    tempo_por_prioridade = df.groupby('prioridade')['tempo_atendimento_horas'].mean().round(2)
    metricas['tempo_por_prioridade'] = tempo_por_prioridade
    print(f"\n📌 Tempo Médio por Prioridade (horas):")
    for prioridade, tempo in tempo_por_prioridade.items():
        print(f"   • {prioridade}: {tempo:.2f} horas")
    
    print("\n✅ Cálculo de métricas concluído!")
    
    return metricas


# ==============================================================================
# ETAPA 6: GERAÇÃO DO RELATÓRIO EXCEL
# ==============================================================================
#
# O que estamos fazendo: Exportando os resultados para um arquivo Excel
# Por que: Excel é o formato padrão em empresas para relatórios
# O que você aprende: Como usar ExcelWriter para criar múltiplas abas

def gerar_relatorio_excel(df, metricas, nome_arquivo='relatorio_ti.xlsx'):
    """
    Função para gerar o relatório final em Excel.
    
    Abas criadas:
    1. Resumo - Métricas principais
    2. Dados_Completos - Base de dados tratada
    3. Por_Status - Análise por status
    4. Por_Tipo - Análise por tipo de chamado
    5. Por_Setor - Análise por departamento
    6. Por_Prioridade - Análise por urgência
    7. Por_Responsavel - Carga por técnico
    """
    print("\n" + "="*60)
    print("📑 GERAÇÃO DO RELATÓRIO EXCEL")
    print("="*60)
    
    # ExcelWriter permite criar um arquivo Excel com múltiplas abas
    # 'with' garante que o arquivo será fechado corretamente
    # engine='openpyxl' é a biblioteca que escreve o arquivo
    
    with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
        
        # ---------------------------------------------------------------------
        # ABA 1: RESUMO
        # ---------------------------------------------------------------------
        # Criando um DataFrame com as métricas resumidas
        print("\n📄 Criando aba 'Resumo'...")
        
        resumo_data = {
            'Métrica': [
                'Total de Chamados',
                'Chamados Abertos',
                'Chamados Em Andamento',
                'Chamados Fechados',
                'Tempo Médio de Atendimento (horas)',
                'Tempo Mínimo de Atendimento (horas)',
                'Tempo Máximo de Atendimento (horas)'
            ],
            'Valor': [
                metricas['total_chamados'],
                metricas['por_status'].get('Aberto', 0),
                metricas['por_status'].get('Em Andamento', 0),
                metricas['por_status'].get('Fechado', 0),
                round(metricas['tempo_medio'], 2) if pd.notna(metricas['tempo_medio']) else 'N/A',
                round(metricas['tempo_min'], 2) if pd.notna(metricas['tempo_min']) else 'N/A',
                round(metricas['tempo_max'], 2) if pd.notna(metricas['tempo_max']) else 'N/A'
            ]
        }
        df_resumo = pd.DataFrame(resumo_data)
        
        # to_excel() escreve o DataFrame em uma aba
        # index=False evita escrever o índice numérico
        df_resumo.to_excel(writer, sheet_name='Resumo', index=False)
        
        # ---------------------------------------------------------------------
        # ABA 2: DADOS COMPLETOS
        # ---------------------------------------------------------------------
        print("📄 Criando aba 'Dados_Completos'...")
        df.to_excel(writer, sheet_name='Dados_Completos', index=False)
        
        # ---------------------------------------------------------------------
        # ABA 3: POR STATUS
        # ---------------------------------------------------------------------
        print("📄 Criando aba 'Por_Status'...")
        df_status = metricas['por_status'].reset_index()
        df_status.columns = ['Status', 'Quantidade']
        df_status['Percentual'] = (df_status['Quantidade'] / metricas['total_chamados'] * 100).round(1)
        df_status.to_excel(writer, sheet_name='Por_Status', index=False)
        
        # ---------------------------------------------------------------------
        # ABA 4: POR TIPO
        # ---------------------------------------------------------------------
        print("📄 Criando aba 'Por_Tipo'...")
        df_tipo = metricas['por_tipo'].reset_index()
        df_tipo.columns = ['Tipo', 'Quantidade']
        df_tipo['Percentual'] = (df_tipo['Quantidade'] / metricas['total_chamados'] * 100).round(1)
        df_tipo.to_excel(writer, sheet_name='Por_Tipo', index=False)
        
        # ---------------------------------------------------------------------
        # ABA 5: POR SETOR
        # ---------------------------------------------------------------------
        print("📄 Criando aba 'Por_Setor'...")
        df_setor = metricas['por_setor'].reset_index()
        df_setor.columns = ['Setor', 'Quantidade']
        df_setor['Percentual'] = (df_setor['Quantidade'] / metricas['total_chamados'] * 100).round(1)
        df_setor.to_excel(writer, sheet_name='Por_Setor', index=False)
        
        # ---------------------------------------------------------------------
        # ABA 6: POR PRIORIDADE
        # ---------------------------------------------------------------------
        print("📄 Criando aba 'Por_Prioridade'...")
        df_prioridade = metricas['por_prioridade'].reset_index()
        df_prioridade.columns = ['Prioridade', 'Quantidade']
        df_prioridade['Percentual'] = (df_prioridade['Quantidade'] / metricas['total_chamados'] * 100).round(1)
        
        # Adicionando tempo médio por prioridade
        df_prioridade['Tempo_Medio_Horas'] = df_prioridade['Prioridade'].map(
            metricas['tempo_por_prioridade']
        )
        df_prioridade.to_excel(writer, sheet_name='Por_Prioridade', index=False)
        
        # ---------------------------------------------------------------------
        # ABA 7: POR RESPONSÁVEL
        # ---------------------------------------------------------------------
        print("📄 Criando aba 'Por_Responsavel'...")
        df_responsavel = metricas['por_responsavel'].reset_index()
        df_responsavel.columns = ['Responsavel', 'Quantidade']
        df_responsavel['Percentual'] = (df_responsavel['Quantidade'] / metricas['total_chamados'] * 100).round(1)
        df_responsavel.to_excel(writer, sheet_name='Por_Responsavel', index=False)
    
    print(f"\n✅ Relatório gerado com sucesso: {nome_arquivo}")
    print(f"   📊 Total de abas criadas: 7")
    
    return nome_arquivo


# ==============================================================================
# ETAPA 7: FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================
#
# O que estamos fazendo: Organizando a execução de todas as etapas
# Por que: Boa prática - separar a lógica em funções e ter um ponto de entrada
# O que você aprende: Organização de código e a convenção if __name__ == "__main__"

def main():
    """
    Função principal que orquestra todo o processamento.
    
    Por que usar uma função main()?
    - Organização: Todo o fluxo fica claro em um lugar
    - Testabilidade: Pode ser chamada de outros scripts
    - Convenção: É padrão em Python
    """
    print("\n" + "="*60)
    print("🚀 GERADOR DE RELATÓRIO DE SUPORTE DE TI")
    print("="*60)
    print("Iniciando processamento...\n")
    
    # Definir caminhos dos arquivos
    arquivo_entrada = 'chamados_ti.csv'
    arquivo_saida = 'relatorio_ti.xlsx'
    
    # ETAPA 3: Carregar dados
    df = carregar_dados(arquivo_entrada)
    
    # Opcional: Inspecionar dados (descomente para ver detalhes)
    # inspecionar_dados(df)
    
    # ETAPA 4: Tratar dados
    df_tratado = tratar_dados(df)
    
    # ETAPA 5: Calcular métricas
    metricas = calcular_metricas(df_tratado)
    
    # ETAPA 6: Gerar relatório Excel
    gerar_relatorio_excel(df_tratado, metricas, arquivo_saida)
    
    print("\n" + "="*60)
    print("✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print(f"\n📁 Arquivo gerado: {arquivo_saida}")
    print("   Abra o arquivo Excel para visualizar o relatório completo.\n")


# ==============================================================================
# PONTO DE ENTRADA DO SCRIPT
# ==============================================================================
# 
# O que é if __name__ == "__main__"?
# 
# Quando você executa um script Python diretamente (python script.py),
# a variável __name__ recebe o valor "__main__".
# 
# Quando você importa o script de outro arquivo (import script),
# a variável __name__ recebe o nome do arquivo ("script").
# 
# Por que usar isso?
# - O código dentro deste if só roda se você executar o arquivo diretamente
# - Se alguém importar suas funções, o main() não roda automaticamente
# - É uma boa prática em Python

if __name__ == "__main__":
    main()
