# Especificação do Problema

`[P4-ETAPA-01]`

## 1. Descrição do problema

Em jogos de cartas colecionáveis organizados em formato de "deck construído por regras", os jogadores montam seus baralhos a partir de uma coleção de cartas, mas precisam obedecer a um conjunto de regras estruturais para que o baralho seja considerado válido em torneios ou partidas organizadas — por exemplo: tamanho fixo do baralho, limite de cópias repetidas de uma mesma carta, e restrição de quais cartas podem ser usadas com base em uma "carta de comando" (commander) que define as cores permitidas no resto do baralho.

Montar um baralho manualmente e verificar se ele obedece a todas essas regras é uma tarefa repetitiva e sujeita a erro humano, especialmente em baralhos com muitas cartas. Além da validação estrutural, os jogadores também costumam querer uma análise estatística do baralho (quantidade de terrenos, distribuição de custos de mana, distribuição de cores) para ajudar a equilibrar suas escolhas.

O contexto de aplicação é o de uma ferramenta auxiliar de bancada — usada por um jogador antes de uma partida, ou por um organizador de torneio antes de aprovar uma lista — que recebe a lista de cartas de um baralho e devolve um relatório de legalidade e um relatório estatístico.

As regras usadas neste trabalho são **inspiradas** em formatos reais de jogos de cartas colecionáveis (como o formato "Commander/EDH" de Magic: The Gathering), mas foram **simplificadas e fixadas nesta especificação** — o sistema não implementa as regras oficiais completas de nenhum jogo específico, e sim um subconjunto autoral definido abaixo, suficiente para ser não-trivial nos quatro paradigmas.

## 2. Objetivo

O sistema deve ser capaz de, a partir da lista de cartas de um baralho (uma carta designada como commander e as demais cartas do baralho):

1. Determinar se o baralho é **legal** ou **ilegal**, segundo as regras da seção 5;
2. Caso seja ilegal, listar **todas** as violações encontradas (não apenas a primeira);
3. Produzir uma **análise estatística** do baralho: total de cartas, número de terrenos, número de cartas não-terreno, custo de mana médio das cartas não-terreno, e distribuição de cores (quantas cartas contêm cada cor de mana).

## 3. Entradas

O sistema recebe:

- **Uma carta commander**, com os atributos:
  - nome (texto, não vazio);
  - identidade de cor (subconjunto de {W, U, B, R, G} — branco, azul, preto, vermelho, verde — podendo ser vazio, o que indica uma carta incolor);
  - tipo (sempre tratada como carta não-terreno).

- **Uma lista de cartas do baralho** (sem contar o commander), onde cada carta possui:
  - nome (texto, não vazio);
  - identidade de cor (subconjunto de {W, U, B, R, G}, podendo ser vazio);
  - tipo: `terreno` ou `não-terreno`;
  - custo de mana convertido (número inteiro ≥ 0; para terrenos, sempre 0);
  - indicação de se é um "terreno básico" (booleano; só faz sentido quando tipo = terreno).

Cada carta na lista pode aparecer **várias vezes na entrada** (uma entrada por cópia física no baralho); o sistema não deve presumir que a entrada já está deduplicada.

## 4. Saídas

O sistema deve produzir:

- **Relatório de legalidade**:
  - um valor booleano indicando se o baralho é legal;
  - uma lista (possivelmente vazia) de violações encontradas, cada uma identificando **qual regra** foi violada e um detalhe legível (ex.: qual carta, ou qual contagem).

- **Relatório estatístico** (produzido independentemente do baralho ser legal ou não, desde que a entrada seja bem formada):
  - número total de cartas no baralho (incluindo o commander);
  - número de terrenos;
  - número de cartas não-terreno;
  - custo de mana médio das cartas não-terreno (0 se não houver nenhuma);
  - para cada uma das 5 cores, quantas cartas do baralho (incluindo o commander) contêm aquela cor em sua identidade de cor.

## 5. Regras do problema

1. **Tamanho do baralho**: o baralho, contando o commander, deve ter exatamente **100 cartas** (cópias, não cartas distintas).
2. **Singleton**: nenhuma carta não-terreno e não-básica pode aparecer mais de **1 vez** no baralho (contando o commander, se o commander também aparecer avulso — o que é considerado uma violação à parte, ver regra 5). Terrenos básicos (`terreno` com `terreno básico = verdadeiro`) não têm limite de cópias.
3. **O commander não é contado como carta do baralho**: se o nome do commander aparecer novamente dentro da lista de cartas do baralho, isso é uma violação (uma carta não pode ser ao mesmo tempo commander e carta comum do baralho).
4. **Identidade de cor**: a identidade de cor de **toda** carta do baralho (cada cor presente nela) deve estar contida na identidade de cor do commander. Uma carta incolor (identidade de cor vazia) é sempre permitida, independentemente da identidade do commander.
5. **Nome não vazio**: toda carta (incluindo o commander) deve ter um nome não vazio; entradas com nome vazio são inválidas e devem ser reportadas como violação, não descartadas silenciosamente.
6. **Custo de mana não negativo**: o custo de mana convertido de qualquer carta deve ser ≥ 0; para terrenos, deve ser sempre 0 (um terreno com custo > 0 é uma violação).

