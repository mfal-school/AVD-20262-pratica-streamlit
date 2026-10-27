# Rascunho de layout → esqueleto do Dashboard 1

Prompt aplicado em 27/10/2026 à revisão do esqueleto de `app.py`, com a imagem abaixo como referência. O app já existia; esta etapa revisou sua estrutura e preservou os cálculos implementados. A declaração de uso de IA será preenchida pelo aluno ao encerrar a atividade.

## Contexto

Estou desenvolvendo o Dashboard 1 da disciplina Análise e Visualização de Dados, Cesar School, período 2026.2. Uso o dataset do Brasileirão da minha EDA: cada registro representa um clube em uma temporada. A versão local contém 450 campanhas, 44 clubes e temporadas de 2003 a 2024.

O objetivo é explorar a correlação e a distribuição das variáveis quantitativas, seguindo a organização da Aula 21: sidebar à esquerda, heatmap ao centro e histograma em uma coluna maior à direita.

## Entrada

Imagem de entrada: `entregas/rascunho-dashboard1.png`. Fonte vetorial editável: `entregas/rascunho-dashboard1.svg`.

Dados: `data/clean/dataset.csv`, lidos por `src/data_loader.py`.

Colunas: `season`, `place`, `team`, `points`, `played`, `won`, `draw`, `loss`, `goals`, `goals_taken`, `goals_diff`, `saldo_resultado` e `goals_log`.

Variáveis quantitativas principais: `points`, `played`, `won`, `draw`, `loss`, `goals`, `goals_taken` e `goals_diff`. Use rótulos em português.

Perguntas: quais variáveis estão associadas à pontuação? Como as campanhas se distribuem em cada variável? Como a distribuição muda entre campanhas com saldo positivo e não positivo?

Layout e interações:

- Título e descrição da unidade de análise no topo.
- Sidebar com multisseleção de temporadas, clubes e variáveis quantitativas; toggle de distinção por saldo; sliders de intervalo para as variáveis selecionadas. Todos os períodos e intervalos vêm selecionados inicialmente; clubes sem seleção significa todos.
- Área principal em duas colunas, proporção `1:1.5`: correlação de Spearman à esquerda e histograma à direita.
- Heatmap entre -1 e 1, com os coeficientes nas células. A seleção de variáveis determina sua matriz.
- Seletor da variável do histograma dentro da coluna de distribuição. Toggle desligado mostra uma distribuição única; ligado separa `Saldo positivo` de `Saldo não positivo`.
- Os filtros de temporadas, clubes e intervalos afetam os dois gráficos. A troca da variável do histograma afeta somente o histograma.

## Restrições

- Use Python, Streamlit e Plotly, com componentes nativos; não use HTML, CSS ou JavaScript.
- Trabalhe em `app.py`, preservando as funcionalidades já existentes. Use `load_data()` de `src/data_loader.py`.
- Não faça download de dados nem reexecute a EDA ao abrir o dashboard.
- Mantenha o dataset completo como estado inicial, incluindo campanhas que não têm 38 jogos. Preserve os outliers.
- `saldo_resultado`: positivo quando `goals_diff > 0`; não positivo quando `goals_diff <= 0`. `goals_log` continua no CSV, mas não integra a lista principal de variáveis desta visualização.
- Use `st.sidebar` e `st.columns([1, 1.5])`, com layout amplo. A sidebar pode ter rolagem para os sliders.
- Mostre mensagens para filtros sem resultados, menos de duas campanhas ou menos de duas variáveis na correlação. Variáveis constantes não têm coeficiente definido.
- A imagem é um rascunho de organização: a contagem de campanhas, os intervalos e os gráficos devem ser calculados a partir do CSV, nunca copiados como valores fixos.
- Esta etapa cobre o Dashboard 1. Os KPIs do Dashboard 2 pertencem à Aula 22.

## Formato de saída

Retorne um esqueleto de `app.py` com título, sidebar e duas colunas posicionadas conforme o rascunho. Comente as etapas de carregamento, filtros, correlação e distribuição; marque com `# TODO` os cálculos ainda não implementados. Se partir do app existente, preserve os cálculos já implementados. Explique brevemente como cada bloco corresponde ao desenho e quais pontos precisam de revisão do aluno.
