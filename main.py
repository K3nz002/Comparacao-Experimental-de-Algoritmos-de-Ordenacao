import sys
import os
import time
import random
import json
import csv
import argparse
import concurrent.futures as cf

def bubble_sort(v):
    """
    Ordena a lista 'v' in-place utilizando o algoritmo Bubble Sort com flag de parada.

    Funcionamento:
        Percorre repetidamente a lista, comparando pares de elementos adjacentes
        e trocando-os caso estejam fora de ordem. Se em uma passagem completa
        nenhuma troca for efetuada, o algoritmo encerra precocemente (vetor já ordenado).

    Complexidade Assintótica:
        - Melhor caso: Omega(n) (vetor já ordenado)
        - Caso médio:  Theta(n^2)
        - Pior caso:   O(n^2) (vetor em ordem estritamente decrescente)
        - Espaço auxiliar: O(1) (in-place)
        - Estabilidade: Estável
    """
    n = len(v)
    for i in range(n - 1):
        swapped = False  # flag de parada caso vetor já esteja ordenado
        for j in range(n - i - 1):
            if v[j] > v[j + 1]:
                v[j], v[j + 1] = v[j + 1], v[j]
                swapped = True
        if not swapped:
            break
    return v


def selection_sort(v):
    """
    Ordena a lista 'v' in-place utilizando o algoritmo Selection Sort.

    Funcionamento:
        Divide o vetor em duas partes: a sublista ordenada (à esquerda) e a não
        ordenada (à direita). A cada iteração i, busca o índice do menor elemento
        restante na sublista não ordenada e o troca diretamente com a posição i.

    Complexidade Assintótica:
        - Melhor caso: Omega(n^2)
        - Caso médio:  Theta(n^2)
        - Pior caso:   O(n^2)
        - Espaço auxiliar: O(1) (in-place)
        - Estabilidade: Não-estável (na implementação padrão por trocas)
    """
    n = len(v)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if v[j] < v[min_idx]:
                min_idx = j
        if min_idx != i:
            v[i], v[min_idx] = v[min_idx], v[i]
    return v


def insertion_sort(v):
    """
    Ordena a lista 'v' in-place utilizando o algoritmo Insertion Sort.

    Funcionamento:
        Percorre a lista da esquerda para a direita, inserindo cada elemento 'chave'
        na sua posição correta na sublista já ordenada à sua esquerda, deslocando
        os elementos maiores uma posição à frente.

    Complexidade Assintótica:
        - Melhor caso: Omega(n) (vetor já ordenado)
        - Caso médio:  Theta(n^2)
        - Pior caso:   O(n^2) (vetor em ordem estritamente decrescente)
        - Espaço auxiliar: O(1) (in-place)
        - Estabilidade: Estável
    """
    n = len(v)
    for i in range(1, n):
        key = v[i]
        j = i - 1
        while j >= 0 and v[j] > key:
            v[j + 1] = v[j]
            j -= 1
        v[j + 1] = key
    return v


def _heapify(v, n, i):
    """
    Procedimento auxiliar do Heap Sort para manter a propriedade de Max-Heap.
    Implementação iterativa para máxima eficiência de execução em Python.
    """
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and v[left] > v[largest]:
            largest = left
        if right < n and v[right] > v[largest]:
            largest = right

        if largest != i:
            v[i], v[largest] = v[largest], v[i]
            i = largest
        else:
            break


def heap_sort(v):
    """
    Ordena a lista 'v' in-place utilizando o algoritmo Heap Sort (com Max-Heap).

    Funcionamento:
        1. Constrói um Max-Heap com todos os elementos do vetor (custo O(n)).
        2. Troca repetidamente a raiz (maior elemento) com o último elemento
           não ordenado e reconstrói o heap na subárvore restante (custo O(log n) por extração).

    Complexidade Assintótica:
        - Melhor caso: Omega(n log n)
        - Caso médio:  Theta(n log n)
        - Pior caso:   O(n log n)
        - Espaço auxiliar: O(1) (in-place)
        - Estabilidade: Não-estável
    """
    n = len(v)

    # Fase 1: Construção do Max-Heap (bottom-up)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(v, n, i)

    # Fase 2: Extração repetida do maior elemento
    for i in range(n - 1, 0, -1):
        v[0], v[i] = v[i], v[0]
        _heapify(v, i, 0)

    return v


