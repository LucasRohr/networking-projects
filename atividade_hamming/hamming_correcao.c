#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define TAM_DADOS 26
#define TAM_HAMMING 31

// Função para verificar se uma posição é potência de 2
bool eh_potencia_de_dois(int pos) {
    return (pos & (pos - 1)) == 0;
}

// Codifica os 26 bits de dados na palavra Hamming (31, 26)
void codificar_hamming(const char *dados, int hamming[TAM_HAMMING + 1]) {
    int idx_dados = 0;

    for (int i = 1; i <= TAM_HAMMING; i++) {
        if (eh_potencia_de_dois(i)) {
            hamming[i] = 0;
        } else {
            hamming[i] = dados[idx_dados++] - '0';
        }
    }

    int paridades[] = {1, 2, 4, 8, 16};
    for (int p = 0; p < 5; p++) {
        int pos_p = paridades[p];
        int xor_sum = 0;

        for (int i = 1; i <= TAM_HAMMING; i++) {
            if (i != pos_p && (i & pos_p) != 0) {
                xor_sum ^= hamming[i];
            }
        }
        hamming[pos_p] = xor_sum;
    }
}

// Re-calcula a paridade na receção e determina a síndrome de Hamming
int calcular_sindrome(const int recebida[TAM_HAMMING + 1], int s_bits[5]) {
    int paridades[] = {1, 2, 4, 8, 16};
    int posicao_erro = 0;

    for (int p = 0; p < 5; p++) {
        int pos_p = paridades[p];
        int xor_sum = 0;

        // O cálculo da síndrome inclui o próprio bit de paridade
        for (int i = 1; i <= TAM_HAMMING; i++) {
            if ((i & pos_p) != 0) {
                xor_sum ^= recebida[i];
            }
        }
        // Armazena o bit de paridade calculado na síndrome
        s_bits[p] = xor_sum;

        // Se a soma XOR não for zero, significa que há um erro na posição correspondente
        if (xor_sum != 0) {
            posicao_erro += pos_p; // A soma das potências com erro dá a posição exata
        }
    }

    return posicao_erro;
}

// Extrai os 26 bits de dados da palavra de 31 bits
void extrair_dados(const int hamming[TAM_HAMMING + 1], char dados_saida[TAM_DADOS + 1]) {
    int idx = 0;
    for (int i = 1; i <= TAM_HAMMING; i++) {
        if (!eh_potencia_de_dois(i)) {
            dados_saida[idx++] = hamming[i] + '0';
        }
    }
    dados_saida[idx] = '\0';
}

int main() {
    const char *entrada_original = "11010011001101011011001010"; // Caso de teste 3
    int palavra_correta[TAM_HAMMING + 1];
    int palavra_com_erro[TAM_HAMMING + 1];
    int palavra_corrigida[TAM_HAMMING + 1];
    int s_bits[5];
    int pos_erro_manual = 12; // Posição escolhida para alterar o bit (exemplo: posição 12)

    // 1. Gerar a palavra codificada original
    codificar_hamming(entrada_original, palavra_correta);

    // 2. Copiar e introduzir um erro num único bit
    for (int i = 1; i <= TAM_HAMMING; i++) {
        palavra_com_erro[i] = palavra_correta[i];
    }
    palavra_com_erro[pos_erro_manual] ^= 1; // Inverte o bit na posição 12

    // 3. Calcular a síndrome de Hamming
    int pos_detetada = calcular_sindrome(palavra_com_erro, s_bits);

    // 4. Corrigir o erro
    for (int i = 1; i <= TAM_HAMMING; i++) {
        palavra_corrigida[i] = palavra_com_erro[i];
    }
    if (pos_detetada > 0) {
        palavra_corrigida[pos_detetada] ^= 1; // Corrige invertendo o bit incorreto
    }

    // 5. Extrair dados originais
    char dados_recuperados[TAM_DADOS + 1];
    extrair_dados(palavra_corrigida, dados_recuperados);

    // Exibição dos resultados
    printf("=== TESTE DE DETECCAO E CORRECAO DE ERRO ===\n\n");
    printf("Entrada de Dados Original (26 bits) : %s\n", entrada_original);
    
    printf("Palavra Hamming Correta   (31 bits) : ");
    for (int i = 1; i <= TAM_HAMMING; i++) printf("%d", palavra_correta[i]);
    printf("\n");

    printf("Palavra com Erro (Posicao %2d)       : ", pos_erro_manual);
    for (int i = 1; i <= TAM_HAMMING; i++) printf("%d", palavra_com_erro[i]);
    printf("\n\n");

    printf("--- DETALHES DA SINDROME ---\n");
    printf("Bits da Síndrome (S16 S8 S4 S2 S1) : %d %d %d %d %d\n",
           s_bits[4], s_bits[3], s_bits[2], s_bits[1], s_bits[0]);
    printf("Soma Decimal da Síndrome           : %d\n", pos_detetada);
    printf("Posição do Bit Identificado        : Posição %d\n\n", pos_detetada);

    printf("Palavra Hamming Corrigida (31 bits) : ");
    for (int i = 1; i <= TAM_HAMMING; i++) printf("%d", palavra_corrigida[i]);
    printf("\n");

    printf("Dados Originais Recuperados         : %s\n", dados_recuperados);

    return 0;
}