import io
from geral import *
import struct

TAM_MAX_BUCKET: int = 5
TAM_BUCKET = 4 + 4 +(TAM_MAX_BUCKET * 4)
LEITURA_BUCKET = "<" + str(TAM_BUCKET // 4) + "i"

def busca_interna(campos_diretorio: list, profundidade_global: int, buckets: io.BufferedWriter, chave: int) -> tuple:
    """Essa função é responsável por realizar as bucas internamente, isto é, ela não gera saídas para o usuário,
    mas auxilia as funções de inserção e remoção"""

    endereco = gerar_endereco(chave, profundidade_global)
    rrn_bk = campos_diretorio[endereco]

    buckets.seek(4 + TAM_BUCKET * rrn_bk) #pula 4 de cabeçalho e vai até o endereço
    bk_encontrado = list(struct.unpack(LEITURA_BUCKET, buckets.read(TAM_BUCKET)))

    quantidade_chaves = bk_encontrado[1]
    for i in range(quantidade_chaves):
        if bk_encontrado[i + 2] == chave:
            return True, rrn_bk, bk_encontrado

    return False, rrn_bk, bk_encontrado

def busca_externa(campos_diretorio: list, profundidade_global: int, buckets: io.BufferedWriter, chave: int) -> list:
    """Essa função é responsável por chamar a busca_interna e produzir a saída esperada pelo usuário"""
    resultado_busca = busca_interna(campos_diretorio, profundidade_global, buckets, chave)
    lista = []

    if resultado_busca[0]:
        lista.append(f">Busca pela chave {chave}: Chave encontrada no bucket {resultado_busca[1]}.")
    else:
        lista.append(f">Busca pela chave {chave}: Chave não encontrada.")
    
    return lista