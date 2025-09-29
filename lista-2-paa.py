from typing import List, Tuple

############ Atenção ################
# Não altere a assinatura das funções.
# Não altere a classe TreeNode.
# Você pode criar outras funções ou classes se julgar necessário, mas deve defini-las no corpo da função do exercicio.

# ==============================================================================
# Problema de exemplo
# ==============================================================================
def problema_0(A: List[int]) -> List[bool]:
    """
    Recebe uma lista de inteiros e retorna uma lista de booleanos
    indicando se cada numero é primo em tempo O(n * sqrt(maxval)).
    """
    def eh_primo(n: int) -> bool:
        if n==2:
            return True
        if n <= 1 or n%2==0:
            return False
        
        # Iterando apenas nos impares para diminuir a constante
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    resultado = []
    for num in A:
        resultado.append(eh_primo(num))

    return resultado


# ==============================================================================
# Problema 1 - A Biblioteca de Alexandria
# ==============================================================================

def problema_1(eventos: List[Tuple[int, int]]) -> Tuple[int, Tuple[int, int]]:
    """
    A administração da biblioteca busca compreender o padrão de uso de seus
    frequentadores e, para isso, precisa identificar o período de pico, ou
    seja, o intervalo de tempo em que há o maior número de usuários presentes.

    O algoritmo deverá receber $n$ pares de inteiros $(a, b)$, onde $a$
    representa o horário de entrada e $b$ o de saída de um usuário. Como
    resultado, ele deve retornar $k, (u, v)$, onde $k$ é a quantidade
    máxima de pessoas na biblioteca e $(u, v)$ é o intervalo de tempo
    maximal (de maior tamanho) correspondente a esse pico. Se houver mais
    de um intervalo de pico maximal, retorne aquele com menor $u$.

    O algoritmo deve ter tempo de execução $O(n \log n)$.
    """

    # Ideia: Montar uma linha temporal para identificar as colisões entre os horários, juntamente com "pesos" para entrada e saída
    # Ir atualizando cada intervalo maximal de acordo com a relação entre total atual de pessoas e o máximo de pessoas na biblioteca

    # Montando a linha temporal (O(n)), marcando se é entrada ou saída
    linha_temporal = []
    n = len(eventos)
    for i in range(n):
        evento = eventos[i]
        linha_temporal.append((evento[0], 1)) # Entrada é 1
        linha_temporal.append((evento[1], -1)) # Saída é -1

    # Ordenando pelo tempo de chegada/saída (O(nlogn))
    linha_temporal.sort(key=lambda x: (x[0], -x[1]))  # Caso dê empate, o tipo entrada vem primeiro
    
    max_pessoas = 0
    atual_pessoas = 0
    intervalos_maximais = []
    intervalo_maximal = None

    # Percorro a linha temporal (O(n))
    for i in range(2*n):
        atual_pessoas += linha_temporal[i][1] # Achando o número atual de pessoas
        if atual_pessoas >= max_pessoas:
            max_pessoas = atual_pessoas
            intervalo_maximal = (linha_temporal[i][0], None, max_pessoas) # Atualizando o máximo de pessoas e começo a contar o início do meu intervalo maximal
        # Finalizo o meu intervalo maximal daquele momento (lembrando que podem haver mais de um intervalo maximal)
        elif atual_pessoas < max_pessoas and intervalo_maximal[1] == None:
            fim = linha_temporal[i][0]
            intervalo = (intervalo_maximal[0], fim, max_pessoas)
            intervalo_maximal = intervalo
        # Se o intervalo estiver completo, adiciono na minha linha do tempo de intervalos maximais
        if intervalo_maximal != None and intervalo_maximal[1] != None:
            intervalos_maximais.append(intervalo_maximal)

    # Ordenando pelo número máximo de pessoas no intervalo maximal (O(nlogn))
    intervalos_maximais.sort(key=lambda x: (x[2], x[1])) # Caso dê empate, pego o intervalo que começou antes

    # Vejo o intervalo maximal que tem o menor tempo de início
    for intervalo in intervalos_maximais:
        if intervalo[2] == max_pessoas:

            return max_pessoas, (intervalo[0], intervalo[1])        


# ==============================================================================
# Problema 2 - Sisi e a Sorveteria
# ==============================================================================

