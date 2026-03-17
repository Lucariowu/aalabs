import csv
import os
import random
import time
from collections import deque

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INPUT_SIZES = [500, 1000, 2000, 5000, 10000, 20000, 30000, 50000]
AVG_DEGREE = 4
REPEATS = 5
SCENARIO_REPEATS = 5
SEED = 42


def generate_connected_graph(n, avg_degree=AVG_DEGREE):
    target_edges = max(n - 1, (n * avg_degree) // 2)
    adjacency = [[] for _ in range(n)]
    edges = set()

    for node in range(1, n):
        parent = random.randint(0, node - 1)
        edge = (parent, node)
        edges.add(edge)
        adjacency[parent].append(node)
        adjacency[node].append(parent)

    while len(edges) < target_edges:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u == v:
            continue
        a, b = (u, v) if u < v else (v, u)
        if (a, b) in edges:
            continue
        edges.add((a, b))
        adjacency[a].append(b)
        adjacency[b].append(a)

    return adjacency, len(edges)


def generate_connected_graph_with_m_edges(n, m):
    adjacency = [[] for _ in range(n)]
    edges = set()

    for node in range(1, n):
        parent = random.randint(0, node - 1)
        a, b = (parent, node) if parent < node else (node, parent)
        edges.add((a, b))
        adjacency[parent].append(node)
        adjacency[node].append(parent)

    while len(edges) < m:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u == v:
            continue
        a, b = (u, v) if u < v else (v, u)
        if (a, b) in edges:
            continue
        edges.add((a, b))
        adjacency[a].append(b)
        adjacency[b].append(a)

    return adjacency, len(edges)


def generate_path_graph(n):
    adjacency = [[] for _ in range(n)]
    for node in range(n - 1):
        adjacency[node].append(node + 1)
        adjacency[node + 1].append(node)
    return adjacency, n - 1


def generate_complete_graph(n):
    adjacency = [list(range(n)) for _ in range(n)]
    for node in range(n):
        adjacency[node].remove(node)
    return adjacency, (n * (n - 1)) // 2


def generate_grid_graph(rows, cols):
    n = rows * cols
    adjacency = [[] for _ in range(n)]

    def index(r, c):
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            u = index(r, c)
            if r + 1 < rows:
                v = index(r + 1, c)
                adjacency[u].append(v)
                adjacency[v].append(u)
            if c + 1 < cols:
                v = index(r, c + 1)
                adjacency[u].append(v)
                adjacency[v].append(u)

    m = rows * (cols - 1) + (rows - 1) * cols
    return adjacency, m


def generate_k_ary_tree(branching_factor, levels):
    total_nodes = (branching_factor ** levels - 1) // (branching_factor - 1)
    adjacency = [[] for _ in range(total_nodes)]

    next_node = 1
    for parent in range(total_nodes):
        for _ in range(branching_factor):
            if next_node >= total_nodes:
                break
            adjacency[parent].append(next_node)
            adjacency[next_node].append(parent)
            next_node += 1

    return adjacency, total_nodes - 1


def generate_disconnected_paths(size_a, size_b):
    n = size_a + size_b
    adjacency = [[] for _ in range(n)]

    for node in range(size_a - 1):
        adjacency[node].append(node + 1)
        adjacency[node + 1].append(node)

    offset = size_a
    for node in range(offset, offset + size_b - 1):
        adjacency[node].append(node + 1)
        adjacency[node + 1].append(node)

    m = (size_a - 1) + (size_b - 1)
    return adjacency, m


def bfs(graph, source=0):
    visited = [False] * len(graph)
    queue = deque([source])
    visited[source] = True
    max_frontier = 1

    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
        if len(queue) > max_frontier:
            max_frontier = len(queue)

    return max_frontier


def dfs(graph, source=0):
    visited = [False] * len(graph)
    stack = [source]
    max_frontier = 1

    while stack:
        node = stack.pop()
        if visited[node]:
            continue
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                stack.append(neighbor)
        if len(stack) > max_frontier:
            max_frontier = len(stack)

    return max_frontier


def bfs_search(graph, source, target):
    visited = [False] * len(graph)
    queue = deque([source])
    visited[source] = True
    max_frontier = 1

    while queue:
        node = queue.popleft()
        if node == target:
            return True, max_frontier
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
        if len(queue) > max_frontier:
            max_frontier = len(queue)

    return False, max_frontier


def dfs_search(graph, source, target):
    visited = [False] * len(graph)
    stack = [source]
    visited[source] = True
    max_frontier = 1

    while stack:
        node = stack.pop()
        if node == target:
            return True, max_frontier
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)
        if len(stack) > max_frontier:
            max_frontier = len(stack)

    return False, max_frontier


