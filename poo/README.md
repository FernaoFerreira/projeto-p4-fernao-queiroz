# Implementação Orientada a Objetos — Validador de Baralhos

`[P4-ETAPA-04]`

Esta pasta contém a reimplementação do validador e analisador de legalidade de baralhos utilizando o **paradigma orientado a objetos (POO)** em Python.

## Estrutura dos Arquivos

- `cartas.py`: Hierarquia de classes de cartas (`Carta`, `CartaTerreno`, `CartaNaoTerreno`, `Commander`) demonstrando herança, encapsulamento e polimorfismo.
- `baralho.py`: Agregado `Baralho` (Aggregate Root) encapsulando a coleção de cartas e cálculos estatísticos do domínio.
- `regras.py`: Hierarquia de regras de legalidade aplicando o padrão **Strategy / Polimorfismo** (`RegraLegalidade`, `RegraTamanho`, `RegraSingleton`, etc.).
- `relatorios.py`: Objetos de valor para relatórios e violações (`Violacao`, `RelatorioEstatistico`, `RelatorioBaralho`).
- `validador.py`: Serviço de domínio `ValidadorBaralho` e adaptadores de entrada.
- `main.py`: Executável de demonstração orientada a objetos.
- `reflexao.md`: Documentação de reflexão conceitual respondendo às comparações entre os paradigmas imperativo e orientado a objetos.

## Como Executar

### Demonstração via CLI
Para executar a demonstração OO com o baralho de exemplo:

```bash
python3 poo/main.py
```

### Execução dos Testes Automatizados
Para rodar a suíte de testes formais contra a implementação orientada a objetos:

```bash
python3 testes/test_poo.py
```
