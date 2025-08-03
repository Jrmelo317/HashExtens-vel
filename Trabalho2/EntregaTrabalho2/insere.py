from busca import busca_interna
import io
from geral import *

TESTE = False
TAM_MAX_BUCKET: int = 5
TAM_BUCKET = 4 + 4 +(TAM_MAX_BUCKET * 4)
LEITURA_BUCKET = "<" + str(TAM_BUCKET // 4) + "i"

def insere(campos_diretorio: list, profundidade_global: int, buckets: io.BufferedWriter, chave: int) -> tuple:
    if TESTE:
        print(f"chave usda na busca interna {chave}")
    achou, ref_bk, bk_encontrado = busca_interna(campos_diretorio, profundidade_global, buckets, chave)

    if achou:
        return False, campos_diretorio, profundidade_global
    
    if TESTE:
        print(f"chave usada no inserir_chave_bk {chave}")
    campos_diretorio, profundidade_global = inserir_chave_bk(chave, ref_bk, bk_encontrado, campos_diretorio, profundidade_global, buckets)
    return True, campos_diretorio, profundidade_global

def insere_externo(campos_diretorio: list, profundidade_global: int, buckets: io.BufferedWriter, chave: int) -> tuple:
    proposicao, campos_diretorio, profundidade_global = insere(campos_diretorio, profundidade_global, buckets, chave)
    resultado = []

    if proposicao:
        resultado.append(f">Inserção da chave {chave}: Sucesso.")
        return resultado, campos_diretorio, profundidade_global
    else:
        resultado.append(f">Inserção da chave {chave}: Falha - Chave duplicada.")
        return resultado, campos_diretorio, profundidade_global

def inserir_chave_bk(chave: int, ref_bk:int, bucket: list, campos_diretorio: list, profundidade_global: int, buckets: io.BufferedWriter):
    quantidade_chaves = bucket[1]

    if quantidade_chaves < TAM_MAX_BUCKET:
        bucket[2 + quantidade_chaves] = chave

        if TESTE:
            print(f"Chave inserida e, inserir_chave_bk {chave}")

        bucket[1] = quantidade_chaves + 1
        escreve_bucket(bucket, ref_bk, buckets)
    
    else:
        campos_diretorio, profundidade_global = dividir_bk(ref_bk, bucket, campos_diretorio, profundidade_global, buckets)
        proposicao, campos_diretorio, profundidade_global = insere(campos_diretorio, profundidade_global, buckets, chave)
    
    return campos_diretorio, profundidade_global

def dividir_bk(ref_bk:int, bucket: list, campos_diretorio: list, profundidade_global: int, buckets: io.BufferedWriter) -> tuple:
    OFF_SET_PONTEIRO_PED = 4 + 4
    
    if bucket[0] == profundidade_global:
        campos_diretorio, profundidade_global = dobrar_dir(campos_diretorio, profundidade_global)
    
    if TESTE and profundidade_global == 1:
        print(campos_diretorio)

    buckets.seek(0)
    cabeca_ped = struct.unpack("<i", buckets.read(4))[0]
    if cabeca_ped != -1:
        rrn_bucket_novo = cabeca_ped
        buckets.seek(4 + rrn_bucket_novo * TAM_BUCKET + OFF_SET_PONTEIRO_PED)
        proxima_pos_ped = struct.unpack("<i", buckets.read(4))[0]
        buckets.seek(0)
        buckets.write(struct.pack("<i", proxima_pos_ped))

    else:
        buckets.seek(0, 2)
        tam_arquivo = buckets.tell()
        rrn_bucket_novo = (tam_arquivo - 4) // TAM_BUCKET
    
    novo_bk = criar_novo_bucket()
    novo_inicio, novo_fim = encontrar_novo_intervalo(bucket, profundidade_global)
    for i in range(novo_inicio, novo_fim + 1):
        campos_diretorio[i] = rrn_bucket_novo

    bucket[0] += 1
    novo_bk[0] = bucket[0]
    bucket, novo_bk = redistribuir_chaves(bucket, novo_bk)
    buckets.seek(4 + ref_bk * TAM_BUCKET)
    buckets.write(struct.pack(LEITURA_BUCKET, *bucket))
    buckets.seek(4 + rrn_bucket_novo * TAM_BUCKET)
    buckets.write(struct.pack(LEITURA_BUCKET, *novo_bk))

    return campos_diretorio, profundidade_global

def criar_novo_bucket() -> list:
    novo_bk = [0, 0]
    for i in range(TAM_MAX_BUCKET):
        novo_bk.append(-1)
    return novo_bk

def dobrar_dir(campos_diretorio: list, profundidade_global: int) -> tuple:
    profundidade_global += 1

    novos_campos = []
    for elemento in campos_diretorio:
        novos_campos.append(elemento)
        novos_campos.append(elemento)
    
    return novos_campos, profundidade_global

def redistribuir_chaves(bucket: list, novo_bk: list) -> tuple:
    lista_de_chaves = []
    
    for i in range(bucket[1]):
        lista_de_chaves.append(bucket[2 + i])
        bucket[2 + i] = -1
    bucket[1] = 0
    novo_bk[1] = 0
    
    local_chave_antigo = 2
    local_chave_novo = 2
    for elemento in lista_de_chaves:
        novo_end = gerar_endereco(elemento, bucket[0])
        if novo_end & 1 == 0:
            bucket[local_chave_antigo] = elemento
            local_chave_antigo += 1
        else:
            novo_bk[local_chave_novo] = elemento
            local_chave_novo += 1
    
    bucket[1] = local_chave_antigo - 2
    novo_bk[1] = local_chave_novo - 2
    
    return bucket, novo_bk


def encontrar_novo_intervalo(bucket: list, profundidade_global: int) -> tuple:
    mascara = 1
    end_comum = gerar_endereco(bucket[2], bucket[0])
    end_comum = end_comum << 1
    end_comum = end_comum | mascara
    bits_a_preencher = profundidade_global - (bucket[0] + 1)
    novo_inicio, novo_fim = end_comum, end_comum
    for i in range(bits_a_preencher):
        novo_inicio = novo_inicio << 1
        novo_fim = novo_fim << 1
        novo_fim = novo_fim | mascara
    return novo_inicio, novo_fim