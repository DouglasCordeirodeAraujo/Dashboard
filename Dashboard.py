import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ================================
# CONFIGURAÇÃO DO STREAMLIT
# ================================
st.set_page_config(
    page_title="Dashboard GPUs",
    layout="wide"
)

# ================================
# CARREGAR DATASET
# ================================
df = pd.read_csv("gpu_benchmark_60_clean.csv")

# ================================
# CRIAÇÃO DE MÉTRICAS
# ================================
df["fps_medio"] = df["g3d_mark"]
df["custo_beneficio"] = df["g3d_mark"] / df["price_usd"]

# ================================
# TÍTULO E INTRODUÇÃO
# ================================
st.title("📊 Dashboard Interativo de Benchmark de GPUs")
st.write("""
Este dashboard apresenta uma análise completa do desempenho e custo-benefício
das principais GPUs do mercado. Os dados incluem pontuação G3D Mark, preço em dólares
e consumo energético (TDP).
""")

# ================================
# MÉTRICAS PRINCIPAIS
# ================================
col1, col2, col3 = st.columns(3)

col1.metric("🎮 FPS Médio (G3D Mark)", f"{df['fps_medio'].mean():.2f}")
col2.metric("💲 Preço Médio (USD)", f"$ {df['price_usd'].mean():.2f}")
col3.metric("🔥 Melhor Custo-Benefício", df.loc[df["custo_beneficio"].idxmax(), "gpu_name"])

# ================================
# FILTROS INTERATIVOS
# ================================
st.sidebar.header("Filtros")

# Filtro por GPU
gpu_select = st.sidebar.selectbox(
    "Selecione uma GPU para análise detalhada:",
    df["gpu_name"].unique()
)

# Filtro por faixa de preço
price_min = df["price_usd"].min()
price_max = df["price_usd"].max()

price_filter = st.sidebar.slider(
    "Selecione uma faixa de preço (USD):",
    min_value=int(price_min),
    max_value=int(price_max),
    value=(int(price_min), int(price_max))
)

# Aplicando filtros
df_filtered = df[
    (df["price_usd"] >= price_filter[0]) &
    (df["price_usd"] <= price_filter[1])
]

# ================================
# GRÁFICO 1: DESEMPENHO DAS GPUs
# ================================
st.subheader("📈 Desempenho (G3D Mark) por GPU")

fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.bar(df_filtered["gpu_name"], df_filtered["g3d_mark"])
ax1.set_ylabel("Pontuação G3D Mark")
ax1.set_xticklabels(df_filtered["gpu_name"], rotation=75, ha='right')
st.pyplot(fig1)

# ================================
# GRÁFICO 2: PREÇO × DESEMPENHO
# ================================
st.subheader("💲 Preço (USD) vs. Desempenho (G3D Mark)")

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.scatter(df_filtered["price_usd"], df_filtered["g3d_mark"])
ax2.set_xlabel("Preço (USD)")
ax2.set_ylabel("G3D Mark")
st.pyplot(fig2)

# ================================
# GRÁFICO 3: CUSTO-BENEFÍCIO
# ================================
st.subheader("🔥 Índice de Custo-Benefício (G3D Mark / USD)")

fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.bar(df_filtered["gpu_name"], df_filtered["custo_beneficio"])
ax3.set_ylabel("Custo-Benefício")
ax3.set_xticklabels(df_filtered["gpu_name"], rotation=75, ha='right')
st.pyplot(fig3)

# ================================
# ANÁLISE DETALHADA (GPU SELECIONADA)
# ================================
st.subheader(f"🔍 Análise Detalhada: **{gpu_select}**")

gpu_data = df[df["gpu_name"] == gpu_select].iloc[0]

st.write(f"""
### 📌 Informações Técnicas
- **G3D Mark:** {gpu_data['g3d_mark']}
- **Preço (USD):** ${gpu_data['price_usd']}
- **TDP (Watts):** {gpu_data['tdp_watts']} W
- **Custo-Benefício:** {gpu_data['custo_beneficio']:.4f}
""")

# ================================
# TABELA COMPLETA
# ================================
st.subheader("📄 Dados Brutos")
st.dataframe(df)


st.write("""
### 📌 Conclusões Gerais
A análise mostrou que GPUs com maior pontuação G3D Mark tendem a ter preços proporcionais, mas alguns modelos apresentam excelente custo-benefício, como a RTX 3060 Ti e a RX 5700 XT. 
O gráfico de preço x desempenho revela uma relação quase linear, porém com pontos fora da curva que entregam bom desempenho por menor custo. 
O filtro interativo permite avaliar facilmente qual GPU se encaixa melhor no orçamento e necessidade de performance.
""")