Um baralho é **legal** se, e somente se, nenhuma violação das regras 1–6 for encontrada.

## 6. Casos de exemplo

> Nos exemplos, cartas são representadas de forma resumida como `Nome [cores] tipo custo`. `T` = terreno, `NT` = não-terreno, `TB` = terreno básico.

**Exemplo 1 — baralho legal simples**
- Entrada: commander `Marisi, Breaker of the Coil [R,G,W] NT`; 99 cartas do baralho, sendo 36 terrenos básicos ("Floresta" ×12, "Montanha" ×12, "Planície" ×12) e 63 cartas não-terreno distintas, todas com identidade de cor ⊆ {R,G,W}, cada uma aparecendo 1 vez, custos entre 1 e 6.
- Saída esperada: `legal = verdadeiro`, `violações = []`; estatística: total = 100, terrenos = 36, não-terrenos = 64 (63 do baralho + commander), custo médio calculado sobre as 64 cartas não-terreno.

**Exemplo 2 — baralho com tamanho errado**
- Entrada: commander válido + apenas 80 cartas no baralho (total 81).
- Saída esperada: `legal = falso`, `violações = [{regra: "tamanho do baralho", detalhe: "esperado 100, encontrado 81"}]`.

**Exemplo 3 — carta duplicada (violação de singleton)**
- Entrada: commander válido + 98 cartas não-terreno distintas + a carta "Sol Ring [] NT custo 1" aparecendo 2 vezes (99 + 1 duplicata = 100 no total).
- Saída esperada: `legal = falso`, `violações = [{regra: "singleton", detalhe: "'Sol Ring' aparece 2 vezes, máximo permitido é 1"}]`.

**Exemplo 4 — violação de identidade de cor**
- Entrada: commander `Marisi, Breaker of the Coil [R,G,W]` + baralho de 99 cartas válidas, exceto por 1 carta `Counterspell [U] NT custo 2` (azul, fora da identidade R/G/W).
- Saída esperada: `legal = falso`, `violações = [{regra: "identidade de cor", detalhe: "'Counterspell' tem cor U, fora da identidade do commander {R,G,W}"}]`.

**Exemplo 5 — múltiplas violações simultâneas**
- Entrada: commander válido + baralho com 90 cartas (tamanho errado) + a carta "Sol Ring" duplicada dentro dessas 90 + 1 carta azul fora da identidade de cor.
- Saída esperada: `legal = falso`, `violações` contendo as **três** violações (tamanho, singleton, identidade de cor), não apenas a primeira encontrada.

## 7. Casos-limite

1. **Baralho vazio**: lista de cartas do baralho com 0 elementos (apenas o commander). O sistema não deve travar; deve reportar violação de tamanho (`esperado 100, encontrado 1`) e ainda assim produzir o relatório estatístico (0 terrenos, 0 cartas não-terreno além do commander, custo médio = 0).
2. **Exatamente no limite (99 vs. 100 vs. 101)**: baralhos com 99 ou 101 cartas totais devem ser reportados como ilegais pela regra de tamanho, mesmo que todas as outras regras sejam respeitadas; apenas exatamente 100 é aceito.
3. **Carta incolor em commander colorido**: uma carta com identidade de cor vazia (ex.: um artefato incolor) deve ser sempre aceita, mesmo que o commander tenha identidade de cor vazia também (commander "incolor"), pois o conjunto vazio é subconjunto de qualquer conjunto, incluindo o vazio.
4. **Nome de carta duplicado com grafias diferentes**: nomes devem ser comparados exatamente como fornecidos (sensível a maiúsculas/minúsculas e espaços); "Sol Ring" e "sol ring" são tratadas como cartas **diferentes** nesta especificação — a normalização de nomes está fora do escopo (ver seção 8).
5. **Terreno não-básico duplicado**: um terreno que não é básico (`terreno básico = falso`) segue a regra de singleton normalmente — só pode aparecer 1 vez; apenas terrenos básicos são isentos desse limite.

## 8. Restrições

Está **fora do escopo** deste projeto:

