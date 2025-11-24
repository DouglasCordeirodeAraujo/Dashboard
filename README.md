# Dashboard de Benchmark de GPUs

Este projeto faz parte da disciplina **Eletiva: Monitoramento de Sistemas** e tem como objetivo criar um dashboard interativo usando **Python**, **Pandas** e **Streamlit** para analisar desempenho e custo-benefício de GPUs.

## 📁 Arquivos do Projeto

- `Dashboard.py` — Código principal do dashboard  
- `gpu_benchmark_60_clean.csv` — Dataset utilizado  
- `requirements.txt` — Dependências do projeto  
- `README.md` — Documentação simples do projeto

## 🚀 Como Executar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute o dashboard:

```streamlit run Dashboard.py
```

📊 Funcionalidades

Exibição de métricas principais

Gráficos de desempenho, preço e custo-benefício

Filtros interativos

Tabela com dados brutos

Análise detalhada por GPU selecionada

🧠 Conclusão

O dashboard permite visualizar facilmente quais GPUs entregam melhor desempenho e custo-benefício, auxiliando na comparação entre diferentes modelos.