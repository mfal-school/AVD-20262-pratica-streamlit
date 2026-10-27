# Dashboard 2 — justificativa das métricas

Planejamento registrado em 27/10/2026, antes do rascunho e da implementação do Dashboard 2.

## Público e pergunta

O painel atende quem acompanha o Brasileirão e quer comparar o desempenho dos clubes ao longo das temporadas: quanto dos pontos possíveis foi conquistado, quanto o clube marcou por jogo e qual foi seu equilíbrio entre ataque e defesa?

Cada linha do dataset é **uma campanha de um clube em uma temporada**, não uma partida. A base tratada contém 450 campanhas, 44 clubes e temporadas de 2003 a 2024. Todos os registros e outliers da EDA são preservados.

## 1. Variáveis escolhidas

| Variável | Papel no painel |
| --- | --- |
| `season` | Período e eixo da evolução temporal. |
| `team` | Categoria do filtro, agrupamento do ranking e seleção no gráfico. |
| `points` | Pontos oficiais registrados para a campanha. |
| `played` | Exposição: quantidade de jogos disputados pelo clube. |
| `goals` | Gols marcados. |
| `goals_diff` | Saldo de gols registrado na base. |

`goals_taken` ajuda a interpretar o saldo, mas o cálculo usa a coluna `goals_diff` preservada na EDA. A posição (`place`) não entra como KPI: calcular a média de colocações pode esconder diferenças no número de participantes. `goals_log` é uma transformação exploratória, sem interpretação direta para o público deste painel.

## 2. Métricas e relação com a teoria

Seja **S** o conjunto de campanhas após os filtros e a seleção no ranking. Todas as somas abaixo usam o mesmo conjunto S.

| Métrica | Fórmula | Conceito de métrica básica | O que comunica e por que foi escolhida |
| --- | --- | --- | --- |
| Campanhas | Número de linhas de S | Contagem absoluta / volume | Expõe o tamanho do recorte. Evita comparar um clube com uma única participação e outro com vinte sem perceber a diferença de cobertura. Não conta jogos nem clubes distintos. |
| Aproveitamento | `100 × Σ points / (3 × Σ played)` | Razão percentual: realizado em relação ao potencial | Resume a eficiência na conquista dos pontos possíveis. Normaliza campanhas de durações diferentes, permitindo comparação mais informativa que o total bruto de pontos. |
| Gols por jogo | `Σ goals / Σ played` | Taxa por unidade de exposição | Mostra a produção ofensiva média de cada participação de clube em um jogo. Um valor de 1,50 significa 1,5 gol marcado pelo clube por jogo, não 1,5 gol total da partida. |
| Saldo por jogo | `Σ goals_diff / Σ played` | Saldo (diferença) normalizado por exposição | Resume o balanço entre ataque e defesa. Positivo indica superávit de gols e negativo indica déficit. Complementa os gols marcados, que isoladamente não mostram os gols sofridos. |

Os indicadores são descritivos. Não foram inventadas metas ou faixas de desempenho para classificá-los como bons ou ruins. A conexão com a teoria usa os conceitos de contagem, razão, taxa, saldo e agregação ponderada; o material específico da aula não estava anexado ao enunciado.

### Agregação e limites

- As taxas são calculadas pela **razão das somas**, equivalente à média das taxas de cada campanha ponderada por seus jogos. Não se calcula uma média simples das porcentagens dos clubes.
- `played` contém campanhas de 37, 38, 42 e 46 jogos. O filtro opcional de 38 jogos permite comparar campanhas de mesma duração; o estado inicial mantém todas.
- Pontos oficiais podem refletir punições ou ajustes. Por isso, o painel usa `points` e não substitui essa coluna por `3 × won + draw`.
- Cada jogo entre dois clubes pode contribuir para duas linhas agregadas de equipe. Portanto, `Σ played` representa **participações de clubes em jogos**, não partidas únicas do campeonato. O painel não divide esse total por dois nem apresenta total de partidas.
- Somar o saldo de todos os clubes tende a produzir um valor próximo de zero. Esse indicador é mais informativo ao selecionar um clube ou grupo; diferenças residuais refletem a base preservada, sem correção artificial.
- Razões são indefinidas quando o denominador é zero. Nesse caso, o painel mostra `—`. Sem campanhas, mostra contagem zero e uma mensagem, nunca uma taxa inventada.
- A comparação entre épocas é descritiva: adversários, regras e composição dos clubes variam. Associação e diferença de desempenho não demonstram causalidade.

