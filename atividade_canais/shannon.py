"""
Módulo: shannon.py
Descrição: Implementação do modelo de capacidade de Shannon para canais com ruído.
Fórmula: C = B * log2(1 + SNR)
"""

import math


def snr_db_para_linear(snr_db: float) -> float:
    """
    Converte a relação sinal-ruído de Decibéis (dB) para escala linear.
    Fórmula: SNR = 10 ** (SNR_dB / 10)
    """
    return 10.0 ** (snr_db / 10.0)


def snr_linear_para_db(snr_linear: float) -> float:
    """
    Converte a relação sinal-ruído de escala linear para Decibéis (dB).
    Fórmula: SNR_dB = 10 * log10(SNR)
    """
    if snr_linear <= 0:
        raise ValueError(
            "SNR em escala linear deve ser maior que zero para conversão em dB."
        )
    return 10.0 * math.log10(snr_linear)


def formatar_capacidade(capacidade_bps: float) -> str:
    """
    Converte a capacidade em bit/s para unidades legíveis (bit/s, kbit/s, Mbit/s).
    """
    if capacidade_bps >= 1e6:
        return f"{capacidade_bps / 1e6:.4f} Mbit/s"
    elif capacidade_bps >= 1e3:
        return f"{capacidade_bps / 1e3:.4f} kbit/s"
    return f"{capacidade_bps:.2f} bit/s"


def calcular_capacidade_shannon(banda_hz: float, snr_linear: float) -> float:
    """
    Calcula o limite de Shannon da capacidade máxima de um canal ruidoso.

    Parâmetros:
        banda_hz (float): Largura de banda do canal em Hertz (Hz).
        snr_linear (float): Relação sinal-ruído em escala linear (SNR = S/N >= 0).

    Retorno:
        float: Limite teórico superior de capacidade em bits por segundo (bit/s).
    """
    # Validações físicas dos parâmetros de entrada
    if banda_hz <= 0:
        raise ValueError("A largura de banda (B) deve ser positiva.")
    if snr_linear < 0:
        raise ValueError("A relação sinal-ruído (SNR) não pode ser negativa.")

    # Capacidade de Shannon: C = B * log2(1 + SNR)
    capacidade = banda_hz * math.log2(1.0 + snr_linear)
    return capacidade


if __name__ == "__main__":
    print("--- Teste do Modelo de Capacidade de Shannon ---")

    # Exemplo de teste interativo (entrada de dados) ou demonstrativo (dados fixos padronizados)
    try:
        # Solicitação de entrada para largura de banda e SNR
        entrada_b = input("Informe a largura de banda em Hz (padrão: 3000): ")
        b = float(entrada_b) if entrada_b.strip() else 3000.0

        tipo_snr = (
            input("Deseja informar SNR em linear (L) ou dB (D)? [L/D] (padrão: D): ")
            .strip()
            .upper()
        )

        if tipo_snr == "L":
            entrada_snr = input("Informe o SNR linear (padrão: 1000): ")
            snr_lin = float(entrada_snr) if entrada_snr.strip() else 1000.0
            snr_db = snr_linear_para_db(snr_lin)
        else:
            entrada_snr = input("Informe o SNR em dB (padrão: 30): ")
            snr_db = float(entrada_snr) if entrada_snr.strip() else 30.0
            snr_lin = snr_db_para_linear(snr_db)

        # Execução do cálculo
        c = calcular_capacidade_shannon(b, snr_lin)

        # Apresentação do resultado estruturado com unidades
        print("\nResultados obtidos:")
        print(f"Largura de Banda (B): {b:,.2f} Hz")
        print(f"SNR Linear: {snr_lin:,.2f}")
        print(f"SNR em dB: {snr_db:.2f} dB")
        print(f"Capacidade Máxima (C): {c:,.2f} bit/s ({formatar_capacidade(c)})")

    except ValueError as erro:
        print(f"Erro de validação: {erro}")