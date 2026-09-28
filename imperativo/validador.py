"""
Módulo de Validação e Análise de Baralhos — Paradigma Imperativo

Este módulo implementa a validação estrutural e a análise estatística de baralhos
utilizando estritamente o paradigma IMPERATIVO (procedural).

Decisões de Projeto:
1. Sem orientação a objetos/classes: cartas e relatórios são estruturados como
   dicionários e listas primitivas.
2. Estado mutável e acumuladores: subprogramas recebem coleções mutáveis (ex: lista de violações)
   e alteram seus estados diretamente via instrução de atribuição/append.
3. Fluxo de controle imperativo: laços explícitos (for) e condicionais (if/elif/else).
"""

def verificar_nome_nao_vazio(commander, cartas_baralho, violacoes):
    """
    Verifica se o commander ou alguma carta do baralho possui nome vazio.
    Modifica a lista 'violacoes' caso encontre nomes inválidos.
    """
    if not commander.get("nome") or str(commander.get("nome")).strip() == "":
        violacoes.append({
            "regra": "nome não vazio",
            "detalhe": "O commander possui um nome vazio ou inválido"
        })

    posicao = 1
    for carta in cartas_baralho:
        nome = carta.get("nome")
        if not nome or str(nome).strip() == "":
            violacoes.append({
                "regra": "nome não vazio",
                "detalhe": f"A carta na posição {posicao} do baralho possui nome vazio"
            })
        posicao += 1


def verificar_tamanho_baralho(commander, cartas_baralho, violacoes):
    """
    Verifica se o baralho possui exatamente 100 cartas no total (1 commander + baralho).
    Modifica 'violacoes' se o total for diferente de 100.
    """
    total_cartas = 1 + len(cartas_baralho)
    if total_cartas != 100:
        violacoes.append({
            "regra": "tamanho do baralho",
            "detalhe": f"esperado 100, encontrado {total_cartas}"
        })


def verificar_commander_no_baralho(commander, cartas_baralho, violacoes):
    """
    Verifica se a carta do commander aparece listada como carta comum do baralho.
    Modifica 'violacoes' caso o commander apareça no baralho.
    """
    nome_commander = commander.get("nome")
    if not nome_commander:
        return

    encontrado = False
    for carta in cartas_baralho:
        if carta.get("nome") == nome_commander:
            encontrado = True
            break

    if encontrado:
        violacoes.append({
            "regra": "commander no baralho",
            "detalhe": f"a carta '{nome_commander}' é o commander e não pode estar na lista do baralho"
        })


def verificar_singleton(cartas_baralho, violacoes):
    """
    Verifica a regra de singleton (máximo de 1 cópia para cartas não-terreno e terrenos não-básicos).
    Acumula as contagens em um dicionário mutável e reporta violações.
    """
    contagens = {}

    # Passo 1: Contar ocorrências das cartas sujeitas à regra de singleton
    for carta in cartas_baralho:
        tipo = carta.get("tipo")
        eh_basico = carta.get("terreno_basico", False)

        # Apenas não-terrenos e terrenos não-básicos estão sujeitos ao singleton
        if tipo != "terreno" or not eh_basico:
            nome = carta.get("nome")
            if nome:
                if nome in contagens:
                    contagens[nome] += 1
                else:
                    contagens[nome] = 1

    # Passo 2: Reportar nomes que excedem 1 cópia
    for nome, qtd in contagens.items():
        if qtd > 1:
            violacoes.append({
                "regra": "singleton",
                "detalhe": f"'{nome}' aparece {qtd} vezes, máximo permitido é 1"
            })