## 3. Widgets definidos antes do desenho

| Controle | Estado inicial | Efeito |
| --- | --- | --- |
| Multisseletor de temporadas, na sidebar | Todas as temporadas | Define o período das duas abas. Seleção vazia produz recorte vazio. |
| Multisseletor de clubes, na sidebar | Vazio = todos os clubes | Restringe as duas abas aos clubes escolhidos. |
| Seletor de variáveis, toggle de saldo e sliders de intervalo, no bloco “Dashboard 1” da sidebar | Oito variáveis e intervalos completos | Afetam somente a exploração do Dashboard 1; não alteram os KPIs do Dashboard 2. |
| Toggle “Somente campanhas com 38 jogos” | Desligado | Restringe o Dashboard 2 às campanhas com exatamente 38 jogos. |
| Slider “Clubes no ranking” | 12; domínio de 1 a 44 | Limita somente as barras exibidas. Sem clique em barras, os indicadores e a evolução continuam considerando todos os clubes do recorte. |
| Clique nas barras do ranking | Sem seleção = todo o recorte | Seleciona um clube; Shift + clique permite vários. Atualiza os KPIs e a evolução por temporada. |
| Botão “Limpar seleção do gráfico” ou duplo clique no ranking | Sem seleção | Retorna aos dados definidos pelos filtros. Mudanças de temporada, clubes, filtro de 38 jogos ou tamanho do ranking também limpam a seleção anterior. |

Não há dependência escondida entre os sliders de variáveis do Dashboard 1 e os KPIs. Os filtros comuns têm rótulo explícito na sidebar.

## 4. Rascunho e visuais

O [rascunho do Dashboard 2](rascunho-dashboard2.png) segue a ordem: sidebar e abas → controles → quatro indicadores → ranking à esquerda e evolução à direita.

- **Ranking de aproveitamento por clube:** barras horizontais ordenadas pelo aproveitamento agregado. Tooltip informa campanhas, jogos e aproveitamento para contextualizar amostras diferentes. Empates são ordenados pelo nome do clube. Não é a classificação oficial de uma temporada.
- **Evolução do aproveitamento por temporada:** linha com pontos, calculada pela mesma razão das somas em cada temporada. Uma única temporada continua visível como ponto. O tooltip mostra o número de campanhas; períodos sem registros ficam como lacunas, sem inventar valores ou ligar anos ausentes.
- **Detalhes das campanhas:** tabela opcional para conferir os registros utilizados nos indicadores e nos gráficos.

O ranking mantém o contexto dos clubes disponíveis ao selecionar uma barra; somente as barras fora da seleção ficam esmaecidas. A seleção é transmitida ao Python por `st.altair_chart(..., on_select="rerun")`, seguindo o [guia da professora](https://github.com/mfal-school/AVD-20262-pratica-streamlit/blob/main/ALTAIR-CROSSFILTER.md). O dataframe selecionado alimenta os quatro KPIs, a evolução e a tabela.

## 5. Identidade visual

Tema claro com fundo `#F7F8F2`, superfícies `#EDF1E7`, destaque verde `#176B4D`, texto `#172C26` e fonte sem serifa do sistema. O verde faz referência ao campo e o fundo claro mantém a leitura de números e gráficos. Configuração centralizada em `.streamlit/config.toml`, sem CSS personalizado. A matriz de correlação preserva uma escala divergente, adequada a coeficientes entre −1 e 1.
