"""
Módulo: nyquist.py
Descrição: Implementação do modelo de capacidade de canal de Nyquist para canais ideais.
Fórmula: C = 2 * B * log2(N)
"""

import math

def formatar_capacidade(capacidade_bps: float) -> str:
    """
    Converte a capacidade em bit/s para unidades legíveis (bit/s, kbit/s, Mbit/s).
    """
    if capacidade_bps >= 1e6:
        return f"{capacidade_bps / 1e6:.4f} Mbit/s"
    elif capacidade_bps >= 1e3:
        return f"{capacidade_bps / 1e3:.4f} kbit/s"
    return f"{capacidade_bps:.2f} bit/s"


def calcular_capacidade_nyquist(banda_hz: float, niveis: int) -> float:
    """
    Calcula a capacidade teórica máxima de um canal segundo Nyquist.

    Parâmetros:
        banda_hz (float): Largura de banda do canal em Hertz (Hz).
        niveis (int): Número de níveis de sinalização discretos (N >= 2).

    Retorno:
        float: Capacidade teórica máxima em bits por segundo (bit/s).
    """
    # Validações físicas dos parâmetros de entrada
    if banda_hz <= 0:
        raise ValueError("A largura de banda (B) deve ser positiva.")
    if niveis < 2:
        raise ValueError(
            "O número de níveis (N) deve ser no mínimo 2 (sinalização binária)."
        )

    # Cálculo do número de bits por símbolo: m = log2(N)
    bits_por_simbolo = math.log2(niveis)

    # Capacidade de Nyquist: C = 2 * B * log2(N)
    capacidade = 2 * banda_hz * bits_por_simbolo
    return capacidade


if __name__ == "__main__":
    print("--- Teste do Modelo de Capacidade de Nyquist ---")

    # Exemplo de teste interativo (entrada de dados) ou demonstrativo (dados fixos padronizados)
    try:
        # Solicitação de entrada para largura de banda e número de níveis
        entrada_b = input("Informe a largura de banda em Hz (padrão: 3000): ")
        b = float(entrada_b) if entrada_b.strip() else 3000.0

        entrada_n = input(
            "Informe o número de níveis de sinalização (padrão: 4): "
        )
        n = int(entrada_n) if entrada_n.strip() else 4

        # Execução do cálculo
        c = calcular_capacidade_nyquist(b, n)

        # Apresentação do resultado estruturado com unidades
        print("\nResultados obtidos:")
        print(f"Largura de Banda (B): {b:,.2f} Hz")
        print(f"Níveis de Sinalização (N): {n} ({math.log2(n):.1f} bits/símbolo)")
        print(f"Capacidade (C): {c:,.2f} bit/s ({formatar_capacidade(c)})")

    except ValueError as erro:
        print(f"Erro de validação: {erro}")