def run_once(fn, graph):
    start = time.perf_counter()
    max_frontier = fn(graph)
    elapsed = time.perf_counter() - start
    return elapsed, max_frontier


def benchmark_algorithm(fn, graph):
    times = []
    frontiers = []

    for _ in range(REPEATS):
        elapsed, frontier = run_once(fn, graph)
        times.append(elapsed)
        frontiers.append(frontier)

    avg_time = sum(times) / len(times)
    avg_frontier = int(round(sum(frontiers) / len(frontiers)))
    return avg_time, avg_frontier


def benchmark_search(fn, graph, source, target, repeats=SCENARIO_REPEATS):
    times = []
    frontiers = []
    found_values = []

    for _ in range(repeats):
        start = time.perf_counter()
        found, frontier = fn(graph, source, target)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        frontiers.append(frontier)
        found_values.append(found)

    avg_time = sum(times) / len(times)
    avg_frontier = int(round(sum(frontiers) / len(frontiers)))
    found_consistent = all(found_values)
    return avg_time, avg_frontier, found_consistent


def ensure_dirs():
    os.makedirs("results", exist_ok=True)
    os.makedirs("figures", exist_ok=True)


def write_csv(name, rows):
    path = os.path.join("results", f"{name}.csv")
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["n", "m", "time_s", "max_frontier"])
        writer.writerows(rows)


def write_table(name, rows):
    path = os.path.join("results", f"{name}_table.tex")
    with open(path, "w") as handle:
        handle.write("\\begin{table}[H]\n")
        handle.write("\\centering\n")
        handle.write("\\caption{" + name.upper() + " Results}\n")
        handle.write("\\begin{tabular}{rrrr}\n")
        handle.write("\\toprule\n")
        handle.write("n & m & time (s) & max frontier\\\\\n")
        handle.write("\\midrule\n")
        for n, m, t, frontier in rows:
            handle.write(f"{n} & {m} & {t:.6f} & {frontier}\\\\\n")
        handle.write("\\bottomrule\n")
        handle.write("\\end{tabular}\n")
        handle.write("\\end{table}\n")


def write_scenarios_csv(rows):
    path = os.path.join("results", "scenarios.csv")
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["scenario", "algorithm", "nodes", "edges", "target_type", "found", "avg_time_ms", "max_frontier"])
        writer.writerows(rows)


def write_scenarios_table(rows):
    path = os.path.join("results", "scenarios_table.tex")
    with open(path, "w") as handle:
        handle.write("\\begin{table}[H]\n")
        handle.write("\\centering\n")
        handle.write("\\caption{Scenario-based BFS and DFS Results}\n")
        handle.write("\\small\n")
        handle.write("\\begin{tabular}{llrrlrr}\n")
        handle.write("\\toprule\n")
        handle.write("Scenario & Alg. & Nodes & Edges & Target type & Found & Avg time (ms)\\\\\n")
        handle.write("\\midrule\n")
        for scenario, algorithm, nodes, edges, target_type, found, avg_time_ms, _ in rows:
            found_text = "True" if found else "False"
            handle.write(f"{scenario} & {algorithm} & {nodes} & {edges} & {target_type} & {found_text} & {avg_time_ms:.4f}\\\\\n")
        handle.write("\\bottomrule\n")
        handle.write("\\end{tabular}\n")
        handle.write("\\end{table}\n")


def scenario_file_slug(scenario_name):
    return scenario_name.lower().replace("/", "_").replace(" ", "_")


def write_scenario_detail_tables(rows):
    grouped = {}
    for row in rows:
        scenario = row[0]
        grouped.setdefault(scenario, []).append(row)

    for scenario_name, scenario_rows in grouped.items():
        slug = scenario_file_slug(scenario_name)
        path = os.path.join("results", f"scenario_{slug}_table.tex")
        with open(path, "w") as handle:
            handle.write("\\begin{table}[H]\n")
            handle.write("\\centering\n")
            handle.write(f"\\caption{{{scenario_name} Criterion Results}}\n")
            handle.write("\\begin{tabular}{lrrlrr}\n")
            handle.write("\\toprule\n")
            handle.write("Algorithm & Nodes & Edges & Target type & Found & Avg time (ms)\\\\\n")
            handle.write("\\midrule\n")
            for _, algorithm, nodes, edges, target_type, found, avg_time_ms, _ in scenario_rows:
                found_text = "True" if found else "False"
                handle.write(f"{algorithm} & {nodes} & {edges} & {target_type} & {found_text} & {avg_time_ms:.4f}\\\\\n")
            handle.write("\\bottomrule\n")
            handle.write("\\end{tabular}\n")
            handle.write("\\end{table}\n")