def problema_2(sabores: List[int]) -> int:
    """
    Sisi quer saber qual foi o período mais longo, em dias consecutivos, que
    ela passou sem repetir um único sabor de sorvete.

    Você deve desenvolver um algoritmo com tempo de execução $O(n)$ que receba
    a sequência de sabores consumidos e retorne o tamanho da maior
    subsequência contínua de valores distintos.
    """

    # Ideia: vamos comparando as sequências e armazenando as sequências vistas
    # Usei o set do Python, que tem a propriedade de armazenar apenas elementos distintos (derivado do hash)

    vistos = set() # No pior caso será O(n) de espaço
    n = len(sabores) # O(1)
    i = 0
    tamanho_maximo = 0

    for j in range(n):  # Passo por todos os sabores (O(n))
        while sabores[j] in vistos: # O(c), com c < n
            vistos.remove(sabores[i]) # O(1) no caso médio por conta da estrutura de tabela hash
            i += 1
        vistos.add(sabores[j]) # O(1) no caso médio por conta da estrutura de tabela hash
        tamanho_maximo = max(tamanho_maximo, j - i + 1)

    return tamanho_maximo



# ==============================================================================
# Problema 3 - Hotel de Hilbert
# ==============================================================================

def problema_3(estadias: List[Tuple[int, int]]) -> Tuple[int, List[int]]:
    """
    O Grande Hotel de Hilbert receberá $n$ hóspedes. Para cada hóspede,
    conhecemos um par de inteiros $(a, b)$, que representam seu tempo de
    chegada e de partida, respectivamente. Para minimizar os custos, o
    gerente deseja utilizar o menor número possível de quartos. Duas pessoas
    podem ocupar o mesmo quarto, desde que o período de estadia delas não se
    sobreponha.

    O algoritmo deverá receber $n$ pares de inteiros $(a, b)$ e retornar
    $k, [r_1, r_2, \dots, r_n]$, onde $k$ é a quantidade mínima de quartos
    necessários e $r_i$ é o quarto que o i-ésimo hóspede (na mesma ordem da
    entrada) deverá utilizar.

    O algoritmo deve ter tempo de execução $O(n \log n)$.
    """

    # Ideia: Ordenar as estadias por ordem de chegada
    # Usar um heap mínimo para anotar os quartos ocupados
    # De acordo com cada tempo de chegada e saída dos hóspedes, dizer no heap se reutilizo o quarto ou aloco um novo

    # Funções auxiliares para fazer o heap mínimo e suas operações de adição e remoção (O(logn)), mostrados em aula
    # Basicamente copiei, colei, traduzi e adaptei o código do Heapfy e, ao invés de criar o heap de uma vez, fiz as funções pop e push

    # O(logn)
    def minHeapfy(arr, i):
        n = len(arr)
        inx_menor = i
        inx_esq = 2 * i + 1
        inx_dir = 2 * i + 2
        if (inx_esq < n and arr[inx_esq][0] < arr[inx_menor][1]): # Adaptei de "arr[inx_esq][0] > arr[inx_menor][1]"" para "arr[inx_esq][0] < arr[inx_menor][1]"" (heap mínimo)
            inx_menor = inx_esq
        if (inx_dir < n and arr[inx_dir][0] < arr[inx_menor][1]):  # Adaptei de "arr[inx_dir][0] > arr[inx_menor][1]"" para "arr[inx_dir][0] < arr[inx_menor][1]"" (heap mínimo)
            inx_menor = inx_dir
        if inx_menor != i:
            arr[i], arr[inx_menor] = arr[inx_menor], arr[i]  # Swap            
            minHeapfy(arr, n, inx_menor)

    # O(logn)
    def minHeapPush(heap, elemento):
        n = len(heap)
        heap.append(elemento)
        i = n - 1
        while i > 0:
            pai = (i - 1) // 2
            if heap[i][0] < heap[pai][0]:
                heap[i], heap[pai] = heap[pai], heap[i]  # Swap
                i = pai
            else:
                break
    
    # O(logn)
    def minHeapPop(heap):
        if not heap:
            return None
        menor = heap[0]
        ultimo = heap.pop()
        if heap:
            heap[0] = ultimo
            minHeapfy(heap, 0)
        return menor

    # Faço a indexação das estadias e ordeno a sequência (O(n) + O(nlogn) = O(nlogn))
    n = len(estadias)
    hospedes_com_indice = []
    for i in range(n):
        hospedes_com_indice.append((estadias[i][0], estadias[i][1], i))
    hospedes_com_indice.sort(key=lambda x: (x[0], x[2]))  # Ordena por tempo de chegada, caso dê empate, pela ordem do input

    # (O(n) de espaço)
    heap = []  # Inicializo o heap com tuplas na forma (saída, quarto)
    resultado = [0] * n  # Inicializo a lista com os resultados dos quartos na ordem
    min_quartos_utilizados = 1  # inicializo o contador de quartos utilizados, no mínimo

    # Para cada hóspede que chegou no hotel (O(n))
    for chegada, saida, i in hospedes_com_indice:
        if heap and heap[0][0] < chegada:  # Vejo se a chegada é maior que a saída e retiro a raiz do heap mínimo (reutilizo o quarto)
            fim, quarto = minHeapPop(heap)  # O(logn)
        else:  # Caso contrário, temos que alocar mais um quarto
            quarto = min_quartos_utilizados
            min_quartos_utilizados += 1  

        # Para ambos os casos, adiciono o hóspede no heap
        resultado[i] = quarto
        minHeapPush(heap, (saida, quarto))  # O(logn)

    return min_quartos_utilizados - 1, resultado



