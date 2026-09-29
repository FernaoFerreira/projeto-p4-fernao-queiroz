# Reflexão — Etapa 04

`[P4-ETAPA-04]`

Este documento analisa criticamente a reestruturação da solução do problema de validação e análise estatística de baralhos sob o **paradigma orientado a objetos (POO)**, comparando-a diretamente com a solução imperativa da Etapa 03.

---

## Como meu modelo mudou do paradigma imperativo para o orientado a objetos?

A transição da abordagem imperativa (procedural) para a orientada a objetos não foi uma mera encapsulação sintática de funções em métodos ou dicionários em atributos. Houve uma **mudança fundamental na atribuição de responsabilidades e na representação do estado do sistema**.

### Comparação Direta entre as Abordagens

| Dimensão | Paradigma Imperativo (Etapa 03) | Paradigma Orientado a Objetos (Etapa 04) |
|---|---|---|
| **Representação do Estado** | Variáveis mutáveis e estruturas primitivas desacopladas (`dict`, `list`). O estado do relatório é acumulado por mutação direta de parâmetros. | Objetos de domínio encapsulados (`Carta`, `Baralho`, `Violacao`, `RelatorioBaralho`). O estado pertence aos objetos que possuem autoridade sobre ele. |
| **Responsabilidades** | Centralizadas em subprogramas procedurais que manipulam dados externos passados como parâmetros. | Distribuídas de forma coesa entre entidades do domínio (`Carta` sabe suas regras próprias, `Baralho` conhece sua coleção, `RegraLegalidade` valida aspectos específicos). |
| **Relacionamento** | Sem relacionamentos explícitos no código; dados são passados como tuplas/dicionários entre funções procedurais. | Relações formais de Herança (`CartaTerreno` IS-A `Carta`), Agregação/Composição (`Baralho` HAS-A `Commander` e `Carta`), e Associação (`ValidadorBaralho` usa `RegraLegalidade`). |
| **Reutilização** | Reutilização de funções por chamadas explícitas de subprogramas. | Reutilização através de polimorfismo, interfaces abstratas e composição de regras (Padrão Strategy). |
| **Encapsulamento** | Inexistente sobre os dados; dicionários possuem todos os seus campos expostos publicamente. | Presente via atributos protegidos (`_nome`, `_cartas`) expostos exclusivamente por `properties` e métodos de consulta. |
| **Extensão do Sistema** | Exige modificar funções existentes (ex: adicionar `if` para novas regras no script procedural). | Princípio Aberto/Fechado (OCP): para adicionar uma nova regra, basta criar uma nova subclasse de `RegraLegalidade` e registrá-la no `ValidadorBaralho`, sem alterar o código existente. |

---

## Detalhamento das Classes Criadas

A implementação em `/poo/` foi organizada nas seguintes classes e responsabilidades:

### 1. Hierarquia de Cartas (`cartas.py`)

- **`Carta` (Classe Abstrata Base)**:
  - *Por que existe*: Define o contrato comum e encapsula o estado básico de qualquer carta (`nome`, `identidade_cor`, `custo_mana`).
  - *Responsabilidades*: Validar nome não vazio, expor propriedades somente-leitura e calcular cores que violam uma identidade.
  - *Métodos abstratos/polimórficos*: `eh_terreno()`, `sujeita_a_singleton()`.

- **`CartaTerreno(Carta)` (Subclasse)**:
  - *Por que existe*: Representa especificamente cartas do tipo terreno, que possuem regras próprias (custo obrigatoriamente zero, distinção entre básico e não-básico).
  - *Responsabilidades*: Encapsular o atributo `_terreno_basico`, sobrescrever `eh_terreno()` retornando `True`, e sobrescrever `custo_valido()` garantindo `custo == 0`.

- **`CartaNaoTerreno(Carta)` (Subclasse)**:
  - *Por que existe*: Representa magias, criaturas e artefatos (cartas não-terreno).
  - *Responsabilidades*: Sobrescrever `eh_terreno()` retornando `False`.

- **`Commander(CartaNaoTerreno)` (Subclasse Especializada)**:
  - *Por que existe*: Representa a carta do Commander, que herda todas as características de uma carta não-terreno, mas possui papel de liderança do baralho.
  - *Responsabilidades*: Definir a identidade de cor de referência para todo o restante do baralho.

