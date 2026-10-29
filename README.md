# AVD-20262-pratica-streamlit

## Dados deste projeto: Brasileirão

O aplicativo agora usa a base da [minha EDA no Colab](https://colab.research.google.com/drive/1uQoUUXiGL20K3pblRo6gENLramU72f4y), em vez do Heart Disease da aula.

- **Fonte:** [Brazilian Football Dataset — Kaggle](https://www.kaggle.com/datasets/lucasyukioimafuko/brasileirao-serie-a-2006-2022), versão **19**, identificada na execução salva do Colab.
- **Unidade de análise:** um clube em uma temporada; 450 campanhas entre 2003 e 2024.
- **Variáveis quantitativas:** `points`, `played`, `won`, `draw`, `loss`, `goals`, `goals_taken` e `goals_diff`.
- **Tratamento:** mantém todos os registros e outliers, cria `saldo_resultado` (`goals_diff > 0`) e `goals_log` (`log1p(goals)`), como no notebook. A transformação logarítmica fica fora das variáveis principais do dashboard.
- **Dashboard 1:** correlação de Spearman e histograma interativo em Plotly, com filtros por temporada, clube e valores das variáveis.
- **Dashboard 2:** indicadores de desempenho, ranking clicável de clubes e evolução por temporada em Altair. O clique no ranking atualiza KPIs, evolução e tabela.

O CSV tratado está em `data/clean/dataset.csv`; o app funciona sem acessar o Colab ou o Kaggle. Para reproduzir a exportação, após instalar as dependências:

```bash
python scripts/prepare_data.py
```

O script usa `data/raw/brasileirao.csv` quando disponível; caso contrário, baixa a versão 19 do Kaggle.

- `notebooks/eda.ipynb`: cópia integral do notebook da Aula 11 indicado no Colab, recuperada em 27/10/2026, incluindo análises, resultados e gráficos salvos. O arquivo original foi preservado sem edição; a versão disponível no Drive foi modificada em 19/10/2026.
- `notebooks/arquivo-eda-original.ipynb`: notebook da professora, mantido para consulta.
- `notebooks/eda-com-downloads.ipynb`: cópia adaptada para execução local ou no Colab, com a fonte fixada na versão 19, leitura de `data/raw/` e exportação final. Execute este notebook para preparar os dados do dashboard.

Em `eda-com-downloads.ipynb`, execute a EDA e a seção final **Download dos Datasets**. Ela salva dois arquivos e, no Colab, também oferece os downloads:

- `brasileirao.csv`: cópia original (`df_raw`), com 11 colunas; coloque em `data/raw/`.
- `dataset.csv`: dados tratados (`df`), com `saldo_resultado` e `goals_log`; substitua o arquivo em `data/clean/`.

As duas versões mantêm as 450 campanhas, conforme a decisão da EDA de preservar os outliers. O filtro de 38 jogos do gráfico final não é aplicado ao CSV exportado. Em execução local, os arquivos já são salvos nas pastas corretas. O link do Colab aponta para um notebook, não para um CSV; as alterações no Colab não são sincronizadas automaticamente.

## Entrega da Aula 21 — parte 1

- Rascunho do Dashboard 1: [entregas/rascunho-dashboard1.png](entregas/rascunho-dashboard1.png).
- Prompt aplicado à revisão do esqueleto: [prompts/layout-skeleton-prompt.md](prompts/layout-skeleton-prompt.md).
- Aplicativo: `app.py`, com sidebar, seletores de variáveis, sliders de intervalo, correlação e distribuição.
- Captura do app em execução: [entregas/dashboard1-em-execucao.png](entregas/dashboard1-em-execucao.png). Em 27/10/2026, o slider de pontos e o seletor do histograma foram testados no navegador; os filtros combinados também passaram nos testes automatizados do Streamlit.
- Declaração de uso de IA: [prompts/declaracao-uso-ia.md](prompts/declaracao-uso-ia.md), a ser preenchida manualmente pelo aluno ao terminar a atividade.

No Windows desta execução, `streamlit skills --yes` concluiu usando automaticamente a instalação global, pois o sistema não permitiu criar os links simbólicos locais.

## Entrega da Aula 22 — parte 2

O aplicativo tem duas abas: **Dashboard 1 · Exploração** e **Dashboard 2 · Desempenho**. A leitura do CSV e a matriz de Spearman usam `@st.cache_data`, com validade de cinco minutos e limite de entradas. O tema claro com destaque verde e fonte sem serifa está em `.streamlit/config.toml`.

As variáveis, métricas e widgets do Dashboard 2 foram definidos antes de desenhar o rascunho e implementar a aba:

- [Rascunho do Dashboard 2](entregas/rascunho-dashboard2.png).
- [Justificativa das métricas, fórmulas e controles](entregas/justificativa-metricas.md).
- [Validação da Parte 2](entregas/validacao-parte2.md).
- [Dashboard 1 atualizado](entregas/dashboard1-parte2-em-execucao.png), [Dashboard 2 em execução](entregas/dashboard2-em-execucao.png) e [exemplo de seleção no ranking](entregas/dashboard2-selecao.png).

**Como usar:** temporadas e clubes, na sidebar, filtram as duas abas. Os controles no bloco “Dashboard 1” afetam apenas a exploração. Na segunda aba, o toggle de 38 jogos restringe as campanhas e o slider limita as barras exibidas. Clique numa barra para selecionar um clube; use Shift + clique para incluir outros. Os KPIs, a evolução e a tabela usam a seleção. Duplo clique no ranking ou o botão de limpeza retorna ao recorte completo dos filtros. Alterar filtros comuns, o toggle de 38 jogos ou o tamanho do ranking limpa a seleção anterior.

O ranking segue o [guia Altair da professora](https://github.com/mfal-school/AVD-20262-pratica-streamlit/blob/main/ALTAIR-CROSSFILTER.md), usando `on_select="rerun"`. Os indicadores são contagem de campanhas, aproveitamento dos pontos, gols por jogo e saldo por jogo. As taxas usam razões das somas, ponderadas pelos jogos dos clubes; não são médias simples dos percentuais nem totais de partidas únicas.

Para executar os testes automatizados, com o venv ativo:

```bash
python -m unittest discover -s tests -v
```

Para regenerar o rascunho:

```bash
python scripts/gerar_rascunho_dashboard2.py
```

A declaração de uso de IA permanece para preenchimento manual do aluno ao encerrar a atividade, conforme sua orientação. O notebook original da Aula 11 foi mantido intacto.

Repositório utilizado para aula prática relacionada a Streamlit na disciplina Análise e Visualização de Dados da Cesar School no período de 2026.2.

Repositório-modelo das Aulas 21, 22 e 23: construção de dois dashboards em Streamlit a partir da EDA desenvolvida em sala. O deploy dos dashboards ocorrerá via Streamlit Community Cloud e serão os seguintes:

- Dashboard 1 = correlação + distribuição das variáveis quantitativas
- Dashboard 2 = KPIs

## Setup

Requer **Python 3.11 a 3.15**. Confira a sua versão antes de começar:

| Sistema | Verificar versão |
| --- | --- |
| macOS / Linux | `python3 --version` |
| Windows | `py --version` |

### 1. Criar e ativar o ambiente virtual

O nome do comando do Python muda por sistema (em muitas máquinas `python` nem existe). Use a linha do seu sistema:

| Sistema | Criar | Ativar |
| --- | --- | --- |
| macOS / Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |
| Windows (PowerShell) | `py -m venv .venv` | `.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `py -m venv .venv` | `.venv\Scripts\activate.bat` |

Se você tem várias versões instaladas, escolha uma compatível, por exemplo `python3.12 -m venv .venv` (macOS/Linux) ou `py -3.12 -m venv .venv` (Windows).

Com o ambiente ativo, o terminal mostra `(.venv)` no início da linha. **A partir daqui os comandos são iguais em todos os sistemas**, porque dentro do venv `python` e `pip` sempre existem.

### 2. Instalar, configurar a IA e rodar

```bash
python -m pip install -r requirements.txt

# Skills de IA do Streamlit (ver seção "IA neste projeto")
streamlit skills --yes

streamlit run app.py
```

### Problemas comuns

- **`python: command not found` / `python` não é reconhecido:** use `python3` (macOS/Linux) ou `py` (Windows) só para criar o venv; depois de ativado, `python` funciona.
- **Linux (Debian/Ubuntu): `ensurepip is not available` ou `No module named venv`:** instale `sudo apt install python3-venv` (ou `python3.X-venv` para a sua versão).
- **Windows: "a execução de scripts foi desabilitada" ao ativar no PowerShell:** rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, ou use o cmd.
- **Python fora de 3.11–3.15:** instale uma versão compatível em [python.org](https://www.python.org/downloads/) e crie o venv com ela, como no exemplo acima.
- **Apareceu `ModuleNotFoundError` ou `streamlit: command not found`:** o venv provavelmente não está ativo. Ative de novo e confira o `(.venv)` no prompt.
- **Erro de certificado no `pip install` (macOS, Python do python.org):** rode `Install Certificates.command`, na pasta Python 3.X em Aplicativos.
- **Erro de certificado SSL ao baixar os dados do Kaggle (macOS, Python do python.org):** rode `Install Certificates.command`, na pasta Python 3.X em Aplicativos, e reinicie o kernel. Se `data/raw/brasileirao.csv` já existir, `eda-com-downloads.ipynb` lê essa cópia local sem baixar novamente.

## Estrutura de dados: `data/raw` vs `data/clean`

- `data/raw/`: o dataset **bruto**, como foi baixado. Nunca é editado à mão.
- `data/clean/`: o dataset **já tratado**, exportado na última célula do notebook de EDA (ex.: `df.to_csv("data/clean/dataset.csv", index=False)`). O `app.py` lê **somente** desta pasta, via `src/data_loader.py`.

### O que vai para o Git

| Pasta | Versionada? | Por quê |
| --- | --- | --- |
| `data/raw/` | **Não** (só o `.gitkeep`) | O bruto pode ser grande ou ter dados sensíveis, e o app não o usa. |
| `data/clean/` | **Sim** | O Streamlit Community Cloud faz deploy a partir do GitHub e só enxerga o que está no repositório. Sem o CSV tratado no repo, o app funciona na sua máquina e **quebra no deploy**. |

### Antes de dar `git push` com o dado tratado

- **O dado é público ou pode ser compartilhado?** Se não for claramente público, use um **repositório privado** (o Community Cloud permite conectar repositórios privados ao autorizar o GitHub; confirme na hora do deploy). Nesse caso, dê acesso de leitura ao professor (como colaborador ou pela organização).
- **Dado sensível** (nomes, CPF, e-mail, telefone, localização exata etc.): remova ou anonimize na EDA, antes de exportar para `data/clean/`. Isso vale mesmo em repositório privado.
- **Tamanho:** o GitHub rejeita arquivos acima de **100 MB**. Se o CSV tratado for grande, reduza colunas e linhas na EDA ou exporte em Parquet (`df.to_parquet(...)`, exige `pyarrow`).
- **Lembre de commitar o arquivo:** confira com `git status` que `data/clean/dataset.csv` aparece como novo arquivo.

## Passo a passo

O passo a passo detalhado de cada aula (Aulas 21, 22 e 23), com pré-requisitos e objetivos, está em [ROTEIRO.md](ROTEIRO.md). Comece por ele depois do Setup.

1. Preserve a entrega original da Aula 11 em `notebooks/eda.ipynb`. Use `notebooks/eda-com-downloads.ipynb` para adaptar a leitura e exportar o dado tratado para `data/clean/`.
2. Construa o `app.py` em cima do esqueleto (sidebar, filtros, Dashboard 1 e Dashboard 2).
3. Faça o deploy no Streamlit Community Cloud (Aula 23).

**Link do app (Aula 23):** _(preencher após o deploy)_

## IA neste projeto

Este projeto usa o **streamlit skills**: um conjunto de instruções (arquivos `SKILL.md`) que a ferramenta de IA lê para escrever código Streamlit seguindo boas práticas (estrutura de layout, cache, widgets, etc.).

**Como instalar:** depois do `pip install -r requirements.txt`, rode na raiz do projeto:

```bash
streamlit skills        # interativo
streamlit skills --yes  # sem confirmações
```

O comando cria *symlinks* para as skills que acompanham a sua instalação do Streamlit, então elas se atualizam sozinhas quando você atualiza o pacote. (A opção `--global` instala para todos os projetos, em vez de só este.)

**Onde fica instalado:**

- `.claude/skills/`: lido pelo Claude Code.
- `.agents/skills/`: lido pelo Gemini CLI, que já encontra essa pasta sozinho.

Essas pastas **não são versionadas** (ver `.gitignore`): os symlinks apontam para o seu ambiente virtual e não funcionam em outra máquina. Cada pessoa roda `streamlit skills` no próprio clone.

**Se você usa outra ferramenta** (ChatGPT, Copilot Chat, etc.): abra o `SKILL.md` correspondente em `.agents/skills/` e cole o conteúdo manualmente no início do chat, antes do seu pedido.

O uso de IA deve ser declarado conforme a seção abaixo.

## Pasta `prompts/`

A pasta [prompts/](prompts/) guarda os registros de **uso de IA**: o template de prompt para transformar o rascunho de layout em esqueleto de código e a **Declaração de Uso de IA** exigida pelo Plano de Ensino. Veja [prompts/README.md](prompts/README.md).

## Pasta `entregas/`

A pasta [entregas/](entregas/) guarda os rascunhos de layout de cada dashboard (`.jpg` ou `.png`) e a justificativa das métricas do Dashboard 2. Veja [entregas/README.md](entregas/README.md) para o detalhe de cada arquivo e o checklist por aula. Não coloque esses arquivos no `.gitignore`.
