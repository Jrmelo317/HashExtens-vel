import io
import struct

"""
Precisa apresentar as remocões
"""

TAM_MAX_BUCKET: int = 5
TAM_BUCKET = 4 + 4 +(TAM_MAX_BUCKET * 4)
LEITURA_BUCKET = "<" + str(TAM_BUCKET // 4) + "i"

def imprime_bk(buckets: io.BufferedWriter):
    print("--------PED--------")
    buckets.seek(0)
    topo_ped = struct.unpack("<i", buckets.read(4))[0]
    print(f"RRN Topo: {topo_ped}")
    print()

    print("------Buckets------")

    buckets.seek(0, 2)
    final_arq = buckets.tell()
    buckets.seek(4)
    total_para_ler = (final_arq - 4) // TAM_BUCKET

    for i in range(total_para_ler):
        bk = list(struct.unpack(LEITURA_BUCKET, buckets.read(TAM_BUCKET)))

        if bk[1] == -1:
            print(f"Bucket {i} --> Removido")
        else:
            print(f"Bucket {i} (Prof = {bk[0]})")
            print(f"ContaChaves = {bk[1]}")
            print(f"Chaves = {bk[2:]}")
        print()
