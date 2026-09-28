# Documentação da Implementação Imperativa

`[P4-ETAPA-03]`

Este documento apresenta as decisões de projeto, a arquitetura e a justificativa conceitual da solução desenvolvida sob o **paradigma imperativo** para a validação e análise estatística de baralhos.

---

## 1. Quais estados são mantidos

Na solução imperativa (`/imperativo/validador.py`), o estado do programa é mantido por meio de variáveis mutáveis locais e coleções que são modificadas passo a passo durante a execução:

- `violacoes`: Lista de dicionários mutável initialized na função `analisar_baralho` e passada por referência aos subprogramas de validação. Cada subprograma insere diretamente novas violações encontradas.
- `contagens`: Dicionário mutável mantido dentro do subprograma `verificar_singleton` para acumular a contagem de ocorrências de cada carta no baralho (`contagens[nome] += 1`).
- `acumuladores de estatísticas`: Variáveis numéricas e dicionários locais mantidos na função `calcular_estatisticas`:
  - `total_cartas`: contador inteiro incrementado a cada carta processada (`total_cartas += 1`);
  - `qtd_terrenos`: contador inteiro incrementado para cartas do tipo terreno (`qtd_terrenos += 1`);
  - `qtd_nao_terrenos`: contador inteiro incrementado para cartas não-terreno (`qtd_nao_terrenos += 1`);
  - `soma_custos_nao_terrenos`: acumulador numérico que soma o custo de mana convertido das cartas não-terreno (`soma_custos_nao_terrenos += custo`);
  - `distribuicao_cores`: dicionário mutável com as chaves `{"W", "U", "B", "R", "G"}` cujos valores inteiros são incrementados quando uma cor é encontrada na identidade de uma carta (`distribuicao_cores[cor] += 1`);
- `eh_legal`: Variável booleana calculada ao final com base na checagem de tamanho da lista `violacoes` (`len(violacoes) == 0`).

---

## 2. Quais operações modificam esses estados

As modificações de estado ocorrem através de instruções explícitas de **atribuição**, **incremento** e **mutação de estruturas de dados**:

- **Atribuição simples**: `total_cartas = 0`, `eh_legal = (len(violacoes) == 0)`, `contagens[nome] = 1`.
- **Incremento e Acumulação**: `total_cartas += 1`, `qtd_terrenos += 1`, `soma_custos_nao_terrenos += custo`, `distribuicao_cores[cor] += 1`.
- **Modificação de listas por efeito colateral**: `violacoes.append({...})`.
- **Reatribuição de ponteiro de laço**: `posicao += 1`.

---

## 3. Onde aparecem efeitos colaterais

Efeitos colaterais são centrais na arquitetura imperativa escolhida:

1. **Mutação de Parâmetros**:
   - Os subprogramas `verificar_nome_nao_vazio`, `verificar_tamanho_baralho`, `verificar_commander_no_baralho`, `verificar_singleton`, `verificar_identidade_cor` e `verificar_custo_mana` não retornam novos dados. Em vez disso, eles recebem a referência da lista `violacoes` e produzem o efeito colateral de anexar diretamente novas violações a essa lista.

2. **I/O no Terminal (Ponto de Entrada `main.py`)**:
   - A função `exibir_relatorio` em `main.py` realiza efeitos colaterais de entrada/saída (impressão de mensagens formatadas via `print`), enviando o resultado da computação para o terminal.

---

## 4. Quais estruturas de controle foram utilizadas

A solução utiliza estritamente as estruturas tradicionais do paradigma imperativo:

- **Laços de Repetição (`for`)**:
  - `for carta in cartas_baralho`: iteração sequencial sobre a lista de cartas para verificação de regras e acúmulo de estatísticas;
  - `for cor in carta.get("identidade_cor", [])`: iteração sobre as cores de cada carta;
  - `for nome, qtd in contagens.items()`: iteração sobre os pares chave-valor para verificar violações de singleton.
- **Interrupção de Laço (`break`)**:
  - Utilizado em `verificar_commander_no_baralho` para interromper a busca assim que o commander é encontrado na lista de cartas.
- **Estruturas Condicionais (`if / elif / else`)**:
  - Desvio de fluxo em `verificar_tamanho_baralho` (`if total_cartas != 100`);
  - Desvio de fluxo em `verificar_singleton` para ignorar terrenos básicos (`if tipo != "terreno" or not eh_basico`);
  - Desvio em `calcular_estatisticas` para contagem diferenciada entre terrenos e não-terrenos.

---

## 5. Como os subprogramas foram organizados

A solução em `/imperativo/validador.py` foi estruturada em procedimentos/funções imperativas com responsabilidades bem delimitadas:

```
analisar_baralho(commander, cartas_baralho)
  │
  ├──► verificar_nome_nao_vazio(...)       (mutaciona 'violacoes')
  ├──► verificar_tamanho_baralho(...)       (mutaciona 'violacoes')
  ├──► verificar_commander_no_baralho(...)  (mutaciona 'violacoes')
  ├──► verificar_singleton(...)             (mutaciona 'violacoes')
  ├──► verificar_identidade_cor(...)        (mutaciona 'violacoes')
  ├──► verificar_custo_mana(...)            (mutaciona 'violacoes')
  │
  ├──► calcular_estatisticas(...)          (retorna dict com totais)
  │
  └──► Constrói o resultado final (legal = len(violacoes) == 0)
```

Cada subprograma de validação é focado em uma única regra (ou grupo de regras afins) e compartilha a mesma convenção de parâmetros: `(commander/cartas_baralho, violacoes)`.

---

## 6. Por que a solução pode ser considerada predominantemente imperativa

 A implementação é **predominantemente imperativa** porque:

1. **Ausência de Abstrações Orientadas a Objetos**: Não há classes, construtores, herança ou métodos de instância. Os dados do problema são mantidos em tipos de dados primitivos/nativos (dicionários e listas).
2. **Modelo de Computação Baseado em Mudança de Estado**: A lógica não é expressa como composições de funções puras ou transformações imutáveis (`map`/`filter`/`reduce`), mas sim como uma receita passo a passo de como alterar o estado de variáveis (acumuladores e listas).
3. **Fluxo de Execução Sequencial e Explícito**: A execução avança instruction-by-instruction, onde a ordem exata das chamadas e a modificação procedural de variáveis determinam o resultado final.

---

## 7. Como os dados entram, são processados e produzem a saída

```
ENTRADA
  Commander: dict {'nome', 'identidade_cor', 'custo_mana', 'tipo'}
  Cartas do Baralho: list[dict {'nome', 'identidade_cor', 'tipo', 'custo_mana', 'terreno_basico'}]
     │
     ▼
PROCESSAMENTO IMPERATIVO
  1. Inicializa o estado mutável: violacoes = []
  2. Executa proceduralmente a verificação de cada regra (modificando violacoes)
  3. Executa a varredura do baralho acumulando estatísticas em variáveis
     │
     ▼
ALTERAÇÃO DE ESTADO E DECISÃO
  - violacoes preenchida com as falhas
  - eh_legal = (len(violacoes) == 0)
     │
     ▼
SAÍDA
  Relatório estruturado: dict {'legal': bool, 'violacoes': list, 'estatisticas': dict}
  Ponto de entrada (main.py): Impressão formatada no terminal
```
