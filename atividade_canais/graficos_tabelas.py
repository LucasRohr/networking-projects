"""
Módulo: graficos_tabelas.py
Descrição: Geração automatizada de tabelas analíticas e gráficos comparativos
para os Experimentos 1 a 4 da Atividade Semanal 10 (Nyquist e Shannon).
Requisitos: pandas, matplotlib
"""

import math
import matplotlib.pyplot as plt
import pandas as pd

# Módulo é desacoplado dos cálculos físicos, consumindo apenas os dados prontos.

def configurar_estilo_grafico():
    """
    Padroniza os parâmetros visuais dos gráficos gerados.
    """
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams.update({
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.titlesize": 13,
        "lines.linewidth": 1.8,
        "lines.markersize": 6
    })


# A assinatura da função recebe 'dados_exp' gerado em experimentos.py
def processar_experimento_1(dados_exp: dict, salvar_imagem: bool = True) -> pd.DataFrame:
    """
    Experimento 1: Capacidade de Nyquist (C vs N para diferentes B).
    Gera tabela consolidada e gráfico de linhas com marcadores.
    """
    # Extrai os dados calculados previamente por experimentos.py sem rechamar nyquist
    bandas = dados_exp["bandas_hz"]
    niveis = dados_exp["niveis"]
    resultados = dados_exp["resultados"]

    # Monta a estrutura tabular consumindo os resultados
    dados = []
    for b in bandas:
        for n in niveis:
            c_bps = resultados[b][n]
            dados.append({
                "Banda (kHz)": b / 1e3,
                "Níveis (N)": n,
                "Bits/Símbolo (m)": int(math.log2(n)),
                "Capacidade (bit/s)": c_bps,
                "Capacidade (kbit/s)": c_bps / 1e3
            })

    df = pd.DataFrame(dados)

    # Exibição tabular no terminal
    print("\n" + "=" * 70)
    print("TABELA ANALÍTICA - EXPERIMENTO 1 (NYQUIST)")
    print("=" * 70)
    print(df.to_string(index=False, formatters={
        "Banda (kHz)": "{:.1f}".format,
        "Capacidade (bit/s)": "{:,.2f}".format,
        "Capacidade (kbit/s)": "{:,.2f}".format
    }))

    # Geração do gráfico C vs N
    plt.figure(figsize=(8, 5))
    for b in bandas:
        sub_df = df[df["Banda (kHz)"] == (b / 1e3)]
        plt.plot(
            sub_df["Níveis (N)"],
            sub_df["Capacidade (kbit/s)"],
            marker="o",
            label=f"B = {b / 1e3:.0f} kHz"
        )

    plt.title("Experimento 1: Capacidade de Nyquist (C) versus Níveis (N)")
    plt.xlabel("Número de Níveis de Sinalização (N)")
    plt.ylabel("Capacidade C (kbit/s)")
    plt.xticks(niveis)
    plt.legend(title="Largura de Banda")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Salva o gráfico em arquivo PNG se solicitado
    if salvar_imagem:
        plt.savefig("experimento_1_nyquist.png", dpi=300)
        print("\n[+] Gráfico salvo: experimento_1_nyquist.png")
    plt.close()

    return df


