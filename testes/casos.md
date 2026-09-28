# Casos de Teste Formais

`[P4-ETAPA-02 / P4-ETAPA-03]`

Este documento especifica os casos de teste formais utilizados para validar a legalidade e as estatísticas de baralhos nas diferentes implementações do projeto.

---

## Estrutura de Dados das Entradas e Saídas

### Representação do Commander
- `nome`: texto (não vazio)
- `identidade_cor`: conjunto/lista de cores (ex: `["R", "G", "W"]`, `[]`)
- `custo_mana`: número inteiro (≥ 0)
- `tipo`: `"não-terreno"` (fixo por especificação)

### Representação de Carta do Baralho
- `nome`: texto (não vazio)
- `identidade_cor`: conjunto/lista de cores (ex: `["U"]`, `[]`)
- `tipo`: `"terreno"` ou `"não-terreno"`
- `custo_mana`: número inteiro (≥ 0; para terrenos, deve ser 0)
- `terreno_basico`: booleano (`True` se for terreno básico, `False` caso contrário)

### Estrutura da Saída
- **Relatório de Legalidade**:
  - `legal`: booleano (`True` ou `False`)
  - `violacoes`: lista de objetos contendo `regra` e `detalhe`
- **Relatório Estatístico**:
  - `total_cartas`: número inteiro
  - `terrenos`: número inteiro
  - `nao_terrenos`: número inteiro
  - `custo_medio_nao_terrenos`: número de ponto flutuante
  - `distribuicao_cores`: dicionário/mapa contendo as contagens para `{"W": int, "U": int, "B": int, "R": int, "G": int}`

---

## Casos de Teste

### Caso 1: Baralho Legal Simples (Exemplo 1)
- **Descrição**: Baralho completo de 100 cartas (1 commander + 99 cartas no baralho) respeitando todas as regras.
- **Entrada**:
  - Commander: `Marisi, Breaker of the Coil` `[R, G, W]`, custo 4.
  - Baralho (99 cartas):
    - 36 terrenos básicos: 12× "Floresta" `[]`, 12× "Montanha" `[]`, 12× "Planície" `[]`.
    - 63 cartas não-terreno distintas com nomes `"Card 1"` até `"Card 63"`, cada uma com custo 2, cores `["G"]`.
- **Saída Esperada**:
  - `legal`: `True`
  - `violacoes`: `[]`
  - Estatísticas:
    - `total_cartas`: 100
    - `terrenos`: 36
    - `nao_terrenos`: 64
    - `custo_medio_nao_terrenos`: 2.03125 (Cálculo: (4 + 63 * 2) / 64 = 130 / 64 = 2.03125)
    - `distribuicao_cores`: `{"W": 1, "U": 0, "B": 0, "R": 1, "G": 64}`

---

### Caso 2: Baralho com Tamanho Incorreto (Exemplo 2)
- **Descrição**: Baralho com quantidade de cartas diferente de 100 no total (80 cartas no baralho + 1 commander = 81).
- **Entrada**:
  - Commander: `Marisi, Breaker of the Coil` `[R, G, W]`, custo 4.
  - Baralho: 80 cartas válidas (30 terrenos básicos, 50 não-terrenos distintos dentro das cores).
- **Saída Esperada**:
  - `legal`: `False`
  - `violacoes`:
    - `{"regra": "tamanho do baralho", "detalhe": "esperado 100, encontrado 81"}`
  - Estatísticas:
    - `total_cartas`: 81
    - `terrenos`: 30
    - `nao_terrenos`: 51

---

### Caso 3: Carta Duplicada - Violação de Singleton (Exemplo 3)
- **Descrição**: Carta não-terreno e não-básica duplicada na lista de cartas do baralho.
- **Entrada**:
  - Commander: `Marisi, Breaker of the Coil` `[R, G, W]`, custo 4.
  - Baralho (99 cartas):
    - 36 terrenos básicos.
    - 61 cartas não-terreno distintas.
    - 2 cópias de `"Sol Ring"` `[]`, custo 1.
