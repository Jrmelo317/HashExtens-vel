import io
from busca import busca_interna
from geral import *

TESTE = False
TAM_MAX_BUCKET: int = 5
TAM_BUCKET = 4 + 4 +(TAM_MAX_BUCKET * 4)
LEITURA_BUCKET = "<" + str(TAM_BUCKET // 4) + "i"

def remover(campos_diretorio: list, profundidade_global: int, buckets: io.BufferedWriter, chave: int) -> tuple:
    if TESTE:
        print(f"chave passada a busca_interna {chave}")

    achou, ref_bk, bk_encontrado = busca_interna(campos_diretorio, profundidade_global, buckets, chave)
    
    if TESTE:
        print(f"Retornos achou, ref_bk e bk_encontrado respectivamente: {achou}, {ref_bk}, {bk_encontrado}")

    if not achou:
        return False, campos_diretorio, profundidade_global
    return remover_chave_bk(chave, ref_bk, bk_encontrado, buckets, campos_diretorio, profundidade_global)

def remove_externo(campos_diretorio: list, profundidade_global: int, buckets: io.BufferedWriter, chave: int) -> tuple:
    prop, campos_diretorio, profundidade_global = remover(campos_diretorio, profundidade_global, buckets, chave)
    lista = []

    if prop:
        lista.append(f">Remoção da chave {chave}: Sucesso")
        return lista, campos_diretorio, profundidade_global
    else:
        lista.append(f">Remoção da chave {chave}: Falha - Chave não encontrada")
        return lista, campos_diretorio, profundidade_global

def remover_chave_bk(chave: int, ref_bk: int, bk_encontrado: list, buckets: io.BufferedWriter, campos_diretorio: list, profundidade_global: int) -> tuple:
    removeu = False
    quantidade_chaves = bk_encontrado[1]
    for i in range(quantidade_chaves):
        if bk_encontrado[2 + i] == chave:
            bk_encontrado.pop(2 + i)
            bk_encontrado.append(-1)

            bk_encontrado[1] -= 1
            escreve_bucket(bk_encontrado, ref_bk, buckets)
            removeu = True
            break
        
    if removeu:
        campos_diretorio, profundidade_global = tentar_combinar_bk(ref_bk, bk_encontrado, campos_diretorio, buckets, profundidade_global)
        return True, campos_diretorio, profundidade_global
    else:
        return False, campos_diretorio, profundidade_global

def tentar_combinar_bk(ref_bk: int, bk_encontrado: list, campos_diretorio: list, buckets: io.BufferedWriter, profundidade_global: int) -> tuple:
    tem_amigo, endereco_amigo = encontrar_bk_amigo(bk_encontrado, profundidade_global)
    if not tem_amigo:
        return campos_diretorio, profundidade_global
    
    if campos_diretorio[endereco_amigo] == ref_bk:
        return campos_diretorio, profundidade_global
    
    buckets.seek(4 + TAM_BUCKET * campos_diretorio[endereco_amigo])
    bucket_amigo = list(struct.unpack(LEITURA_BUCKET, buckets.read(TAM_BUCKET)))

    if (bucket_amigo[1] + bk_encontrado[1]) <= TAM_MAX_BUCKET:
        ref_amigo = campos_diretorio[endereco_amigo]
        bucket = combinar_bk(ref_bk, bk_encontrado, ref_amigo, bucket_amigo)

        buckets.seek(4 + TAM_BUCKET * ref_bk)
        buckets.write(struct.pack(LEITURA_BUCKET, *bucket))

        buckets.seek(0)
        primeiro_ped = struct.unpack("<i", buckets.read(4))[0]

        bucket_amigo[1] = -1
        bucket_amigo[2] = primeiro_ped

        buckets.seek(4 + TAM_BUCKET * ref_amigo)
        buckets.write(struct.pack(LEITURA_BUCKET, *bucket_amigo))

        buckets.seek(0)
        buckets.write(struct.pack("<i", ref_amigo))

        campos_diretorio[endereco_amigo] = ref_bk

        combinou_dir, campos_diretorio, profundidade_global = tentar_combinar_dir(campos_diretorio, profundidade_global)
        if combinou_dir:
            campos_diretorio, profundidade_global = tentar_combinar_bk(ref_bk, bucket, campos_diretorio, buckets, profundidade_global)
            return campos_diretorio, profundidade_global

        return campos_diretorio, profundidade_global
    
    return campos_diretorio, profundidade_global
    
def tentar_combinar_dir(campos_diretorio: list, profundidade_global: int) -> tuple:
    if profundidade_global == 0:
        return False, campos_diretorio, profundidade_global
    
    tam_dir = 2 ** profundidade_global
    diminuir = True

    for i in range(0, tam_dir - 1, 2):
        if campos_diretorio[i] != campos_diretorio[i + 1]:
            diminuir = False
            break
    
    if diminuir:
        novo_dir = []
        for i in range(0, tam_dir - 1, 2):
            novo_dir.append(campos_diretorio[i])
        profundidade_global -= 1
        return diminuir, novo_dir, profundidade_global
    
    return diminuir, campos_diretorio, profundidade_global
    
def combinar_bk(ref_bk: int, bk_encontrado: list, ref_amigo: int, bucket_amigo) -> list:
    chaves = []
    for i in range(bk_encontrado[1]):
        chaves.append(bk_encontrado[i + 2])
    for i in range(bucket_amigo[1]):
        chaves.append(bucket_amigo[i + 2])
    
    for i in range(len(chaves)):
        bk_encontrado[i + 2] = chaves[i]
    bk_encontrado[1] = len(chaves)
    bk_encontrado[0] -= 1
    return bk_encontrado
    
def encontrar_bk_amigo(bk_encontrado: list, profundidade_global: int) -> tuple:
    if profundidade_global == 0 or bk_encontrado[0] < profundidade_global:
        return False, None
    
    end_comum = gerar_endereco(bk_encontrado[2], bk_encontrado[0])
    end_amigo = end_comum ^ 1
    return True, end_amigo

