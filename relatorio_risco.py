# ===== CONFIGURAÇÕES INICIAIS =====

import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import yfinance as yf

np.random.seed(42)

tickers_ativos = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "WEGE3.SA"]
ticker_bench   = "BOVA11.SA"
inicio         = "2019-01-01"
fim            = "2024-12-31"

todos_tickers = tickers_ativos + [ticker_bench]
dados = yf.download(todos_tickers, start=inicio, end=fim, auto_adjust=True, progress=False)["Close"]
dados = dados.dropna()


# ===== TAREFA 1: Value at Risk =====

# 1 - log-retornos diários e posição distribuida igualmente
posicao        = 100_000.0
pesos_ew       = np.array([0.25, 0.25, 0.25, 0.25])

retornos      = np.log(dados / dados.shift(1)).dropna()
ret_ativos    = retornos[tickers_ativos]
ret_benchmark = retornos[ticker_bench]
retornos_port      = ret_ativos @ pesos_ew

# 2 - VaR 95% e 99% pelos 3 métodos
# Método Histórico
var95_hist = np.percentile(retornos_port, 5)
var99_hist = np.percentile(retornos_port, 1)

# Método Paramétrico (Normal)
mu    = retornos_port.mean()
sigma = retornos_port.std()
var95_norm = stats.norm.ppf(0.05, mu, sigma)
var99_norm = stats.norm.ppf(0.01, mu, sigma)

# Método Monte Carlo
simulacoes = np.random.normal(mu, sigma, 50000)
var95_mc   = np.percentile(simulacoes, 5)
var99_mc   = np.percentile(simulacoes, 1)

# 3 - Apresentação de resultados
print("===== TAREFA 1: VaR =====")
tabela_var = pd.DataFrame({
    "Método":       ["Histórico", "Paramétrico (Normal)", "Monte Carlo"],
    "VaR 95% (%)":  [var95_hist * 100, var95_norm * 100, var95_mc * 100],
    "VaR 99% (%)":  [var99_hist * 100, var99_norm * 100, var99_mc * 100],
    "VaR 95% (R$)": [abs(var95_hist) * posicao, abs(var95_norm) * posicao, abs(var95_mc) * posicao],
    "VaR 99% (R$)": [abs(var99_hist) * posicao, abs(var99_norm) * posicao, abs(var99_mc) * posicao],
})

tabela_var = tabela_var.set_index("Método")
tabela_var = tabela_var.round(4)

print(tabela_var.to_string())

print("\nA 95%, o método PARAMÉTRICO é o mais conservador, com VaR = 2,74% superando o histórico de 2,28% e o Monte Carlo de 2,72%")
print("A 99%, por outro lado, o método HISTÓRICO passa a ser o mais conservador, com VaR = 4,33%, superando o Paramétrico de 3,90% e o Monte Carlo de 3,93%")
print("Essa diferença ocorre pois na região central (95%) a Normal SUPERESTIMA o risco, enquanto nas caudas extremas (99%) ela SUBESTIMA o risco, não capturando a frequêncai real de eventos extremos (black swans).")


# ===== TAREFA 2: CVaR =====
# 1 - CVaR 99% pelo método histórico
var99     = var99_hist
cvar99    = retornos_port[retornos_port <= var99].mean()

# 2 - CVaR em valor absoluto e comparação com o VaR99%
var99_va  = abs(var99)  * posicao
cvar99_va = abs(cvar99) * posicao
excesso   = cvar99_va - var99_va

print("\n===== TAREFA 2: CVaR =====")
print("Etapa 2 - Valores CVar e VaR 99% em R$")
print(f"VaR 99%: R$ {var99_va:,.2f} | CVaR 99%: R$ {cvar99_va:,.2f} | Excesso: R$ {excesso:,.2f}")

# 3 - Comparação entre CVaR e VaR 99%
print("\nEtapa 3 - Comparação CVaR e VaR 99%")
excesso_pct = (cvar99_va / var99_va - 1) * 100

print(f"O CVaR 99% é {excesso_pct:.1f}% maior que o VaR 99% (quase o dobro), indicando que a cauda esquerda do portfólio é extremamente pesada, com uma perda imensa.")
print("Essa diferença evidencia como o CVaR é mais preciso, pois não cai na armadilha de subestimar o risco como ocorre no VaR.")
print("Tal comportamento é um dos motivos pelos quais o CVaR é considerado um risco mais robusto e preferencialmente utilizado pelos gestores e reguladores.")

# ===== TAREFA 3: Drawdown =====
# 1 - Cálculo da série de Drawdown equally-weighted
valor_port = (1 + retornos_port).cumprod()
pico       = valor_port.cummax()
drawdown   = (valor_port - pico) / pico

# 2 - Identificação do Maximum Drawdown: maior queda percentual, data e tempo de recuperação
mdd      = drawdown.min()
data_mdd = drawdown.idxmin()

pico_anterior = valor_port[:data_mdd].idxmax()
nivel_pico    = valor_port[pico_anterior]
recuperacao   = valor_port[data_mdd:][valor_port[data_mdd:] >= nivel_pico]

print("\n===== TAREFA 3: Drawdown =====")
print(f"Maximum Drawdown : {mdd*100:.2f}%")
print(f"Data do MDD      : {data_mdd.date()}")
print(f"Pico anterior    : {pico_anterior.date()}")

if len(recuperacao) > 0:
    data_rec = recuperacao.index[0]
    dias_rec = (data_rec - data_mdd).days
    print(f"O portfólio se recuperou em {data_rec.date()}, {dias_rec} dias corridos após o fundo.")
