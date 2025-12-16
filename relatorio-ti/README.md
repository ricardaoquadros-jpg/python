# 📊 Automação de Relatório de Suporte de TI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Script Python para automatizar a geração de relatórios de suporte de TI, 
com dashboard interativo para visualização de métricas.**

[Funcionalidades](#-funcionalidades) •
[Instalação](#-instalação) •
[Como Usar](#-como-usar) •
[Screenshots](#-screenshots) •
[Tecnologias](#-tecnologias)

</div>

---

## ✨ Funcionalidades

### 📄 Gerador de Relatório (`gerador_relatorio.py`)
- ✅ Leitura de dados de arquivo CSV
- ✅ Tratamento automático de dados (datas, valores nulos)
- ✅ Cálculo de 8 métricas de negócio
- ✅ Exportação para Excel com 7 abas organizadas

### 🌐 Dashboard Interativo (`dashboard.py`)
- ✅ 6 cards de métricas em tempo real
- ✅ 4 filtros interativos (status, tipo, setor, prioridade)
- ✅ 6 gráficos Plotly (pizza, barras, horizontais)
- ✅ Tabela de dados com seletor de colunas
- ✅ Design responsivo e moderno

---

## � Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/relatorio-ti-python.git

# 2. Entre na pasta do projeto
cd relatorio-ti-python

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## 🚀 Como Usar

### Gerar Relatório Excel

```bash
python gerador_relatorio.py
```

Isso irá:
1. Ler os dados de `chamados_ti.csv`
2. Processar e calcular métricas
3. Gerar `relatorio_ti.xlsx` com 7 abas

### Executar Dashboard

```bash
streamlit run dashboard.py
```

Acesse em: **http://localhost:8501**

---

## 📸 Screenshots

### Dashboard Streamlit

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Dashboard de Suporte de TI                              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │   120    │  │    15    │  │     5    │  │  4.5h    │    │
│  │  Total   │  │ Abertos  │  │Em Andmto │  │ Tempo Méd│    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                             │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  │
│  │   📊 Gráfico Pizza      │  │   📈 Gráfico Barras     │  │
│  │   Chamados por Tipo     │  │   Chamados por Setor    │  │
│  └─────────────────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## � Métricas Calculadas

| Métrica | Descrição |
|---------|-----------|
| Total de chamados | Contagem geral de tickets |
| Por status | Aberto, Em Andamento, Fechado |
| Por tipo | Hardware, Software, Rede, Acesso |
| Tempo médio | Média de horas para resolução |
| Por setor | Demanda por departamento |
| Por prioridade | Baixa, Média, Alta, Crítica |
| Por responsável | Carga de trabalho por técnico |
| Tempo por prioridade | SLA por nível de urgência |

---

## � Tecnologias

| Tecnologia | Uso |
|------------|-----|
| **Python 3.12** | Linguagem principal |
| **Pandas** | Manipulação e análise de dados |
| **OpenPyXL** | Exportação para Excel |
| **Streamlit** | Dashboard web interativo |
| **Plotly** | Gráficos interativos |

---

## 📁 Estrutura do Projeto

```
relatorio-ti/
├── chamados_ti.csv        # Dataset simulado (120 chamados)
├── gerador_relatorio.py   # Script de geração do relatório
├── dashboard.py           # Dashboard Streamlit
├── relatorio_ti.xlsx      # Relatório gerado (output)
├── requirements.txt       # Dependências Python
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Esta documentação
```

---

## 📚 O que aprendi neste projeto

- **Pandas**: Leitura de CSV, DataFrames, agrupamentos, agregações
- **ETL**: Extract → Transform → Load
- **Métricas de TI**: KPIs relevantes para Service Desk
- **Streamlit**: Criação de dashboards web com Python
- **Plotly**: Gráficos interativos e responsivos
- **Boas práticas**: Código modular, funções, documentação

---

## 🔮 Evoluções Futuras

- [ ] Integração com APIs (Asana, Jira, ServiceNow)
- [ ] Agendamento automático (cron/Task Scheduler)
- [ ] Envio de relatórios por email
- [ ] Conexão com banco de dados
- [ ] Deploy do dashboard na nuvem (Streamlit Cloud)

---

## 📝 Licença

Este projeto é de uso livre para fins educacionais e profissionais.

---

<div align="center">

**Desenvolvido como projeto de aprendizado em Python aplicado a dados**

⭐ Se este projeto te ajudou, deixe uma estrela!

</div>