- Verificar listas de cartas banidas/restritas por qualquer organização de torneio real;
- Buscar dados de cartas (nome, cores, custo) em uma base de dados externa ou API — todos os atributos das cartas fazem parte da entrada fornecida ao sistema;
- Suportar mais de um commander por baralho (mecânica de "parceiro"/partner) ou mecânicas especiais adicionais (companion, background, etc.);
- Normalização/correção de nomes de cartas (acentuação, maiúsculas/minúsculas, sinônimos);
- Qualquer interface gráfica, persistência em banco de dados ou leitura de arquivos externos — a forma de entrada/saída concreta (linha de comando, arquivo texto, etc.) será definida em etapa posterior, e pode variar entre paradigmas;
- Sugestão automática de cartas para corrigir um baralho ilegal (o sistema apenas diagnostica, não conserta).

## 9. Principais conceitos do domínio

- **Carta**: unidade básica do baralho, com nome, identidade de cor, tipo e custo de mana.
- **Commander**: carta especial que define a identidade de cor permitida no restante do baralho.
- **Identidade de cor**: subconjunto das cinco cores de mana associado a uma carta.
- **Terreno / Terreno básico**: categoria de carta com custo 0, subdividida entre básica (sem limite de cópias) e não-básica (limite de 1 cópia).
- **Baralho (deck)**: conjunto (com possíveis repetições) de cartas mais o commander.
- **Regra de legalidade**: cada uma das seis restrições estruturais listadas na seção 5.
- **Violação**: par (regra descumprida, detalhe da ocorrência) gerado quando uma regra não é satisfeita.
- **Relatório de legalidade**: resultado da verificação de todas as regras contra um baralho.
- **Relatório estatístico**: conjunto de métricas agregadas calculadas sobre o baralho (contagens, média, distribuição de cores).

## 10. Adequação aos quatro paradigmas

- **Imperativo**: as regras da seção 5 são naturalmente expressas como uma sequência de passos que percorrem a lista de cartas, mantêm contadores (total, contagem por nome, contagem por cor) e vão acumulando violações em uma estrutura mutável — um algoritmo passo a passo clássico de laços e condicionais.
- **Orientado a objetos**: o domínio tem entidades com atributos e comportamento próprio — `Carta`, `Commander` (podendo ser uma especialização de `Carta`) e `Baralho`, que pode encapsular sua lista de cartas e expor métodos como `verificarLegalidade()` e `gerarEstatisticas()`, escondendo os detalhes de verificação de cada regra atrás de uma interface coesa.
- **Funcional**: tanto a verificação de legalidade quanto a análise estatística podem ser expressas como funções puras que transformam uma lista de cartas em um relatório, compondo operações de `map`/`filter`/`reduce` (agrupar por nome para checar singleton, somar custos para a média, filtrar por cor para a distribuição) sem qualquer estado mutável compartilhado.
- **Lógico**: as regras da seção 5 podem ser escritas diretamente como fatos e cláusulas declarativas (ex.: `legal(Baralho) :- tamanho(Baralho, 100), singleton_ok(Baralho), identidade_cor_ok(Baralho), ...`), e o mecanismo de unificação/backtracking do Prolog é natural tanto para verificar um baralho dado quanto, futuramente, para consultar quais cartas causam violação — a própria noção de "conjunto de regras que devem ser satisfeitas" é o caso de uso clássico de um paradigma declarativo baseado em regras.

## 11. Linguagens inicialmente consideradas

| Paradigma | Linguagens candidatas | Justificativa |
|---|---|---|
| Imperativo | C, Python (estilo procedural) | C representa o paradigma imperativo de forma mais "pura" (controle explícito de laços, sem estruturas de alto nível escondendo o algoritmo); Python fica como alternativa caso se priorize velocidade de desenvolvimento sobre pureza conceitual. |
| Orientado a Objetos | Java, C# | Ambas têm suporte de primeira classe a classes, encapsulamento, herança e interfaces, além de ferramentas maduras de testes; a escolha final dependerá do ambiente de desenvolvimento disponível. |
| Funcional | Haskell, Elixir | Haskell é fortemente tipada e puramente funcional, o que força a modelagem sem estado mutável de forma explícita; Elixir é uma alternativa mais pragmática, funcional mas rodando sobre a BEAM, caso se prefira uma sintaxe mais próxima de linguagens convencionais. |
| Lógico | SWI-Prolog | É a implementação de Prolog mais usada em contexto acadêmico, com boa documentação e suporte nativo a unificação, backtracking e regras declarativas — adequada para expressar as regras de legalidade como cláusulas lógicas. |

A escolha definitiva de uma linguagem por paradigma será justificada em detalhe nas etapas de implementação correspondentes.
