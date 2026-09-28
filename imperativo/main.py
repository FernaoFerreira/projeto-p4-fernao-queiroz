"""
Ponto de entrada do executável — Implementação Imperativa [P4-ETAPA-03]

Este script executa uma demonstração imperativa do validador de baralhos,
exibindo relatórios de legalidade e estatísticas no terminal.
"""

import sys
from validador import analisar_baralho


def criar_baralho_exemplo():
    """Cria os dados de entrada do Exemplo 1 para demonstração."""
    commander = {
        "nome": "Marisi, Breaker of the Coil",
        "identidade_cor": ["R", "G", "W"],
        "custo_mana": 4,
        "tipo": "não-terreno"
    }

    cartas_baralho = []

    # 36 Terrenos básicos (12 Floresta, 12 Montanha, 12 Planície)
    for _ in range(12):
        cartas_baralho.append({
            "nome": "Floresta",
            "identidade_cor": [],
            "tipo": "terreno",
            "custo_mana": 0,
            "terreno_basico": True
        })
        cartas_baralho.append({
            "nome": "Montanha",
            "identidade_cor": [],
            "tipo": "terreno",
            "custo_mana": 0,
            "terreno_basico": True
        })
        cartas_baralho.append({
            "nome": "Planície",
            "identidade_cor": [],
            "tipo": "terreno",
            "custo_mana": 0,
            "terreno_basico": True
        })

    # 63 Cartas não-terreno distintas
    for i in range(1, 64):
        cartas_baralho.append({
            "nome": f"Card {i}",
            "identidade_cor": ["G"],
            "tipo": "não-terreno",
            "custo_mana": 2,
            "terreno_basico": False
        })

    return commander, cartas_baralho


def exibir_relatorio(resultado):
    """Exibe o relatório formatado imperativamente."""
    print("=" * 60)
    print("         RELATÓRIO DE LEGALIDADE E ANÁLISE DO BARALHO")
    print("=" * 60)
    
    if resultado["legal"]:
        print("Status: LEGAL ✅")
    else:
        print("Status: ILEGAL ❌")

    print("\n[Violações Encontradas]")
    if len(resultado["violacoes"]) == 0:
        print("  Nenhuma violação encontrada.")
    else:
        for idx, v in enumerate(resultado["violacoes"], 1):
            print(f"  {idx}. [{v['regra']}] {v['detalhe']}")

    est = resultado["estatisticas"]
    print("\n[Relatório Estatístico]")
    print(f"  Total de cartas: {est['total_cartas']}")
    print(f"  Terrenos: {est['terrenos']}")
    print(f"  Não-terrenos: {est['nao_terrenos']}")
    print(f"  Custo de mana médio (não-terrenos): {est['custo_medio_nao_terrenos']:.2f}")
    print("  Distribuição de cores:")
    for cor, qtd in est["distribuicao_cores"].items():
        print(f"    - {cor}: {qtd}")
    print("=" * 60)


def main():
    print("[ETAPA 03 - IMPLEMENTAÇÃO IMPERATIVA]")
    print("Carregando baralho de exemplo...")
    commander, baralho = criar_baralho_exemplo()
    
    print("Executando análise imperativa...")
    resultado = analisar_baralho(commander, baralho)
    
    exibir_relatorio(resultado)


if __name__ == "__main__":
    main()
