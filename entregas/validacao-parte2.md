# Validação da Parte 2 — 27/10/2026

## Pré-requisitos conferidos

- App da Parte 1 executado sem exceções; seletor do histograma e slider de pontos respondendo.
- Remoto `origin` na conta `raulferraz85`, com o commit `88dba66` da Parte 1.
- Ambiente Python 3.12.3, Streamlit 1.66.1 e Altair 6.3.0. Dependências necessárias já instaladas.

## Testes automatizados

Comando: `python -m unittest discover -s tests -v`.

Resultado: **13 testes passaram**. Arquivos: `tests/test_dashboard.py` e `tests/test_metrics.py`.

| Cenário | Resultado verificado |
| --- | --- |
| Estado inicial | Duas abas, dois gráficos Plotly, dois gráficos Altair e quatro KPIs. |
| Zero variáveis | Mensagens orientam a seleção; Dashboard 2 continua disponível. |
| Uma variável | Histograma disponível e correlação indisponível com explicação. |
| Duas ou mais variáveis | Matriz e histograma renderizam normalmente. |
| Combinação de temporadas e intervalos | Em 2024, pontos entre 40 e 60 retornam 12 campanhas no D1; o D2 mantém as 20 campanhas da temporada. A matriz foi comparada com `scipy.stats.spearmanr` e o histograma com as linhas esperadas do CSV. |
| Troca de variável e separação por saldo | Histograma muda; os dois grupos somam 450 campanhas. Remover a variável exibida do seletor redefine a escolha para uma opção válida. |
| Variável constante e uma campanha | Coeficiente indefinido é explicado; uma única campanha não tenta calcular correlação. |
| Nenhuma temporada | Ambas as abas permanecem acessíveis, sem gráficos vazios enganosos; campanhas = 0 e razões = `—`. |
| Intervalos incompatíveis no D1 | Nenhuma campanha no D1; D2 não é interrompido e mantém seu recorte. |
| Filtro de 38 jogos | 378 campanhas. Com temporada 2003 selecionada, D2 fica vazio sem erro. |
| Limite de barras | Exibir uma única barra não reduz os KPIs quando não há seleção. |
| Fórmulas | Dados sintéticos com durações distintas confirmam a razão das somas, sem média simples dos percentuais. Denominador zero produz razão indefinida. |
| Seleção e lacunas temporais | Seleção vazia, simples, múltipla e sem correspondências; anos ausentes interrompem a linha. |
| Cache | Duas leituras da mesma fonte provocam uma única chamada ao CSV; alterar o dataframe retornado não contamina a próxima leitura. |

## Teste no navegador

O app foi aberto no Microsoft Edge em execução headless, com perfil separado, em `http://127.0.0.1:8501`. As interações foram feitas por eventos de mouse e teclado, não por alteração direta do dataframe.

- Estado inicial: **450 campanhas**, **45,5%** de aproveitamento, **1,28** gol por jogo e saldo arredondado para **0,00** por jogo.
- Clique em **Palmeiras**: **20 campanhas**, **54,0%**, **1,47** gol por jogo e **0,34** de saldo por jogo; a evolução também foi atualizada.
- Shift + clique em **São Paulo**: seleção dos dois clubes, **42 campanhas**, **53,9%**, **1,45** gol por jogo e **0,34** de saldo por jogo.
- Botão de limpeza: retorno às 450 campanhas do recorte completo.
- Ativar o filtro de 38 jogos após selecionar um clube: seleção anterior limpa e KPIs recalculados para 378 campanhas.
- Alterar o limite do ranking após selecionar um clube: seleção limpa, sem limitar os KPIs ao número de barras.

Capturas: [Dashboard 1](dashboard1-parte2-em-execucao.png), [Dashboard 2](dashboard2-em-execucao.png) e [seleção de Palmeiras](dashboard2-selecao.png).

## Entrega

Rascunho, justificativa e implementação do Dashboard 2 concluídos. A declaração de uso de IA será preenchida manualmente pelo aluno, conforme sua orientação; ela não foi alterada nesta etapa.