# ==============================================================================
# Problema 4 - Quadra
# ==============================================================================

def problema_4(A: List[int], k: int) -> Tuple[int, int, int, int]:
    """
    Dado um vetor $A$ com $n$ inteiros e um valor alvo $k$, encontre quatro
    índices distintos cuja soma dos elementos seja igual a $k$.

    O algoritmo deve retornar uma tupla com os quatro índices em ordem
    crescente, $(a, b, c, d)$ com $a<b<c<d$, que satisfaça a condição
    $A_a + A_b + A_c + A_d = k$.

    Caso existam múltiplas soluções, retornar qualquer uma delas é suficiente.
    Se nenhuma combinação válida for encontrada, o algoritmo deve retornar
    (-1, -1, -1, -1).

    O algoritmo deve ter uma complexidade de tempo de $O(n^2 \log n)$.
    """

    # Ideia: Transformar o problema de quatro números em um problema de dois
    # Fazemos uma lista com todas as possíveis combinações de A[i] + A[j] (tal lista terá n(n-1)/2 termos)
    # Ordenamos essa lista pelo valor da soma para realizar uma busca com dois ponteiros
    
    n = len(A)
    pares = []

    # Gera todos os pares possíveis de elementos em A (O(n^2))
    for i in range(n):
        for j in range(i + 1, n):
            pares.append((A[i] + A[j], i, j))

    # Ordena os pares pelo valor da soma (O(n^2logn))
    pares.sort()

    # Ponteiros para busca em duas extremidades
    left = 0
    right = len(pares) - 1

    # Busca enquanto os ponteiros não se cruzarem
    while left < right:
        soma_left, i1, j1 = pares[left]
        soma_right, i2, j2 = pares[right]
        total = soma_left + soma_right    # soma das duas somas de pares

        # Caso encontramos uma soma igual a k
        if total == k:
            # Conjunto com os índices dos 4 elementos
            indices = {i1, j1, i2, j2}

            # Verifica se os 4 índices são distintos
            if len(indices) == 4:
                return tuple(sorted([i1, j1, i2, j2]))  # O(1)

            # Se houver colisão de índices, tenta mover os ponteiros
            l_next = left + 1
            r_prev = right - 1
            if l_next < right:
                left += 1
            elif r_prev > left:
                right -= 1
            else:
                break

        # Se a soma total for menor que k, aumenta soma movendo ponteiro da esquerda
        elif total < k:
            left += 1
        # Se a soma total for maior que k, diminui soma movendo ponteiro da direita
        else:
            right -= 1

    # Se não encontrou nenhuma solução válida
    return (-1, -1, -1, -1)


# ==============================================================================
# Problema 5 - Os blocos
# ==============================================================================

def problema_5(blocos: List[int]) -> int:
    """
    Você recebeu $n$ blocos de madeira e seu desafio é empilhá-los, formando
    o menor número possível de torres, seguindo duas regras:
    1. Um bloco só pode ser colocado sobre outro se o seu tamanho for menor ou
       igual ao do bloco inferior.
    2. Os blocos devem ser processados um a um, na sequência predefinida em
       que são apresentados.

    A cada bloco, você deve decidir se o coloca no topo de uma torre existente
    ou se inicia uma nova torre com ele. O algoritmo deve encontrar o número
    mínimo de torres necessárias com complexidade $O(n \log n)$.
    """

    # Ideia: Fazer um "hash", mas colocando apenas o topo da torre 
    # e contando quando devemos adicionar uma nova torre

    # Função auxiliar para, dada um array ordenado, retornar o índice mais a direita 
    # que um elemento x será adicionado na lista em O(logn)

    def adicionar_mais_a_direita(arr, x):
        inicio = 0
        fim = len(arr)
        while inicio < fim:
            meio = (inicio + fim) // 2
            if x < arr[meio]:
                fim = meio
            else:
                inicio = meio + 1
        return inicio

    min_torres = []

    for bloco in blocos:  # Para todos os blocos da lista
        i = adicionar_mais_a_direita(min_torres, -bloco)  # Pego o índice mais a direita (O(logn))
        if i < len(min_torres):  # Verifico se preciso adicionar uma nova torre
            min_torres[i] = -bloco
        else:
            min_torres.append(-bloco)  # Adiciono em O(1)

    num_min_torres = len(min_torres)  # Calculo o tamanho da lista em O(1)

    return num_min_torres


