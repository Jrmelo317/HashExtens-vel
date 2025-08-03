"""
Sempre que ativada, essa funcionalidade apresentará na tela o conteúdo de todas as células do diretório, além das
seguintes informações: (a) profundidade; (b) tamanho atual; e (c) número total de buckets referenciados.
"""

def imprime_dir(campos_dir: list, pl: int):
    lista_buckets = []

    print("------Diretório------")
    for i in range(len(campos_dir)):
        print(f"dir[{i}] = bucket({campos_dir[i]})")
        if campos_dir[i] not in lista_buckets:
            lista_buckets.append(campos_dir[i])

    print()
    print(f"Profundidade = {pl}")
    print(f"Tamanho atual = {len(campos_dir)}")
    print(f"Total de buckets = {len(lista_buckets)}")