- **Saída Esperada**:
  - `legal`: `False`
  - `violacoes`:
    - `{"regra": "singleton", "detalhe": "'Sol Ring' aparece 2 vezes, máximo permitido é 1"}`
  - Estatísticas:
    - `total_cartas`: 100
    - `terrenos`: 36
    - `nao_terrenos`: 64

---

### Caso 4: Violação de Identidade de Cor (Exemplo 4)
- **Descrição**: Carta no baralho possui cor fora da identidade de cor do commander.
- **Entrada**:
  - Commander: `Marisi, Breaker of the Coil` `[R, G, W]`, custo 4.
  - Baralho (99 cartas):
    - 36 terrenos básicos.
    - 62 cartas não-terreno válidas.
    - 1 carta `"Counterspell"` `["U"]`, custo 2.
- **Saída Esperada**:
  - `legal`: `False`
  - `violacoes`:
    - `{"regra": "identidade de cor", "detalhe": "'Counterspell' tem cor U, fora da identidade do commander {R, G, W}"}`

---

### Caso 5: Múltiplas Violações Simultâneas (Exemplo 5)
- **Descrição**: O baralho apresenta violações de tamanho, singleton e identidade de cor simultaneamente.
- **Entrada**:
  - Commander: `Marisi, Breaker of the Coil` `[R, G, W]`, custo 4.
  - Baralho (90 cartas):
    - 30 terrenos básicos.
    - 57 cartas não-terreno distintas válidas.
    - 2 cópias de `"Sol Ring"` `[]` (duplicata).
    - 1 carta `"Counterspell"` `["U"]` (cor proibida).
    - Total de cartas no baralho = 90 (com commander = 91).
- **Saída Esperada**:
  - `legal`: `False`
  - `violacoes`: contendo as 3 violações descritas (tamanho do baralho, singleton, e identidade de cor).

---

### Caso 6: Caso-Limite 1 - Baralho Vazio (Apenas Commander)
- **Descrição**: Baralho sem nenhuma carta no baralho principal (apenas o commander).
- **Entrada**:
  - Commander: `Marisi, Breaker of the Coil` `[R, G, W]`, custo 4.
  - Baralho: `[]` (0 cartas).
- **Saída Esperada**:
  - `legal`: `False`
  - `violacoes`:
    - `{"regra": "tamanho do baralho", "detalhe": "esperado 100, encontrado 1"}`
  - Estatísticas:
    - `total_cartas`: 1
    - `terrenos`: 0
    - `nao_terrenos`: 1
    - `custo_medio_nao_terrenos`: 4.0
    - `distribuicao_cores`: `{"W": 1, "U": 0, "B": 0, "R": 1, "G": 1}`

---

### Caso 7: Caso-Limite 2 - Limites Estritos de Tamanho (99 vs 100 vs 101)
- **Descrição**: Testar o comportamento em torno da contagem limite de 100 cartas totais.
- **Entrada 7a**: Commander + 98 cartas no baralho (total 99).
  - Saída: `legal: False`, violação de tamanho (`encontrado 99`).
- **Entrada 7b**: Commander + 99 cartas válidas no baralho (total 100).
  - Saída: `legal: True`, `violacoes: []`.
- **Entrada 7c**: Commander + 100 cartas no baralho (total 101).
  - Saída: `legal: False`, violação de tamanho (`encontrado 101`).

---

### Caso 8: Caso-Limite 3 - Terreno Não-Básico Duplicado, Commander no Baralho, Nome Vazio e Custos Inválidos
- **Descrição**: Testar regras específicas do contrato:
  - **8a**: Terreno não-básico duplicado (ex: 2× `"Reliquary Tower"`, `terreno_basico = False`) gera violação de singleton.
  - **8b**: Commander presente na lista do baralho (mesmo nome) gera violação da regra de commander no baralho.
  - **8c**: Carta ou commander com nome vazio `""` gera violação da regra de nome não vazio.
  - **8d**: Carta com custo de mana negativo (< 0) ou terreno com custo > 0 gera violação de custo de mana.
