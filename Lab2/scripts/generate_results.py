import csv
import os
import random
import sys
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.setrecursionlimit(500_000)

SMALL_INPUTS = [100, 500, 1000, 2000, 5000, 10000]
LARGE_INPUTS = [20000, 30000, 50000, 75000, 100000]
INPUT_SIZES = SMALL_INPUTS + LARGE_INPUTS
REPEATS = 3


# --------------- algorithms ---------------

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def _heapify(arr, n, i):
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest == i:
            break
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest


def heapsort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)
    return arr


def shell_sort(arr):
    arr = arr[:]
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


# --------------- registry ---------------

ALGORITHMS = {
    "quicksort": ("QuickSort", quicksort),
    "mergesort": ("MergeSort", merge_sort),
    "heapsort": ("HeapSort", heapsort),
    "shellsort": ("ShellSort", shell_sort),
}


# --------------- helpers ---------------

def generate_random_array(n):
    return [random.randint(0, 10 * n) for _ in range(n)]


def time_run(fn, arr):
    best = None
    for _ in range(REPEATS):
        data = arr[:]
        start = time.perf_counter()
        fn(data)
        elapsed = time.perf_counter() - start
        if best is None or elapsed < best:
            best = elapsed
    return best


def ensure_dirs():
    os.makedirs("results", exist_ok=True)
    os.makedirs("figures", exist_ok=True)


def write_csv(name, rows):
    path = os.path.join("results", f"{name}.csv")
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["n", "time_s"])
        writer.writerows(rows)


def write_table(name, rows):
    path = os.path.join("results", f"{name}_table.tex")
    with open(path, "w") as handle:
        handle.write("\\begin{table}[H]\n")
        handle.write("\\centering\n")
        handle.write("\\caption{" + name.replace("_", " ").title() + " Results}\n")
        handle.write("\\begin{tabular}{rr}\n")
        handle.write("\\toprule\n")
        handle.write("n & time (s)\\\\\n")
        handle.write("\\midrule\n")
        for n, t in rows:
            handle.write(f"{n} & {t:.6f}\\\\\n")
        handle.write("\\bottomrule\n")
        handle.write("\\end{tabular}\n")
        handle.write("\\end{table}\n")


def plot_single(name, title, rows):
    ns = [n for n, _ in rows]
    ts = [t for _, t in rows]
    plt.figure(figsize=(7, 4))
    plt.plot(ns, ts, marker="o")
    plt.title(title)
    plt.xlabel("n (array size)")
    plt.ylabel("Time (s)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join("figures", f"{name}.png"), dpi=200)
    plt.close()


def plot_comparison(all_results):
    plt.figure(figsize=(8, 4.5))
    for name, title, rows in all_results:
        ns = [n for n, _ in rows]
        ts = [t for _, t in rows]
        plt.plot(ns, ts, marker="o", label=title)
    plt.title("Sorting Algorithm Comparison")
    plt.xlabel("n (array size)")
    plt.ylabel("Time (s)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join("figures", "comparison.png"), dpi=200)
    plt.close()


def main():
    random.seed(42)
    ensure_dirs()

    # pre-generate arrays so every algorithm gets the same data
    arrays = {n: generate_random_array(n) for n in INPUT_SIZES}

    all_results = []
    for key, (title, fn) in ALGORITHMS.items():
        rows = []
        for n in INPUT_SIZES:
            elapsed = time_run(fn, arrays[n])
            rows.append((n, elapsed))
            print(f"{title:>12s}  n={n:>7d}  t={elapsed:.6f}s")
        write_csv(key, rows)
        write_table(key, rows)
        plot_single(key, title, rows)
        all_results.append((key, title, rows))

    plot_comparison(all_results)
    print("Done.")


if __name__ == "__main__":
    main()