else:
    print("O portfólio não se recuperou completamente até o final do período analisado.")

# 3 - Gráfico da série de Drawdown
plt.figure(figsize=(12, 5))
plt.fill_between(drawdown.index, drawdown * 100, 0, color="crimson", alpha=0.5, label="Drawdown")
plt.plot(drawdown.index, drawdown * 100, color="darkred", linewidth=0.8)
plt.axhline(0, color="black", linewidth=1, linestyle="--")
plt.title("Drawdown do Portfólio Equally-Weighted (2019–2024)")
plt.xlabel("Data")
plt.ylabel("Drawdown (%)")
plt.legend()
plt.tight_layout()
plt.savefig("drawdown.png", dpi=150)
plt.close()

print("O gráfico foi salvo como: drawdown.png")

# 4 - Análise de coincidência do Maximum Drawdown com a COVID-19
covid_inicio   = pd.Timestamp("2020-03-11")
coincide_covid = (covid_inicio - pd.Timedelta(days=45)) <= data_mdd <= (covid_inicio + pd.Timedelta(days=90))

print("\nEtapa 4 - Coincidência com a COVID-19")
if coincide_covid:
    print("O maior drawdown coincide com a crise do COVID-19 (fevereiro-março/2020).")
else:
    print("O maior drawdown não coincide diretamente com o pico da crise COVID (março/2020).")


# ===== TAREFA 4: Otimização de Markowitz e Fronteira Eficiente =====
# 1 - Vetor de retornos médios anualizados e matriz de covariância anualizada
ret_medios = ret_ativos.mean() * 252
matriz_cov = ret_ativos.cov()  * 252

# 2 - Simulação de Monte Carlo
n_sim     = 10000
results   = []
pesos_sim = []
ret_sim = []
vol_sim = []
sh_sim  = []

for i in range(n_sim):

    w = np.random.random(len(tickers_ativos))
    w = np.random.dirichlet(np.ones(4))

    mu_an = ret_ativos.mean() * 252
    cov = ret_ativos.cov() * 252

    retorno = np.dot(w, mu_an)

    risco = np.sqrt(
        np.dot(w.T, np.dot(cov, w))
    )

    ret_sim.append(retorno)
    vol_sim.append(risco)
    pesos_sim.append(w)

# 3 - Índice de Sharpe
for i in range(n_sim):
    sh_sim.append(ret_sim[i] / vol_sim[i])

ret_sim = np.array(ret_sim)
vol_sim = np.array(vol_sim)
sh_sim  = np.array(sh_sim)

idx_ms   = np.argmax(sh_sim)

pesos_ms = pesos_sim[idx_ms]
ret_ms   = ret_sim[idx_ms]
vol_ms   = vol_sim[idx_ms]
sh_ms    = sh_sim[idx_ms]

# 4 - Plotagem da nuvem de porfólios simulados (destauqe para equal-weight e máximo Sharpe)
ret_ew = pesos_ew @ ret_medios.values
vol_ew = np.sqrt(pesos_ew @ matriz_cov.values @ pesos_ew)
sh_ew  = ret_ew / vol_ew

plt.figure(figsize=(11, 7))
grafico = plt.scatter(vol_sim * 100, ret_sim * 100, c=sh_sim, cmap="viridis", alpha=0.4, s=6)
plt.colorbar(grafico, label="Índice de Sharpe")
plt.scatter(vol_ew * 100, ret_ew * 100, color="red",  s=150, zorder=5, label=f"Equally-weighted (Sharpe={sh_ew:.2f})",  edgecolors="black")
plt.scatter(vol_ms * 100, ret_ms * 100, color="gold", s=200, zorder=6, label=f"Máximo Sharpe (Sharpe={sh_ms:.2f})", marker="*", edgecolors="black")
plt.title("Fronteira Eficiente – PETR4, VALE3, ITUB4, WEGE3 (2019–2024)")
plt.xlabel("Volatilidade Anualizada (%)")
plt.ylabel("Retorno Anualizado (%)")
plt.legend()
plt.tight_layout()
plt.savefig("fronteira_eficiente.png", dpi=150)
plt.close()

print("\n===== TAREFA 4: Otimização de Markowitz e Fronteira Eficiente =====")
print("O gráfico com a plotagem da nuvem de portfólios foi salvo como: fronteira_eficiente.png")

# 5 - Análise comparativa entre os portfólios equally-weighted e de máximo Sharpe
print(f"\n{'Ativo':<14} {'Equally-Weighted':>18} {'Máximo Sharpe':>15}")
print("-" * 50)
for i, tk in enumerate(tickers_ativos):
    print(f"{tk:<14} {pesos_ew[i]*100:>17.1f}% {pesos_ms[i]*100:>14.2f}%")
print("-" * 50)
print(f"{'Retorno anual':<14} {ret_ew*100:>17.2f}% {ret_ms*100:>14.2f}%")
print(f"{'Volatilidade':<14} {vol_ew*100:>17.2f}% {vol_ms*100:>14.2f}%")
print(f"{'Sharpe':<14} {sh_ew:>18.3f} {sh_ms:>15.3f}")

ganho_sharpe    = (sh_ms / sh_ew - 1) * 100
ativo_dominante = tickers_ativos[np.argmax(pesos_ms)]

print(f"\nO portfólio de máximo Sharpe é {ganho_sharpe:.1f}% mais eficiente que o equally-weighted.")
print(f"O ativo com maior peso no portfólio ótimo é {ativo_dominante} ({pesos_ms[np.argmax(pesos_ms)]*100:.1f}%),")
print("pois apresentou a melhor relação retorno/risco e menor correlação com os demais no período.")