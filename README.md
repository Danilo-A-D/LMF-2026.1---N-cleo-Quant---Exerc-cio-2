EXERCÍCIO 2 - NÚCLEO QUANT LMF (2026.1)
========================

O QUE FOI IMPLEMENTADO
O presente trabalho é um relatório completo de risco do portfólio composto pelos ativos PETR4.SA (Petrobras), VALE3.SA (Vale), ITUB4.SA (Itaú Unibanco) e WEGE3.SA (WEG S.A.), com BOVA11.SA (ETF Ibovespa) como benchmark de mercado, cobrindo o período de 2019 a 2024 — janela que inclui a crise do COVID-19 e o ciclo de alta de juros no Brasil.
O projeto foi dividido em 4 tarefas, dadas as instruções da atividade, sendo elas:
1- Value at Risk (VaR) -> cálculo dos log-retornos diários, posição igualmente distribuída de R$ 100.000 entre os 4 ativos e estimativa do VaR 95% e 99% por três métodos: Histórico (percentil empírico), Paramétrico (distribuição Normal) e Monte Carlo (50.000 simulações)
2- CVaR (Expected Shortfall) -> cálculo do Conditional Value at Risk 99% histórico, conversão para valor absoluto e comparação com o VaR 99%, evidenciando a severidade das perdas na cauda esquerda do portfólio
3- Drawdown -> construção da série de valor acumulado do portfólio equally-weighted, cálculo do Maximum Drawdown, identificação do pico anterior, data do fundo e tempo de recuperação, com geração de gráfico da série de drawdown ao longo do tempo
4- Otimização de Markowitz e Fronteira Eficiente -> cálculo do vetor de retornos médios anualizados e da matriz de covariância anualizada, simulação de Monte Carlo com 10.000 portfólios de pesos aleatórios, cálculo do Índice de Sharpe para cada portfólio, identificação do portfólio de máximo Sharpe e plotagem da fronteira eficiente com destaque para o portfólio equally-weighted e o portfólio ótimo

========================
GUIA DE EXECUÇÃO

1. Baixe o arquivo 'relatorio_risco.py'
2. Abra o terminal e instale as bibliotecas necessárias: python -m pip install yfinance pandas numpy scipy matplotlib com as versões indicadas no arquivo requirements.txt
3. Abra o arquivo no VS Code e clique em Run no canto superior direito. Os resultados de cada tarefa aparecerão no terminal e os dois gráficos (drawdown.png e fronteira_eficiente.png) serão salvos automaticamente na mesma pasta do script.

========================
CONCLUSÕES

VALUE AT RISK (VaR)
O comportamento do VaR entre os métodos revela a assimetria das caudas reais do portfólio. A 95%, o método paramétrico foi o mais conservador (R$ 2.737), superando o histórico — pois a distribuição Normal aloca probabilidade excessiva nas regiões intermediárias. Já a 99%, o método histórico se tornou o mais conservador, evidenciando que os retornos reais possuem assimetria negativa: eventos extremos ocorrem com frequência maior do que a Normal prevê. Monte Carlo e paramétrico convergiram em ambos os níveis, confirmando que ambos assumem normalidade. A principal lição é que nenhum método é universalmente mais conservador — a escolha depende do nível de confiança e do perfil de cauda do ativo analisado.

CVaR (EXPECTED SHORTFALL)
O CVaR 99% histórico atingiu um valor 92,9% acima do VaR 99%. Isso indica que a cauda esquerda do portfólio é extremamente pesada: nos 1% piores dias, a perda média foi quase o dobro do limiar do VaR. Um gap dessa magnitude evidencia que o VaR funcionaria como um indicador enganoso de segurança, pois nada informa sobre o tamanho da catástrofe quando é violado. Reguladores preferem o CVaR pois não cai na armadilha de subestimar o risco como ocorre no VaR.

DRAWDOWN
O portfólio sofreu seu Maximum Drawdown de -47,14% entre o pico de 19/02/2020 e o fundo de 18/03/2020 — menos de 30 dias corridos de queda livre. A data do pico coincide exatamente com o topo histórico pré-pandemia do Ibovespa e o fundo alinha-se com o momento mais agudo do crash brasileiro. A magnitude do drawdown foi amplificada pelas composições setoriais. A recuperação ocorreu em 23/11/2020, 250 dias corridos após o fundo (~8,3 meses), impulsionada pelos estímulos fiscais e monetários globais sem precedente e pelo desempenho resiliente da WEGE3, que saiu do crash mais valorizada do que entrou. Vale notar que um drawdown de 47% exige um retorno subsequente de +89% apenas para recompor o capital original — assimetria que reforça a importância de estratégias de proteção de cauda (hedge, stop de portfólio, diversificação geográfica).

FRONTEIRA EFICIENTE DE MARKOWITZ
O portfólio de máximo Sharpe (0,927) superou o equally-weighted (0,648) em 43,1% na métrica de eficiência risco-retorno, com retorno anualizado de 29,44% contra 17,56%, ao custo de volatilidade ligeiramente superior (31,75% vs 27,09%). O algoritmo concentrou 70,2% do portfólio ótimo em WEGE3, ativo que apresentou a melhor combinação de retorno superior, menor correlação com os ciclos de commodities que dominam PETR4 e VALE3, e volatilidade relativamente controlada para o nível de retorno entregue no período. ITUB4 foi praticamente zerado (0,3%) por apresentar o pior Sharpe individual do grupo, pressionado pelo ciclo de alta de juros. É importante ressaltar as limitações do resultado: o portfólio ótimo é retrospectivo e calibrado com dados históricos; uma concentração de 70% em um único ativo seria inaceitável para a maioria dos mandatos institucionais; e a adoção de taxa livre de risco rf = 0 é uma simplificação relevante dado que a Selic oscilou entre 2% e 13,75% no período analisado, o que alteraria muito os Sharpes reais e possivelmente a composição do portfólio ótimo.
