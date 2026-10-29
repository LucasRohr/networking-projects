"""
Módulo: experimentos.py
Descrição: Execução e estruturação dos Experimentos 1 a 4 da Atividade Semanal 10
Integra os modelos de Nyquist e Shannon com ponto de entrada em main()
"""

from nyquist import calcular_capacidade_nyquist, formatar_capacidade
from shannon import calcular_capacidade_shannon, snr_db_para_linear

def executar_experimento_1() -> dict:
    """
    Experimento 1 - Capacidade de Nyquist (Canal sem ruído).
    Varia a largura de banda B (1, 5 e 10 kHz) e os níveis N (2, 4, 8 e 16).
    """
    print("\n" + "=" * 65)
    print("EXPERIMENTO 1: Capacidade de Nyquist")
    print("=" * 65)

    # Parâmetros especificados
    larguras_banda_hz = [1000.0, 5000.0, 10000.0]  # 1 kHz, 5 kHz e 10 kHz
    niveis_sinalizacao = [2, 4, 8, 16]

    resultados = {b: {} for b in larguras_banda_hz}

    print(f"{'Banda (kHz)':<14} | {'Níveis (N)':<12} | {'Capacidade (bit/s)':<20} | {'Formatado':<15}")
    print("-" * 65)

    # Cálculo da capacidade de Nyquist para todas as combinações
    for b in larguras_banda_hz:
        for n in niveis_sinalizacao:
            c = calcular_capacidade_nyquist(b, n)
            resultados[b][n] = c
            print(f"{b / 1e3:<14.1f} | {n:<12} | {c:<20,.2f} | {formatar_capacidade(c):<15}")

    return {
        "bandas_hz": larguras_banda_hz,
        "niveis": niveis_sinalizacao,
        "resultados": resultados
    }


def executar_experimento_2() -> dict:
    """
    Experimento 2 - Capacidade de Shannon (Canal com ruído).
    Varia SNR linear (1000, 5000, 10000 e 50000) e B de 1 a 10 kHz.
    """
    print("\n" + "=" * 65)
    print("EXPERIMENTO 2: Capacidade de Shannon")
    print("=" * 65)

    # Parâmetros especificados
    snrs_lineares = [1000.0, 5000.0, 10000.0, 50000.0]
    larguras_banda_hz = [b * 1000.0 for b in range(1, 11)]  # 1 a 10 kHz em passos de 1 kHz

    resultados = {snr: {} for snr in snrs_lineares}
    menor_c = float("inf")
    maior_c = float("-inf")
    par_menor = ()
    par_maior = ()

    # Cálculo da capacidade e identificação dos valores extremos
    for snr in snrs_lineares:
        for b in larguras_banda_hz:
            c = calcular_capacidade_shannon(b, snr)
            resultados[snr][b] = c

            if c < menor_c:
                menor_c = c
                par_menor = (b, snr)
            if c > maior_c:
                maior_c = c
                par_maior = (b, snr)

    # Amostragem dos dados limites para exibição resumida
    print(f"{'SNR Linear':<12} | {'Banda (kHz)':<14} | {'Capacidade (bit/s)':<20} | {'Formatado':<15}")
    print("-" * 65)
    for snr in snrs_lineares:
        for b in [1000.0, 5000.0, 10000.0]:  # Exibição resumida de amostras
            c = resultados[snr][b]
            print(f"{snr:<12,.0f} | {b / 1e3:<14.1f} | {c:<20,.2f} | {formatar_capacidade(c):<15}")

    print("\nExtremos obtidos no Experimento 2:")
    print(f"- Menor Capacidade: {menor_c:,.2f} bit/s ({formatar_capacidade(menor_c)}) "
          f"em B = {par_menor[0] / 1e3:.1f} kHz, SNR = {par_menor[1]:,.0f}")
    print(f"- Maior Capacidade: {maior_c:,.2f} bit/s ({formatar_capacidade(maior_c)}) "
          f"em B = {par_maior[0] / 1e3:.1f} kHz, SNR = {par_maior[1]:,.0f}")

    return {
        "snrs": snrs_lineares,
        "bandas_hz": larguras_banda_hz,
        "resultados": resultados,
        "extremos": {
            "menor": (menor_c, par_menor),
            "maior": (maior_c, par_maior)
        }
    }