def plot_single(name, title, rows):
    ns = [n for n, _, _, _ in rows]
    ts = [t for _, _, t, _ in rows]
    plt.figure(figsize=(7, 4))
    plt.plot(ns, ts, marker="o")
    plt.title(title)
    plt.xlabel("n (number of vertices)")
    plt.ylabel("Time (s)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join("figures", f"{name}.png"), dpi=200)
    plt.close()


def plot_comparison(bfs_rows, dfs_rows):
    ns = [n for n, _, _, _ in bfs_rows]
    bfs_t = [t for _, _, t, _ in bfs_rows]
    dfs_t = [t for _, _, t, _ in dfs_rows]

    plt.figure(figsize=(8, 4.5))
    plt.plot(ns, bfs_t, marker="o", label="BFS")
    plt.plot(ns, dfs_t, marker="o", label="DFS")
    plt.title("BFS vs DFS Comparison")
    plt.xlabel("n (number of vertices)")
    plt.ylabel("Time (s)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join("figures", "comparison.png"), dpi=200)
    plt.close()


def build_scenarios():
    scenarios = []

    graph, m = generate_path_graph(20000)
    scenarios.append(("Chain/Path", graph, m, 0, 19999, "deep target"))

    graph, m = generate_k_ary_tree(branching_factor=3, levels=9)
    scenarios.append(("Balanced Tree", graph, m, 0, len(graph) - 1, "deep leaf"))

    graph, m = generate_complete_graph(2000)
    scenarios.append(("Dense/Complete", graph, m, 0, 1, "any neighbor"))

    graph, m = generate_grid_graph(120, 120)
    scenarios.append(("Grid", graph, m, 0, len(graph) - 1, "opposite corner"))

    graph, m = generate_k_ary_tree(branching_factor=2, levels=10)
    scenarios.append(("Deep vs Shallow", graph, m, 0, 1, "shallow"))
    scenarios.append(("Deep vs Shallow", graph, m, 0, len(graph) - 1, "deep"))

    graph, m = generate_connected_graph_with_m_edges(4500, 15367)
    scenarios.append(("Large Random", graph, m, 0, random.randint(1, 4499), "random target"))

    graph, m = generate_disconnected_paths(4000, 4000)
    scenarios.append(("Disconnected", graph, m, 0, 7999, "unreachable"))

    return scenarios


def main():
    random.seed(SEED)
    ensure_dirs()

    graphs = {}
    edge_counts = {}

    for n in INPUT_SIZES:
        graph, m = generate_connected_graph(n)
        graphs[n] = graph
        edge_counts[n] = m

    bfs_rows = []
    dfs_rows = []

    for n in INPUT_SIZES:
        graph = graphs[n]
        m = edge_counts[n]

        bfs_time, bfs_frontier = benchmark_algorithm(bfs, graph)
        dfs_time, dfs_frontier = benchmark_algorithm(dfs, graph)

        bfs_rows.append((n, m, bfs_time, bfs_frontier))
        dfs_rows.append((n, m, dfs_time, dfs_frontier))

        print(f"n={n:>6d} m={m:>7d} | BFS={bfs_time:.6f}s ({bfs_frontier}) | DFS={dfs_time:.6f}s ({dfs_frontier})")

    write_csv("bfs", bfs_rows)
    write_csv("dfs", dfs_rows)
    write_table("bfs", bfs_rows)
    write_table("dfs", dfs_rows)

    plot_single("bfs", "BFS Execution Time", bfs_rows)
    plot_single("dfs", "DFS Execution Time", dfs_rows)
    plot_comparison(bfs_rows, dfs_rows)

    scenarios = build_scenarios()
    scenario_rows = []

    for scenario_name, graph, m, source, target, target_type in scenarios:
        bfs_time, bfs_frontier, bfs_found = benchmark_search(bfs_search, graph, source, target)
        dfs_time, dfs_frontier, dfs_found = benchmark_search(dfs_search, graph, source, target)

        bfs_ms = bfs_time * 1000.0
        dfs_ms = dfs_time * 1000.0

        scenario_rows.append((scenario_name, "BFS", len(graph), m, target_type, bfs_found, bfs_ms, bfs_frontier))
        scenario_rows.append((scenario_name, "DFS", len(graph), m, target_type, dfs_found, dfs_ms, dfs_frontier))

        print(
            f"{scenario_name:>14s} | BFS={bfs_ms:8.4f} ms found={bfs_found} | "
            f"DFS={dfs_ms:8.4f} ms found={dfs_found}"
        )

    write_scenarios_csv(scenario_rows)
    write_scenarios_table(scenario_rows)
    write_scenario_detail_tables(scenario_rows)

    print("Done.")


if __name__ == "__main__":
    main()
