

def divide_list(l, n_elements):
    """Divide uma lista em M partes. Isso servirá para não sobrecarregar a consulta do elastic.
    Todas as requisições ao elastic não terão mais de N elementos, então dividiremos a lista
    recebida como parâmetro em M partes, cada uma com N elementos.
    :param l:list: A lista a ser dividida.
    :param n_elements:int: A quantidade máxima de elementos para cada parte.
    :returns divisions:list: Uma lista com as divisões (lista de listas), cada uma com N elementos.
    """

    divisions = []
    for i in range(0, len(l), n_elements):
        if i + n_elements < len(l):
            divisions.append(l[i:i+n_elements])
        else:
            divisions.append(l[i:])

    return divisions