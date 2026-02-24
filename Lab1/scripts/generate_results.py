import csv
import os
import sys
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SMALL_INPUTS = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45]
LARGE_INPUTS = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
INPUT_SIZES = SMALL_INPUTS + LARGE_INPUTS
REPEATS = 3


def fib_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fib_memoized(n):
    if n < 2:
        return n

    memo = {0: 0, 1: 1}
    stack = [n]
    while stack:
        k = stack.pop()
        if k in memo:
            continue

        k1, k2 = k - 1, k - 2
        if k1 in memo and k2 in memo:
            memo[k] = memo[k1] + memo[k2]
            continue

        stack.append(k)
        if k1 not in memo:
            stack.append(k1)
        if k2 not in memo:
            stack.append(k2)

    return memo[n]


def fib_fast_doubling(n):
    def solve(k):
        if k == 0:
            return (0, 1)
        a, b = solve(k // 2)
        c = a * (2 * b - a)
        d = a * a + b * b
        if k % 2 == 0:
            return (c, d)
        return (d, c + d)

    return solve(n)[0]


def fib_binomial(n):
    if n == 0:
        return 0
    max_k = (n - 1) // 2
    term = 1
    total = 0
    for k in range(max_k + 1):
        total += term
        if k < max_k:
            numerator = (n - 2 * k - 1) * (n - 2 * k - 2)
            denominator = (k + 1) * (n - k - 1)
            term = term * numerator // denominator
    return total


def fib_matrix_fast(n):
    if n == 0:
        return 0

    def mat_mul(a, b):
        return [
            [a[0][0] * b[0][0] + a[0][1] * b[1][0],
             a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0],
             a[1][0] * b[0][1] + a[1][1] * b[1][1]],
        ]

    def mat_pow(p):
        result = [[1, 0], [0, 1]]
        base = [[1, 1], [1, 0]]
        while p > 0:
            if p & 1:
                result = mat_mul(result, base)
            base = mat_mul(base, base)
            p >>= 1
        return result

    return mat_pow(n)[0][1]


ALGORITHMS = {
    "iterative": ("Iterative Linear", fib_iterative),
    "memoized": ("Memoized Recursion", fib_memoized),
    "fast_doubling": ("Fast Doubling", fib_fast_doubling),
    "binomial": ("Binomial Sum", fib_binomial),
    "matrix_fast": ("Fast Matrix Exponentiation", fib_matrix_fast),
}


def time_run(fn, n):
    best = None
    for _ in range(REPEATS):
        start = time.perf_counter()
        fn(n)
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
    plt.xlabel("n")
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
    plt.yscale("log")
    plt.title("Fibonacci Algorithm Comparison")
    plt.xlabel("n")
    plt.ylabel("Time (s, log scale)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join("figures", "comparison.png"), dpi=200)
    plt.close()


def main():
    ensure_dirs()

    all_results = []
    for key, (title, fn) in ALGORITHMS.items():
        rows = []
        for n in INPUT_SIZES:
            elapsed = time_run(fn, n)
            rows.append((n, elapsed))
        write_csv(key, rows)
        write_table(key, rows)
        plot_single(key, title, rows)
        all_results.append((key, title, rows))

    plot_comparison(all_results)


if __name__ == "__main__":
    main()
