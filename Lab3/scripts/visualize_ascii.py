#!/usr/bin/env python3
"""
BFS and DFS Algorithm Visualization - ASCII Terminal Version
Supports custom graph input and step-by-step animation in terminal
"""

from collections import deque
import time


class ASCIIAlgorithmVisualizer:
    def __init__(self):
        self.graph = {}
        self.start_node = None
        self.bfs_steps = []
        self.dfs_steps = []
        
    def input_graph(self):
        """Get graph input from user"""
        print("\n" + "="*70)
        print("ALGORITHM VISUALIZATION - ASCII TERMINAL VERSION")
        print("="*70)
        print("\nInput format:")
        print("  - Enter edges as: 0-1, 1-2, 2-3, etc.")
        print("  - Use spaces or commas as separators")
        print("  - Example: 0-1 1-2 1-3 2-4")
        print("\nPresets available:")
        print("  1: Simple chain (0-1-2-3)")
        print("  2: Tree (0 -> 1,2; 1 -> 3,4; 2 -> 5)")
        print("  3: Cycle with branches")
        print("  4: Complete graph (triangle)")
        print("  5: Custom input")
        
        choice = input("\nSelect option (1-5) or enter edges directly: ").strip()
        
        presets = {
            '1': "0-1 1-2 2-3",
            '2': "0-1 0-2 1-3 1-4 2-5",
            '3': "0-1 1-2 2-3 3-0 1-4 3-5",
            '4': "0-1 1-2 2-0",
        }
        
        if choice in presets:
            edge_input = presets[choice]
        else:
            edge_input = choice
        
        # Parse edges
        self.graph = {}
        edge_list = edge_input.replace(',', ' ').split()
        
        for edge in edge_list:
            if '-' in edge:
                a, b = edge.split('-')
                a, b = int(a), int(b)
                
                if a not in self.graph:
                    self.graph[a] = []
                if b not in self.graph:
                    self.graph[b] = []
                    
                self.graph[a].append(b)
                self.graph[b].append(a)
        
        if not self.graph:
            raise ValueError("No valid edges parsed")
        
        # Get starting node
        print(f"\nAvailable nodes: {sorted(self.graph.keys())}")
        start = input("Enter starting node: ").strip()
        self.start_node = int(start)
        
        if self.start_node not in self.graph:
            raise ValueError(f"Node {self.start_node} not in graph")
        
        print(f"\nGraph created with {len(self.graph)} nodes")
        print(f"Edges: {edge_input}")
        print(f"Start node: {self.start_node}\n")
        
    def record_bfs_steps(self):
        """Record BFS traversal steps"""
        visited = set()
        queue = deque([self.start_node])
        visited.add(self.start_node)
        order = []
        
        steps = []
        steps.append({
            'current': self.start_node,
            'visited': visited.copy(),
            'frontier': list(queue),
            'order': order.copy(),
            'action': f"Initialize: Add node {self.start_node} to queue"
        })
        
        while queue:
            node = queue.popleft()
            order.append(node)
            
            for neighbor in sorted(self.graph[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    steps.append({
                        'current': neighbor,
                        'visited': visited.copy(),
                        'frontier': list(queue),
                        'order': order.copy(),
                        'action': f"Process node {node}: Add neighbor {neighbor} to queue"
                    })
        
        self.bfs_steps = steps
        
    def record_dfs_steps(self):
        """Record DFS traversal steps"""
        visited = set()
        stack = [self.start_node]
        visited.add(self.start_node)
        order = []
        
        steps = []
        steps.append({
            'current': self.start_node,
            'visited': visited.copy(),
            'frontier': stack.copy(),
            'order': order.copy(),
            'action': f"Initialize: Add node {self.start_node} to stack"
        })
        
        while stack:
            node = stack.pop()
            order.append(node)
            
            for neighbor in sorted(self.graph[node], reverse=True):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
                    steps.append({
                        'current': neighbor,
                        'visited': visited.copy(),
                        'frontier': stack.copy(),
                        'order': order.copy(),
                        'action': f"Process node {node}: Add neighbor {neighbor} to stack"
                    })
        
        self.dfs_steps = steps
        
    def print_state(self, algorithm='bfs', step=0):
        """Print current algorithm state"""
        steps = self.bfs_steps if algorithm == 'bfs' else self.dfs_steps
        data_structure = "Queue (FIFO)" if algorithm == 'bfs' else "Stack (LIFO)"
        title = "BFS - Breadth-First Search" if algorithm == 'bfs' else "DFS - Depth-First Search"
        
        step = min(step, len(steps) - 1)
        state = steps[step]
        
        print(f"\n{title}")
        print(f"Data Structure: {data_structure}")
        print(f"Step {step + 1}/{len(steps)}")
        print("-" * 70)
        print(f"Action: {state['action']}")
        print(f"Current Node: {state['current']}")
        print(f"Visited Set: {sorted(state['visited'])}")
        print(f"Queue/Stack: {state['frontier']}")
        print(f"Visit Order: {state['order']}")
        
        # Visual representation
        print(f"\nGraph visualization:")
        all_nodes = sorted(self.graph.keys())
        for node in all_nodes:
            if node == state['current']:
                status = "→ [CURRENT]"
            elif node in state['visited']:
                status = "✓ [VISITED]"
            else:
                status = "  [UNVISITED]"
            print(f"  Node {node}{status}")
        
    def animate_algorithm(self, algorithm='bfs', delay=0.5):
        """Show step-by-step animation"""
        steps = self.bfs_steps if algorithm == 'bfs' else self.dfs_steps
        
        for step in range(len(steps)):
            self.print_state(algorithm, step)
            
            if step < len(steps) - 1:
                input("Press Enter for next step...")
            
    def compare_algorithms(self):
        """Show both algorithms side-by-side summary"""
        print("\n" + "="*70)
        print("ALGORITHM COMPARISON")
        print("="*70)
        
        print(f"\nGraph: {len(self.graph)} nodes, Start node: {self.start_node}")
        print(f"Total steps - BFS: {len(self.bfs_steps)}, DFS: {len(self.dfs_steps)}")
        
        print("\n" + "-"*70)
        print("BFS (Breadth-First Search)")
        print("-"*70)
        if self.bfs_steps:
            final_bfs = self.bfs_steps[-1]
            print(f"Final visit order: {final_bfs['order']}")
            print(f"All visited: {sorted(final_bfs['visited'])}")
        
        print("\n" + "-"*70)
        print("DFS (Depth-First Search)")
        print("-"*70)
        if self.dfs_steps:
            final_dfs = self.dfs_steps[-1]
            print(f"Final visit order: {final_dfs['order']}")
            print(f"All visited: {sorted(final_dfs['visited'])}")
            
    def interactive_menu(self):
        """Interactive menu for user"""
        while True:
            print("\nOptions:")
            print("  1: Animate BFS (step-by-step)")
            print("  2: Animate DFS (step-by-step)")
            print("  3: Compare BFS vs DFS")
            print("  4: New graph")
            print("  5: Exit")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                self.animate_algorithm('bfs')
            elif choice == '2':
                self.animate_algorithm('dfs')
            elif choice == '3':
                self.compare_algorithms()
            elif choice == '4':
                self.input_graph()
                self.record_bfs_steps()
                self.record_dfs_steps()
            elif choice == '5':
                print("\nGoodbye!")
                break
            else:
                print("Invalid choice")


def main():
    visualizer = ASCIIAlgorithmVisualizer()
    
    try:
        visualizer.input_graph()
        visualizer.record_bfs_steps()
        visualizer.record_dfs_steps()
        visualizer.interactive_menu()
    except Exception as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    main()
