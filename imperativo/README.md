# Implementação Imperativa — Validador de Baralhos

`[P4-ETAPA-03]`

Esta pasta contém a implementação do validador e analisador de legalidade de baralhos utilizando o **paradigma imperativo (procedural)** em Python.

## Estrutura dos Arquivos

- `validador.py`: Módulo principal da implementação imperativa. Contém os subprogramas de verificação de regras, acúmulo estatístico e a função `analisar_baralho`.
- `main.py`: Executável de demonstração em linha de comando.
- `documentacao.md`: Documentação técnica detalhada respondendo aos 7 tópicos obrigatórios sobre decisões de projeto, estados mantidos, efeitos colaterais e estruturas de controle.

## Como Executar

### Demonstração via CLI
Para executar a demonstração imperativa com o baralho de exemplo:

```bash
python3 imperativo/main.py
```

### Execução dos Testes Automatizados
Para rodar a suíte de testes formais (Casos 1–5 e Casos-limite 1–3) contra a implementação imperativa:

```bash
python3 testes/test_imperativo.py
```