### 2. Agregado Baralho (`baralho.py`)

- **`Baralho` (Aggregate Root)**:
  - *Por que existe*: Representa a entidade unificada do baralho (Commander + coleção de cartas).
  - *Responsabilidades*: Encapsular a lista de cartas, expor consultas agregadas (`total_cartas()`, `obter_cartas_sujeitas_a_singleton()`) e calcular de forma coesa seu próprio relatório estatístico (`calcular_estatisticas()`).

### 3. Hierarquia de Regras / Padrão Strategy (`regras.py`)

- **`RegraLegalidade` (Classe Abstrata Interface)**:
  - *Por que existe*: Estabelece a interface polimórfica `validar(baralho: Baralho) -> list[Violacao]`.
- **Subclasses Concretas de Regra**:
  - `RegraNomeNaoVazio`: Valida nomes não vazios no Commander e nas cartas.
  - `RegraTamanho`: Valida a contagem exata de 100 cartas no `Baralho`.
  - `RegraCommanderNoBaralho`: Valida se o Commander não está duplicado na lista.
  - `RegraSingleton`: Valida o limite de 1 cópia utilizando a consulta polimórfica de singleton do `Baralho`.
  - `RegraIdentidadeCor`: Valida a compatibilidade de cores com o Commander.
  - `RegraCustoMana`: Valida se cada carta respeita as regras de custo.

### 4. Serviço de Domínio e Relatórios (`validador.py` e `relatorios.py`)

- **`ValidadorBaralho` (Domain Service)**:
  - *Por que existe*: Orquestra a execução das estratégias de validação cadastradas.
  - *Responsabilidades*: Manter a lista de `RegraLegalidade`, iterar sobre elas gerando o `RelatorioBaralho`.
- **Objetos de Valor (`Violacao`, `RelatorioEstatistico`, `RelatorioBaralho`)**:
  - *Por que existem*: Encapsulam imutavelmente os resultados da validação e estatísticas, provendo o método `para_dicionario()` para exportação.

---

## Análise dos Pilares de Orientação a Objetos na Implementação

### Encapsulamento
Todos os atributos internos das classes foram definidos com prefixo protegido (`_nome`, `_cartas`, `_regras`) e são expostos externamente apenas por `@property` que retornam cópias imutáveis ou conjuntos seguros (ex: `return set(self._identidade_cor)`), impedindo que código externo corrompa o estado do objeto.

### Composição e Agregação
- **Agregação**: A classe `Baralho` agrega uma referência para `Commander` e uma lista de objetos `Carta`. As cartas existem conceitualmente por si só, mas dentro do `Baralho` formam uma unidade agregada.
- **Composição**: O `ValidadorBaralho` é composto por uma coleção de instâncias de `RegraLegalidade`. O relatório final `RelatorioBaralho` é composto por objetos `Violacao` e `RelatorioEstatistico`.

### Polimorfismo
O polimorfismo é aplicado de forma centralizada em dois locais:
1. **Comportamento Polimórfico de Cartas**: O método `sujeita_a_singleton()` em `Carta` e `eh_basica()` permitem que o `Baralho` filtre cartas sem precisar fazer checagem manual de tipos com `isinstance`. Da mesma forma, `custo_valido()` comporta-se de maneira polimórfica entre `CartaTerreno` e `CartaNaoTerreno`.
2. **Polimorfismo de Regras (Strategy Pattern)**: O `ValidadorBaralho` itera sobre a lista `self._regras` chamando `regra.validar(baralho)` de forma totalmente agnóstica em relação a qual regra concreta está sendo executada.

### Herança e sua Justificativa
A herança foi utilizada em duas hierarquias onde há relação conceitual válida e natural no domínio (*IS-A*):
1. `CartaTerreno` e `CartaNaoTerreno` herdam de `Carta`: Ambas compartilham o conceito base de carta do jogo (nome, cores, custo), mas especializam comportamentos do tipo.
2. Subclasses de `RegraLegalidade` herdam de `RegraLegalidade`: Representa o contrato de interface de estratégias de validação.

A herança **não foi forçada em locais indevidos**: por exemplo, `Baralho` não herda de `list`, e sim engloba uma lista por composição. `Commander` herda de `CartaNaoTerreno` por ser uma carta não-terreno do jogo, sem artificialidade.