def _worker_chunk(seeds, n):
    """
    Executa um lote (chunk) de realizações em um processo independente.
    Garante que:
      1. Cada realização gera um vetor aleatório vi com n elementos.
      2. São criadas 4 cópias idênticas vi^(1), vi^(2), vi^(3), vi^(4).
      3. A medição de tempo com time.perf_counter() ocorre EXCLUSIVAMENTE
         durante a execução do algoritmo de ordenação.
      4. Retorna a soma acumulada dos tempos de cada algoritmo no chunk.
    """
    sum_bubble = 0.0
    sum_selection = 0.0
    sum_insertion = 0.0
    sum_heap = 0.0

    for seed in seeds:
        rng = random.Random(seed)
        # Geração do vetor aleatório desordenado vi
        v_base = [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]

        # Criação de 4 cópias idênticas
        v_bubble = v_base.copy()
        v_selection = v_base.copy()
        v_insertion = v_base.copy()
        v_heap = v_base.copy()

        # Medição Bubble Sort
        t0 = time.perf_counter()
        bubble_sort(v_bubble)
        sum_bubble += (time.perf_counter() - t0)

        # Medição Selection Sort
        t0 = time.perf_counter()
        selection_sort(v_selection)
        sum_selection += (time.perf_counter() - t0)

        # Medição Insertion Sort
        t0 = time.perf_counter()
        insertion_sort(v_insertion)
        sum_insertion += (time.perf_counter() - t0)

        # Medição Heap Sort
        t0 = time.perf_counter()
        heap_sort(v_heap)
        sum_heap += (time.perf_counter() - t0)

    return sum_bubble, sum_selection, sum_insertion, sum_heap


def run_battery(n, r, num_workers=None, chunk_size=50):
    """
    Executa uma bateria experimental para um dado tamanho de vetor n com r realizações.
    Utiliza ProcessPoolExecutor para paralelizar as realizações nos múltiplos núcleos
    da CPU, mantendo total rigor e precisão nas medições de cada realização individual.
    """
    if num_workers is None:
        cpu_count = os.cpu_count() or 4
        # Deixar 1 a 2 núcleos livres para o sistema operacional manter fluidez
        num_workers = max(1, min(cpu_count - 1, 10))

    print(f"\n[{time.strftime('%H:%M:%S')}] Iniciando bateria: n = {n}, r = {r:,} realizações "
          f"({num_workers} processos paralelos)...")

    # Divide as r sementes em lotes (chunks)
    all_seeds = list(range(r))
    chunks = [all_seeds[i:i + chunk_size] for i in range(0, r, chunk_size)]

    total_bubble = 0.0
    total_selection = 0.0
    total_insertion = 0.0
    total_heap = 0.0

    completed_runs = 0
    t_start = time.perf_counter()

    with cf.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(_worker_chunk, chunk, n) for chunk in chunks]

        for future in cf.as_completed(futures):
            b, s, i_t, h = future.result()
            total_bubble += b
            total_selection += s
            total_insertion += i_t
            total_heap += h
            completed_runs += chunk_size

            # Barra de progresso amigável no console
            pct = min(100.0, (completed_runs / r) * 100.0)
            elapsed = time.perf_counter() - t_start
            print(f"\r  Progresso: {completed_runs if completed_runs <= r else r}/{r} ({pct:5.1f}%) | "
                  f"Tempo decorrido: {elapsed:.1f}s", end="", flush=True)

    print()
    elapsed_total = time.perf_counter() - t_start
    print(f"  Concluído em {elapsed_total:.2f}s!")

    return {
        "Bubble Sort": total_bubble / r,
        "Selection Sort": total_selection / r,
        "Insertion Sort": total_insertion / r,
        "Heap Sort": total_heap / r
    }


# ==============================================================================
# 3. GERAÇÃO DOS GRÁFICOS
# ==============================================================================

