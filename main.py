from _typeshed import _type_checker_internals
def bubbleSort(v):
    '''
    Bubble sort é um algoritmo de ordenação simples
    que funciona comparando pares de elementos adjacentes
    e trocando-os se estiverem na ordem errada. Por exemplo
    se o número do primeiro índice for maior que o segundo eles iram trocar
    e assim sucessivamente.

    Complexidade: 0(n^2)
    '''
    for i in range(len(v) - 1):
        '''
        swap para otimizar o bubble sort
        ele verifica se os elementos já estão ordenados
        se não houver swap na iteração, significa que o array está ordenado
        '''
        swap = False
        for j in range(len(v) - i - 1):
            if v[j] > v[j+1]:
                v[j], v[j+1] = v[j+1], v[j]
                swap = True
        if not swap:
            break
    return v

def selectionSort(v):
    '''
    Selection Sort é um algoritmo de ordenação simples
    que funciona encontrando o menor elemento do array
    e trocando-o com o primeiro elemento. Ele faz isso para 
    cada posição do array.

    Complexidade: 0(n^2)
    '''
    for i in range(len(v) - 1):
        '''
        enquanto j for menor que 0 e v[j] for maior que a chave
        significa que a chave está na posição errada
        e os elementos que estão a direita da chave
        devem ser movidos para a direita
        '''
        min_index = i
        for j in range(i+1, len(v)):
            if v[min_index] > v[j]:
                min_index = j
        min_value = v.pop(min_index)
        v.insert(i, min_value)
    return v

def insertionSort(v):
    '''
    Insertion Sort é um algoritmo de ordenação simples
    que funciona inserindo o elemento na posição correta.

    Complexidade: 0(n^2)
    '''
    for i in range(1, len(v)):
        '''
        a posição i sempre representa a fronteira
        entre ordenados (a esquerda de i) e não ordenados (a direita de i)
        '''
        chave = v[i]
        j = i-1
        '''
        enquanto j for menor que 0 e v[j] for maior que a chave
        significa que a chave está na posição errada
        e os elementos que estão a direita da chave
        devem ser movidos para a direita
        '''
        while j >= 0 and v[j] > chave:
            v[j+1] = v[j]
            j = j-1
        v[j+1] = chave
    return v

def heapSort(v):
    '''
    Heap Sort é um algoritmo de ordenação eficiente
    que funciona construindo uma heap binária e
    extraindo os elementos da heap na ordem correta.

    Complexidade: 0(n log n)
    '''
    n = len(v)
    def heapify(v, n, i):
        maior = i    
        esquerda = 2 * i + 1    
        direita = 2 * i + 2  

        if esquerda < n and v[esquerda] > v[maior]:
            maior = esquerda

        if direita < n and v[direita] > v[maior]:
            maior = direita

        if maior != i:
            v[i], v[maior] = v[maior], v[i]
            heapify(v, n, maior)

    # constroe um max-heap e "afunda" o maior elemento
    for i in range(n//2 - 1, -1, -1):
        heapify(v, n, i)

    # remove o maior elemento e "afunda" o novo maior elemento
    for i in range(n - 1, 0, -1):
        v[i], v[0] = v[0], v[i]
        heapify(v, i, 0)

    return v

def main():
    pass

if __name__ == "__main__":
    main()