# A assinatura da função recebe 'dados_exp' gerado em experimentos.py
def processar_experimento_2(dados_exp: dict, salvar_imagem: bool = True) -> pd.DataFrame:
    """
    Experimento 2: Capacidade de Shannon (C vs B para diferentes SNR lineares).
    Gera tabela em formato de matriz e gráfico multilinear.
    """
    # Extrai os dados e extremos já processados em experimentos.py
    snrs = dados_exp["snrs"]
    bandas = dados_exp["bandas_hz"]
    resultados = dados_exp["resultados"]
    extremos = dados_exp["extremos"]

    # Constrói a lista de dados a partir dos resultados já calculados
    dados = []
    for snr in snrs:
        for b in bandas:
            c_bps = resultados[snr][b]
            dados.append({
                "SNR Linear": snr,
                "Banda (kHz)": b / 1e3,
                "Capacidade (bit/s)": c_bps,
                "Capacidade (kbit/s)": c_bps / 1e3
            })

    df = pd.DataFrame(dados)

    # Construção de tabela (Banda x SNR) para melhor visualização
    df_pivot = df.pivot(index="Banda (kHz)", columns="SNR Linear", values="Capacidade (kbit/s)")

    print("\n" + "=" * 70)
    print("TABELA ANALÍTICA - EXPERIMENTO 2 (SHANNON: C em kbit/s)")
    print("=" * 70)
    print(df_pivot.to_string())

    # Identificação dos pontos extremos absolutos
    # Utiliza os extremos calculados diretamente no experimento sem recalcular
    menor_c, par_menor = extremos["menor"]
    maior_c, par_maior = extremos["maior"]

    print("\nExtremos de Capacidade Identificados:")
    print(f"- Mínima: {menor_c / 1e3:.2f} kbit/s "
          f"(B = {par_menor[0] / 1e3:.0f} kHz, SNR = {par_menor[1]:,.0f})")
    print(f"- Máxima: {maior_c / 1e3:.2f} kbit/s "
          f"(B = {par_maior[0] / 1e3:.0f} kHz, SNR = {par_maior[1]:,.0f})")

    # Geração do gráfico C vs B
    plt.figure(figsize=(9, 5.5))
    for snr in snrs:
        sub_df = df[df["SNR Linear"] == snr]
        plt.plot(
            sub_df["Banda (kHz)"],
            sub_df["Capacidade (kbit/s)"],
            marker="s",
            label=f"SNR = {snr:,.0f}"
        )

    plt.title("Experimento 2: Capacidade de Shannon (C) versus Largura de Banda (B)")
    plt.xlabel("Largura de Banda B (kHz)")
    plt.ylabel("Capacidade C (kbit/s)")
    plt.xticks(range(1, 11))
    plt.legend(title="Relação Sinal-Ruído")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()

    if salvar_imagem:
        plt.savefig("experimento_2_shannon.png", dpi=300)
        print("[+] Gráfico salvo: experimento_2_shannon.png")
    plt.close()

    return df


# A assinatura da função recebe 'dados_exp' gerado em experimentos.py
def processar_experimento_3(dados_exp: dict, salvar_imagem: bool = True) -> pd.DataFrame:
    """
    Experimento 3: Influência do Ruído no Limite de Shannon (B = 5 kHz fixo, SNR de 0 a 40 dB).
    Gera tabela detalhada e curva logarítmica característica.
    """
    # Extrai os dados calculados do dicionário de entrada sem chamar shannon
    snrs_db = dados_exp["snrs_db"]
    resultados = dados_exp["resultados"]

    # Monta a estrutura tabular a partir do dicionário de resultados recebido
    dados = []
    for snr_db in snrs_db:
        snr_lin = resultados[snr_db]["snr_linear"]
        c_bps = resultados[snr_db]["capacidade"]
        dados.append({
            "SNR (dB)": snr_db,
            "SNR Linear": snr_lin,
            "Capacidade (bit/s)": c_bps,
            "Capacidade (kbit/s)": c_bps / 1e3
        })

    df = pd.DataFrame(dados)

    print("\n" + "=" * 70)
    print("TABELA ANALÍTICA - EXPERIMENTO 3 (INFLUÊNCIA DO RUÍDO - B = 5 kHz)")
    print("=" * 70)
    print(df.to_string(index=False, formatters={
        "SNR (dB)": "{:.0f}".format,
        "SNR Linear": "{:,.2f}".format,
        "Capacidade (bit/s)": "{:,.2f}".format,
        "Capacidade (kbit/s)": "{:,.2f}".format
    }))

    # Comparativo direto destacado nos marcos de 10, 20, 30 e 40 dB
    marcos = [10.0, 20.0, 30.0, 40.0]
    df_marcos = df[df["SNR (dB)"].isin(marcos)]
    print("\nConfronto direto dos marcos solicitados (10, 20, 30 e 40 dB):")
    for _, linha in df_marcos.iterrows():
        print(f"-> {linha['SNR (dB)']:2.0f} dB | Linear: {linha['SNR Linear']:10.2f} | "
              f"Capacidade: {linha['Capacidade (kbit/s)']:6.2f} kbit/s")

    # Geração do gráfico C vs SNR (dB)
    plt.figure(figsize=(8, 5))
    plt.plot(df["SNR (dB)"], df["Capacidade (kbit/s)"], marker="o", color="darkred", label="B = 5 kHz")

    # Realce visual dos pontos avaliados (marcos solicitados de dB)
    for ponto in marcos:
        c_val = df.loc[df["SNR (dB)"] == ponto, "Capacidade (kbit/s)"].values[0]
        plt.scatter(ponto, c_val, color="black", s=50, zorder=5)
        plt.annotate(
            f"{c_val:.1f} kbit/s",
            (ponto, c_val),
            textcoords="offset points",
            xytext=(-15, 8),
            fontsize=9
        )

    plt.title("Experimento 3: Capacidade de Shannon versus SNR (dB)")
    plt.xlabel("Relação Sinal-Ruído SNR (dB)")
    plt.ylabel("Capacidade C (kbit/s)")
    plt.xticks(range(0, 45, 5))
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()

    if salvar_imagem:
        plt.savefig("experimento_3_ruido.png", dpi=300)
        print("\n[+] Gráfico salvo: experimento_3_ruido.png")
    plt.close()

    return df