def generate_charts(results, ratios, output_dir):
    """
    Gera e salva três gráficos de alta qualidade para apresentação no relatório:
      1. comparacao_tempos.png: Curvas lineares de tempo médio vs tamanho n.
      2. comparacao_escala_log.png: Escala log-log evidenciando a declividade das ordens assintóticas.
      3. razoes_crescimento.png: Comparação das razões experimentais R1 e R2 com os valores teóricos.
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("[AVISO] Matplotlib não está disponível para gerar gráficos.")
        return

    os.makedirs(output_dir, exist_ok=True)
    ns = sorted(results.keys())
    algos = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Heap Sort"]
    colors = {
        "Bubble Sort": "#E63946",
        "Selection Sort": "#F4A261",
        "Insertion Sort": "#2A9D8F",
        "Heap Sort": "#1D3557"
    }
    markers = {
        "Bubble Sort": "o",
        "Selection Sort": "s",
        "Insertion Sort": "^",
        "Heap Sort": "D"
    }

    # --------------------------------------------------------------------------
    # Gráfico 1: Tempo Médio de Execução (Escala Linear em Milissegundos)
    # --------------------------------------------------------------------------
    plt.figure(figsize=(9, 6), dpi=300)
    for algo in algos:
        # Converter para milissegundos para facilitar leitura
        times_ms = [results[n][algo] * 1000.0 for n in ns]
        plt.plot(ns, times_ms, marker=markers[algo], linewidth=2.2, markersize=8,
                 label=algo, color=colors[algo])
        for x, y in zip(ns, times_ms):
            plt.annotate(f"{y:.2f} ms", (x, y), textcoords="offset points",
                         xytext=(0, 8), ha="center", fontsize=8, fontweight="bold")

    plt.title("Comparação Experimental do Tempo Médio de Ordenação\n(Escala Linear)", fontsize=13, fontweight="bold")
    plt.xlabel("Tamanho do Vetor (n)", fontsize=11)
    plt.ylabel("Tempo Médio (ms)", fontsize=11)
    plt.xticks(ns)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10, loc="upper left")
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "comparacao_tempos.png")
    plt.savefig(chart1_path)
    plt.close()
    print(f"[OK] Gráfico gerado: {chart1_path}")

    # --------------------------------------------------------------------------
    # Gráfico 2: Comparação em Escala Log-Log
    # --------------------------------------------------------------------------
    plt.figure(figsize=(9, 6), dpi=300)
    for algo in algos:
        times_ms = [results[n][algo] * 1000.0 for n in ns]
        plt.loglog(ns, times_ms, marker=markers[algo], linewidth=2.2, markersize=8,
                   label=algo, color=colors[algo], base=2)

    plt.title("Comparação Experimental de Ordenação\n(Escala Logarítmica - Base 2)", fontsize=13, fontweight="bold")
    plt.xlabel("Tamanho do Vetor (n) [Escala Log2]", fontsize=11)
    plt.ylabel("Tempo Médio (ms) [Escala Log2]", fontsize=11)
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend(fontsize=10, loc="upper left")
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "comparacao_escala_log.png")
    plt.savefig(chart2_path)
    plt.close()
    print(f"[OK] Gráfico gerado: {chart2_path}")

    # --------------------------------------------------------------------------
    # Gráfico 3: Razões de Crescimento R1 e R2 vs Valores Teóricos
    # --------------------------------------------------------------------------
    plt.figure(figsize=(10, 6), dpi=300)
    x = np.arange(len(algos))
    width = 0.35

    r1_values = [ratios[algo]["R1"] for algo in algos]
    r2_values = [ratios[algo]["R2"] for algo in algos]

    rects1 = plt.bar(x - width/2, r1_values, width, label="R1 = T(2000)/T(1000)", color="#457B9D")
    rects2 = plt.bar(x + width/2, r2_values, width, label="R2 = T(4000)/T(2000)", color="#E76F51")

    # Linhas de referência teórica: 4.0 para Theta(n^2) e ~2.2 para Theta(n log n)
    plt.axhline(y=4.0, color="#E63946", linestyle="--", linewidth=1.5, label="Teórico Theta(n²): 4.0x")
    plt.axhline(y=2.2, color="#2A9D8F", linestyle=":", linewidth=1.8, label="Teórico Theta(n log n): ~2.2x")

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.annotate(f"{height:.2f}x",
                         xy=(rect.get_x() + rect.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha="center", va="bottom", fontsize=9, fontweight="bold")

    autolabel(rects1)
    autolabel(rects2)

    plt.title("Razões de Crescimento Empíricas ao Dobrar o Tamanho da Entrada\n(R1 e R2 vs Esperado Teórico)",
              fontsize=13, fontweight="bold")
    plt.xlabel("Algoritmo", fontsize=11)
    plt.ylabel("Razão de Crescimento (Fator multiplicador)", fontsize=11)
    plt.xticks(x, algos, fontsize=10)
    plt.ylim(0, max(max(r1_values), max(r2_values)) * 1.25)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.legend(fontsize=9, loc="upper right")
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "razoes_crescimento.png")
    plt.savefig(chart3_path)
    plt.close()
    print(f"[OK] Gráfico gerado: {chart3_path}")


# ==============================================================================
# 4. FUNÇÃO PRINCIPAL E APRESENTAÇÃO DOS RESULTADOS
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Experimento comparativo de algoritmos de ordenação conforme especificação UnDF."
    )
    parser.add_argument("--workers", type=int, default=None,
                        help="Número de processos paralelos a utilizar (padrão: CPU_COUNT - 1).")
    parser.add_argument("--test-mode", action="store_true",
                        help="Modo de teste rápido com número reduzido de realizações (para validação imediata).")
    args = parser.parse_args()

    print("=" * 78)
    print(" COMPLEXIDADE ALGORÍTMICA - TRABALHO 1: COMPARAÇÃO EXPERIMENTAL")
    print(" Universidade do Distrito Federal – UnDF | Ciência da Computação")
    print(" Prof. Dr. Jayme Milanezi Junior")
    print("=" * 78)

    # Definição das três baterias conforme Tabela da Seção 2 do PDF
    if args.test_mode:
        print("[MODO DE TESTE RÁPIDO ATIVADO: realizações reduzidas para validação de fluxo]")
        batteries = [
            (1000, 100),
            (2000, 50),
            (4000, 20)
        ]
    else:
        batteries = [
            (1000, 10_000),
            (2000, 2_500),
            (4000, 625)
        ]

    # Dicionário para armazenar resultados: results[n][algoritmo] = tempo_medio
    results = {}

    for n, r in batteries:
        results[n] = run_battery(n, r, num_workers=args.workers)

    # --------------------------------------------------------------------------
    # Cálculo das Razões R1 e R2 conforme Seção 5 do PDF
    # --------------------------------------------------------------------------
    algos = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Heap Sort"]
    ratios: Dict[str, Dict[str, float]] = {}

    for algo in algos:
        t1000 = results[1000][algo]
        t2000 = results[2000][algo]
        t4000 = results[4000][algo]
        r1 = t2000 / t1000 if t1000 > 0 else 0.0
        r2 = t4000 / t2000 if t2000 > 0 else 0.0
        ratios[algo] = {"R1": r1, "R2": r2}

    # --------------------------------------------------------------------------
    # Exibição da Tabela Oficial Formatada
    # --------------------------------------------------------------------------
    print("\n" + "=" * 78)
    print(" TABELA OFICIAL DE RESULTADOS - TEMPOS MÉDIOS DE EXECUÇÃO")
    print("=" * 78)
    header = f"{'Algoritmo':<18} | {'n = 1000':<15} | {'n = 2000':<15} | {'n = 4000':<15}"
    print(header)
    print("-" * len(header))
    for algo in algos:
        t1 = results[1000][algo]
        t2 = results[2000][algo]
        t3 = results[4000][algo]
        # Exibe em milissegundos e segundos
        row = f"{algo:<18} | {t1*1000:8.3f} ms ({t1:7.4f}s) | {t2*1000:8.3f} ms ({t2:7.4f}s) | {t3*1000:8.3f} ms ({t3:7.4f}s)"
        print(row)
    print("-" * len(header))

    print("\n" + "=" * 78)
    print(" RAZÕES DE CRESCIMENTO EXPERIMENTAIS AO DOBRAR O TAMANHO DA ENTRADA")
    print("   R1 = T(2000) / T(1000)   |   R2 = T(4000) / T(2000)")
    print("   Teórico Theta(n²): ~4.00x | Teórico Theta(n log n): ~2.20x")
    print("=" * 78)
    header_r = f"{'Algoritmo':<18} | {'Complexidade':<16} | {'R1 (2000/1000)':<16} | {'R2 (4000/2000)':<16}"
    print(header_r)
    print("-" * len(header_r))
    complexities = {
        "Bubble Sort": "Theta(n^2)",
        "Selection Sort": "Theta(n^2)",
        "Insertion Sort": "Theta(n^2)",
        "Heap Sort": "Theta(n log n)"
    }
    for algo in algos:
        r1 = ratios[algo]["R1"]
        r2 = ratios[algo]["R2"]
        c = complexities[algo]
        print(f"{algo:<18} | {c:<16} | {r1:13.3f}x    | {r2:13.3f}x")
    print("-" * len(header_r))

    # --------------------------------------------------------------------------
    # Salvamento dos Resultados em Arquivos (JSON e CSV)
    # --------------------------------------------------------------------------
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "resultados.json")
    csv_path = os.path.join(base_dir, "resultados.csv")
    graphs_dir = os.path.join(base_dir, "graficos")

    output_data = {
        "experiment_info": {
            "title": "Trabalho 1: Comparacao Experimental de Algoritmos de Ordenacao",
            "institution": "Universidade do Distrito Federal - UnDF",
            "course": "Ciencia da Computacao",
            "professor": "Prof. Dr. Jayme Milanezi Junior",
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "batteries": {str(n): r for n, r in batteries}
        },
        "average_times_seconds": {str(n): results[n] for n in results},
        "ratios": ratios
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    print(f"\n[OK] Dados exportados para: {json_path}")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Complexidade", "Tempo_Medio_n1000_s", "Tempo_Medio_n2000_s", "Tempo_Medio_n4000_s", "R1", "R2"])
        for algo in algos:
            writer.writerow([
                algo,
                complexities[algo],
                f"{results[1000][algo]:.6f}",
                f"{results[2000][algo]:.6f}",
                f"{results[4000][algo]:.6f}",
                f"{ratios[algo]['R1']:.4f}",
                f"{ratios[algo]['R2']:.4f}"
            ])
    print(f"[OK] Dados exportados para: {csv_path}")

    # --------------------------------------------------------------------------
    # Geração dos Gráficos
    # --------------------------------------------------------------------------
    generate_charts(results, ratios, graphs_dir)
    print("\nExperimento concluído com sucesso!")


if __name__ == "__main__":
    main()