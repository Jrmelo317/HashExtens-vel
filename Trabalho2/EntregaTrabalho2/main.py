import sys
from busca import busca_externa
from remove import remove_externo
from insere import insere_externo
from imprime_diretorio import imprime_dir
from impressao_buckets import imprime_bk
import os
import io
import struct
from geral import *

TESTE = False

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("OPERAÇÃO NÃO ESPECÍFICADA!")
        sys.exit(1)

    instrucao = sys.argv[1]

    try:

        if not os.path.exists("diretorio.dat") or not os.path.exists("buckets.dat"):
            with open("diretorio.dat", "w+b") as diretorio:
                with open("buckets.dat", "w+b") as buckets:
                    inicializa_hashing(diretorio, buckets)

        with open("buckets.dat", "r+b") as buckets:
            with open("diretorio.dat", "r+b") as diretorio:

                info_diretorio = carrega_diretorio_memoria(diretorio)
                profundidade_global = info_diretorio[0]
                campos_diretorio = info_diretorio[1]

                if instrucao == "-e":

                    if len(sys.argv) < 3:
                        print("ERRO NÃO FORNECEU ARQUIVO DE OPERAÇÕES!")
                        sys.exit(1)
                    
                    arquivo_instrucoes = sys.argv[2]

                    with open(arquivo_instrucoes, "r") as instrucoes:

                        linha = instrucoes.readline().split() #le a linha, remove os espaços e transforma em lista

                        if TESTE:
                            print(f"profundidade_global {profundidade_global}")
                            print(f"campos_diretorio {campos_diretorio}")

                        while True:
                            acao = linha[0]
                            chave = int(linha[1])
                            if TESTE:
                                print(chave)

                            if acao == "i":
                                resultado, campos_diretorio, profundidade_global = insere_externo(campos_diretorio, profundidade_global, buckets, chave)
                        
                            elif acao == "r":
                                resultado, campos_diretorio, profundidade_global = remove_externo(campos_diretorio, profundidade_global, buckets, chave)
                        
                            elif acao == "b":
                                resultado = busca_externa(campos_diretorio, profundidade_global, buckets, chave)
                        
                            for elemento in resultado:
                                print(elemento)
                        
                            print()

                            linha = instrucoes.readline().strip().split(' ', 1) # le a proxima linha
                            if linha[0] == '':
                                break
                        
                
                elif instrucao == "-pd":
                    imprime_dir(campos_diretorio, profundidade_global)
                
                elif instrucao == "-pb":
                    imprime_bk(buckets)
                
                else:
                    print("OPÇÃO NÃO SUPORTADA, OPÇÕES: -e, -pd, pb")
                
                escreve_diretorio(diretorio, campos_diretorio, profundidade_global)
        
    except ValueError as e:
        print(f"ERRO: {e}")