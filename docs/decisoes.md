# Registro de decisões

Este documento acumulará, a cada etapa, as decisões de projeto tomadas (linguagens escolhidas, estruturas de dados, trade-offs entre paradigmas) e a justificativa de cada uma.

## [P4-ETAPA-01]

- Problema definido: validação e análise de legalidade de baralhos (ver `problema.md` / `especificacao.md`).
- Linguagens candidatas por paradigma listadas na seção 11 de `especificacao.md`; escolha definitiva será registrada aqui a partir da Etapa 03.

## [P4-ETAPA-02]

- Formalização do contrato semântico de dados e especificação detalhada dos 5 casos de exemplo e 3 casos-limite no documento `/testes/casos.md`.

## [P4-ETAPA-03]

- **Linguagem Escolhida**: Python 3 (estilo estritamente procedural/imperativo).
- **Estruturas de Dados**: Dicionários (`dict`) e listas (`list`) primitivas para representação do commander e das cartas. Nenhuma classe/orientação a objetos foi utilizada.
- **Modelo de Estado**: Mantido através de coleções e acumuladores mutáveis (`violacoes = []`, `total_cartas += 1`, `contagens[nome] += 1`).
- **Efeitos Colaterais**: Utilizados intencionalmente nos subprogramas de validação, que mutacionam diretamente a lista de violações recebida por referência.
- **Suíte de Testes**: Implementada em `/testes/test_imperativo.py` executando 8 casos de teste cobrindo todas as 6 regras do problema e estatísticas.

## [P4-ETAPA-04]

- **Linguagem Escolhida**: Python 3 (paradigma orientado a objetos).
- **Modelagem de Domínio**: Hierarquia de cartas (`Carta`, `CartaTerreno`, `CartaNaoTerreno`, `Commander`), Agregado `Baralho` e Objetos de Valor de Relatório.
- **Encapsulamento e Estado**: Atributos protegidos por `@property` com estado mantido nos próprios objetos do domínio.
- **Polimorfismo e Herança**: Aplicados no filtro de regras de cartas (`sujeita_a_singleton()`, `eh_terreno()`) e na hierarquia de regras de legalidade (`RegraLegalidade` via padrão Strategy).
- **Suíte de Testes**: Implementada em `/testes/test_poo.py` executando os 9 testes formais contra a implementação OO.
- **Reflexão**: Registrada em `/poo/reflexao.md` detalhando as diferenças conceituais em relação à implementação imperativa.
