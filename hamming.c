#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define TAM_DADOS 26
#define TAM_HAMMING 31

// Função para validar se a entrada possui exatamente 26 bits ('0' ou '1')
bool validar_entrada(const char *str) {
    if (strlen(str) != TAM_DADOS) {
        return false;
    }
    for (int i = 0; i < TAM_DADOS; i++) {
        if (str[i] != '0' && str[i] != '1') {
            return false;
        }
    }
    return true;
}

// Verifica se uma posição é potência de 2 (posições dos bits de paridade: 1, 2, 4, 8, 16)
bool eh_potencia_de_dois(int pos) {
    return (pos & (pos - 1)) == 0;
}

// Função principal de codificação Hamming (31, 26)
void codificar_hamming(const char *dados, int hamming[TAM_HAMMING + 1]) {
    int idx_dados = 0;

    // 1. Distribui os 26 bits de dados nas posições que NÃO são potências de 2
    for (int i = 1; i <= TAM_HAMMING; i++) {
        if (eh_potencia_de_dois(i)) {
            hamming[i] = 0; // Reserva espaço para os bits de paridade
        } else {
            hamming[i] = dados[idx_dados++] - '0';
        }
    }

    // 2. Calcula os 5 bits de paridade (P1, P2, P4, P8, P16) usando paridade par
    int paridades[] = {1, 2, 4, 8, 16};
    for (int p = 0; p < 5; p++) {
        int pos_p = paridades[p]; // Para cada bit de paridade (1, 2, 4, 8, 16)
        int xor_sum = 0;

        for (int i = 1; i <= TAM_HAMMING; i++) {
            // Verifica se a posição atual contribui para o cálculo do bit de paridade
            if (i != pos_p && (i & pos_p) != 0) {
                // Se a posição i contribui para o bit de paridade pos_p, realiza XOR
                xor_sum ^= hamming[i];
            }
        }
        hamming[pos_p] = xor_sum; // Define o bit de paridade na posição correta
    }
}

int main() {
    char entrada[100];
    int hamming[TAM_HAMMING + 1]; // Índice 1 a 31 para mapeamento direto das posições

    printf("=== CODIFICADOR HAMMING (31, 26) ===\n\n");
    printf("Digite a sequencia binaria de 26 bits: ");

    if (scanf("%99s", entrada) != 1) {
        printf("Erro ao ler a entrada.\n");
        return 1;
    }

    // Validação da entrada binária
    while (!validar_entrada(entrada)) {
        printf("\n[ERRO] Entrada invalida! A sequencia deve ter EXATAMENTE 26 bits (apenas '0' e '1').\n");
        printf("Digite novamente: ");
        scanf("%99s", entrada);
    }

    // Gera a palavra codificada
    codificar_hamming(entrada, hamming);

    // Exibição da entrada original e palavra codificada
    printf("\n----------------------------------------------------\n");
    printf("Entrada Original (26 bits): %s\n", entrada);
    printf("Palavra Hamming  (31 bits): ");
    for (int i = 1; i <= TAM_HAMMING; i++) {
        printf("%d", hamming[i]);
    }
    printf("\n----------------------------------------------------\n");

    return 0;
}