# ==============================================================================
# Problema 6: O Grande Sistema Planetário
# ==============================================================================

def problema_6(A: List[int], k: int) -> int:
    """
    Dado um conjunto de períodos orbitais $A_1, A_2, \dots, A_n$ e um número
    alvo de voltas $k$, encontre o menor número inteiro de anos, $T$, no qual
    a soma total de órbitas completadas por todos os $n$ planetas do sistema
    seja maior ou igual a $k$.

    A complexidade esperada é de $O(n \cdot \log(M))$, onde $M$ é a maior
    resposta possível.
    """

    # Ideia: Temos que achar o menor T inteiro tal que sum(floor(T / A_i) for A_i in A) >= k
    # Para isso, descobri um limite superior razoável para T manipulando a desigualdade (k*min(A))
    # Logo, montariamos um array auxiliar [0,1,2,..,k*min(A)] e faríamos uma busca binária modificada nele
    # Começaríamos no meio do array. Se o total de órbitas desse T for >= k, vamos para a porção esquerda, pois queremos diminuir T
    # Caso contrário, vamos para a porção direita

    # Funções auxiliares para calcular o piso de um número real x em O(1) e
    # para calcular o total de órbitas para um valor T em O(n)

    def floor(x:float) -> int:
        if x >= 0:
            return int(x)
        else:
            return int(x) - (x != int(x))

    def total_orbitas(T: int) -> int:
        return sum(floor(T / A_i) for A_i in A) # O(n)
    
    # Um limite superior razoável para T
    min_A = min(A)  # O(n)
    max_T = k * min_A  

    # Implementação da busca binária para encontrar o menor T
    esquerda = 0
    direita = max_T
    while esquerda < direita:  # O(logM), em que M seria o limite superior cotado para T
        meio = (esquerda + direita) // 2
        if total_orbitas(meio) >= k:  # O(n)
            direita = meio
        else:
            esquerda = meio + 1

    return esquerda


# ==============================================================================
# Problema 7: Otimização
# ==============================================================================

def problema_7(A: List[int]) -> int:
    """
    Dado um vetor $A$ com $n$ inteiros, projete um algoritmo linear que retorna
    o menor valor inteiro $k$ que minimiza a soma:
    $$ \sum_{i=1}^{n} |A_i-k| $$
    A complexidade de tempo deve ser $O(n)$.
    """

    # Ideia: vimos em estatística que a mediana minimiza tal soma. 
    # Logo, devemos calcular a mediana de A e ver qual elemento de A mais se aproxima dela
    # Portanto, podemos usar o algoritmo median of medians

    # Funções auxiliares para fazer o algoritmo mediana das medianas (O(n)), mostrado em aula
    # Basicamente copiei, colei e traduzi os códigos dos slides para Python

    def particao(arr:List[int], inicio:int, fim:int, pivo:int) -> int:
        for i in range(inicio, fim + 1):
            if arr[i] == pivo:
                arr[i], arr[fim] = arr[fim], arr[i]
                break
        store_inx = inicio
        for i in range(inicio, fim):
            if arr[i] < pivo:
                arr[i], arr[store_inx] = arr[store_inx], arr[i]
                store_inx += 1
        arr[store_inx], arr[fim] = arr[fim], arr[store_inx]  # Swap
        return store_inx
    
    # No caso da mediana das medianas, sempre ordenaremos 5 elementos, ou seja, para nós, essa função é O(1)
    # Contudo, para um array geral, a função é O(nlogn)
    def medianaArray(arr:List[int]) -> int:
        arr.sort()
        return arr[len(arr) // 2]
    
    def selectMOM(arr:List[int], p:int, r:int, k:int) -> int:
        n = r - p + 1
        if k <= 0 or k > n:
            return -1
        mediana = []
        i = 0
        posicao = p
        while posicao <= r:
            tamanho = r - posicao + 1
            tamanho_grupo = 5 if tamanho >= 5 else tamanho
            grupo = arr[posicao:posicao + tamanho_grupo]
            mediana.append(medianaArray(grupo))
            i += 1
            posicao += 5
        mom = mediana[i - 1] if i == 1 else selectMOM(mediana, 0, i - 1, i // 2)
        j = particao(arr, p, r, mom)
        if j - p == k - 1:
            return arr[j]
        elif j - p > k - 1:
            return selectMOM(A, p, j - 1, k)
        else:
            return selectMOM(A, j + 1, r, k - j + p - 1)
    
    # Pego o tamanho da lista, a posição central da lista e calculo a mediana em O(n)
    n = len(A) # O(1)
    k_pos = (n + 1) // 2
    mediana = selectMOM(A.copy(), 0, n - 1, k_pos) # O(n)

    return mediana