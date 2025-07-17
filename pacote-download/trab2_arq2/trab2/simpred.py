import sys

def le_trace(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()
    # Remove quebras de linha e separa os campos
    return [linha.strip().split() for linha in linhas]

def predicao_not_taken(trace):
    acertos = 0
    for endereco, destino, ocorrido in trace:
        if ocorrido == 'N':
            acertos += 1
    return acertos

def predicao_taken(trace):
    acertos = 0
    for endereco, destino, ocorrido in trace:
        if ocorrido == 'T':
            acertos += 1
    return acertos

def predicao_direcao(trace):
    acertos = 0
    for endereco, destino, ocorrido in trace:
        # Convertendo para inteiros, para comparacao
        endereco_int = int(endereco)
        destino_int = int(destino)

        # Determinando a predicao
        if destino_int < endereco_int: # Desvio para TRAS
            predicao = 'T'
        else:                          # Desvio para FRENTE
            predicao = 'N'
        
        # Verificacao da predicao
        if predicao == ocorrido:
            acertos += 1
        
    return acertos

def predicao_1bit(trace, n_linhas_bpb, bpb_1bit):
    acertos = 0
    for endereco, destino, ocorrido in trace:
        # Convertendo para inteiros
        endereco_int = int(endereco)

        # Calcula o indice
        indice = (endereco_int >> 2) % n_linhas_bpb

        # Prediz com base no bit de historico
        if bpb_1bit[indice] == 0:
            predicao_1bit = 'N'
        else:
            predicao_1bit = 'T'

        # Compara com o resultado real para ver se foi um acerto
        if predicao_1bit == ocorrido:
            acertos += 1

        # Atualiza o BPB com o resultado real do desvio
        if ocorrido == 'T':
            bpb_1bit[indice] = 1
        else:
            bpb_1bit[indice] = 0

    return acertos

def predicao_2bit(trace, n_linhas_bpb, bpb_2bit):
    acertos = 0
    for endereco, destino, ocorrido in trace:
         # Convertendo para inteiros
        endereco_int = int(endereco)

        # Calcula o indice
        indice = (endereco_int >> 2) % n_linhas_bpb

        # Estado atual do BPB
        estado_atual = bpb_2bit[indice]

        # Estados:
        # 00 -> 0
        # 01 -> 1
        # 10 -> 2
        # 11 -> 3

        # Fazer a predicao, com base no estado atual
        if estado_atual < 2:
            predicao = 'N'
        else:
            predicao = 'T'

        # Contando os acertos
        if predicao == ocorrido:
            acertos += 1

        # Implementacao do automato visto em aula
        if estado_atual == 0:
            if ocorrido == 'T':
                bpb_2bit[indice] = 1
            # Se o ocorrido for 'N', permanece em 0, nada precisa ser feito

        elif estado_atual == 1:
            if ocorrido == 'T':
                bpb_2bit[indice] = 3
            else:
                bpb_2bit[indice] = 0
        
        elif estado_atual == 2:
            if ocorrido == 'T':
                bpb_2bit[indice] = 3
            else:
                bpb_2bit[indice] = 0
        
        elif estado_atual == 3:
            # Se o ocorrido for 'T', permanece em 3, nada precisa ser feito
            if ocorrido == 'N':
                bpb_2bit[indice] = 2
        
    return acertos
        
def main():
    if len(sys.argv) != 3:
        print("Uso: simpred arquivoTrace nLinhasBPB")
        return

    nome_arquivo = sys.argv[1]
    n_linhas_bpb = int(sys.argv[2])

    # Começando os BPBs zerados    
    bpb_1bit = [0] * n_linhas_bpb
    bpb_2bit = [0] * n_linhas_bpb

    trace = le_trace(nome_arquivo)
    n_branches = len(trace)

    # Numero de acertos para cada tecnica
    acertos_nt = predicao_not_taken(trace)
    acertos_t = predicao_taken(trace)
    acertos_direcao = predicao_direcao(trace)
    acertos_1bit = predicao_1bit(trace, n_linhas_bpb, bpb_1bit)
    acertos_2bit = predicao_2bit(trace, n_linhas_bpb, bpb_2bit)

    # Prints
    print(f"Not-Taken: {100 * acertos_nt / n_branches:.2f}%")
    print(f"Taken: {100 * acertos_t / n_branches:.2f}%")
    print(f"Direcao: {100 * acertos_direcao / n_branches:.2f}%")
    print(f"1bit: {100 * acertos_1bit / n_branches:.2f}%")
    print(f"2bit: {100 * acertos_2bit / n_branches:.2f}%")
if __name__ == '__main__':
    main()