# Projeto P4 — Um Problema, Quatro Paradigmas

**Disciplina:** Paradigmas de Linguagens de Programação
**Aluno:** Fernão Queiroz Ferreira

## Sobre o projeto

Este repositório documenta o desenvolvimento, ao longo do semestre, de soluções para **um único problema** implementadas em **quatro paradigmas de programação** diferentes: imperativo, orientado a objetos, funcional e lógico. O objetivo não é traduzir um mesmo código de uma linguagem para outra, e sim reformular a solução de acordo com o modelo de pensamento de cada paradigma.

## Problema escolhido

**Validador e Analisador de Legalidade de Baralhos** (formato inspirado em "Commander/EDH"): dado um commander e a lista de cartas de um baralho, o sistema determina se o baralho é legal segundo um conjunto de regras estruturais, reporta todas as violações encontradas e produz uma análise estatística do baralho.

Ver a especificação completa em [`docs/especificacao.md`](docs/especificacao.md).

## Estrutura do repositório

```
projeto-p4-fernao/
│
├── README.md
│
├── docs/
│   ├── problema.md            # resumo do problema escolhido
│   ├── especificacao.md       # especificação completa (Etapa 01)
│   ├── decisoes.md            # registro de decisões técnicas por etapa
│   └── comparacao-final.md    # comparação entre paradigmas (etapa final)
│
├── testes/
│   └── casos.md                # casos de teste formais (Etapa 02)
│
├── imperativo/                 # implementação imperativa
├── poo/                        # implementação orientada a objetos
├── funcional/                  # implementação funcional
├── logico/                     # implementação lógica
└── integrado/                  # integração/comparação final entre implementações
```

## Progresso das etapas

| Etapa | Tag | Status |
|---|---|---|
| 01 — Proposta e especificação do problema | `[P4-ETAPA-01]` | ✅ concluída |
| 02 — Contrato semântico e testes | `[P4-ETAPA-02]` | ⬜ pendente |
| 03 — Implementação imperativa | `[P4-ETAPA-03]` | ⬜ pendente |
| 04 — Implementação orientada a objetos | `[P4-ETAPA-04]` | ⬜ pendente |
| 05 — Implementação funcional | `[P4-ETAPA-05]` | ⬜ pendente |
| 06 — Implementação lógica | `[P4-ETAPA-06]` | ⬜ pendente |
| 07 — Comparação final | `[P4-ETAPA-07]` | ⬜ pendente |

*(numeração de etapas 02+ é provisória — ajustar conforme o roteiro definitivo passado em aula.)*