def verificar_identidade_cor(commander, cartas_baralho, violacoes):
    """
    Verifica se todas as cores da identidade de cor de cada carta do baralho
    estão contidas na identidade de cor do commander.
    """
    cores_commander = set(commander.get("identidade_cor", []))
    cores_commander_fmt = "{" + ", ".join(sorted(list(cores_commander))) + "}"

    for carta in cartas_baralho:
        cores_carta = carta.get("identidade_cor", [])
        cores_proibidas = []
        for cor in cores_carta:
            if cor not in cores_commander:
                cores_proibidas.append(cor)

        if len(cores_proibidas) > 0:
            cores_proibidas_str = ", ".join(sorted(cores_proibidas))
            nome_carta = carta.get("nome", "Desconhecida")
            violacoes.append({
                "regra": "identidade de cor",
                "detalhe": f"'{nome_carta}' tem cor {cores_proibidas_str}, fora da identidade do commander {cores_commander_fmt}"
            })


def verificar_custo_mana(cartas_baralho, violacoes):
    """
    Verifica regras de custo de mana:
    - Nenhuma carta pode ter custo < 0
    - Terrenos devem ter custo == 0
    """
    for carta in cartas_baralho:
        nome = carta.get("nome", "Desconhecida")
        custo = carta.get("custo_mana", 0)
        tipo = carta.get("tipo")

        if custo < 0:
            violacoes.append({
                "regra": "custo de mana",
                "detalhe": f"a carta '{nome}' possui custo de mana negativo: {custo}"
            })

        if tipo == "terreno" and custo > 0:
            violacoes.append({
                "regra": "custo de mana",
                "detalhe": f"o terreno '{nome}' possui custo de mana maior que zero: {custo}"
            })


def calcular_estatisticas(commander, cartas_baralho):
    """
    Processa e calcula todas as estatísticas do baralho através da manutenção
    de acumuladores mutáveis.
    """
    total_cartas = 0
    qtd_terrenos = 0
    qtd_nao_terrenos = 0
    soma_custos_nao_terrenos = 0
    distribuicao_cores = {"W": 0, "U": 0, "B": 0, "R": 0, "G": 0}

    # Processamento do Commander (sempre tratado como carta não-terreno)
    total_cartas += 1
    qtd_nao_terrenos += 1
    soma_custos_nao_terrenos += commander.get("custo_mana", 0)

    for cor in commander.get("identidade_cor", []):
        if cor in distribuicao_cores:
            distribuicao_cores[cor] += 1

    # Processamento das cartas do baralho
    for carta in cartas_baralho:
        total_cartas += 1
        tipo = carta.get("tipo")

        if tipo == "terreno":
            qtd_terrenos += 1
        else:
            qtd_nao_terrenos += 1
            soma_custos_nao_terrenos += carta.get("custo_mana", 0)

        for cor in carta.get("identidade_cor", []):
            if cor in distribuicao_cores:
                distribuicao_cores[cor] += 1

    custo_medio = 0.0
    if qtd_nao_terrenos > 0:
        custo_medio = soma_custos_nao_terrenos / qtd_nao_terrenos

    return {
        "total_cartas": total_cartas,
        "terrenos": qtd_terrenos,
        "nao_terrenos": qtd_nao_terrenos,
        "custo_medio_nao_terrenos": custo_medio,
        "distribuicao_cores": distribuicao_cores
    }


def analisar_baralho(commander, cartas_baralho):
    """
    Subprograma principal da análise imperativa.

    Orquestra a execução da verificação das regras e da geração de estatísticas,
    controlando o estado do relatório.
    """
    violacoes = []

    # Execução sequencial das verificações de regras (efeitos colaterais em 'violacoes')
    verificar_nome_nao_vazio(commander, cartas_baralho, violacoes)
    verificar_tamanho_baralho(commander, cartas_baralho, violacoes)
    verificar_commander_no_baralho(commander, cartas_baralho, violacoes)
    verificar_singleton(cartas_baralho, violacoes)
    verificar_identidade_cor(commander, cartas_baralho, violacoes)
    verificar_custo_mana(cartas_baralho, violacoes)

    # Cálculo estatístico
    estatisticas = calcular_estatisticas(commander, cartas_baralho)

    # Definição do estado final de legalidade
    eh_legal = (len(violacoes) == 0)

    return {
        "legal": eh_legal,
        "violacoes": violacoes,
        "estatisticas": estatisticas
    }
