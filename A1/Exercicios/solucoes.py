""" A1 2022 questão 2 """
def q2_2022(A, x):
    n = len(A)
    encontrei = False
    lista_soma = []
    A.sort()

    def buscaBinaria(arr, k):
        inicio = 0
        fim = len(arr) - 1
        while inicio <= fim:
            meio = (inicio + fim) // 2
            valor_meio = arr[meio]
            if valor_meio == k:
                return True
            elif valor_meio < k:
                inicio = meio + 1
            else:
                fim = meio - 1
        return False

    for i in range(n-3):
        for j in range(1, n-2):
            soma = A[i] + A[j]
            lista_soma.append(soma)

    for soma in lista_soma:
        complemento = x - soma
        encontrei = buscaBinaria(A, complemento)

    return encontrei
    

""" A1 2022 questão 3; A1 2024 questão 4 """
""" Item a """
def q3_a_2022(A):
    n = len(A)
    indices = [0,0]
    max_soma = 0
    for i in range(0,n-1):
        for j in range(i+1, n):
            soma = 0
            for k in range(i,j):
                soma += A[k]
            if soma > max_soma:
                max_soma = soma
                indices[0] = i
                indices[1] = j
    return indices

""" Item b """
def q3_b_2022(A):
    n = len(A)
    indices = [0,0]
    max_soma = 0
    for i in range(0,n-1):
        soma = A[i]
        for j in range(i+1, n):
            soma =+ A[j]
            if soma > max_soma:
                max_soma = soma
                indices[0] = i
                indices[1] = j
    return indices

""" Item c """
def q3_c_2022(A):
    n = len(A)
    max_global = A[0]
    max_local = A[0]
    start_index_global = 0
    end_index_global = 0
    start_index_local = 0
    for i in range(1, n):
        current_element = A[i]
        if current_element > max_local + current_element:
            max_local = current_element
            start_index_local = i
        else:
            max_local = max_local + current_element
        if max_local > max_global:
            max_global = max_local
            end_index_global = i
            start_index_global = start_index_local
    return [start_index_global, end_index_global]

""" A1 2022 questão 5 """
def q5_2022(A, B):
    A.sort()
    C = A.copy()
    hash = {}

    for num in A:
        if num in hash:
            hash[num] += 1
        else:
            hash[num] = 1

    
    return hash

A = [5,8,9,3,5,7,1,3,4,9,3,5,1,8,4]
B = [3,5,7,2]
print(q5_2022(A,B))

""" A1 2022 questão 6 """

""" A1 2023 questão 2 """

""" A1 2023 questão 3 """

""" A1 2023 questão 4; Simulado A1 2025 questão 2 """

""" A1 2023 questão 5; Simulado A1 2025 questão 4 """

""" A1 2024 questão 3 """

""" Simulado A1 2025 questão 3 """