def executar_experimento_3() -> dict:
    """
    Experimento 3 - Influência do Ruído no Limite de Shannon.
    Fixa B = 5 kHz e varia SNR de 0 a 40 dB (incrementos de 5 dB).
    """
    print("\n" + "=" * 65)
    print("EXPERIMENTO 3: Influência do Ruído (SNR em dB)")
    print("=" * 65)

    banda_hz = 5000.0  # 5 kHz
    snrs_db = [float(x) for x in range(0, 45, 5)]  # 0 a 40 dB em passos de 5 dB

    resultados = {}

    print(f"{'SNR (dB)':<10} | {'SNR Linear':<14} | {'Capacidade (bit/s)':<20} | {'Formatado':<15}")
    print("-" * 65)

    # Conversão de dB para escala linear e cálculo de Shannon para cada SNR
    for snr_db in snrs_db:
        snr_linear = snr_db_para_linear(snr_db)
        c = calcular_capacidade_shannon(banda_hz, snr_linear)
        resultados[snr_db] = {
            "snr_linear": snr_linear,
            "capacidade": c
        }
        print(f"{snr_db:<10.1f} | {snr_linear:<14.2f} | {c:<20,.2f} | {formatar_capacidade(c):<15}")

    # Comparativo dos patamares de 10, 20, 30 e 40 dB
    print("\nComparativo direto dos patamares de 10 dB:")
    for patamar in [10.0, 20.0, 30.0, 40.0]:
        c_patamar = resultados[patamar]["capacidade"]
        print(f"-> SNR = {patamar:2.0f} dB: {c_patamar:,.2f} bit/s ({formatar_capacidade(c_patamar)})")

    return {
        "banda_hz": banda_hz,
        "snrs_db": snrs_db,
        "resultados": resultados
    }


def executar_experimento_4() -> dict:
    """
    Experimento 4 - Nyquist versus Shannon.
    B = 3 kHz, SNR = 30 dB e N = 2, 4, 8, 16, 32 e 64 níveis.
    """
    print("\n" + "=" * 65)
    print("EXPERIMENTO 4: Comparativo Nyquist versus Shannon")
    print("=" * 65)

    banda_hz = 3000.0  # 3 kHz
    snr_db = 30.0
    snr_linear = snr_db_para_linear(snr_db)
    niveis = [2, 4, 8, 16, 32, 64]

    # Cálculo da capacidade limite de Shannon (fixa para o canal com ruído)
    c_shannon = calcular_capacidade_shannon(banda_hz, snr_linear)

    print(f"Parâmetros: Banda = {banda_hz / 1e3:.1f} kHz | SNR = {snr_db:.1f} dB (Linear = {snr_linear:.1f})")
    print(f"Limite Superior Teórico de Shannon: {c_shannon:,.2f} bit/s ({formatar_capacidade(c_shannon)})\n")

    print(f"{'Níveis (N)':<12} | {'Nyquist (bit/s)':<18} | {'Shannon (bit/s)':<18} | {'Ultrapassa Shannon?'}")
    print("-" * 65)

    resultados_nyquist = {}
    configuracoes_superadas = []

    # Comparação ponto a ponto entre a formulação de Nyquist e o teto de Shannon
    for n in niveis:
        c_nyquist = calcular_capacidade_nyquist(banda_hz, n)
        resultados_nyquist[n] = c_nyquist
        ultrapassou = c_nyquist > c_shannon # Verifica se a capacidade de Nyquist excede o limite de Shannon

        if ultrapassou:
            configuracoes_superadas.append((n, c_nyquist))

        status = "SIM (Inviável fisicamente)" if ultrapassou else "NÃO (Dentro do limite)"
        print(f"{n:<12} | {c_nyquist:<18,.2f} | {c_shannon:<18,.2f} | {status}")

    print("\nAnálise das violações do limite de Shannon:")
    for n_val, taxa in configuracoes_superadas:
        excesso = taxa - c_shannon # Calcula o excesso de capacidade em relação ao limite de Shannon
        print(f"- Com N = {n_val}: Nyquist produz {taxa:,.2f} bit/s (excede Shannon em +{excesso:,.2f} bit/s).")

    return {
        "banda_hz": banda_hz,
        "snr_db": snr_db,
        "snr_linear": snr_linear,
        "niveis": niveis,
        "c_shannon": c_shannon,
        "c_nyquist": resultados_nyquist,
        "superadas": configuracoes_superadas
    }


def main():
    """
    Ponto de entrada: executa sequencialmente todos os experimentos
    """
    print("### INÍCIO DA EXECUÇÃO DOS EXPERIMENTOS DE CAPACIDADE DE CANAL ###")
    executar_experimento_1()
    executar_experimento_2()
    executar_experimento_3()
    executar_experimento_4()
    print("\n" + "=" * 65)
    print("### TODOS OS EXPERIMENTOS FORAM CONCLUÍDOS COM SUCESSO ###\n")


if __name__ == "__main__":
    main()