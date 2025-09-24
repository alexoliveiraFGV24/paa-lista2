from typing import List, Tuple
import math

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
    # Usei o set do Python, que tem a propriedade de armazenar apenas elementos distintos

    vistos = set() # No pior caso será O(n) de espaço
    n = len(sabores) # O(1)
    i = 0
    max_len = 0

    for j in range(n):  # Passo por todos os sabores (O(n))
        while sabores[j] in vistos: # O(c), com c < n
            vistos.remove(sabores[i])
            i += 1
        vistos.add(sabores[j]) # O(1) no caso médio por conta da estrutura de tabela hash
        max_len = max(max_len, j - i + 1)

    return max_len



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

    # Funções auxiliares para fazer o heap mínimo e suas operações de adição e remoção (O(logn)), mostrado em aula
    # Basicamente copiei, colei e traduzi os códigos dos slides para Python 
    
    # Ordeno por tempo de entrada (O(nlogn))
    estadias.sort(key=lambda x: x[0])



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
    pass


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
    pass


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

    # Ideia: Temos que achar o menor T inteiro tal que sum(math.floor(T / A_i) for A_i in A) >= k
    # Para isso, descobri um limite superior razoável para T manipulando a desigualdade (k*min(A))
    # Logo, montariamos um array auxiliar [0,1,2,..,k*min(A)] e faríamos uma busca binária modificada nele
    # Começaríamos no meio do array. Se o total de órbitas desse T for >= k, vamos para a porção esquerda, pois queremos diminuir T
    # Caso contrário, vamos para a porção direita 

    # Função auxiliar para calcular o total de órbitas para um valor T
    def total_orbitas(T: int) -> int:
        return sum(math.floor(T / A_i) for A_i in A) # O(n)
    
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

    def partition(arr, low, high, pivot):
        for i in range(low, high + 1):
            if arr[i] == pivot:
                arr[i], arr[high] = arr[high], arr[i]
                break
        store_index = low
        for i in range(low, high):
            if arr[i] < pivot:
                arr[i], arr[store_index] = arr[store_index], arr[i]
                store_index += 1
        arr[store_index], arr[high] = arr[high], arr[store_index]
        return store_index
    
    def medianOf(A:List[int]):
        A = sorted(A)  # Função prória do Python que substitui o Quicksort
        return A[len(A) // 2]
    
    def selectMOM(A:List[int], p:int, r:int, k:int):
        n = r - p + 1
        if k <= 0 or k > n:
            return -1
        median = []
        i = 0
        pos = p
        while pos <= r:
            size = r - pos + 1
            group_size = 5 if size >= 5 else size
            group = A[pos:pos + group_size]
            median.append(medianOf(group))
            i += 1
            pos += 5
        mom = median[i - 1] if i == 1 else selectMOM(median, 0, i - 1, i // 2)
        j = partition(A, p, r, mom)
        if j - p == k - 1:
            return A[j]
        elif j - p > k - 1:
            return selectMOM(A, p, j - 1, k)
        else:
            return selectMOM(A, j + 1, r, k - j + p - 1)
    
    # Pego o tamanho da lista, a posição central da lista e calculo a mediana em O(n)
    n = len(A) # O(1)
    k_pos = (n + 1) // 2
    mediana = selectMOM(A.copy(), 0, n - 1, k_pos) # O(n)

    return mediana