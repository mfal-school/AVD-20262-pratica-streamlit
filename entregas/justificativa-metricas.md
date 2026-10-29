# Justificativa das métricas — Dashboard 2

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

### Métrica 1: Campanhas

- **Variável:** registros identificados por `team` (clube) e `season` (temporada). Cada linha representa uma campanha.
- **O que mede:** o número de campanhas presentes no recorte selecionado; não conta partidas nem clubes distintos.
- **Fórmula e conceito:** número de linhas de S — contagem absoluta, que informa o volume de observações.
- **Por que foi escolhida:** permite avaliar a cobertura da comparação. Um indicador calculado sobre uma campanha tem um contexto diferente de outro calculado sobre vinte.
- **Público-alvo:** pessoas que acompanham o Brasileirão e comparam clubes ou períodos.
- **Qual decisão pode ser apoiada:** ampliar o período selecionado ou conferir a quantidade de campanhas antes de comparar os demais indicadores.
- **O que comunica ao público-alvo:** quantas participações de clubes em temporadas sustentam os números exibidos. Por exemplo, “20 campanhas” significa vinte registros de clube e temporada no recorte.

### Métrica 2: Aproveitamento

- **Variável:** `points` (pontos oficiais) e `played` (jogos disputados pelo clube).
- **O que mede:** a porcentagem dos pontos possíveis conquistada pelos clubes nas campanhas selecionadas.
- **Fórmula e conceito:** `100 × Σ points / (3 × Σ played)` — razão percentual entre o resultado realizado e o potencial de pontos.
- **Por que foi escolhida:** permite comparar campanhas de durações diferentes sem depender apenas do total bruto de pontos.
- **Público-alvo:** torcedores e leitores interessados na eficiência dos clubes na conquista de pontos.
- **Qual decisão pode ser apoiada:** identificar clubes ou temporadas com maior aproveitamento para comparar sua trajetória no gráfico de evolução.
- **O que comunica ao público-alvo:** quanto do total de pontos disponíveis foi obtido. Um aproveitamento de 60% significa conquistar 60 de cada 100 pontos possíveis; não significa vencer 60% das partidas.

### Métrica 3: Gols por jogo

- **Variável:** `goals` (gols marcados) e `played` (jogos disputados pelo clube).
- **O que mede:** a quantidade média de gols marcados por participação de clube em um jogo, dentro do recorte selecionado.
- **Fórmula e conceito:** `Σ goals / Σ played` — taxa por unidade de exposição, ponderada pela quantidade de jogos.
- **Por que foi escolhida:** resume a produção ofensiva sem favorecer uma campanha apenas porque ela teve mais jogos.
- **Público-alvo:** pessoas que desejam comparar a produção ofensiva de clubes e temporadas.
- **Qual decisão pode ser apoiada:** escolher clubes ou períodos para investigar diferenças na produção ofensiva e relacioná-las ao aproveitamento.
- **O que comunica ao público-alvo:** quantos gols o clube marcou, em média, por jogo. Um valor de 1,50 indica 1,5 gol marcado pelo clube por jogo; não representa o total de gols dos dois adversários na partida.

### Métrica 4: Saldo por jogo

- **Variável:** `goals_diff` (saldo de gols registrado na base) e `played` (jogos disputados pelo clube). `goals_taken` (gols sofridos) auxilia a interpretação do saldo.
- **O que mede:** o saldo médio de gols por participação de clube em um jogo, considerando as campanhas selecionadas.
- **Fórmula e conceito:** `Σ goals_diff / Σ played` — saldo normalizado pela quantidade de jogos, combinando diferença e taxa.
- **Por que foi escolhida:** complementa os gols por jogo ao considerar o balanço entre gols marcados e sofridos. Marcar muitos gols, isoladamente, não informa quanto o clube sofreu.
- **Público-alvo:** pessoas que desejam entender o equilíbrio entre ataque e defesa dos clubes.
- **Qual decisão pode ser apoiada:** identificar clubes ou períodos com saldo positivo ou negativo e aprofundar a comparação dos seus resultados.
- **O que comunica ao público-alvo:** se o clube marcou mais ou menos gols do que sofreu, em média. Um saldo de +0,50 por jogo indica meio gol a mais marcado do que sofrido por jogo; um valor negativo indica o inverso. Ao reunir todos os clubes, o saldo tende a se aproximar de zero, por isso a seleção de clubes é importante para interpretá-lo.

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
