def bubbleSort(v):
    
    for i in range(len(v)):
        for j in range(len(v)):
            if v[i] < v[j]:
                v[i], v[j] = v[j], v[i]
    return v

def selectionSort(v):
    for i in range(len(v)):
        for j in range(len(v)):
            if v[i] < v[j]:
                v[i], v[j] = v[j], v[i]
    return v

def insertionSort(v):
    for i in range(len(v)):
        chave = v[i]
        j = i-1
        while j >= 0 and v[j] > chave:
            v[j+1] = v[j]
            j = j-1
        v[j+1] = chave
    return v

def mergeSort(v):
    pass

def main():
    pass

if __name__ == "__main__":
    main()