# A assinatura da função agora recebe 'dados_exp' gerado em experimentos.py
def processar_experimento_4(dados_exp: dict, salvar_imagem: bool = True) -> pd.DataFrame:
    """
    Experimento 4: Nyquist versus Shannon (B = 3 kHz, SNR = 30 dB, N = 2 a 64).
    Gera tabela de viabilidade física e gráfico com linha horizontal de corte.
    """
    # Extrai os parâmetros e valores comparativos calculados em experimentos.py
    snr_lin = dados_exp["snr_linear"]
    niveis = dados_exp["niveis"]

    # Limite invariante do canal com ruído
    # Obtém a capacidade de Shannon já calculada no experimento
    c_shannon_bps = dados_exp["c_shannon"]
    c_shannon_kbps = c_shannon_bps / 1e3
    resultados_nyquist = dados_exp["c_nyquist"]

    # Monta a tabela utilizando os cálculos prévios de Nyquist e Shannon
    dados = []
    for n in niveis:
        c_nyq_bps = resultados_nyquist[n]
        c_nyq_kbps = c_nyq_bps / 1e3
        ultrapassa = c_nyq_bps > c_shannon_bps

        dados.append({
            "Níveis (N)": n,
            "Bits/Símbolo (m)": int(math.log2(n)),
            "Nyquist (kbit/s)": c_nyq_kbps,
            "Shannon Limite (kbit/s)": c_shannon_kbps,
            "Excesso (kbit/s)": (c_nyq_kbps - c_shannon_kbps) if ultrapassa else 0.0,
            "Viabilidade Física": "Inviável (C > Shannon)" if ultrapassa else "Viável"
        })

    df = pd.DataFrame(dados)

    print("\n" + "=" * 75)
    print("TABELA ANALÍTICA - EXPERIMENTO 4 (CONFRONTO NYQUIST VS. SHANNON)")
    print(f"Parâmetros de Canal: B = 3.0 kHz | SNR = 30 dB (Linear = {snr_lin:.1f})")
    print(f"Teto Físico de Shannon: {c_shannon_kbps:.2f} kbit/s")
    print("=" * 75)
    print(df.to_string(index=False, formatters={
        "Nyquist (kbit/s)": "{:,.2f}".format,
        "Shannon Limite (kbit/s)": "{:,.2f}".format,
        "Excesso (kbit/s)": "{:,.2f}".format
    }))

    # Geração do gráfico comparativo
    plt.figure(figsize=(8.5, 5.5))
    plt.plot(
        df["Níveis (N)"],
        df["Nyquist (kbit/s)"],
        marker="o",
        color="royalblue",
        label="Taxa de Nyquist (Canal Ideal)"
    )
    plt.axhline(
        y=c_shannon_kbps,
        color="crimson",
        linestyle="--",
        linewidth=2,
        label=f"Teto de Shannon ({c_shannon_kbps:.2f} kbit/s)"
    )

    # Destaque da zona assintótica e inviável (Capacidade de Nyquist > Limite de Shannon)
    plt.fill_between(
        df["Níveis (N)"],
        c_shannon_kbps,
        df["Nyquist (kbit/s)"],
        where=(df["Nyquist (kbit/s)"] >= c_shannon_kbps),
        color="crimson",
        alpha=0.15,
        label="Região de Inviabilidade Física (Ruído AWGN)"
    )

    plt.title("Experimento 4: Confronto Nyquist vs. Limite Teórico de Shannon")
    plt.xlabel("Níveis de Sinalização (N)")
    plt.ylabel("Taxa de Transmissão (kbit/s)")
    plt.xticks(niveis)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()

    if salvar_imagem:
        plt.savefig("experimento_4_confronto.png", dpi=300)
        print("\n[+] Gráfico salvo: experimento_4_confronto.png")
    plt.close()

    return df


def main():
    """
    Executa a rotina completa de síntese em tabelas e renderização gráfica.
    Caso executado diretamente, dispara o pipeline de experimentos (guarda de execução).
    """
    print("### PROCESSANDO TABELAS E GRÁFICOS DA ATIVIDADE SEMANAL 10 ###")
    # Importação dinâmica interna para evitar acoplamento circular
    import experimentos
    experimentos.main()


if __name__ == "__main__":
    main()