import struct
import io
from busca import *

TESTE = False
TAM_MAX_BUCKET: int = 5
TAM_BUCKET = 4 + 4 +(TAM_MAX_BUCKET * 4)
LEITURA_BUCKET = "<" + str(TAM_BUCKET // 4) + "i"


def inicializa_hashing(diretorio: io.BufferedWriter, buckets: io.BufferedWriter):
    cabecalho = struct.pack("<i", -1)

    profundidade_local = struct.pack("<i", 0)
    contador_chaves = struct.pack("<i", 0)

    arquivos_empacotados = bytearray(cabecalho + profundidade_local + contador_chaves)

    for i in range(TAM_MAX_BUCKET):
        chave = struct.pack("<i", -1)
        arquivos_empacotados += chave
    
    if TESTE:
        print(arquivos_empacotados)
    
    buckets.write(arquivos_empacotados)

    profundidade_global = struct.pack("<i", 0)
    ponteiro_inicial = struct.pack("<i", 0)

    arquivos_empacotados = profundidade_global + ponteiro_inicial

    if TESTE:
        print("inicial ")
        print(arquivos_empacotados)

    diretorio.write(arquivos_empacotados)



def carrega_diretorio_memoria(diretorio: io.BufferedWriter) -> list:
    diretorio.seek(0)
    profundidade_global = struct.unpack("<i", diretorio.read(4))[0]
    campos_diretorio = diretorio.read(4 * (2 ** profundidade_global))

    formato = "<" + str(2 ** profundidade_global) + "i"

    lista_ponteiros = list(struct.unpack(formato, campos_diretorio))
    lista = [profundidade_global, lista_ponteiros]

    return lista

def escreve_diretorio(diretorio: io.BufferedWriter, campos_diretorio: list, profundidade_global: int):
    diretorio.seek(0)
    diretorio.write(struct.pack("<i", profundidade_global))

    diretorios_binario = bytearray()
    for elemento in campos_diretorio:
        diretorios_binario += struct.pack("<i", elemento)
    
    diretorio.write(diretorios_binario)
    diretorio.truncate()

def gerar_endereco(chave: int, profundidade: int) -> int:
    """
    Essa função cria uma mascara e um retorno, cada fez que o loop ocorre ela abre um espaço ao final de retorno, pega o menor bit
    da chave usando o operador & e a mascara, e adiciona a retorno no espaço aberto anteriormente usando o operador |, depois disso
    joga o ultimo bit da chave fora, e repete o processo
    """
    val_ret = 0
    mascara = 1
    val_hash = chave

    for i in range(profundidade):
        val_ret = val_ret << 1
        bit_baixa_ordem = val_hash & mascara
        val_ret = val_ret | bit_baixa_ordem
        val_hash = val_hash >> 1

    return val_ret 

def escreve_bucket(bucket: list, rrn: int, buckets: io.BufferedWriter):
    dados_bytes = struct.pack(LEITURA_BUCKET, *bucket)
    buckets.seek(4 + rrn * TAM_BUCKET)
    buckets.write(dados_bytes)